__all__ = ("Committer", "OptionalCommitter", "Author", "OptionalAuthor")

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from typing_extensions import NotRequired


class Committer(TypedDict):
    name: str
    email: str
    date: NotRequired[str]


class OptionalCommitter(TypedDict):
    name: NotRequired[str]
    email: NotRequired[str]


class Author(TypedDict):
    name: str
    email: str
    date: NotRequired[str]


class OptionalAuthor(TypedDict):
    name: NotRequired[str]
    email: NotRequired[str]
