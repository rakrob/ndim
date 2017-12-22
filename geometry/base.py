import numpy as np
from geometry.factories import *


def Point(*args, **kwargs):
    internal_array = np.asarray(list(args) + list(kwargs.values()))

    class_attr_dict = {}

    property_name_index = tuple(
        zip(kwargs.keys(), [i + len(args) for i in range(0, len(kwargs.keys()))]))

    for property_name in property_name_index:
        property_obj = key_lookup_property_factory(property_name[1])
        class_attr_dict.update({property_name[0]: property_obj})

    class_attr_dict.update({'__getitem__': getitem_factory()})
    class_attr_dict.update({'__setitem__': setitem_factory()})

    class_attr_dict.update({'dimension': dimension_property_factory()})

    point_cls = type(f'{len(internal_array)}D Point', (), class_attr_dict)

    point_instance = point_cls()
    point_instance._values = internal_array

    return point_instance
