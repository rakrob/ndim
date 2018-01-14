from geometry.base import *


def test_vector_initialization():
    x = Point(1, 2, 3)
    x_v = Vector(x)

    assert (str(type(x_v))) == "<class 'geometry.base.3D Vector'>"

    y = Vector(4, 1, 2, 3)

    assert (str(type(y))) == "<class 'geometry.base.4D Vector'>"


def test_vector_indexing_get():
    x = Vector(1, 2, 3)

    assert x[0] == 1
    assert x[1] == 2
    assert x[2] == 3


def test_vector_indexing_set():
    x = Vector(1, 2, 3)

    x[0] = 4
    x[1] = 5
    x[2] = 6

    assert x[0] == 4
    assert x[1] == 5
    assert x[2] == 6


def test_vector_key_lookup_get():
    x = Vector(x=1, y=2, z=3)

    assert x.x == 1
    assert x.y == 2
    assert x.z == 3


def test_vector_key_lookup_set():
    x = Vector(x=1, y=2, z=3)

    x.x = 4
    x.y = 5
    x.z = 6

    assert x.x == 4
    assert x.y == 5
    assert x.z == 6


def test_vector_mixed_addressing():
    x = Vector(1, y=2, z=3)

    assert x[2] == x.z == 3

    x[1] = 4

    assert x.y == 4
    assert x[0] == 1


def test_dimension():
    x = Vector(1, 2, 3)

    assert x.dimension == 3

    y = Vector(1, 2, z=3, x=4, n=5)

    assert y.dimension == 5


def test_signature():
    x = Vector(1, 2, 3)
    y = Vector(x=1, y=2, z=3)

    assert x.signature != y.signature

    z = Vector(4, 5, 6)
    w = Vector(x=4, y=5, z=6)

    assert x.signature == z.signature
    assert y.signature == w.signature


def test_repr():
    x = Vector(1, 2, 3)

    assert str(x) == "<1.00, 2.00, 3.00>"

    y = Vector(0, 4 + 3j, 7)

    assert str(y) == "<0.00, 4.00 + 3.00j, 7.00>"


def test_hash():
    x = Vector(1, 2, 3)
    y = Vector(1, 2, 3)
    w = Vector(3, 4, 5, 6)
    z = Vector(x=1, y=2, z=3)

    assert x.__hash__() == y.__hash__()
    assert x.__hash__() != z.__hash__()
    assert x.__hash__() != w.__hash__()


def test_equality():
    x = Vector(1, 2, 3)
    y = Vector(1, 2, 3)

    q = Vector(4, 5, 6)

    z = Vector(x=1, y=2, z=3)
    w = Vector(x=1, y=2, z=3)

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


def test_add():
    x = Vector(1, 2, 3)
    y = Vector(2, 4, 6)

    z = Vector(3, 4, 5)

    assert x + x == y
    assert x + 2 == 2 + x == z

    w = Vector(x=1, y=2, z=3)

    caught_exception = None

    try:
        assert x + w == y
    except TypeError as e:
        caught_exception = e
    finally:
        assert caught_exception is not None


def test_negative():
    x = Vector(1, 2, 3)
    y = Vector(-1, -2, -3)

    assert -x == y


def test_subtract():
    x = Vector(1, 2, 3)
    y = Vector(2, 4, 6)

    z = Vector(3, 4, 5)

    w = Vector(2, 1, 0)

    assert y - x == x
    assert z - 2 == x

    assert 5 - z == w


def test_multiplication():
    x = Vector(1, 2, 3)
    y = Vector(2, 4, 6)

    assert x * 2 == 2 * x == y

    caught_exception = None

    try:
        x * y
    except TypeError as e:
        caught_exception = e
    finally:
        assert caught_exception is not None


def test_division():
    x = Vector(1, 2, 3)
    y = Vector(2, 4, 6)

    assert y / 2 == x

    z = Vector(6, 3, 2)

    assert 12 / y == z

    caught_exception = None

    try:
        y / x
    except TypeError as e:
        caught_exception = e
    finally:
        assert caught_exception is not None


def test_invert():
    x = Vector(2, 3, 4)
    y = Vector(.5, 1.0 / 3.0, .25)

    assert ~x == y
