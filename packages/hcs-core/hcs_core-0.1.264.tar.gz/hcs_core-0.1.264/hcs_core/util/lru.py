from collections import OrderedDict
from collections.abc import MutableSet


class LRUSet(MutableSet):
    def __init__(self, capacity):
        self.capacity = capacity
        self.data = OrderedDict()

    def add(self, item):
        """Add an item to the set."""
        if item in self.data:
            self.data.move_to_end(item)  # Mark as recently used
        else:
            self.data[item] = None  # Add new item
            if len(self.data) > self.capacity:
                self.data.popitem(last=False)  # Remove the least recently used item

    def discard(self, item):
        """Remove an item if it exists, do nothing otherwise."""
        self.data.pop(item, None)

    def __contains__(self, item):
        """Check if an item is in the set, and mark it as recently used."""
        if item in self.data:
            self.data.move_to_end(item)  # Mark as recently used
            return True
        return False

    def __len__(self):
        """Return the number of items in the set."""
        return len(self.data)

    def __iter__(self):
        """Iterate over the items in the set."""
        return iter(self.data)

    def __repr__(self):
        """Return a string representation of the set."""
        return f"{type(self).__name__}({list(self.data.keys())}, capacity={self.capacity})"


class LRUDict(OrderedDict):
    def __init__(self, capacity):
        super().__init__()
        self.capacity = capacity

    def __setitem__(self, key, value):
        if key in self:
            self.move_to_end(key)
        super().__setitem__(key, value)
        if len(self) > self.capacity:
            self.popitem(last=False)

    def __getitem__(self, key):
        if key in self:
            self.move_to_end(key)
        return super().__getitem__(key)
