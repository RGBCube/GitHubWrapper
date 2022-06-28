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


GeneratedObject = List[SimpleUser]
