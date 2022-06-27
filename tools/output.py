from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, TypedDict

if TYPE_CHECKING:
    from typing_extensions import NotRequired


class LicenseSimple(TypedDict):
    key: str
    name: str
    url: Optional[str]
    spdx_id: Optional[str]
    node_id: str
    html_url: NotRequired[str]


GeneratedObjectResult = List[LicenseSimple]
