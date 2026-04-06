# BST - lab 1 - variant 3

Our variant is to implement a binary search tree (BinaryTree) and its basic operations

## Project structure

- src/binary_tree.py -- Implementation of the BinaryTree class with core BST operations.
- tests/test_binary_tree.py -- Unit tests for BinaryTree.

## Features implemented

- Insert elements into the binary search tree
- Remove elements from the binary search tree
- Check existence of an element (member)
- Get the number of elements (size)
- Convert tree to sorted list using in-order traversal
- Basic unit tests for add, remove, size, member and to_list

## Contribution

Lin Shengkai -- Implementation of add, remove, member, size, to_list and related internal methods
Xia Jiale -- Finish the test_binary_tree.py.

## Changelog

- 31.03.2026 - 0
  Initial implementation of BinaryTree with some core operations(add,member,remove,size,to_list)

- 01.04.2026 - 1
  Change the structure of files, and rename the file by the rule of snake_case.
  Add the test file.

## Design notes

The tree maintains the binary search tree property: for any node, all left descendants are smaller,
and all right descendants are larger.
