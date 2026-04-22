from __future__ import annotations

from typing import (
    TypeVar,
    Generic,
    Optional,
    Any,
    Callable,
    Iterator,
)

T = TypeVar("T")
U = TypeVar("U")


class _Node(Generic[T]):
    __slots__ = ("value", "left", "right")

    def __init__(self, value: T) -> None:
        """Initialize an empty binary search tree node"""
        self.value: T = value
        self.left: Optional[_Node[T]] = None
        self.right: Optional[_Node[T]] = None

    @staticmethod
    def _lt(a: Any, b: Any) -> bool:
        # Custom less than comparator, in order to solve None.
        if a is None and b is None:
            return False
        if a is None:
            return True
        if b is None:
            return False
        result: bool = a < b
        return result

    def _eq_inorder(self, other: Optional[_Node[T]]) -> bool:
        stack_self: list[_Node[T]] = []
        stack_other: list[_Node[T]] = []
        cur_self: Optional[_Node[T]] = self
        cur_other: Optional[_Node[T]] = other

        while cur_self or stack_self or cur_other or stack_other:
            while cur_self:
                stack_self.append(cur_self)
                cur_self = cur_self.left
            while cur_other:
                stack_other.append(cur_other)
                cur_other = cur_other.left

            if bool(stack_self) != bool(stack_other):
                return False

            if not stack_self:
                break

            node_self = stack_self.pop()
            node_other = stack_other.pop()

            if node_self.value != node_other.value:
                return False

            cur_self = node_self.right
            cur_other = node_other.right

        return True

    def add(self, element: T) -> None:
        """Insert an element into the BST, automatically avoid duplicates"""
        if element == self.value:
            return
        if self._lt(element, self.value):
            if self.left is None:
                self.left = _Node(element)
            else:
                self.left.add(element)
        else:
            if self.right is None:
                self.right = _Node(element)
            else:
                self.right.add(element)

    def member(self, element: T) -> bool:
        """Check if the element exists in the BST"""
        if element == self.value:
            return True
        if self._lt(element, self.value):
            return self.left.member(element) if self.left else False
        return self.right.member(element) if self.right else False

    def size(self) -> int:
        """Calculate the total number of elements in the tree"""
        left_size = self.left.size() if self.left else 0
        right_size = self.right.size() if self.right else 0
        return 1 + left_size + right_size

    def to_list(self) -> list[T]:
        """Convert BST to a sorted list using in-order traversal"""
        result: list[T] = []
        self._in_order(result)
        return result

    def _in_order(self, result: list[T]) -> None:
        """Internal helper for in-order traversal"""
        if self.left:
            self.left._in_order(result)
        result.append(self.value)
        if self.right:
            self.right._in_order(result)

    def remove(self, element: T) -> Optional[_Node[T]]:
        """remove the element."""
        if element == self.value:
            if self.left is None:
                return self.right
            if self.right is None:
                return self.left
            successor = self.right
            while successor.left:
                successor = successor.left
            self.value = successor.value
            self.right = self.right.remove(successor.value)
            return self

        if self._lt(element, self.value):
            if self.left:
                self.left = self.left.remove(element)
        else:
            if self.right:
                self.right = self.right.remove(element)
        return self


class BinaryTree(Generic[T]):
    def __init__(self) -> None:
        self._root: Optional[_Node[T]] = None

    def add(self, element: T) -> None:
        if self._root is None:
            self._root = _Node(element)
        else:
            self._root.add(element)

    def member(self, element: T) -> bool:
        return self._root.member(element) if self._root else False

    def size(self) -> int:
        return self._root.size() if self._root else 0

    def remove(self, element: T) -> None:
        if self._root:
            self._root = self._root.remove(element)

    def to_list(self) -> list[T]:
        return self._root.to_list() if self._root else []

    def from_list(self, lst: list[T]) -> None:
        self._root = None
        for elem in lst:
            self.add(elem)

    def filter(self, predicate: Callable[[T], bool]) -> None:
        kept = [v for v in self.to_list() if predicate(v)]
        self.from_list(kept)

    def map(self, func: Callable[[T], T]) -> None:
        new_values = [func(v) for v in self.to_list()]
        self.from_list(new_values)

    def reduce(self, func: Callable[[U, T], U], initial: U) -> U:
        result: U = initial
        for v in self.to_list():
            result = func(result, v)
        return result

    @classmethod
    def empty(cls) -> BinaryTree[T]:
        return cls()

    def concat(self, other: BinaryTree[T]) -> None:
        for elem in other.to_list():
            self.add(elem)

    def __iter__(self) -> Iterator[T]:
        return iter(self.to_list())

    def __str__(self) -> str:
        return "{" + ", ".join(str(v) for v in self.to_list()) + "}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BinaryTree):
            return NotImplemented
        if self._root is None:
            return other._root is None
        if other._root is None:
            return False
        return self._root._eq_inorder(other._root)
