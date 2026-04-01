import unittest
from hypothesis import given,  strategies

from binaryTree import BinaryTree


class TestBinaryTree(unittest.TestCase):
    def test_add_member_size(self):
        tree = BinaryTree()
        tree.add(5)
        tree.add(3)
        tree.add(7)
        self.assertEqual(tree.member(5), True)
        self.assertEqual(tree.size(), 3)

    def test_remove(self):
        tree = BinaryTree()
        tree.add(5)
        tree.remove(5)

    def test_to_list(self):
        tree = BinaryTree()
        tree.add(3)
        tree.add(7)
        tree.add(5)
        self.assertEqual(tree.to_list(), [3, 5, 7])


