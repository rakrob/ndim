def getitem_factory() -> callable:
    def getitem(self, key):
        return self._values[key]

    return getitem


def setitem_factory() -> callable:
    def setitem(self, key, value):
        self._values[key] = value

    return setitem


def key_lookup_property_factory(property_index) -> property:
    def property_get(self):
        return self._values[property_index]

    def property_set(self, value):
        self._values[property_index] = value

    prop = property(property_get, property_set)

    return prop


def dimension_property_factory() -> property:
    def dimension_get(self):
        return len(self._values)

    dimension = property(dimension_get)

    return dimension
