from __future__ import annotations

__all__ = ("HTTPClient",)

import asyncio
import logging
import platform
import time
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Awaitable, Dict, List, Literal, NamedTuple, Optional, Union

from aiohttp import ClientSession, __version__ as aiohttp_version

from ..errors import error_from_request
from ..utils import human_readable_time_until

try:
    import orjson  # type: ignore
except ImportError:
    import json

    json_loads = json.loads
else:
    json_loads = orjson.loads

if TYPE_CHECKING:
    from aiohttp import BasicAuth
    from typing_extensions import Self

    from ..objects import File
    from ..types import Author, Committer, OptionalAuthor, OptionalCommitter, SecurityAndAnalysis


log = logging.getLogger("github")


class RateLimits(NamedTuple):
    remaining: int
    used: int
    total: int
    reset_time: datetime
    last_request: datetime


# ====== STYLE GUIDE ===== #
# All route method names should be
# The exact same from the GitHub API
# Docs, excluding 'the', 'a' etc
# Names should be shortened, e.g:
# Information -> Info
# Repository -> Repo

# ========= TODO ========= #
# Make a good paginator
# Make objects for all API Types
# Make the requests return TypedDicts with those objects
# Make specific errors
# Make it so an error gets raised when the cooldown is reached
# Make markdown raw request route (???)

# === ROUTES CHECKLIST === #
# Actions
# Activity
# Apps
# Billing
# Branches
# Checks
# Codes of conduct           DONE
# Code Scanning
# Codespaces
# Collaborators
# Commits
# Dependabot
# Dependency Graph
# Deploy keys                DONE
# Deployments
# Emojis                     DONE
# Enterprise administration
# Gists                      DONE
# Git database
# Gitignore                  DONE
# Interactions
# Issues
# Licenses                   DONE
# Markdown                   DONE
# Meta                       DONE
# Metrics
# Migrations
# OAuth authorizations
# Organizations
# Packages
# Pages
# Projects
# Pulls
# Rate limit
# Reactions
# Releases
# Repositories               DONE
# SCIM
# Search                     DONE
# Teams
# Users                      DONE
# Webhooks


class HTTPClient:
    __session: ClientSession
    _rates: RateLimits
    _last_ping: float
    _latency: float

    def __new__(cls, **kwargs: Any) -> Awaitable[HTTPClient]:
        # Basically async def __init__
        return cls.__async_init(**kwargs)

    @classmethod
    async def __async_init(
        cls,
        *,
        headers: Optional[Dict[str, str]] = None,
        auth: Optional[BasicAuth] = None,
    ) -> HTTPClient:
        self = super(cls, cls).__new__(cls)

        headers = headers or {}

        headers.setdefault(
            "User-Agent",
            "GitHub-API-Wrapper (https://github.com/Varmonke/GitHub-API-Wrapper) @"
            f" 2.0.0a CPython/{platform.python_version()} aiohttp/{aiohttp_version}",
        )

        self.__session = ClientSession(headers=headers, auth=auth)

        time_0 = datetime.fromtimestamp(0)

        self._rates = RateLimits(60, 0, 60, time_0, time_0)

        self._last_ping = float("-inf")
        self._latency = 0

        return self

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *_) -> None:
        await self.__session.close()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"

    @property
    def is_ratelimited(self) -> bool:
        return self._rates.remaining < 2

    async def latency(self) -> float:
        last_ping = self._last_ping

        # If there was no ping or the last ping was more than 5 seconds ago (or is currently ratelimited).
        if not self.is_ratelimited and time.monotonic() > last_ping + 5:
            self._last_ping = time.monotonic()

            start = time.monotonic()
            await self.get_github_api_root()
            self._latency = time.monotonic() - start

        return self._latency

    async def request(
        self, method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"], path: str, /, **kwargs: Any
    ):
        if self.is_ratelimited:
            log.info(
                "Ratelimit exceeded, trying again in"
                f" {human_readable_time_until(self._rates.reset_time - datetime.now(timezone.utc))} (URL:"
                f" {path}, method: {method})"
            )

            # TODO: I get about 3-4 hours of cooldown
            # this might not be a good idea, might make
            # this raise an error instead.
            await asyncio.sleep(
                max((self._rates.reset_time - datetime.now(timezone.utc)).total_seconds(), 0)
            )

        async with self.__session.request(
            method, f"https://api.github.com{path}", **kwargs
        ) as response:
            headers = response.headers

            self._rates = RateLimits(
                int(headers["X-RateLimit-Remaining"]),
                int(headers["X-RateLimit-Used"]),
                int(headers["X-RateLimit-Limit"]),
                datetime.fromtimestamp(int(headers["X-RateLimit-Reset"])).replace(
                    tzinfo=timezone.utc
                ),
                datetime.now(timezone.utc),
            )

            if 200 <= response.status <= 299:
                data = await response.text(encoding="utf-8")

                if response.headers["Content-Type"] == "application/json":
                    return json_loads(data)

                return data

            raise error_from_request(response)

    # === ROUTES === #

    # === USERS === #

    async def get_authenticated_user(self):
        return await self.request("GET", "/user")

    async def update_authenticated_user(
        self,
        *,
        name: Optional[str] = None,
        email: Optional[str] = None,
        blog: Optional[str] = None,
        twitter_username: Optional[str] = None,
        company: Optional[str] = None,
        location: Optional[str] = None,
        hireable: Optional[str] = None,
        bio: Optional[str] = None,
    ):
        data = {}

        if name:
            data["name"] = name
        if email:
            data["email"] = email
        if blog:
            data["blog"] = blog
        if twitter_username:
            data["twitter_username"] = twitter_username
        if company:
            data["company"] = company
        if location:
            data["location"] = location
        if hireable:
            data["hireable"] = hireable
        if bio:
            data["bio"] = bio

        return await self.request("PATCH", "/user", json=data)

    async def list_users(self, *, since: Optional[int] = None, per_page: Optional[int] = None):
        params = {}

        if since:
            params["since"] = since
        if per_page:
            params["per_page"] = per_page

        return await self.request("GET", "/users", params=params)

    async def get_user(self, *, username: str):
        return await self.request("GET", f"/users/{username}")

    async def get_context_info_for_user(
        self,
        *,
        username: str,
        subject_type: Optional[
            Literal["organization", "repository", "user", "pull_request"]
        ] = None,
        subject_id: Optional[int] = None,
    ):
        params = {}

        if subject_type:
            params["subject_type"] = subject_type
        if subject_id:
            params["subject_id"] = subject_id

        return await self.request("GET", f"/users/{username}/hovercard", params=params)

    async def list_blocked_users_for_authenticated_user(self):
        return await self.request("GET", "/user/blocks")

    async def check_user_blocked_for_authenticated_user(self, *, username: str):
        return await self.request("GET", f"/user/blocks/{username}")

    async def block_user(self, *, username: str):
        return await self.request("PUT", f"/user/blocks/{username}")

    async def unblock_user(self, *, username: str):
        return await self.request("DELETE", f"/user/blocks/{username}")

    async def set_primary_email_visibility_for_authenticated_user(
        self, *, visibility: Literal["public", "private"]
    ):
        return await self.request(
            "PATCH", "/user/email/visibility", json={"visibility": visibility}
        )

    async def list_email_addresses_for_the_authenticated_user(
        self, *, per_page: Optional[int] = None, page: Optional[int] = None
    ):
        params = {}

        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", "/user/emails", params=params)

    async def add_email_addresses_for_the_authenticated_user(self, *, emails: List[str]):
        return await self.request("POST", "/user/emails", json={"email": emails})

    async def delete_email_addresses_for_the_authenticated_user(self, *, emails: List[str]):
        return await self.request("DELETE", "/user/emails", json={"email": emails})

    async def list_public_email_addresses_for_the_authenticated_user(
        self, *, per_page: Optional[int] = None, page: Optional[int] = None
    ):
        params = {}

        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", "/user/emails/public", params=params)

    async def list_followers_of_the_authenticated_user(
        self, *, per_page: Optional[int] = None, page: Optional[int] = None
    ):
        params = {}

        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", "/user/followers", params=params)

    async def list_following_for_the_authenticated_user(
        self, *, per_page: Optional[int] = None, page: Optional[int] = None
    ):
        params = {}

        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", "/user/following", params=params)

    async def check_person_followed_by_authenticated_user(self, *, username: str):
        return await self.request("GET", f"/user/following/{username}")

    async def follow_user(self, *, username: str):
        return await self.request("PUT", f"/user/following/{username}")

    async def unfollow_user(self, *, username: str):
        return await self.request("DELETE", f"/user/following/{username}")

    async def list_followers_for_user(
        self, *, username: str, per_page: Optional[int] = None, page: Optional[int] = None
    ):
        params = {}

        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", f"/users/{username}/followers", params=params)

    async def list_following_for_user(
        self, *, username: str, per_page: Optional[int] = None, page: Optional[int] = None
    ):
        params = {}

        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", f"/users/{username}/following", params=params)

    async def check_user_follows_another_user(self, *, username: str, target_user: str):
        return await self.request("GET", f"/users/{username}/following/{target_user}")

    async def list_gpg_keys_for_authenticated_user(
        self, *, per_page: Optional[int] = None, page: Optional[int] = None
    ):
        params = {}

        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", "/user/gpg_keys", params=params)

    async def create_gpg_key_for_authenticated_user(
        self, *, name: Optional[str] = None, armored_public_key: str
    ):
        data = {
            "armored_public_key": armored_public_key,
        }

        if name:
            data["name"] = name

        return await self.request("POST", "/user/gpg_keys", json=data)

    async def get_gpg_key_for_authenticated_user(self, *, gpg_key_id: int):
        return await self.request("GET", f"/user/gpg_keys/{gpg_key_id}")

    async def delete_gpg_key_for_authenticated_user(self, *, gpg_key_id: int):
        return await self.request("DELETE", f"/user/gpg_keys/{gpg_key_id}")

    async def list_gpg_keys_for_user(
        self, *, username: str, per_page: Optional[int] = None, page: Optional[int] = None
    ):
        params = {}

        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", f"/users/{username}/gpg_keys", params=params)

    async def list_public_ssh_keys_for_authenticated_user(
        self, *, per_page: Optional[int] = None, page: Optional[int] = None
    ):
        params = {}

        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", "/user/keys", params=params)

    async def create_public_ssh_key_for_authenticated_user(
        self, *, title: Optional[str] = None, key: str
    ):
        data = {
            "key": key,
        }

        if title:
            data["title"] = title

        return await self.request("POST", "/user/keys", json=data)

    async def get_public_ssh_key_for_authenticated_user(self, *, key_id: int):
        return await self.request("GET", f"/user/keys/{key_id}")

    async def delete_public_ssh_key_for_authenticated_user(self, *, key_id: int):
        return await self.request("DELETE", f"/user/keys/{key_id}")

    async def list_public_ssh_keys_for_user(
        self, *, username: str, per_page: Optional[int] = None, page: Optional[int] = None
    ):
        params = {}

        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", f"/users/{username}/keys", params=params)

    # === REPOS === #

    async def list_org_repos(
        self,
        *,
        org: str,
        type: Optional[
            Literal["all", "public", "private", "forks", "sources", "member", "internal"]
        ] = None,
        sort: Optional[Literal["created", "updated", "pushed", "full_name"]] = None,
        direction: Optional[Literal["asc", "desc"]] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
    ):
        params = {}

        if type:
            params["type"] = type
        if sort:
            params["sort"] = sort
        if direction:
            params["direction"] = direction
        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", f"/orgs/{org}/repos", params=params)

    async def create_org_repo(
        self,
        *,
        org: str,
        name: str,
        description: Optional[str] = None,
        homepage: Optional[str] = None,
        private: Optional[bool] = None,
        visibility: Optional[Literal["public", "private", "internal"]] = None,
        has_issues: Optional[bool] = None,
        has_projects: Optional[bool] = None,
        has_wiki: Optional[bool] = None,
        is_template: Optional[bool] = None,
        team_id: Optional[int] = None,
        auto_init: Optional[bool] = None,
        gitignore_template: Optional[str] = None,
        license_template: Optional[str] = None,
        allow_squash_merge: Optional[bool] = None,
        allow_merge_commit: Optional[bool] = None,
        allow_rebase_merge: Optional[bool] = None,
        allow_auto_merge: Optional[bool] = None,
        delete_branch_on_merge: Optional[bool] = None,
        use_squash_pr_title_as_default: Optional[bool] = None,
    ):
        data: Dict[str, Union[str, bool, int]] = {
            "name": name,
        }

        if description:
            data["description"] = description
        if homepage:
            data["homepage"] = homepage
        if private:
            data["private"] = private
        if visibility:
            data["visibility"] = visibility
        if has_issues:
            data["has_issues"] = has_issues
        if has_projects:
            data["has_projects"] = has_projects
        if has_wiki:
            data["has_wiki"] = has_wiki
        if is_template:
            data["is_template"] = is_template
        if team_id:
            data["team_id"] = team_id
        if auto_init:
            data["auto_init"] = auto_init
        if gitignore_template:
            data["gitignore_template"] = gitignore_template
        if license_template:
            data["license_template"] = license_template
        if allow_squash_merge:
            data["allow_squash_merge"] = allow_squash_merge
        if allow_merge_commit:
            data["allow_merge_commit"] = allow_merge_commit
        if allow_rebase_merge:
            data["allow_rebase_merge "] = allow_rebase_merge
        if allow_auto_merge:
            data["allow_auto_merge"] = allow_auto_merge
        if delete_branch_on_merge:
            data["delete_branch_on_merge"] = delete_branch_on_merge
        if use_squash_pr_title_as_default:
            data["use_squash_pr_title_as_default"] = use_squash_pr_title_as_default

        return await self.request("POST", f"/orgs/{org}/repos", json=data)

    async def get_repo(self, *, owner: str, repo: str):
        return await self.request("GET", f"/repos/{owner}/{repo}")

    async def update_repo(
        self,
        *,
        owner: str,
        repo: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        homepage: Optional[str] = None,
        private: Optional[bool] = None,
        visibility: Optional[Literal["public", "private", "internal"]] = None,
        security_and_analysis: Optional[SecurityAndAnalysis] = None,
        has_issues: Optional[bool] = None,
        has_projects: Optional[bool] = None,
        has_wiki: Optional[bool] = None,
        is_template: Optional[bool] = None,
        default_branch: Optional[str] = None,
        allow_squash_merge: Optional[bool] = None,
        allow_merge_commit: Optional[bool] = None,
        allow_rebase_merge: Optional[bool] = None,
        allow_auto_merge: Optional[bool] = None,
        delete_branch_on_merge: Optional[bool] = None,
        use_squash_pr_title_as_default: Optional[bool] = None,
        archived: Optional[bool] = None,
        allow_forking: Optional[bool] = None,
    ):
        data = {}

        if name:
            data["name"] = name
        if description:
            data["description"] = description
        if homepage:
            data["homepage"] = homepage
        if private:
            data["private"] = private
        if visibility:
            data["visibility"] = visibility
        if security_and_analysis:
            data["security_and_analysis"] = security_and_analysis
        if has_issues:
            data["has_issues"] = has_issues
        if has_projects:
            data["has_projects"] = has_projects
        if has_wiki:
            data["has_wiki"] = has_wiki
        if is_template:
            data["is_template"] = is_template
        if default_branch:
            data["default_branch"] = default_branch
        if allow_squash_merge:
            data["allow_squash_merge"] = allow_squash_merge
        if allow_merge_commit:
            data["allow_merge_commit"] = allow_merge_commit
        if allow_rebase_merge:
            data["allow_rebase_merge "] = allow_rebase_merge
        if allow_auto_merge:
            data["allow_auto_merge "] = allow_auto_merge
        if delete_branch_on_merge:
            data["delete_branch_on_merge "] = delete_branch_on_merge
        if use_squash_pr_title_as_default:
            data["use_squash_pr_title_as_default"] = use_squash_pr_title_as_default
        if archived:
            data["archived"] = archived
        if allow_forking:
            data["allow_forking"] = allow_forking

        return await self.request("PATCH", f"/repos/{owner}/{repo}", json=data)

    async def delete_repo(self, *, owner: str, repo: str):
        return await self.request("DELETE", f"/repos/{owner}/{repo}")

    async def enable_automated_security_fixes_for_repo(self, *, owner: str, repo: str):
        return await self.request("PUT", f"/repos/{owner}/{repo}/automated-security-fixes")

    async def disable_automated_security_fixes_for_repo(self, *, owner: str, repo: str):
        return await self.request("DELETE", f"/repos/{owner}/{repo}/automated-security-fixes")

    async def list_codeowners_errors_for_repo(
        self, *, owner: str, repo: str, ref: Optional[str] = None
    ):
        params = {}

        if ref:
            params["ref"] = ref

        return await self.request("GET", f"/repos/{owner}/{repo}/codeowners/errors", params=params)

    async def list_repo_contributors(
        self,
        *,
        owner: str,
        repo: str,
        anon: Optional[bool] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
    ):
        params = {}

        if anon:
            params["anon"] = anon
        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", f"/repos/{owner}/{repo}/contributors", params=params)

    async def create_repo_dispatch_event(
        self, *, owner: str, repo: str, event_name: str, client_payload: Optional[str] = None
    ):
        data = {
            "event_name": event_name,
        }

        if client_payload:
            data["client_payload"] = client_payload

        return await self.request("POST", f"/repos/{owner}/{repo}/dispatches", json=data)

    async def list_repo_languages(self, *, owner: str, repo: str):
        return await self.request("GET", f"/repos/{owner}/{repo}/languages")

    async def list_repo_tags(
        self, *, owner: str, repo: str, per_page: Optional[int] = None, page: Optional[int] = None
    ):
        params = {}

        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", f"/repos/{owner}/{repo}/tags", params=params)

    async def list_repo_teams(
        self, *, owner: str, repo: str, per_page: Optional[int] = None, page: Optional[int] = None
    ):
        params = {}

        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", f"/repos/{owner}/{repo}/teams", params=params)

    async def get_all_repo_topics(
        self, *, owner: str, repo: str, per_page: Optional[int] = None, page: Optional[int] = None
    ):
        params = {}

        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", f"/repos/{owner}/{repo}/topics", params=params)

    async def replace_all_repo_topics(self, *, owner: str, repo: str, names: List[str]):
        return await self.request("PUT", f"/repos/{owner}/{repo}/topics", json={"names": names})

    async def transfer_repo(
        self, *, owner: str, repo: str, new_owner: str, team_ids: Optional[List[int]] = None
    ):
        data: Dict[str, Union[str, List[int]]] = {
            "new_owner": new_owner,
        }

        if team_ids:
            data["team_ids"] = team_ids

        return await self.request("POST", f"/repos/{owner}/{repo}/transfer", json=data)

    async def check_vulnerability_alerts_enabled_for_repo(self, *, owner: str, repo: str):
        return await self.request("GET", f"/repos/{owner}/{repo}/vulnerability-alerts")

    async def enable_repo_vulnerability_alerts(self, *, owner: str, repo: str):
        return await self.request("PUT", f"/repos/{owner}/{repo}/vulnerability-alerts")

    async def disable_repo_vulnerability_alerts(self, *, owner: str, repo: str):
        return await self.request("DELETE", f"/repos/{owner}/{repo}/vulnerability-alerts")

    async def create_repo_using_template(
        self,
        *,
        template_owner: str,
        template_repo: str,
        owner: Optional[str] = None,
        name: str,
        include_all_branches: Optional[bool] = None,
        private: Optional[bool] = None,
    ):
        data: Dict[str, Union[str, bool]] = {
            "name": name,
        }

        if owner:
            data["owner"] = owner
        if include_all_branches:
            data["include_all_branches"] = include_all_branches
        if private:
            data["private"] = private

        return await self.request(
            "POST", f"/repos/{template_owner}/{template_repo}/generate", json=data
        )

    async def list_public_repos(self, *, since: Optional[int] = None):
        params = {}

        if since:
            params["since"] = since

        return await self.request("GET", "/repositories", params=params)

    async def list_repos_for_authenticated_user(
        self,
        *,
        visibility: Optional[Literal["all", "private", "public"]] = None,
        affiliation: Optional[Literal["owner", "collaborator", "organization_member"]] = None,
        type: Optional[Literal["all", "owner", "public", "private", "member"]] = None,
        sort: Optional[Literal["created", "updated", "pushed", "full_name"]] = None,
        direction: Optional[Literal["asc", "desc"]] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        since: Optional[str] = None,
        before: Optional[str] = None,
    ):
        data = {}

        if visibility:
            data["visibility"] = visibility
        if affiliation:
            data["affiliation"] = affiliation
        if type:
            data["type"] = type
        if sort:
            data["sort"] = sort
        if direction:
            data["direction"] = direction
        if per_page:
            data["per_page"] = per_page
        if page:
            data["page"] = page
        if since:
            data["since"] = since
        if before:
            data["before"] = before

        return self.request("POST", "/user/repos", json=data)

    async def create_repo_for_authenticated_user(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        homepage: Optional[str] = None,
        private: Optional[bool] = None,
        has_issues: Optional[bool] = None,
        has_projects: Optional[bool] = None,
        has_wiki: Optional[bool] = None,
        team_id: Optional[int] = None,
        auto_init: Optional[bool] = None,
        gitignore_template: Optional[str] = None,
        license_template: Optional[str] = None,
        allow_squash_merge: Optional[bool] = None,
        allow_merge_commit: Optional[bool] = None,
        allow_rebase_merge: Optional[bool] = None,
        allow_auto_merge: Optional[bool] = None,
        delete_branch_on_merge: Optional[bool] = None,
        has_downloads: Optional[bool] = None,
        is_template: Optional[bool] = None,
    ):
        data: Dict[str, Union[str, bool, int]] = {
            "name": name,
        }

        if description:
            data["description"] = description
        if homepage:
            data["homepage"] = homepage
        if private:
            data["private"] = private
        if has_issues:
            data["has_issues"] = has_issues
        if has_projects:
            data["has_projects"] = has_projects
        if has_wiki:
            data["has_wiki"] = has_wiki
        if team_id:
            data["team_id"] = team_id
        if auto_init:
            data["auto_init"] = auto_init
        if gitignore_template:
            data["gitignore_template"] = gitignore_template
        if license_template:
            data["license_template"] = license_template
        if allow_squash_merge:
            data["allow_squash_merge"] = allow_squash_merge
        if allow_merge_commit:
            data["allow_merge_commit"] = allow_merge_commit
        if allow_rebase_merge:
            data["allow_rebase_merge"] = allow_rebase_merge
        if allow_auto_merge:
            data["allow_auto_merge"] = allow_auto_merge
        if delete_branch_on_merge:
            data["delete_branch_on_merge"] = delete_branch_on_merge
        if has_downloads:
            data["has_downloads"] = has_downloads
        if is_template:
            data["is_template"] = is_template

        return await self.request("POST", "/user/repos", json=data)

    async def list_repos_for_user(
        self,
        *,
        username: str,
        type: Optional[
            Literal["all", "public", "private", "forks", "sources", "member", "internal"]
        ] = None,
        sort: Optional[Literal["created", "updated", "pushed", "full_name"]] = None,
        direction: Optional[Literal["asc", "desc"]] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
    ):
        params = {}

        if type:
            params["type"] = type
        if sort:
            params["sort"] = sort
        if direction:
            params["direction"] = direction
        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", f"/users/{username}/repos", params=params)

    async def list_repo_autolinks(self, *, owner: str, repo: str, page: Optional[int] = None):
        params = {}

        if page:
            params["page"] = page

        return await self.request("GET", f"/repos/{owner}/{repo}/autolinks", params=params)

    async def create_autolink_reference_for_repo(
        self, *, owner: str, repo: str, key_prefix: str, url_template: str
    ):
        return await self.request(
            "POST",
            f"/repos/{owner}/{repo}/autolinks",
            json={"key_prefix": key_prefix, "url_template": url_template},
        )

    async def get_autolink_reference_for_repo(self, *, owner: str, repo: str, autolink_id: str):
        return await self.request("GET", f"/repos/{owner}/{repo}/autolinks/{autolink_id}")

    async def delete_autolink_reference_for_repo(self, *, owner: str, repo: str, autolink_id: str):
        return await self.request("DELETE", f"/repos/{owner}/{repo}/autolinks/{autolink_id}")

    async def get_repo_content(
        self, *, owner: str, repo: str, path: str, ref: Optional[str] = None
    ):
        params = {}

        if ref:
            params["ref"] = ref

        return await self.request("GET", f"/repos/{owner}/{repo}/contents/{path}", params=params)

    async def create_or_update_repo_file_contents(
        self,
        *,
        owner: str,
        repo: str,
        path: str,
        message: str,
        content: str,
        sha: Optional[str] = None,
        branch: Optional[str] = None,
        committer: Optional[Committer] = None,
        author: Optional[Author] = None,
    ):
        data: Dict[str, Union[str, Committer, Author]] = {
            "message": message,
            "content": content,
        }

        if sha:
            data["sha"] = sha
        if branch:
            data["branch"] = branch
        if committer:
            data["committer"] = committer
        if author:
            data["author"] = author

        return await self.request("PUT", f"/repos/{owner}/{repo}/contents/{path}", json=data)

    async def delete_repo_file(
        self,
        *,
        owner: str,
        repo: str,
        path: str,
        message: str,
        sha: str,
        branch: Optional[str] = None,
        committer: Optional[OptionalCommitter] = None,
        author: Optional[OptionalAuthor] = None,
    ):
        data: Dict[str, Union[str, OptionalCommitter, OptionalAuthor]] = {
            "message": message,
            "sha": sha,
        }

        if branch:
            data["branch"] = branch
        if committer:
            data["committer"] = committer
        if author:
            data["author"] = author

        return await self.request("DELETE", f"/repos/{owner}/{repo}/contents/{path}", json=data)

    async def get_repo_readme(self, *, owner: str, repo: str):
        return await self.request("GET", f"/repos/{owner}/{repo}/readme")

    async def get_repo_readme_for_directory(
        self, *, owner: str, repo: str, dir: str, ref: Optional[str] = None
    ):
        params = {}

        if ref:
            params["ref"] = ref

        return await self.request("GET", f"/repos/{owner}/{repo}/readme/{dir}", params=params)

    async def download_repo_archive(
        self,
        *,
        owner: str,
        repo: str,
        archive_format: Literal["tarball", "zipball"],
        ref: Optional[str] = None,
    ):
        params = {}

        if ref:
            params["ref"] = ref

        return await self.request("GET", f"/repos/{owner}/{repo}/{archive_format}", params=params)

    async def list_repo_forks(
        self,
        *,
        owner: str,
        repo: str,
        sort: Optional[Literal["newest", "oldest", "stargazers", "watchers"]] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
    ):
        params = {}

        if sort:
            params["sort"] = sort
        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", f"/repos/{owner}/{repo}/forks", params=params)

    async def create_repo_fork(self, *, owner: str, repo: str, organization: Optional[str] = None):
        data = {}

        if organization:
            data["organization"] = organization

        return await self.request("POST", f"/repos/{owner}/{repo}/forks", json=data)

    async def enable_git_lfs_for_repo(self, *, owner: str, repo: str):
        return await self.request("PUT", f"/repos/{owner}/{repo}/lfs")

    async def disable_git_lfs_for_repo(self, *, owner: str, repo: str):
        return await self.request("DELETE", f"/repos/{owner}/{repo}/lfs")

    async def list_tag_protection_states_for_repo(self, *, owner: str, repo: str):
        return await self.request("GET", f"/repos/{owner}/{repo}/tags/protection")

    async def create_tag_protection_state_for_repo(
        self,
        *,
        owner: str,
        repo: str,
        pattern: str,
    ):
        data = {}

        if pattern:
            data["pattern"] = pattern

        return await self.request("POST", f"/repos/{owner}/{repo}/tags/protection", json=data)

    async def delete_tag_protection_state_for_repo(
        self, *, owner: str, repo: str, tag_protection_id: int
    ):
        return await self.request(
            "DELETE", f"/repos/{owner}/{repo}/tags/protection/{tag_protection_id}"
        )

    # === GISTS === #

    async def list_gists_for_authenticated_user(
        self,
        *,
        since: Optional[str] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
    ):
        params = {}

        if since:
            params["since"] = since
        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", "/gists", params=params)

    async def create_gist(
        self, *, description: Optional[str] = None, files: List[File], public: Optional[bool] = None
    ):
        data: Dict[str, Union[str, bool, Dict[str, str]]] = {
            "files": {f.name: f.read() for f in files},
        }

        if description:
            data["description"] = description
        if public:
            data["public"] = public

        return await self.request("POST", "/gists", json=data)

    async def list_public_gists(
        self,
        *,
        since: Optional[str] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
    ):
        params = {}

        if since:
            params["since"] = since
        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", "/gists/public", params=params)

    async def list_starred_gists(
        self,
        *,
        since: Optional[str] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
    ):
        params = {}

        if since:
            params["since"] = since
        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", "/gists/starred", params=params)

    async def get_gist(self, *, gist_id: str):
        return await self.request("GET", f"/gists/{gist_id}")

    async def update_gist(
        self, *, gist_id: str, description: Optional[str] = None, files: Optional[List[File]] = None
    ):
        data = {}

        if description:
            data["description"] = description
        if files:
            data["files"] = {f.name: f.read() for f in files}

        return await self.request("PATCH", f"/gists/{gist_id}")

    async def delete_gist(self, *, gist_id: str):
        return await self.request("DELETE", f"/gists/{gist_id}")

    async def list_gist_commits(
        self, *, gist_id: str, per_page: Optional[int] = None, page: Optional[int] = None
    ):
        params = {}

        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", f"/gists/{gist_id}/commits", params=params)

    async def list_gist_forks(
        self, *, gist_id: str, per_page: Optional[int] = None, page: Optional[int] = None
    ):
        params = {}

        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", f"/gists/{gist_id}/forks", params=params)

    async def fork_gist(self, *, gist_id: str):
        return await self.request("POST", f"/gists/{gist_id}/forks")

    async def check_gist_starred(self, *, gist_id: str):
        return await self.request("GET", f"/gists/{gist_id}/star")

    async def star_gist(self, *, gist_id: str):
        return await self.request("PUT", f"/gists/{gist_id}/star")

    async def unstar_gist(self, *, gist_id: str):
        return await self.request("DELETE", f"/gists/{gist_id}/star")

    async def get_gist_revision(self, *, gist_id: str, sha: str):
        return await self.request("GET", f"/gists/{gist_id}/{sha}")

    async def list_gists_for_user(
        self,
        *,
        username: str,
        since: Optional[str] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
    ):
        params = {}

        if since:
            params["since"] = since
        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", f"/users/{username}/gists", params=params)

    async def list_gist_comments(
        self, *, gist_id: str, per_page: Optional[int] = None, page: Optional[int] = None
    ):
        params = {}

        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", f"/gists/{gist_id}/comments", params=params)

    async def create_gist_comment(self, *, gist_id: str, body: str):
        return await self.request("POST", f"/gists/{gist_id}/comments", json={"body": body})

    async def get_gist_comment(self, *, gist_id: str, comment_id: str):
        return await self.request("GET", f"/gists/{gist_id}/comments/{comment_id}")

    async def update_gist_comment(self, *, gist_id: str, comment_id: str, body: str):
        return await self.request(
            "PATCH", f"/gists/{gist_id}/comments/{comment_id}", json={"body": body}
        )

    async def delete_gist_comment(self, *, gist_id: str, comment_id: str):
        return await self.request("DELETE", f"/gists/{gist_id}/comments/{comment_id}")

    # === LICENSES === #

    async def get_all_commonly_used_licenses(self):
        return await self.request("GET", "/licenses")

    async def get_license(self, *, license: str):
        return await self.request("GET", f"/licenses/{license}")

    async def get_license_for_repo(self, *, owner: str, repo: str):
        return await self.request("GET", f"/repos/{owner}/{repo}/license")

    # === GITIGNORE === #

    async def get_all_gitignore_templates(self):
        return await self.request("GET", "/gitignore/templates")

    async def get_gitignore_template(self, *, name: str):
        return await self.request("GET", f"/gitignore/templates/{name}")

    # === EMOJIS === #

    async def get_emojis(self):
        return await self.request("GET", "/emojis")

    # === CODES OF CONDUCT === #

    async def get_all_codes_of_conduct(self):
        return await self.request("GET", "/codes_of_conduct")

    async def get_code_of_conduct(self, *, key: str):
        return await self.request("GET", f"/codes_of_conduct/{key}")

    # === DEPLOY KEYS === #

    async def list_deploy_keys(
        self, *, owner: str, repo: str, per_page: Optional[int] = None, page: Optional[int] = None
    ):
        params = {}

        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", f"/repos/{owner}/{repo}/keys", params=params)

    async def create_deploy_key(
        self,
        *,
        owner: str,
        repo: str,
        title: Optional[str] = None,
        key: str,
        read_only: Optional[bool] = None,
    ):
        data: Dict[str, Union[str, bool]] = {
            "key": key,
        }

        if title:
            data["title"] = title
        if read_only:
            data["read_only"] = read_only

        return await self.request("POST", f"/repos/{owner}/{repo}/keys", data=data)

    async def get_deploy_key(self, *, owner: str, repo: str, key_id: int):
        return await self.request("GET", f"/repos/{owner}/{repo}/keys/{key_id}")

    async def delete_deploy_key(self, *, owner: str, repo: str, key_id: int):
        return await self.request("DELETE", f"/repos/{owner}/{repo}/keys/{key_id}")

    # === MARKDOWN === #

    async def render_markdown(
        self,
        *,
        text: str,
        mode: Optional[Literal["markdown", "gfm"]] = None,
        context: Optional[str] = None,
    ):
        data = {
            "text": text,
        }

        if mode:
            data["mode"] = mode
        if context:
            data["context"] = context

        return await self.request("POST", "/markdown", data=data)

    # TODO: Implement Markdown raw request, idk

    # === META === #

    async def get_github_api_root(self):
        return await self.request("GET", "/")

    async def get_git_hub_meta_info(self):
        return await self.request("GET", "/meta")

    async def get_octocat(self):
        return await self.request("GET", "/octocat")

    async def get_the_zen_of_github(self):
        return await self.request("GET", "/zen")

    # === SEARCH === #

    async def search_code(
        self,
        *,
        q: str,
        sort: Optional[Literal["indexed"]] = None,
        order: Optional[Literal["desc", "asc"]] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
    ):
        data: Dict[str, Union[str, int]] = {
            "q": q,
        }

        if sort:
            data["sort"] = sort
        if order:
            data["order"] = order
        if per_page:
            data["per_page"] = per_page
        if page:
            data["page"] = page

        return await self.request("GET", "/search/code", data=data)

    async def search_commits(
        self,
        *,
        q: str,
        sort: Optional[Literal["author-date", "committer-date"]] = None,
        order: Optional[Literal["desc", "asc"]] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
    ):
        params: Dict[str, Union[str, int]] = {
            "q": q,
        }

        if sort:
            params["sort"] = sort
        if order:
            params["order"] = order
        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", "/search/commits", params=params)

    async def search_issues_and_pull_requests(
        self,
        *,
        q: str,
        sort: Optional[
            Literal[
                "comments",
                "reactions",
                "reactions-+1",
                "reactions--1",
                "reactions-smile",
                "reactions-thinking_face",
                "reactions-heart",
                "reactions-tada",
                "interactions",
                "created",
                "updated",
            ]
        ] = None,
        order: Optional[Literal["desc", "asc"]] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
    ):
        params: Dict[str, Union[str, int]] = {
            "q": q,
        }

        if sort:
            params["sort"] = sort
        if order:
            params["order"] = order
        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", "/search/issues", params=params)

    async def search_labels(
        self,
        *,
        repository_id: int,
        q: str,
        sort: Optional[Literal["created", "updated"]] = None,
        order: Optional[Literal["desc", "asc"]] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
    ):
        params = {
            "repository_id": repository_id,
            "q": q,
        }

        if sort:
            params["sort"] = sort
        if order:
            params["order"] = order
        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", "/search/labels", params=params)

    async def search_repos(
        self,
        *,
        q: str,
        sort: Optional[Literal["stars", "forks", "help-wanted-issues", "updated"]] = None,
        order: Optional[Literal["desc", "asc"]] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
    ):
        params: Dict[str, Union[str, int]] = {
            "q": q,
        }

        if sort:
            params["sort"] = sort
        if order:
            params["order"] = order
        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", "/search/repositories", params=params)

    async def search_topics(
        self,
        *,
        q: str,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
    ):
        params: Dict[str, Union[str, int]] = {
            "q": q,
        }

        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", "/search/topics", params=params)

    async def search_users(
        self,
        *,
        q: str,
        sort: Optional[Literal["followers", "repositories", "joined"]] = None,
        order: Optional[Literal["desc", "asc"]] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
    ):
        params: Dict[str, Union[str, int]] = {
            "q": q,
        }

        if sort:
            params["sort"] = sort
        if order:
            params["order"] = order
        if per_page:
            params["per_page"] = per_page
        if page:
            params["page"] = page

        return await self.request("GET", "/search/users", params=params)
