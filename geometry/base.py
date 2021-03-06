import numpy as np
from geometry.factories import point, vector


class Geometry:
    """
    Base class for all ndim objects. Defines some properties that should be implemented in all higher-level classes.

    Some compromises were made here in order to enforce non-optional properties that really should be implemented for
    any custom geometries that might be included in ndim later. Any base classes (i.e., classes that are not
    collections) should inherit from Geometry and define a dimension and a signature, in order to make absolutely sure
    that coordinate systems do not get mismatched at runtime.

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
    internal_array = np.asarray([complex(x) for x in args] + [complex(x) for x in kwargs.values()])

    class_attr_dict = {}

    # Zip the keys from kwargs up with their position in internal_array
    property_name_index = tuple(
        zip(kwargs.keys(), [i + len(args) for i in range(0, len(kwargs.keys()))]))

    # Superclass initialization inside of init function
    class_attr_dict.update({'__init__': point.init_factory(Geometry)})

    # Additional function factories to create metaclass-wide functions and properties
    class_attr_dict.update({'__getitem__': point.getitem_factory()})
    class_attr_dict.update({'__setitem__': point.setitem_factory()})

    # Use a predefined function factory to create getters and setters that address internal_array at the proper index
    # when the property is called
    for property_name in property_name_index:
        property_obj = point.key_lookup_property_factory(property_name[1])
        class_attr_dict.update({property_name[0]: property_obj})

    # Make sure to override the property getters in Geometry, otherwise we'll throw errors when reading them
    class_attr_dict.update({'dimension': point.dimension_property_factory()})
    class_attr_dict.update({'signature': point.signature_property_factory(len(internal_array), property_name_index)})

    # Assign functions for some standard operators, equality, etc.
    class_attr_dict.update(point.operator_function_factory(property_name_index))

    # Create the class, instance it, and set values of properties before returning our newly instanced class object
    # Make sure to inherit from the Geometry class
    point_cls = type(f'{len(internal_array)}D Point', (Geometry,), class_attr_dict)
    point_instance = point_cls()
    point_instance._values = internal_array

    return point_instance


def Vector(*args, **kwargs):
    """
    Returns an instance of a vector with dimension equal to the number of arguments.

    Vector is a function that acts as a "Mock Class" that, through the use of metaprogramming, creates a class with an
    addressable underlying Point class, but with additional operators that are only valid for vectors. Vectors can be
    created with a list of numeric arguments, a list of keyword arguments, a combination of both, or a Point. However,
    keyword arguments must always come after non-keyword arguments, as with Points.

    Once the class is created, it is instanced and its values are set. The function then returns that instance as if it
    were just initialized.
    """
    class_attr_dict = {}
    repr_point = None

    # If vector is initialized with a point, use it and its underlying properties, otherwise, create a new point
    if len(args) > 0:
        arg = args[0]
        type_repr = str(type(arg))
        if len(type_repr) > 7 \
                and type_repr[len(type_repr) - 7:len(type_repr) - 2] == 'Point' \
                and Geometry in arg.__class__.__bases__:
            repr_point = arg

    if repr_point is None:
        repr_point = Point(*args, **kwargs)

    # Superclass initialization inside of init function
    class_attr_dict.update({'__init__': vector.init_factory(Geometry)})

    class_attr_dict.update({'__getitem__': vector.getitem_factory()})
    class_attr_dict.update({'__setitem__': vector.setitem_factory()})

    # Use a predefined function factory to create getters and setters that address _point at the proper index
    # when the property is called
    for property_name in dir(repr_point):
        property_obj = vector.key_lookup_property_factory(property_name)
        class_attr_dict.update({property_name: property_obj})

    class_attr_dict.update({'dimension': vector.dimension_property_factory()})
    class_attr_dict.update({'signature': vector.signature_property_factory(repr_point)})

    # Assign functions for the standard math operators
    class_attr_dict.update(vector.operator_function_factory())

    # Vector norm and unit vector should be a callable from inside the class
    class_attr_dict.update({'norm': vector.norm_function_factory()})
    class_attr_dict.update({'unit': vector.unit_function_factory()})

    vector_cls = type(f'{repr_point.dimension}D Vector', (Geometry,), class_attr_dict)
    vector_instance = vector_cls()
    vector_instance._point = repr_point

    return vector_instance
