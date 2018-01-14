import numpy as np
from geometry.factories import point


class Geometry:
    """
    Base class for all ndim objects. Defines some properties that should be implemented in all higher-level classes.

    Some compromises were made here in order to enforce non-optional properties that really should be implemented for
    any custom geometries that might be included in ndim later. Any base classes (i.e., classes that are not
    collections) should inherit from Geometry and define a dimension and a signature, in order to make absolutely sure
    that coordinates systems do not get mismatched at runtime.

    Enforcing the mandatory override of properties isn't exactly pythonic, but effort should be made going forward
    to keep the number of mandatory properties to a minimum.
    """

    def __init__(self):
        # Placeholder for now, but I'm certain some initialization behaviors will need to be defined eventually.
        pass

    @property
    def dimension(self):
        raise NotImplementedError(
            'This property should be implemented on a per-class basis, defined by the number of linearly independent '
            'dimensions that define the object.')

    @dimension.setter
    def dimension(self, dimension):
        # Dimension needs to be readonly. There's absolutely no way to add a dimension to a point in a way that's
        # foolproof. Instead, if a dimension needs to be added to a Geometric object, a new class/object should be
        # created.
        raise AttributeError('The dimension of an object is read-only.')

    @property
    def signature(self):
        raise NotImplementedError(
            'This property should be implemented on a per-class basis, defined by a hash function consisting of some '
            'tuple of the dimension of the object and the indices of the other attributes in internal arrays. No '
            'standard form is enforced, but it is recommended that the signatures of the underlying geometry match in '
            'addition to the top-level objects.')

    @signature.setter
    def signature(self, signature):
        # If dimension can't change, then signature can't change. This is textbook readonly territory.
        raise AttributeError('The signature of an object is a hash of its dimension and properties, and is read-only.')


def Point(*args, **kwargs):
    """
    Returns an instance of a point with dimension equal to the number of arguments.

    Point is a function that acts as a "Mock Class" that, through the use of metaprogramming, creates a class with an
    addressable underlying numpy array and properties from keys in kwargs. Points can be created with a list of numeric
    arguments, a list of keyword arguments, or a combination of both. However, keyword arguments must always come after
    non-keyword arguments.

    Once the class is created, it is instanced and its values are set. The function then returns that instance as if it
    were just initialized.
    """
    # TODO: Support complex numbers
    internal_array = np.asarray([complex(x) for x in args] + [complex(x) for x in kwargs.values()])

    class_attr_dict = {}

    # Zip the keys from kwargs up with their position in internal_array
    property_name_index = tuple(
        zip(kwargs.keys(), [i + len(args) for i in range(0, len(kwargs.keys()))]))

    # Use a predefined function factory to create getters and setters that address internal_array at the proper index
    # when the property is called
    for property_name in property_name_index:
        property_obj = point.key_lookup_property_factory(property_name[1])
        class_attr_dict.update({property_name[0]: property_obj})

    # Additional function factories to create metaclass-wide functions and properties
    class_attr_dict.update({'__getitem__': point.getitem_factory()})
    class_attr_dict.update({'__setitem__': point.setitem_factory()})

    # Assign functions for the standard math operators
    class_attr_dict.update(point.operator_function_factory(property_name_index))

    # Make sure to override the property getters in Geometry, otherwise we'll throw errors when reading them
    class_attr_dict.update({'dimension': point.dimension_property_factory()})
    class_attr_dict.update({'signature': point.signature_property_factory(len(internal_array), property_name_index)})

    # Create the class, instance it, and set values of properties before returning our newly instanced class object
    # Make sure to inherit from the Geometry class
    point_cls = type(f'{len(internal_array)}D Point', (Geometry,), class_attr_dict)
    point_instance = point_cls()
    point_instance._values = internal_array

    return point_instance
