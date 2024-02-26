from abc import ABC


class TagsMixin(ABC):
    _tags: set[str]

    def __init__(self, tags: set[str] = set()) -> None:
        self._tags = tags

    @property
    def tags(self) -> set[str]:
        return self._tags
    
    def add_tag(self, value: str) -> None:
        self._tags.add(value)
        
    def remove_tag(self, value: str) -> None:
        self._tags.remove(value)

    def has_tags(self, *tags: str) -> bool:
        return set(tags) <= self._tags
