from geometry.base import *


def test_point_initialization():
    x = Point(1, 2, 3)

    assert (str(type(x))) == "<class 'geometry.base.3D Point'>"

    y = Point(4, 1, 2, 3)

    assert (str(type(y))) == "<class 'geometry.base.4D Point'>"


def test_point_indexing_get():
    x = Point(1, 2, 3)

    assert x[0] == 1
    assert x[1] == 2
    assert x[2] == 3


def test_point_indexing_set():
    x = Point(1, 2, 3)

    x[0] = 4
    x[1] = 5
    x[2] = 6

    assert x[0] == 4
    assert x[1] == 5
    assert x[2] == 6


def test_point_key_lookup_get():
    x = Point(x=1, y=2, z=3)

    assert x.x == 1
    assert x.y == 2
    assert x.z == 3


def test_point_key_lookup_set():
    x = Point(x=1, y=2, z=3)

    x.x = 4
    x.y = 5
    x.z = 6

    assert x.x == 4
    assert x.y == 5
    assert x.z == 6


def test_point_mixed_addressing():
    x = Point(1, y=2, z=3)

    assert x[2] == x.z == 3

    x[1] = 4

    assert x.y == 4
    assert x[0] == 1


def test_dimension():
    x = Point(1, 2, 3)

    assert x.dimension == 3

    y = Point(1, 2, z=3, x=4, n=5)

    assert y.dimension == 5
