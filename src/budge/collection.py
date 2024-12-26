from dataclasses import dataclass, field


@dataclass
class Collection[T]:
    _attr_parent: str
    _parent: object
    data: dict[int, T] = field(init=False, default_factory=dict)

    def add(self, *items: T):
        for item in items:
            self[hash(item)] = item

    def remove(self, item: T):
        del self[hash(item)]

    def discard(self, item: T):
        try:
            self.remove(item)
        except KeyError:
            pass

    def pop(self, key: int):
        item = self.data.pop(key)
        self._detach(item)
        return item

    def clear(self):
        for item in self:
            self._detach(item)

        self.data.clear()

    def __contains__(self, item: T):
        return hash(item) in self.data

    def __delitem__(self, key: int):
        item = self.data[key]
        del self.data[key]
        self._detach(item)

    def __getitem__(self, key: int):
        return self.data[key]

    def __iter__(self):
        return iter(self.data.values())

    def __len__(self):
        return len(self.data)

    def __setitem__(self, key: int, item: T):
        if item not in self:
            self._attach(item)
            self.data[key] = item

    def _attach(self, item: T):
        if getattr(item, self._attr_parent) is not None:
            raise ValueError("item already belongs to a collection")

        setattr(item, self._attr_parent, self._parent)

    def _detach(self, item: T):
        if getattr(item, self._attr_parent) is not self._parent:
            raise ValueError("item does not belong to this collection")

        setattr(item, self._attr_parent, None)
