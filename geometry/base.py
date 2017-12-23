import numpy as np
from geometry.factories import *


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
    internal_array = np.asarray(list(args) + list(kwargs.values()))

    class_attr_dict = {}

    # Zip the keys from kwargs up with their position in internal_array
    property_name_index = tuple(
        zip(kwargs.keys(), [i + len(args) for i in range(0, len(kwargs.keys()))]))

    # Use a predefined function factory to create getters and setters that address internal_array at the proper index
    # when the property is called
    for property_name in property_name_index:
        property_obj = key_lookup_property_factory(property_name[1])
        class_attr_dict.update({property_name[0]: property_obj})

    # Additional function factories to create metaclass-wide functions and properties
    class_attr_dict.update({'__getitem__': getitem_factory()})
    class_attr_dict.update({'__setitem__': setitem_factory()})

    class_attr_dict.update({'dimension': dimension_property_factory()})

    # Create the class, instance it, and set values of properties before returning our newly instanced class object
    point_cls = type(f'{len(internal_array)}D Point', (), class_attr_dict)
    point_instance = point_cls()
    point_instance._values = internal_array

    return point_instance
