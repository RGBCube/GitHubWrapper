from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, TypedDict

if TYPE_CHECKING:
    from typing_extensions import NotRequired


class LicenseSimple(TypedDict):
    # Example: mit
    key: str
    # Example: MIT License
    name: str
    # Format: uri
    # Example: https://api.github.com/licenses/mit
    url: Optional[str]
    # Example: MIT
    spdx_id: Optional[str]
    # Example: MDc6TGljZW5zZW1pdA==
    node_id: str
    # Format: uri
    html_url: NotRequired[str]


class SimpleUser(TypedDict):
    name: NotRequired[Optional[str]]
    email: NotRequired[Optional[str]]
    # Example: octocat
    login: str
    # Example: 1
    id: int
    # Example: MDQ6VXNlcjE=
    node_id: str
    # Format: uri
    # Example: https://github.com/images/error/octocat_happy.gif
    avatar_url: str
    # Example: 41d064eb2195891e12d0413f63227ea7
    gravatar_id: Optional[str]
    # Format: uri
    # Example: https://api.github.com/users/octocat
    url: str
    # Format: uri
    # Example: https://github.com/octocat
    html_url: str
    # Format: uri
    # Example: https://api.github.com/users/octocat/followers
    followers_url: str
    # Example: https://api.github.com/users/octocat/following{/other_user}
    following_url: str
    # Example: https://api.github.com/users/octocat/gists{/gist_id}
    gists_url: str
    # Example: https://api.github.com/users/octocat/starred{/owner}{/repo}
    starred_url: str
    # Format: uri
    # Example: https://api.github.com/users/octocat/subscriptions
    subscriptions_url: str
    # Format: uri
    # Example: https://api.github.com/users/octocat/orgs
    organizations_url: str
    # Format: uri
    # Example: https://api.github.com/users/octocat/repos
    repos_url: str
    # Example: https://api.github.com/users/octocat/events{/privacy}
    events_url: str
    # Format: uri
    # Example: https://api.github.com/users/octocat/received_events
    received_events_url: str
    # Example: User
    type: str
    site_admin: bool
    # Example: "2020-07-09T00:17:55Z"
    starred_at: NotRequired[str]


class Permissions(TypedDict):
    admin: bool
    pull: bool
    triage: NotRequired[bool]
    push: bool
    maintain: NotRequired[bool]


class SimpleUser(TypedDict):
    name: NotRequired[Optional[str]]
    email: NotRequired[Optional[str]]
    # Example: octocat
    login: str
    # Example: 1
    id: int
    # Example: MDQ6VXNlcjE=
    node_id: str
    # Format: uri
    # Example: https://github.com/images/error/octocat_happy.gif
    avatar_url: str
    # Example: 41d064eb2195891e12d0413f63227ea7
    gravatar_id: Optional[str]
    # Format: uri
    # Example: https://api.github.com/users/octocat
    url: str
    # Format: uri
    # Example: https://github.com/octocat
    html_url: str
    # Format: uri
    # Example: https://api.github.com/users/octocat/followers
    followers_url: str
    # Example: https://api.github.com/users/octocat/following{/other_user}
    following_url: str
    # Example: https://api.github.com/users/octocat/gists{/gist_id}
    gists_url: str
    # Example: https://api.github.com/users/octocat/starred{/owner}{/repo}
    starred_url: str
    # Format: uri
    # Example: https://api.github.com/users/octocat/subscriptions
    subscriptions_url: str
    # Format: uri
    # Example: https://api.github.com/users/octocat/orgs
    organizations_url: str
    # Format: uri
    # Example: https://api.github.com/users/octocat/repos
    repos_url: str
    # Example: https://api.github.com/users/octocat/events{/privacy}
    events_url: str
    # Format: uri
    # Example: https://api.github.com/users/octocat/received_events
    received_events_url: str
    # Example: User
    type: str
    site_admin: bool
    # Example: "2020-07-09T00:17:55Z"
    starred_at: NotRequired[str]


class Repository(TypedDict):
    # Example: 42
    id: int
    # Example: MDEwOlJlcG9zaXRvcnkxMjk2MjY5
    node_id: str
    # Example: Team Environment
    name: str
    # Example: octocat/Hello-World
    full_name: str
    license: Optional[LicenseSimple]
    organization: NotRequired[Optional[SimpleUser]]
    forks: int
    permissions: NotRequired[Permissions]
    owner: SimpleUser
    private: bool
    # Format: uri
    # Example: https://github.com/octocat/Hello-World
    html_url: str
    # Example: This your first repo!
    description: Optional[str]
    fork: bool
    # Format: uri
    # Example: https://api.github.com/repos/octocat/Hello-World
    url: str
    # Example: http://api.github.com/repos/octocat/Hello-World/{archive_format}{/ref}
    archive_url: str
    # Example: http://api.github.com/repos/octocat/Hello-World/assignees{/user}
    assignees_url: str
    # Example: http://api.github.com/repos/octocat/Hello-World/git/blobs{/sha}
    blobs_url: str
    # Example: http://api.github.com/repos/octocat/Hello-World/branches{/branch}
    branches_url: str
    # Example: http://api.github.com/repos/octocat/Hello-World/collaborators{/collaborator}
    collaborators_url: str
    # Example: http://api.github.com/repos/octocat/Hello-World/comments{/number}
    comments_url: str
    # Example: http://api.github.com/repos/octocat/Hello-World/commits{/sha}
    commits_url: str
    # Example: http://api.github.com/repos/octocat/Hello-World/compare/{base}...{head}
    compare_url: str
    # Example: http://api.github.com/repos/octocat/Hello-World/contents/{+path}
    contents_url: str
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/contributors
    contributors_url: str
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/deployments
    deployments_url: str
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/downloads
    downloads_url: str
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/events
    events_url: str
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/forks
    forks_url: str
    # Example: http://api.github.com/repos/octocat/Hello-World/git/commits{/sha}
    git_commits_url: str
    # Example: http://api.github.com/repos/octocat/Hello-World/git/refs{/sha}
    git_refs_url: str
    # Example: http://api.github.com/repos/octocat/Hello-World/git/tags{/sha}
    git_tags_url: str
    # Example: git:github.com/octocat/Hello-World.git
    git_url: str
    # Example: http://api.github.com/repos/octocat/Hello-World/issues/comments{/number}
    issue_comment_url: str
    # Example: http://api.github.com/repos/octocat/Hello-World/issues/events{/number}
    issue_events_url: str
    # Example: http://api.github.com/repos/octocat/Hello-World/issues{/number}
    issues_url: str
    # Example: http://api.github.com/repos/octocat/Hello-World/keys{/key_id}
    keys_url: str
    # Example: http://api.github.com/repos/octocat/Hello-World/labels{/name}
    labels_url: str
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/languages
    languages_url: str
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/merges
    merges_url: str
    # Example: http://api.github.com/repos/octocat/Hello-World/milestones{/number}
    milestones_url: str
    # Example: http://api.github.com/repos/octocat/Hello-World/notifications{?since,all,participating}
    notifications_url: str
    # Example: http://api.github.com/repos/octocat/Hello-World/pulls{/number}
    pulls_url: str
    # Example: http://api.github.com/repos/octocat/Hello-World/releases{/id}
    releases_url: str
    # Example: git@github.com:octocat/Hello-World.git
    ssh_url: str
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/stargazers
    stargazers_url: str
    # Example: http://api.github.com/repos/octocat/Hello-World/statuses/{sha}
    statuses_url: str
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/subscribers
    subscribers_url: str
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/subscription
    subscription_url: str
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/tags
    tags_url: str
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/teams
    teams_url: str
    # Example: http://api.github.com/repos/octocat/Hello-World/git/trees{/sha}
    trees_url: str
    # Example: https://github.com/octocat/Hello-World.git
    clone_url: str
    # Format: uri
    # Example: git:git.example.com/octocat/Hello-World
    mirror_url: Optional[str]
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/hooks
    hooks_url: str
    # Format: uri
    # Example: https://svn.github.com/octocat/Hello-World
    svn_url: str
    # Format: uri
    # Example: https://github.com
    homepage: Optional[str]
    language: Optional[str]
    # Example: 9
    forks_count: int
    # Example: 80
    stargazers_count: int
    # Example: 80
    watchers_count: int
    # Example: 108
    size: int
    # Example: master
    default_branch: str
    # Example: 0
    open_issues_count: int
    # Example: True
    is_template: NotRequired[bool]
    topics: NotRequired[List[str]]
    # Example: True
    has_issues: bool
    # Example: True
    has_projects: bool
    # Example: True
    has_wiki: bool
    has_pages: bool
    # Example: True
    has_downloads: bool
    archived: bool
    disabled: bool
    visibility: NotRequired[str]
    # Format: date-time
    # Example: 2011-01-26T19:06:43Z
    pushed_at: Optional[str]
    # Format: date-time
    # Example: 2011-01-26T19:01:12Z
    created_at: Optional[str]
    # Format: date-time
    # Example: 2011-01-26T19:14:43Z
    updated_at: Optional[str]
    # Example: True
    allow_rebase_merge: NotRequired[bool]
    template_repository: NotRequired[Optional[dict]]
    temp_clone_token: NotRequired[str]
    # Example: True
    allow_squash_merge: NotRequired[bool]
    # Example: False
    allow_auto_merge: NotRequired[bool]
    # Example: False
    delete_branch_on_merge: NotRequired[bool]
    # Example: False
    allow_update_branch: NotRequired[bool]
    use_squash_pr_title_as_default: NotRequired[bool]
    # Example: True
    allow_merge_commit: NotRequired[bool]
    allow_forking: NotRequired[bool]
    subscribers_count: NotRequired[int]
    network_count: NotRequired[int]
    open_issues: int
    watchers: int
    master_branch: NotRequired[str]
    # Example: "2020-07-09T00:17:42Z"
    starred_at: NotRequired[str]


GeneratedObjectResult = Repository
