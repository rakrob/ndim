import numpy as np
from copy import deepcopy
from geometry.functions import vector


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
    """Function factory for accessing an internal Point object _point"""

    def getitem(self, key):
        return self._point[key]

    return getitem


def setitem_factory() -> callable:
    """Function factory for setting values in an internal Point object _point"""

    def setitem(self, key, value):
        self._point[key] = value

    return setitem


def key_lookup_property_factory(attr) -> property:
    """Create properties to get/set attributes of an internal Point object _point that has attribute 'attr'"""

    def property_get(self):
        return getattr(self._point, attr)

    def property_set(self, value):
        setattr(self._point, attr, value)

    prop = property(property_get, property_set)

    return prop


def dimension_property_factory() -> property:
    def dimension_get(self):
        return self._point.dimension

    dimension = property(dimension_get)

    return dimension


def signature_property_factory(point) -> property:
    """Will return a hash uniquely identifying the dimension and attributes of the geometry."""

    sig = hash((tuple(dir(point)), point.signature))

    def signature_get(self):
        return sig

    dimension = property(signature_get)

    return dimension


def operator_function_factory() -> dict:
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
    scalar_operation_error_description = \
        'This operation is not defined for two objects of type %s. One of the operators must be a scalar number. ' + \
        'If multiplication between two %ss is desired, use either the inner() or outer() functions for the inner ' + \
        'outer products, respectively.'

    def rep(self):
        rep_str = '<'
        for i in range(0, self.dimension):
            val = self._point[i]
            rep_str += '%.2f, ' % val.real if val.imag == 0 else '%.2f + %.2fj, ' % (val.real, val.imag)
        return rep_str[:len(rep_str) - 2] + '>'

    multifunction_dict.update({'__repr__': rep})

    def hsh(self):
        # It's important to hash again here, as Vectors should not have equal hash representations as their
        # underlying Point objects.
        return hash(self._point.__hash__())

    multifunction_dict.update({'__hash__': hsh})

    def directory(self):
        return dir(self._point)

    multifunction_dict.update({'__dir__': directory})

    def eq(self, other):
        # Vectors are equal if their underlying points are equal.
        try:
            # Accessing a protected member is less than kosher but otherwise we'd have to dump all the type checking
            # for Points in here so this is a little more DRY.
            return self._point == other._point
        except TypeError:
            # Catching and re-throwing the exception gives us a way to overwrite the class names, so users aren't
            # confused if they get a type mismatch for a point but they were comparing vectors
            raise TypeError(type_error_description % (str(type(self)), str(type(other))))

    multifunction_dict.update({'__eq__': eq})

    def ne(self, other):
        return not self.__eq__(other)

    multifunction_dict.update({'__ne__': ne})

    def add(self, other):
        # By using a deepcopy we don't have to worry about creating a whole new class just to make another vector
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

        # Multiplication (and division) should only be defined for Vectors and scalar types. Vector multiplication is
        # defined instead by the inner and outer product.
        if not np.isscalar(other):
            raise TypeError(scalar_operation_error_description % (str(type(self)), str(type(self))))

        for i in range(0, final_answer.dimension):
            final_answer[i] *= complex(other)

        return final_answer

    multifunction_dict.update({'__mul__': mul})

    def rmul(self, other):
        return self.__mul__(other)

    multifunction_dict.update({'__rmul__': rmul})

    def truediv(self, other):
        final_answer = deepcopy(self)

        if not np.isscalar(other):
            raise TypeError(scalar_operation_error_description % (str(type(self)), str(type(self))))

        return final_answer * (1.0 / complex(other))

    multifunction_dict.update({'__truediv__': truediv})

    def rtruediv(self, other):
        final_answer = deepcopy(self)

        if not np.isscalar(other):
            raise TypeError(scalar_operation_error_description % (str(type(self)), str(type(self))))

        for i in range(0, final_answer.dimension):
            final_answer[i] = complex(other) / final_answer[i]

        return final_answer

    multifunction_dict.update({'__rtruediv__': rtruediv})

    def neg(self):
        final_answer = deepcopy(self)

        return -1.0 * final_answer

    multifunction_dict.update({'__neg__': neg})

    def inv(self):
        final_answer = deepcopy(self)

        return 1.0 / final_answer

    multifunction_dict.update({'__invert__': inv})

    return multifunction_dict


def norm_function_factory() -> callable:
    """Function factory to return a vector norm in complex space."""

    def norm(self) -> complex:
        inner_product = vector.inner(self, self)

        return inner_product ** 0.5

    return norm


def unit_function_factory() -> callable:
    """Function factory to return a unit vector - that is, a vector with magnitude 1 and the same direction as self."""

    def unit(self):
        return self / self.norm()

    return unit
