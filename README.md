# BST-lab1-variant3 - Binary Search Tree Implementation

This project implements a binary search tree with core operations,
advanced functions, and full unit tests.

## Project Structure

- binary_tree.py          Binary search tree implementation
- test_binary_tree.py     Test cases for all tree operations

## Features

### Core Methods
- add: Insert an element
- remove: Delete an element
- member: Check existence
- size: Get element count
- to_list: Convert to sorted list
- from_list: Build tree from list

### Advanced Methods
- filter: Keep elements by condition
- map: Transform all elements
- reduce: Aggregate values
- empty: Create empty tree
- concat: Merge two trees
- __iter__: Support iteration

## Contribution Log

### 31.03.2026 — Lin Shengkai
- Implemented core methods:
  - add
  - remove
  - member
  - size
  - to_list
- Wrote related test cases

### 07.04.2026 — Xia Jiale
- Implemented advanced methods:
  - filter
  - map
  - reduce
  - empty
  - concat
- Wrote related test cases

### 07.04.2026 — Lin Shengkai
- Adjusted project structure
- Fixed code style
- Fixed README format
- Passed all CI checks

## Design Notes

This binary search tree maintains the BST property:
- Left child is smaller
- Right child is larger
- Automatic duplicate removal
- Supports None values
- Full test coverage including property-based testing
- 