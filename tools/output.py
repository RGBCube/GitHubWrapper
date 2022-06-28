from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, TypedDict

if TYPE_CHECKING:
    from typing_extensions import NotRequired


class SimpleUser(TypedDict):
    name: NotRequired[Optional[str]]
    email: NotRequired[Optional[str]]
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: Optional[str]
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    type: str
    site_admin: bool
    starred_at: NotRequired[str]


class Permissions(TypedDict):
    admin: NotRequired[bool]
    maintain: NotRequired[bool]
    push: NotRequired[bool]
    triage: NotRequired[bool]
    pull: NotRequired[bool]


class LicenseSimple(TypedDict):
    key: str
    name: str
    url: Optional[str]
    spdx_id: Optional[str]
    node_id: str
    html_url: NotRequired[str]


class Repository(TypedDict):
    id: int
    node_id: str
    name: str
    full_name: str
    license: Optional[LicenseSimple]
    organization: NotRequired[Optional[SimpleUser]]
    forks: int
    permissions: NotRequired[Permissions]
    owner: SimpleUser
    private: bool
    html_url: str
    description: Optional[str]
    fork: bool
    url: str
    archive_url: str
    assignees_url: str
    blobs_url: str
    branches_url: str
    collaborators_url: str
    comments_url: str
    commits_url: str
    compare_url: str
    contents_url: str
    contributors_url: str
    deployments_url: str
    downloads_url: str
    events_url: str
    forks_url: str
    git_commits_url: str
    git_refs_url: str
    git_tags_url: str
    git_url: str
    issue_comment_url: str
    issue_events_url: str
    issues_url: str
    keys_url: str
    labels_url: str
    languages_url: str
    merges_url: str
    milestones_url: str
    notifications_url: str
    pulls_url: str
    releases_url: str
    ssh_url: str
    stargazers_url: str
    statuses_url: str
    subscribers_url: str
    subscription_url: str
    tags_url: str
    teams_url: str
    trees_url: str
    clone_url: str
    mirror_url: Optional[str]
    hooks_url: str
    svn_url: str
    homepage: Optional[str]
    language: Optional[str]
    forks_count: int
    stargazers_count: int
    watchers_count: int
    size: int
    default_branch: str
    open_issues_count: int
    is_template: NotRequired[bool]
    topics: NotRequired[List[str]]
    has_issues: bool
    has_projects: bool
    has_wiki: bool
    has_pages: bool
    has_downloads: bool
    archived: bool
    disabled: bool
    visibility: NotRequired[str]
    pushed_at: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    allow_rebase_merge: NotRequired[bool]
    template_repository: NotRequired[Optional[dict]]
    temp_clone_token: NotRequired[str]
    allow_squash_merge: NotRequired[bool]
    allow_auto_merge: NotRequired[bool]
    delete_branch_on_merge: NotRequired[bool]
    allow_update_branch: NotRequired[bool]
    use_squash_pr_title_as_default: NotRequired[bool]
    allow_merge_commit: NotRequired[bool]
    allow_forking: NotRequired[bool]
    subscribers_count: NotRequired[int]
    network_count: NotRequired[int]
    open_issues: int
    watchers: int
    master_branch: NotRequired[str]
    starred_at: NotRequired[str]


class CodeOfConduct(TypedDict):
    key: str
    name: str
    url: str
    body: NotRequired[str]
    html_url: Optional[str]


class MinimalRepository(TypedDict):
    id: int
    node_id: str
    name: str
    full_name: str
    owner: SimpleUser
    private: bool
    html_url: str
    description: Optional[str]
    fork: bool
    url: str
    archive_url: str
    assignees_url: str
    blobs_url: str
    branches_url: str
    collaborators_url: str
    comments_url: str
    commits_url: str
    compare_url: str
    contents_url: str
    contributors_url: str
    deployments_url: str
    downloads_url: str
    events_url: str
    forks_url: str
    git_commits_url: str
    git_refs_url: str
    git_tags_url: str
    git_url: NotRequired[str]
    issue_comment_url: str
    issue_events_url: str
    issues_url: str
    keys_url: str
    labels_url: str
    languages_url: str
    merges_url: str
    milestones_url: str
    notifications_url: str
    pulls_url: str
    releases_url: str
    ssh_url: NotRequired[str]
    stargazers_url: str
    statuses_url: str
    subscribers_url: str
    subscription_url: str
    tags_url: str
    teams_url: str
    trees_url: str
    clone_url: NotRequired[str]
    mirror_url: NotRequired[Optional[str]]
    hooks_url: str
    svn_url: NotRequired[str]
    homepage: NotRequired[Optional[str]]
    language: NotRequired[Optional[str]]
    forks_count: NotRequired[int]
    stargazers_count: NotRequired[int]
    watchers_count: NotRequired[int]
    size: NotRequired[int]
    default_branch: NotRequired[str]
    open_issues_count: NotRequired[int]
    is_template: NotRequired[bool]
    topics: NotRequired[List[str]]
    has_issues: NotRequired[bool]
    has_projects: NotRequired[bool]
    has_wiki: NotRequired[bool]
    has_pages: NotRequired[bool]
    has_downloads: NotRequired[bool]
    archived: NotRequired[bool]
    disabled: NotRequired[bool]
    visibility: NotRequired[str]
    pushed_at: NotRequired[Optional[str]]
    created_at: NotRequired[Optional[str]]
    updated_at: NotRequired[Optional[str]]
    permissions: NotRequired[Permissions]
    role_name: NotRequired[str]
    template_repository: NotRequired[Optional[Repository]]
    temp_clone_token: NotRequired[str]
    delete_branch_on_merge: NotRequired[bool]
    subscribers_count: NotRequired[int]
    network_count: NotRequired[int]
    code_of_conduct: NotRequired[CodeOfConduct]
    license: NotRequired[Optional[dict]]
    forks: NotRequired[int]
    open_issues: NotRequired[int]
    watchers: NotRequired[int]
    allow_forking: NotRequired[bool]


class GeneratedObject116(TypedDict):
    text: NotRequired[str]
    indices: NotRequired[List[int]]


class GeneratedObject122(TypedDict):
    object_url: NotRequired[str]
    object_type: NotRequired[Optional[str]]
    property: NotRequired[str]
    fragment: NotRequired[str]
    matches: NotRequired[List[GeneratedObject116]]


class CodeSearchResultItem(TypedDict):
    name: str
    path: str
    sha: str
    url: str
    git_url: str
    html_url: str
    repository: MinimalRepository
    score: float
    file_size: NotRequired[int]
    language: NotRequired[Optional[str]]
    last_modified_at: NotRequired[str]
    line_numbers: NotRequired[List[str]]
    text_matches: NotRequired[List[GeneratedObject122]]


class GeneratedObject188(TypedDict):
    total_count: int
    incomplete_results: bool
    items: List[CodeSearchResultItem]


GeneratedObject = GeneratedObject188
