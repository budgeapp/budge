from dataclasses import dataclass, field
from uuid import UUID, uuid4

import pytest

from budge.collection import Collection


@dataclass
class Item:
    id: UUID = field(default_factory=uuid4)
    parent: object | None = field(default=None)

    def __hash__(self):
        return hash(self.id)


@pytest.fixture
def parent():
    return object()


@pytest.fixture
def collection(parent):
    return Collection[Item]("parent", parent)


def test_add_item(collection):
    item = Item()
    collection.add(item)
    assert item in collection
    assert item.parent == collection._parent


def test_add_multiple_items(collection):
    items = [Item(), Item()]
    collection.add(*items)
    assert all(item in collection for item in items)
    assert all(item.parent == collection._parent for item in items)


def test_add_item_already_in_other_collection(collection):
    item = Item()
    item.parent = object()
    with pytest.raises(ValueError, match="item already belongs to a collection"):
        collection.add(item)


def test_remove_item(collection):
    item = Item()
    collection.add(item)
    collection.remove(item)
    assert item not in collection
    assert item.parent is None


def test_remove_item_not_in_collection(collection):
    item = Item()
    with pytest.raises(KeyError):
        collection.remove(item)


def test_remove_item_in_other_collection(collection):
    item = Item()
    collection.add(item)
    item.parent = None
    with pytest.raises(ValueError, match="item does not belong to this collection"):
        collection.remove(item)


def test_discard_item(collection):
    item = Item()
    collection.add(item)
    collection.discard(item)
    assert item not in collection
    assert item.parent is None


def test_discard_item_not_in_collection(collection):
    item = Item()
    collection.discard(item)


def test_pop_item(collection):
    item = Item()
    collection.add(item)
    popped = collection.pop(hash(item))
    assert popped == item
    assert item not in collection
    assert item.parent is None


def test_clear_collection(collection):
    items = [Item(), Item()]
    collection.add(*items)
    collection.clear()
    assert len(collection) == 0
    assert all(item.parent is None for item in items)


def test_get_item(collection):
    item = Item()
    collection.add(item)
    assert collection[hash(item)] == item
