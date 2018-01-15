from copy import deepcopy
import numpy as np

_type_error_description = \
    'This operation is not defined for types %s and %s. This error can ' + \
    'also occur if the dimensions of the objects are the same, but the attribute names are different. ' + \
    'This is intentionally done to prevent operations done on objects of the same dimensionality, but in' + \
    'different vector spaces or coordinate systems.'

_dimensionality_error_description = \
    'This operation is not defined for vectors with dimensionality %i.'


def _type_check(vector_1, vector_2):
    # Defer the type import so we don't get a circular reference. Anyhow, this is the only location we will need to
    # import Geometry to anyhow.
    from geometry.base import Geometry

    type_repr_1 = str(type(vector_1))
    type_repr_2 = str(type(vector_2))

    if type_repr_1 != type_repr_2 \
            or Geometry not in vector_1.__class__.__bases__ \
            or Geometry not in vector_2.__class__.__bases__ \
            or vector_1.signature != vector_2.signature \
            or type_repr_1[len(type_repr_1) - 8:len(type_repr_1) - 2] != 'Vector':
        raise TypeError(_type_error_description % (str(type(vector_1)), str(type(vector_2))))


def inner(vector_1, vector_2) -> complex:
    _type_check(vector_1, vector_2)

    inner_product: complex = 0.0 + 0.0j

    for i in range(0, vector_1.dimension):
        inner_product += vector_1[i] * vector_2[i]

    return inner_product


def cross(vector_1, vector_2):
    _type_check(vector_1, vector_2)

    if vector_1.dimension not in (3, 7):
        raise TypeError(_dimensionality_error_description % vector_1.dimension +
                        ' Non-trivial bilinear products of two vectors that are vector-valued, anticommutative and ' +
                        'orthogonal exist only in 3 and 7 dimensions.')

    # There are supposedly 480 tables that satisfy this requirement for 7 dimensions. We're going to be using only one
    # for the sake of brevity. Basically it's some black magic to do this in 7 dimensions, and we can rip off the first
    # three columns and rows to do it in 3.
    # TODO: Make this less wonky. Maybe default to this table but let the user define their own if they wish?
    dimensionality_lookup = list()
    dimensionality_lookup.append([[0, 0], [1, 2], [-1, 1], [1, 4], [-1, 3], [-1, 6], [1, 5]])
    dimensionality_lookup.append([[-1, 2], [0, 1], [1, 0], [1, 5], [1, 6], [-1, 3], [-1, 4]])
    dimensionality_lookup.append([[1, 1], [-1, 0], [0, 2], [1, 6], [-1, 5], [1, 4], [-1, 3]])
    dimensionality_lookup.append([[-1, 4], [-1, 5], [-1, 6], [0, 3], [1, 0], [1, 1], [1, 2]])
    dimensionality_lookup.append([[1, 3], [-1, 6], [1, 5], [-1, 0], [0, 4], [-1, 2], [1, 1]])
    dimensionality_lookup.append([[1, 6], [1, 3], [-1, 4], [-1, 1], [1, 2], [0, 5], [-1, 0]])
    dimensionality_lookup.append([[-1, 5], [1, 4], [1, 3], [-1, 2], [-1, 1], [1, 0], [0, 6]])

    cross_product = deepcopy(vector_1)

    for i in range(0, cross_product.dimension):
        cross_product[i] = 0.0

    # Use the lookup to figure out what dimension we're supposed to be assigning to what
    for x in range(0, cross_product.dimension):
        for y in range(0, cross_product.dimension):
            cross_product[dimensionality_lookup[x][y][1]] += vector_1[x] * vector_2[y] * dimensionality_lookup[x][y][0]

    return cross_product


def angle(vector_1, vector_2):
    _type_check(vector_1, vector_2)

    if np.isclose(vector_1.norm(), 0.0) or np.isclose(vector_2.norm(), 0.0):
        raise ZeroDivisionError(
            'An angle between any Vector pair where one of the two has magnitude = 0 does not exist.')

    return np.arccos(inner(vector_1, vector_2) / (vector_1.norm() * vector_2.norm()))
