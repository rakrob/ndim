import numpy as np
from copy import deepcopy


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
    """Defines custom functions for the operators +, -, *, /, ==, and **, as well as __hash__ and __repr__"""
    multifunction_dict = {}
    type_error_description = \
        'This operation is not defined for types %s and %s. This error can ' + \
        'also occur if the dimensions of the objects are the same, but the attribute names are different. ' + \
        'This is intentionally done to prevent operations done on objects of the same dimensionality, but in' + \
        'different vector spaces or coordinate systems.'
    signature_error_description = \
        'Signature mismatch. The dimensions of the objects are the same, but the attribute names are ' + \
        'different. This error is intentionally thrown to prevent operations done on objects of the same ' + \
        'dimensionality, but in different vector spaces or coordinate systems.'

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

    def eq(self, other):
        # The philosophy here is that, while comparing the hashes between Points would probably be less of a headache,
        # 1. Best practices dictate an error should be thrown when two attribute sets don't match, and
        # 2. If another completely different object of a different class hashes to the same value, what good is an
        # equality function anyhow?

        # string comparison here is yucky but because each type is created dynamically, they don't match even if the
        # signatures are the same. So it's useful for at least checking that.
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

    def add(self, other):
        # By using a deepcopy we don't have to worry about creating a whole new class just to make another point
        final_answer = deepcopy(self)

        if str(type(other)) == str(type(self)):
            if self.signature != other.signature:
                raise TypeError(signature_error_description)

            for i in range(0, final_answer.dimension):
                final_answer[i] += other[i]

        else:
            for i in range(0, final_answer.dimension):
                final_answer[i] += complex(other)

        return final_answer

    multifunction_dict.update({'__add__': add})

    def radd(self, other):
        return self.__add__(other)

    multifunction_dict.update({'__radd__': radd})

    def sub(self, other):
        return self.__add__(- other)

    multifunction_dict.update({'__sub__': sub})

    def rsub(self, other):
        return self.__neg__().__add__(other)

    multifunction_dict.update({'__rsub__': rsub})

    def mul(self, other):
        final_answer = deepcopy(self)

        if str(type(other)) == str(type(self)):
            if self.signature != other.signature:
                raise TypeError(signature_error_description)

            for i in range(0, final_answer.dimension):
                final_answer[i] *= other[i]

        else:
            for i in range(0, final_answer.dimension):
                final_answer[i] *= complex(other)

        return final_answer

    multifunction_dict.update({'__mul__': mul})

    def rmul(self, other):
        return self.__mul__(other)

    multifunction_dict.update({'__rmul__': rmul})

    def truediv(self, other):
        final_answer = deepcopy(self)

        if str(type(other)) == str(type(self)):
            if self.signature != other.signature:
                raise TypeError(signature_error_description)

            for i in range(0, final_answer.dimension):
                final_answer[i] /= other[i]

        else:
            for i in range(0, final_answer.dimension):
                final_answer[i] /= complex(other)

        return final_answer

    multifunction_dict.update({'__truediv__': truediv})

    def rtruediv(self, other):
        final_answer = deepcopy(self)

        if str(type(other)) == str(type(self)):
            if self.signature != other.signature:
                raise TypeError(signature_error_description)

            for i in range(0, final_answer.dimension):
                final_answer[i] = other[i] / final_answer[i]

        else:
            for i in range(0, final_answer.dimension):
                final_answer[i] = complex(other) / final_answer[i]

        return final_answer

    multifunction_dict.update({'__rtruediv__': rtruediv})

    def neg(self):
        final_answer = deepcopy(self)

        for i in range(0, final_answer.dimension):
            final_answer[i] = -1.0 * final_answer[i]

        return final_answer

    multifunction_dict.update({'__neg__': neg})

    def pw(self, power, modulo=None):
        final_answer = deepcopy(self)

        for i in range(0, final_answer.dimension):
            if modulo is None:
                final_answer[i] = pow(final_answer[i], power)
            else:
                final_answer[i] = pow(final_answer[i], power, modulo)

        return final_answer

    multifunction_dict.update({'__pow__': pw})

    def rpow(self, other, modulo=None):
        final_answer = deepcopy(self)

        for i in range(0, final_answer.dimension):
            if modulo is None:
                final_answer[i] = pow(other, final_answer[i])
            else:
                final_answer[i] = pow(other, final_answer[i], modulo)

        return final_answer

    multifunction_dict.update({'__rpow__': rpow})

    def inv(self):
        final_answer = deepcopy(self)

        for i in range(0, final_answer.dimension):
            final_answer[i] = 1.0 / final_answer[i]

        return final_answer

    multifunction_dict.update({'__invert__': inv})

    return multifunction_dict
