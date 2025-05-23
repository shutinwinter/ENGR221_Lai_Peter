import pytest # type: ignore

from ..myarray import MyArray

@pytest.mark.arraytest1
def test_init_array_len(len=0):
    a = MyArray(len)
    assert (a.length() == 0 and a.values() == [])

@pytest.mark.arraytest1
def test_init_array_length_vals(vals=['E', 'N', 'G', 'R', 2, 2, 1]):
    a = MyArray(vals)
    assert (a.length() == len(vals) and a.values() == vals)

@pytest.mark.arraytest2
def test_insert_array():
    a = MyArray(['E', 'N', 'G', 'R', 2, 2, 1])
    a.insert('!')
    assert (a.get(7) == '!' and a.length() == 8)

@pytest.mark.arraytest2
def test_insert_empty_array():
    a = MyArray(0)
    a.insert('Hello')
    assert (a.get(0) == 'Hello' and a.length() == 1)

@pytest.mark.arraytest3
def test_delete_array():
    a = MyArray(['E', 'N', 'G', 'R', 2, 2, 1])
    a.delete(2)
    assert (a.values() == ['E', 'N', 'G', 'R', 1] and a.length() == 5)

@pytest.mark.arraytest3
def test_delete_array_absent():
    a = MyArray(['E', 'N', 'G', 'R', 2, 2, 1])
    a.delete(0)
    assert (a.values() == ['E', 'N', 'G', 'R', 2, 2, 1] and a.length() == 7)