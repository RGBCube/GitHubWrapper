from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, TypedDict

if TYPE_CHECKING:
    from typing_extensions import NotRequired


class Repository(TypedDict):
    # Example: 42
    id: NotRequired[int]
    # Example: MDEwOlJlcG9zaXRvcnkxMjk2MjY5
    node_id: NotRequired[str]
    # Example: Team Environment
    name: NotRequired[str]
    # Example: octocat/Hello-World
    full_name: NotRequired[str]


class LicenseSimple(TypedDict):
    # Example: mit
    key: NotRequired[str]
    # Example: MIT License
    name: NotRequired[str]
    # Format: uri
    # Example: https://api.github.com/licenses/mit
    url: NotRequired[Optional[str]]
    # Example: MIT
    spdx_id: NotRequired[Optional[str]]
    # Example: MDc6TGljZW5zZW1pdA==
    node_id: NotRequired[str]
    # Format: uri
    html_url: NotRequired[str]
    license: NotRequired[Optional[LicenseSimple]]


class SimpleUser(TypedDict):
    name: NotRequired[Optional[str]]
    email: NotRequired[Optional[str]]
    # Example: octocat
    login: NotRequired[str]
    # Example: 1
    id: NotRequired[int]
    # Example: MDQ6VXNlcjE=
    node_id: NotRequired[str]
    # Format: uri
    # Example: https://github.com/images/error/octocat_happy.gif
    avatar_url: NotRequired[str]
    # Example: 41d064eb2195891e12d0413f63227ea7
    gravatar_id: NotRequired[Optional[str]]
    # Format: uri
    # Example: https://api.github.com/users/octocat
    url: NotRequired[str]
    # Format: uri
    # Example: https://github.com/octocat
    html_url: NotRequired[str]
    # Format: uri
    # Example: https://api.github.com/users/octocat/followers
    followers_url: NotRequired[str]
    # Example: https://api.github.com/users/octocat/following{/other_user}
    following_url: NotRequired[str]
    # Example: https://api.github.com/users/octocat/gists{/gist_id}
    gists_url: NotRequired[str]
    # Example: https://api.github.com/users/octocat/starred{/owner}{/repo}
    starred_url: NotRequired[str]
    # Format: uri
    # Example: https://api.github.com/users/octocat/subscriptions
    subscriptions_url: NotRequired[str]
    # Format: uri
    # Example: https://api.github.com/users/octocat/orgs
    organizations_url: NotRequired[str]
    # Format: uri
    # Example: https://api.github.com/users/octocat/repos
    repos_url: NotRequired[str]
    # Example: https://api.github.com/users/octocat/events{/privacy}
    events_url: NotRequired[str]
    # Format: uri
    # Example: https://api.github.com/users/octocat/received_events
    received_events_url: NotRequired[str]
    # Example: User
    type: NotRequired[str]
    site_admin: NotRequired[bool]
    # Example: "2020-07-09T00:17:55Z"
    starred_at: NotRequired[str]
    organization: NotRequired[Optional[SimpleUser]]
    forks: NotRequired[int]


class Permissions(TypedDict):
    admin: NotRequired[bool]
    pull: NotRequired[bool]
    triage: NotRequired[bool]
    push: NotRequired[bool]
    maintain: NotRequired[bool]
    permissions: NotRequired[Permissions]


class SimpleUser(TypedDict):
    name: NotRequired[Optional[str]]
    email: NotRequired[Optional[str]]
    # Example: octocat
    login: NotRequired[str]
    # Example: 1
    id: NotRequired[int]
    # Example: MDQ6VXNlcjE=
    node_id: NotRequired[str]
    # Format: uri
    # Example: https://github.com/images/error/octocat_happy.gif
    avatar_url: NotRequired[str]
    # Example: 41d064eb2195891e12d0413f63227ea7
    gravatar_id: NotRequired[Optional[str]]
    # Format: uri
    # Example: https://api.github.com/users/octocat
    url: NotRequired[str]
    # Format: uri
    # Example: https://github.com/octocat
    html_url: NotRequired[str]
    # Format: uri
    # Example: https://api.github.com/users/octocat/followers
    followers_url: NotRequired[str]
    # Example: https://api.github.com/users/octocat/following{/other_user}
    following_url: NotRequired[str]
    # Example: https://api.github.com/users/octocat/gists{/gist_id}
    gists_url: NotRequired[str]
    # Example: https://api.github.com/users/octocat/starred{/owner}{/repo}
    starred_url: NotRequired[str]
    # Format: uri
    # Example: https://api.github.com/users/octocat/subscriptions
    subscriptions_url: NotRequired[str]
    # Format: uri
    # Example: https://api.github.com/users/octocat/orgs
    organizations_url: NotRequired[str]
    # Format: uri
    # Example: https://api.github.com/users/octocat/repos
    repos_url: NotRequired[str]
    # Example: https://api.github.com/users/octocat/events{/privacy}
    events_url: NotRequired[str]
    # Format: uri
    # Example: https://api.github.com/users/octocat/received_events
    received_events_url: NotRequired[str]
    # Example: User
    type: NotRequired[str]
    site_admin: NotRequired[bool]
    # Example: "2020-07-09T00:17:55Z"
    starred_at: NotRequired[str]
    owner: NotRequired[SimpleUser]
    private: NotRequired[bool]
    # Format: uri
    # Example: https://github.com/octocat/Hello-World
    html_url: NotRequired[str]
    # Example: This your first repo!
    description: NotRequired[Optional[str]]
    fork: NotRequired[bool]
    # Format: uri
    # Example: https://api.github.com/repos/octocat/Hello-World
    url: NotRequired[str]
    # Example: http://api.github.com/repos/octocat/Hello-World/{archive_format}{/ref}
    archive_url: NotRequired[str]
    # Example: http://api.github.com/repos/octocat/Hello-World/assignees{/user}
    assignees_url: NotRequired[str]
    # Example: http://api.github.com/repos/octocat/Hello-World/git/blobs{/sha}
    blobs_url: NotRequired[str]
    # Example: http://api.github.com/repos/octocat/Hello-World/branches{/branch}
    branches_url: NotRequired[str]
    # Example: http://api.github.com/repos/octocat/Hello-World/collaborators{/collaborator}
    collaborators_url: NotRequired[str]
    # Example: http://api.github.com/repos/octocat/Hello-World/comments{/number}
    comments_url: NotRequired[str]
    # Example: http://api.github.com/repos/octocat/Hello-World/commits{/sha}
    commits_url: NotRequired[str]
    # Example: http://api.github.com/repos/octocat/Hello-World/compare/{base}...{head}
    compare_url: NotRequired[str]
    # Example: http://api.github.com/repos/octocat/Hello-World/contents/{+path}
    contents_url: NotRequired[str]
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/contributors
    contributors_url: NotRequired[str]
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/deployments
    deployments_url: NotRequired[str]
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/downloads
    downloads_url: NotRequired[str]
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/events
    events_url: NotRequired[str]
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/forks
    forks_url: NotRequired[str]
    # Example: http://api.github.com/repos/octocat/Hello-World/git/commits{/sha}
    git_commits_url: NotRequired[str]
    # Example: http://api.github.com/repos/octocat/Hello-World/git/refs{/sha}
    git_refs_url: NotRequired[str]
    # Example: http://api.github.com/repos/octocat/Hello-World/git/tags{/sha}
    git_tags_url: NotRequired[str]
    # Example: git:github.com/octocat/Hello-World.git
    git_url: NotRequired[str]
    # Example: http://api.github.com/repos/octocat/Hello-World/issues/comments{/number}
    issue_comment_url: NotRequired[str]
    # Example: http://api.github.com/repos/octocat/Hello-World/issues/events{/number}
    issue_events_url: NotRequired[str]
    # Example: http://api.github.com/repos/octocat/Hello-World/issues{/number}
    issues_url: NotRequired[str]
    # Example: http://api.github.com/repos/octocat/Hello-World/keys{/key_id}
    keys_url: NotRequired[str]
    # Example: http://api.github.com/repos/octocat/Hello-World/labels{/name}
    labels_url: NotRequired[str]
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/languages
    languages_url: NotRequired[str]
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/merges
    merges_url: NotRequired[str]
    # Example: http://api.github.com/repos/octocat/Hello-World/milestones{/number}
    milestones_url: NotRequired[str]
    # Example: http://api.github.com/repos/octocat/Hello-World/notifications{?since,all,participating}
    notifications_url: NotRequired[str]
    # Example: http://api.github.com/repos/octocat/Hello-World/pulls{/number}
    pulls_url: NotRequired[str]
    # Example: http://api.github.com/repos/octocat/Hello-World/releases{/id}
    releases_url: NotRequired[str]
    # Example: git@github.com:octocat/Hello-World.git
    ssh_url: NotRequired[str]
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/stargazers
    stargazers_url: NotRequired[str]
    # Example: http://api.github.com/repos/octocat/Hello-World/statuses/{sha}
    statuses_url: NotRequired[str]
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/subscribers
    subscribers_url: NotRequired[str]
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/subscription
    subscription_url: NotRequired[str]
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/tags
    tags_url: NotRequired[str]
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/teams
    teams_url: NotRequired[str]
    # Example: http://api.github.com/repos/octocat/Hello-World/git/trees{/sha}
    trees_url: NotRequired[str]
    # Example: https://github.com/octocat/Hello-World.git
    clone_url: NotRequired[str]
    # Format: uri
    # Example: git:git.example.com/octocat/Hello-World
    mirror_url: NotRequired[Optional[str]]
    # Format: uri
    # Example: http://api.github.com/repos/octocat/Hello-World/hooks
    hooks_url: NotRequired[str]
    # Format: uri
    # Example: https://svn.github.com/octocat/Hello-World
    svn_url: NotRequired[str]
    # Format: uri
    # Example: https://github.com
    homepage: NotRequired[Optional[str]]
    language: NotRequired[Optional[str]]
    # Example: 9
    forks_count: NotRequired[int]
    # Example: 80
    stargazers_count: NotRequired[int]
    # Example: 80
    watchers_count: NotRequired[int]
    # Example: 108
    size: NotRequired[int]
    # Example: master
    default_branch: NotRequired[str]
    # Example: 0
    open_issues_count: NotRequired[int]
    # Example: True
    is_template: NotRequired[bool]
    topics: NotRequired[List[str]]
    # Example: True
    has_issues: NotRequired[bool]
    # Example: True
    has_projects: NotRequired[bool]
    # Example: True
    has_wiki: NotRequired[bool]
    has_pages: NotRequired[bool]
    # Example: True
    has_downloads: NotRequired[bool]
    archived: NotRequired[bool]
    disabled: NotRequired[bool]
    visibility: NotRequired[str]
    # Format: date-time
    # Example: 2011-01-26T19:06:43Z
    pushed_at: NotRequired[Optional[str]]
    # Format: date-time
    # Example: 2011-01-26T19:01:12Z
    created_at: NotRequired[Optional[str]]
    # Format: date-time
    # Example: 2011-01-26T19:14:43Z
    updated_at: NotRequired[Optional[str]]
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
    open_issues: NotRequired[int]
    watchers: NotRequired[int]
    master_branch: NotRequired[str]
    # Example: "2020-07-09T00:17:42Z"
    starred_at: NotRequired[str]


GeneratedObjectResult = Repository
