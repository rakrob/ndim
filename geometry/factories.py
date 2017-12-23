# Get and set item factories are defined in order to access an internal class array called _values
def getitem_factory() -> callable:
    def getitem(self, key):
        return self._values[key]

    return getitem


def setitem_factory() -> callable:
    def setitem(self, key, value):
        self._values[key] = value

    return setitem


# Create properties to arbitrarily access a class array called _values via an index
def key_lookup_property_factory(property_index) -> property:
    def property_get(self):
        return self._values[property_index]

    def property_set(self, value):
        self._values[property_index] = value

    prop = property(property_get, property_set)

    return prop


# Defining all metaclass properties in factories seems like a nicer way of doing things, DRY, etc.
def dimension_property_factory() -> property:
    def dimension_get(self):
        return len(self._values)

    dimension = property(dimension_get)

    return dimension
