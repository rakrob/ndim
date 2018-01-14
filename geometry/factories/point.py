import numpy as np


def init_factory(parent_class=None) -> callable:
    """Function factory to initialize a parent class if there is one, else return a basic __init__."""
    if parent_class is None:
        def init(self):
            pass
    else:
        def init(self):
            parent_class.__init__(self)

    return init


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
    # Defining all metaclass properties in factories seems like a nicer way of doing things, DRY, etc.

    def dimension_get(self):
        return len(self._values)

    dimension = property(dimension_get)

    return dimension


def signature_property_factory(dimension, property_indices) -> property:
    """Will return a hash uniquely identifying the dimension and attributes of the geometry."""

    sig = hash((dimension, property_indices))

    def signature_get(self):
        return sig

    dimension = property(signature_get)

    return dimension


def operator_function_factory(property_indices) -> dict:
    """Defines custom functions for the operators == and !=, as well as __hash__ and __repr__"""
    multifunction_dict = {}
    type_error_description = \
        'This operation is not defined for types %s and %s. This error can ' + \
        'also occur if the dimensions of the objects are the same, but the attribute names are different. ' + \
        'This is intentionally done to prevent operations done on objects of the same dimensionality, but in' + \
        'different vector spaces or coordinate systems.'
    property_list = tuple([prop[0] for prop in property_indices])

    def rep(self):
        rep_str = '('
        for val in self._values:
            rep_str += '%.2f, ' % val.real if val.imag == 0 else '%.2f + %.2fj, ' % (val.real, val.imag)
        return rep_str[:len(rep_str) - 2] + ')'

    multifunction_dict.update({'__repr__': rep})

    def hsh(self):
        # TODO: Define a better way of dealing with floating point imprecision than just rounding off at 8 decimals
        return hash((tuple(np.round(val, 8) for val in self._values), property_indices))

    multifunction_dict.update({'__hash__': hsh})

    # Hijacking __dir__ allows us to get a clean representation of all the dimensions of the object without having to
    # exclude other class attributes in __dict__
    def directory(self):
        return property_list

    multifunction_dict.update({'__dir__': directory})

    def eq(self, other):
        # The philosophy here is that, while comparing the hashes between Points would probably be less of a headache,
        # 1. Best practices dictate an error should be thrown when two attribute sets don't match, and
        # 2. If another completely different object of a different class hashes to the same value, what good is an
        # equality function anyhow?
        #
        # string comparison here is yucky but because each type is created dynamically, they don't match even if the
        # signatures are the same. So it's useful for at least checking that.
        #
        # The other option is to create a large table of classes and store them, so that, if we were to generate a
        # class with the same signature, we'd just use the previously created one. That's equally as messy, I think,
        # because now we have global state, which is less than ideal for a library like this.
        if str(type(other)) != str(type(self)) or self.signature != other.signature:
            raise TypeError(type_error_description % (str(type(self)), str(type(other))))

        for i in range(0, self.dimension):
            # TODO: Define a better way of dealing with floating point imprecision than just rounding off at 8 decimals
            if np.abs(self[i] - other[i]) >= 1e-8:
                return False

        return True

    multifunction_dict.update({'__eq__': eq})

    def ne(self, other):
        # Just return the opposite of __eq__ and we get all our type checking for free.
        return not self.__eq__(other)

    multifunction_dict.update({'__ne__': ne})

    return multifunction_dict
