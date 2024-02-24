from abc import ABC


class TagsMixin(ABC):
    _tags: set[str]

    def __init__(self, tags: set[str] = set()) -> None:
        self._tags = tags

    @property
    def tags(self) -> set[str]:
        return self._tags

    def has_tags(self, *tags: str) -> bool:
        return set(tags) <= self._tags
