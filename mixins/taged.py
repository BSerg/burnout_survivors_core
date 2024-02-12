from abc import ABC


class TagsMixin(ABC):
    _tags: set[str]

    def __init__(self, tags: set[str] = set()) -> None:
        self._tags = tags

    @property
    def tags(self):
        return self._tags

    def has_tag(self, tag: str) -> bool:
        return tag in self.tags
