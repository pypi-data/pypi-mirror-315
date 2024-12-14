import typing

from .classic import classic

if typing.TYPE_CHECKING:
    levenshtein: typing.Callable[[str, str], int]

try:
    from .native import wagner_fischer_native  # type: ignore

    levenshtein = wagner_fischer_native
except ImportError:
    from .wagner_fischer import wagner_fischer

    levenshtein = wagner_fischer

__all__ = ["classic", "levenshtein", "wagner_fischer"]
