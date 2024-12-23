from dataclasses import dataclass


@dataclass
class Collection[T](set[T]):
    _attr_parent: str
    _parent: object

    def add(self, *items: T):
        for item in items:
            if getattr(item, self._attr_parent) is not None:
                raise ValueError("item already belongs to another collection")

            super().add(item)
            setattr(item, self._attr_parent, self._parent)

    def remove(self, item: T):
        self._detach(item)
        super().remove(item)

    def discard(self, item: T):
        self._detach(item)
        super().discard(item)

    def pop(self) -> T:
        item = super().pop()
        self._detach(item)
        return item

    def clear(self):
        for item in self:
            self._detach(item)
        super().clear()

    def _detach(self, item: T):
        if getattr(item, self._attr_parent) is not self._parent:
            raise ValueError("item does not belong to this collection")

        setattr(item, self._attr_parent, None)
