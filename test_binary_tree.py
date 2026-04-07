import pytest
from hypothesis import given
import hypothesis.strategies as st
from binary_tree import BinaryTree


# Author: Daybreakxia

# ---------- basic functions test ----------
# To test, the code is :
# pytest tests/test_binary_tree.py -v
# This basic test codes include:
# 1. test_size()
# 2. test_member()
# 3. test_add_duplicate()
# 4. test_to_list()
# 5. test_from_list()
# 6. test_remove()

def test_size():
    tree = BinaryTree()
    assert tree.size() == 0
    tree.add(5)
    assert tree.size() == 1
    tree.add(3)
    tree.add(7)
    assert tree.size() == 3


def test_member():
    tree = BinaryTree()
    assert tree.member(5) is False
    tree.add(5)
    assert tree.member(5) is True
    tree.add(3)
    tree.add(7)
    assert tree.member(3) is True
    assert tree.member(7) is True
    assert tree.member(9) is False


def test_add_duplicate():
    tree = BinaryTree()
    tree.add(5)
    tree.add(5)
    assert tree.size() == 1
    assert tree.to_list() == [5]


def test_to_list():
    tree = BinaryTree()
    assert tree.to_list() == []
    tree.add(5)
    assert tree.to_list() == [5]
    tree.add(3)
    tree.add(7)
    assert tree.to_list() == [3, 5, 7]  # In order ascending


def test_from_list():
    test_data = [[], [5], [3, 5, 7], [7, 3, 5, 3]]
    for e in test_data:
        tree = BinaryTree()
        tree.from_list(e)
        # The set will remove duplicates,  remember
        expected = sorted(set(e))
        assert tree.to_list() == expected


def test_remove():
    tree = BinaryTree()
    tree.remove(5)  # Test empty tree
    assert tree.size() == 0

    tree.from_list([5, 3, 7, 2, 4, 6, 8])
    # the tree is like this:
    #       5
    #    3     7
    # 2   4   6   8

    # Delete leaf node
    tree.remove(2)
    assert tree.member(2) is False
    assert tree.size() == 6
    # Delete a node with only one child node
    tree.remove(3)  # 3 has child node 4
    assert tree.member(3) is False
    assert tree.member(4) is True
    # Delete a node with two child nodes
    tree.remove(5)  # root node
    assert tree.member(5) is False
    assert tree.size() == 4
    # try delete a node that does not exist
    tree.remove(100)
    assert tree.size() == 4


# ---------- advanced functions test ----------
# so there are some advanced functions to test
# 1. test_filter()
# 2. test_map()
# 3. test_reduce()
# 4. test_empty()
# 5. test_concat()
# 6. test_iter()

def test_filter():
    tree = BinaryTree()
    tree.filter(lambda x: x > 0)  # empty tree
    assert tree.to_list() == []

    tree.from_list([1, 2, 3, 4, 5])
    tree.filter(lambda x: x % 2 == 0)  # find the even number
    assert tree.to_list() == [2, 4]

    tree.filter(lambda x: x > 10)  # find the number > 10
    assert tree.to_list() == []


def test_map():
    tree = BinaryTree()
    tree.map(lambda x: x + 1)
    assert tree.to_list() == []

    tree.from_list([1, 2, 3])
    tree.map(lambda x: x * 2)
    assert tree.to_list() == [2, 4, 6]

    # Mapping can lead to duplicates, it can remove them automatically
    tree.from_list([-2, -1, 1, 2])
    tree.map(abs)
    assert tree.to_list() == [1, 2]  # only 1 and 2


def test_reduce():
    tree = BinaryTree()
    assert tree.reduce(lambda acc, x: acc + x, 0) == 0
    assert tree.reduce(lambda acc, x: acc * x, 1) == 1

    # Summation
    tree.from_list([1, 2, 3, 4])
    assert tree.reduce(lambda acc, x: acc + x, 0) == 10

    # Find the product
    assert tree.reduce(lambda acc, x: acc * x, 1) == 24

    # Find Max
    assert tree.reduce(lambda acc, x: acc if acc > x else x, -float('inf')) == 4

    # Find size by reduce
    assert tree.reduce(lambda acc, _: acc + 1, 0) == tree.size()


def test_empty():
    tree1 = BinaryTree.empty()
    assert tree1.size() == 0
    tree2 = BinaryTree()
    assert tree2.size() == 0
    # empty tree is same
    assert tree1.to_list() == tree2.to_list()


def test_concat():
    tree1 = BinaryTree()
    tree2 = BinaryTree()
    tree1.concat(tree2)
    assert tree1.size() == 0

    tree1.from_list([1, 2, 3])
    tree2.from_list([3, 4, 5])
    tree1.concat(tree2)
    assert tree1.to_list() == [1, 2, 3, 4, 5]  # Deduplication after merging
    assert tree2.to_list() == [3, 4, 5]  # tree2 did not change


def test_iter():
    x = [3, 1, 2, 4]
    tree = BinaryTree()
    tree.from_list(x)
    tmp = []
    for elem in tree:
        tmp.append(elem)
    # The iteration order should be inorder traversal
    assert tmp == [1, 2, 3, 4]
    # Iteration does not change the tree
    assert tree.to_list() == [1, 2, 3, 4]

    # the iteration of empty tree
    empty_tree = BinaryTree()
    with pytest.raises(StopIteration):
        next(iter(empty_tree))


# ---------- Attribute-based testing (PBT) ----------
# this is a test for the BinaryTree class
# it include:
# 1. test_from_list_to_list_roundtrip
# 2. test_size_equals_len_of_set
# 3. test_member_of_added_element
# 4. test_remove_removes_element
# 5. test_monoid_associativity
# 6. test_empty_identity

@given(st.lists(st.integers()))
def test_from_list_to_list_roundtrip(a):
    tree = BinaryTree()
    tree.from_list(a)
    b = tree.to_list()
    # After converting a set to a list, it should be deduplicated and sorted.
    assert b == sorted(set(a))


@given(st.lists(st.integers()))
def test_size_equals_len_of_set(a):
    tree = BinaryTree()
    tree.from_list(a)
    assert tree.size() == len(set(a))


@given(st.lists(st.integers()))
def test_member_of_added_element(a):
    tree = BinaryTree()
    for elem in a:
        tree.add(elem)
    for elem in set(a):
        assert tree.member(elem) is True


@given(st.lists(st.integers()), st.integers())
def test_remove_removes_element(a, b):
    tree = BinaryTree()
    tree.from_list(a)
    before = tree.size()
    tree.remove(b)
    after = tree.size()
    if b in set(a):
        assert after == before - 1
        assert tree.member(b) is False
    else:
        assert after == before


# Monoid group property test
@given(st.lists(st.integers()), st.lists(st.integers()), st.lists(st.integers()))
def test_monoid_associativity(a, b, c):
    # emm, what we need test is this : (a ⊕ b) ⊕ c  == a ⊕ (b ⊕ c)
    def build_tree(lst):
        t = BinaryTree()
        t.from_list(lst)
        return t

    # (a ⊕ b) ⊕ c first
    left = build_tree(a)
    left.concat(build_tree(b))
    left.concat(build_tree(c))

    # a ⊕ (b ⊕ c) second, and you can see we copy bc because concat will change it
    bc = build_tree(b)
    bc.concat(build_tree(c))
    right = build_tree(a)
    right.concat(bc)

    assert left.to_list() == right.to_list()


@given(st.lists(st.integers()))
def test_empty_identity(a):
    tree = BinaryTree()
    tree.from_list(a)
    empty = BinaryTree.empty()
    # this test: a ⊕ empty == a
    tree.concat(empty)
    assert tree.to_list() == sorted(set(a))
    # empty ⊕ a == a
    empty.concat(tree)
    assert empty.to_list() == sorted(set(a))


# ---------- Test None. ----------
# add some tests for None.Now it is an element.It can be added or removed now.
def test_none_handling():
    tree = BinaryTree()
    # add None
    tree.add(None)
    assert tree.size() == 1
    assert tree.member(None) is True
    assert tree.to_list() == [None]

    # add None again
    tree.add(None)
    assert tree.size() == 1

    # add None and integer
    tree.add(5)
    tree.add(3)
    assert tree.size() == 3
    assert tree.to_list() == [None, 3, 5]

    # delete None
    tree.remove(None)
    assert tree.size() == 2
    assert tree.member(None) is False
    assert tree.to_list() == [3, 5]

    # Delete None again
    tree.remove(None)
    assert tree.size() == 2

    # Test to_list
    tree.from_list([None, 1, None, 2])
    assert tree.to_list() == [None, 1, 2]

    # test filter
    tree.from_list([None, 1, 2, 3])
    tree.filter(lambda x: x is None or x > 1)
    assert tree.to_list() == [None, 2, 3]

    # test map
    tree.from_list([1, 2, 3])
    tree.map(lambda x: None if x == 2 else x)
    assert tree.to_list() == [None, 1, 3]

    # test reduce
    tree.from_list([None, 2, 3])
    total = tree.reduce(lambda acc, x: acc + (x if x is not None else 0), 0)
    assert total == 5
