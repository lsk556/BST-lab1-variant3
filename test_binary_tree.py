from typing import Optional
import pytest
from hypothesis import given
import hypothesis.strategies as st
from binary_tree import BinaryTree


def test_size() -> None:
    tree: BinaryTree[int] = BinaryTree()
    assert tree.size() == 0
    tree.add(5)
    assert tree.size() == 1
    tree.add(3)
    tree.add(7)
    assert tree.size() == 3


def test_member() -> None:
    tree: BinaryTree[int] = BinaryTree()
    assert tree.member(5) is False
    tree.add(5)
    assert tree.member(5) is True
    tree.add(3)
    tree.add(7)
    assert tree.member(3) is True
    assert tree.member(7) is True
    assert tree.member(9) is False


def test_add_duplicate() -> None:
    tree: BinaryTree[int] = BinaryTree()
    tree.add(5)
    tree.add(5)
    assert tree.size() == 1
    assert tree.to_list() == [5]


def test_to_list() -> None:
    tree: BinaryTree[int] = BinaryTree()
    assert tree.to_list() == []
    tree.add(5)
    assert tree.to_list() == [5]
    tree.add(3)
    tree.add(7)
    assert tree.to_list() == [3, 5, 7]


def test_from_list() -> None:
    test_data: list[list[int]] = [[], [5], [3, 5, 7], [7, 3, 5, 3]]
    for e in test_data:
        tree: BinaryTree[int] = BinaryTree()
        tree.from_list(e)
        expected = sorted(set(e))
        assert tree.to_list() == expected


def test_remove() -> None:
    tree: BinaryTree[int] = BinaryTree()
    tree.remove(5)
    assert tree.size() == 0

    tree.from_list([5, 3, 7, 2, 4, 6, 8])
    tree.remove(2)
    assert tree.member(2) is False
    assert tree.size() == 6

    tree.remove(3)
    assert tree.member(3) is False
    assert tree.member(4) is True

    tree.remove(5)
    assert tree.member(5) is False
    assert tree.size() == 4

    tree.remove(100)
    assert tree.size() == 4


def test_filter() -> None:
    tree: BinaryTree[int] = BinaryTree()
    tree.filter(lambda x: x > 0)
    assert tree.to_list() == []

    tree.from_list([1, 2, 3, 4, 5])
    tree.filter(lambda x: x % 2 == 0)
    assert tree.to_list() == [2, 4]

    tree.filter(lambda x: x > 10)
    assert tree.to_list() == []


def test_map() -> None:
    tree: BinaryTree[int] = BinaryTree()
    tree.map(lambda x: x + 1)
    assert tree.to_list() == []

    tree.from_list([1, 2, 3])
    tree.map(lambda x: x * 2)
    assert tree.to_list() == [2, 4, 6]

    tree.from_list([-2, -1, 1, 2])
    tree.map(abs)
    assert tree.to_list() == [1, 2]


def test_map_with_none() -> None:
    tree: BinaryTree[Optional[int]] = BinaryTree()
    tree.from_list([1, 2, 3])
    tree.map(lambda x: None if x == 2 else x)
    assert tree.to_list() == [None, 1, 3]


def test_reduce() -> None:
    tree: BinaryTree[int] = BinaryTree()
    assert tree.reduce(lambda acc, x: acc + x, 0) == 0
    assert tree.reduce(lambda acc, x: acc * x, 1) == 1

    tree.from_list([1, 2, 3, 4])
    assert tree.reduce(lambda acc, x: acc + x, 0) == 10
    assert tree.reduce(lambda acc, x: acc * x, 1) == 24
    assert tree.reduce(lambda a, x: a if a > x else x, -float("inf")) == 4
    assert tree.reduce(lambda acc, _: acc + 1, 0) == tree.size()


def test_empty() -> None:
    tree1: BinaryTree[int] = BinaryTree.empty()
    assert tree1.size() == 0
    tree2: BinaryTree[int] = BinaryTree()
    assert tree2.size() == 0
    assert tree1.to_list() == tree2.to_list()


def test_concat() -> None:
    tree1: BinaryTree[int] = BinaryTree()
    tree2: BinaryTree[int] = BinaryTree()
    tree1.concat(tree2)
    assert tree1.size() == 0

    tree1.from_list([1, 2, 3])
    tree2.from_list([3, 4, 5])
    tree1.concat(tree2)
    assert tree1.to_list() == [1, 2, 3, 4, 5]
    assert tree2.to_list() == [3, 4, 5]


def test_iter() -> None:
    x = [3, 1, 2, 4]
    tree: BinaryTree[int] = BinaryTree()
    tree.from_list(x)
    tmp = []
    for elem in tree:
        tmp.append(elem)
    assert tmp == [1, 2, 3, 4]
    assert tree.to_list() == [1, 2, 3, 4]

    empty_tree: BinaryTree[int] = BinaryTree()
    with pytest.raises(StopIteration):
        next(iter(empty_tree))


@given(st.lists(st.integers()))
def test_from_list_to_list_roundtrip(a: list[int]) -> None:
    tree: BinaryTree[int] = BinaryTree()
    tree.from_list(a)
    b = tree.to_list()
    assert b == sorted(set(a))


@given(st.lists(st.integers()))
def test_size_equals_len_of_set(a: list[int]) -> None:
    tree: BinaryTree[int] = BinaryTree()
    tree.from_list(a)
    assert tree.size() == len(set(a))


@given(st.lists(st.integers()))
def test_member_of_added_element(a: list[int]) -> None:
    tree: BinaryTree[int] = BinaryTree()
    for elem in a:
        tree.add(elem)
    for elem in set(a):
        assert tree.member(elem) is True


@given(st.lists(st.integers()), st.integers())
def test_remove_removes_element(a: list[int], b: int) -> None:
    tree: BinaryTree[int] = BinaryTree()
    tree.from_list(a)
    before = tree.size()
    tree.remove(b)
    after = tree.size()
    if b in set(a):
        assert after == before - 1
        assert tree.member(b) is False
    else:
        assert after == before


@given(st.lists(st.integers()), st.lists(st.integers()), st.lists(st.integers()))
def test_monoid_associativity(a: list[int], b: list[int], c: list[int]) -> None:
    def build_tree(lst: list[int]) -> BinaryTree[int]:
        t: BinaryTree[int] = BinaryTree()
        t.from_list(lst)
        return t

    left = build_tree(a)
    left.concat(build_tree(b))
    left.concat(build_tree(c))

    bc = build_tree(b)
    bc.concat(build_tree(c))
    right = build_tree(a)
    right.concat(bc)

    assert left == right


@given(st.lists(st.integers()))
def test_empty_identity(a: list[int]) -> None:
    tree: BinaryTree[int] = BinaryTree()
    tree.from_list(a)
    empty: BinaryTree[int] = BinaryTree.empty()
    tree.concat(empty)
    assert tree.to_list() == sorted(set(a))
    empty.concat(tree)
    assert empty.to_list() == sorted(set(a))


def test_none_handling() -> None:
    tree: BinaryTree[Optional[int]] = BinaryTree()
    tree.add(None)
    assert tree.size() == 1
    assert tree.member(None) is True
    assert tree.to_list() == [None]

    tree.add(None)
    assert tree.size() == 1

    tree.add(5)
    tree.add(3)
    assert tree.size() == 3
    assert tree.to_list() == [None, 3, 5]

    tree.remove(None)
    assert tree.size() == 2
    assert tree.member(None) is False
    assert tree.to_list() == [3, 5]

    tree.remove(None)
    assert tree.size() == 2

    tree.from_list([None, 1, None, 2])
    assert tree.to_list() == [None, 1, 2]

    tree.from_list([None, 1, 2, 3])
    tree.filter(lambda x: x is None or (x is not None and x > 1))
    assert tree.to_list() == [None, 2, 3]

    tree.from_list([1, 2, 3])
    tree.map(lambda x: None if x == 2 else x)
    assert tree.to_list() == [None, 1, 3]

    tree.from_list([None, 2, 3])
    total = tree.reduce(lambda acc, x: acc + (x if x is not None else 0), 0)
    assert total == 5
