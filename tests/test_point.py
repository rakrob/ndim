from geometry.base import Point


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


def test_signature():
    x = Point(1, 2, 3)
    y = Point(x=1, y=2, z=3)

    assert x.signature != y.signature

    z = Point(4, 5, 6)
    w = Point(x=4, y=5, z=6)

    assert x.signature == z.signature
    assert y.signature == w.signature


def test_repr():
    x = Point(1, 2, 3)

    assert str(x) == "(1.00, 2.00, 3.00)"

    y = Point(0, 4 + 3j, 7)

    assert str(y) == "(0.00, 4.00 + 3.00j, 7.00)"


def test_hash():
    x = Point(1, 2, 3)
    y = Point(1, 2, 3)
    w = Point(3, 4, 5, 6)
    z = Point(x=1, y=2, z=3)

    assert x.__hash__() == y.__hash__()
    assert x.__hash__() != z.__hash__()
    assert x.__hash__() != w.__hash__()


def test_equality():
    x = Point(1, 2, 3)
    y = Point(1, 2, 3)

    q = Point(4, 5, 6)

    z = Point(x=1, y=2, z=3)
    w = Point(x=1, y=2, z=3)

    assert x == y
    assert z == w

    assert x != q

    caught_exception = None

    try:
        assert x == z
    except TypeError as e:
        caught_exception = e
    finally:
        assert caught_exception is not None
