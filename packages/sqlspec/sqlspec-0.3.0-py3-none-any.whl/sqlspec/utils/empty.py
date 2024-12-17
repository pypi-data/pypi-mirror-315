from __future__ import annotations

from enum import Enum
from typing import Final, Literal, Union

from sqlspec.typing import UnsetType

__all__ = ("Empty", "EmptyType")


class _EmptyEnum(Enum):
    """A sentinel enum used as placeholder."""

    EMPTY = 0


EmptyType = Union[Literal[_EmptyEnum.EMPTY], UnsetType]
Empty: Final = _EmptyEnum.EMPTY
