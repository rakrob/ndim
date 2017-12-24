def getitem_factory() -> callable:
    """Function factory for accessing an internal class array called _values"""

    def getitem(self, key):
        return self._values[key]

    return getitem


def setitem_factory() -> callable:
    """Function factory for setting values in an internal class array called _values"""

    def setitem(self, key, value):
        self._values[key] = value

    return setitem


def key_lookup_property_factory(property_index) -> property:
    """Create properties to arbitrarily access a class array called _values via an index"""

    def property_get(self):
        return self._values[property_index]

    def property_set(self, value):
        self._values[property_index] = value

    prop = property(property_get, property_set)

    return prop


def dimension_property_factory() -> property:
    """Defining all metaclass properties in factories seems like a nicer way of doing things, DRY, etc."""

    def dimension_get(self):
        return len(self._values)

    dimension = property(dimension_get)

    return dimension


def signature_property_factory(dimension, property_indices) -> property:
    """Will return a hash uniquely identifying the geometry."""

    sig = hash((dimension, property_indices))

    def signature_get(self):
        return sig

    dimension = property(signature_get)

    return dimension
