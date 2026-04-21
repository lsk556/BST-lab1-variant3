from __future__ import annotations
from typing import Callable, Generic, Iterable, Iterator, Protocol, TypeVar

T = TypeVar('T')
U = TypeVar('U')


class Comparable(Protocol):
    """Protocol for types that support less-than comparison."""

    def __lt__(self, other: object) -> bool:
        ...


class _Node(Generic[T]):
    __slots__ = ('value', 'left', 'right')

    def __init__(self, value: T) -> None:
        self.value: T = value
        self.left: _Node[T] | None = None
        self.right: _Node[T] | None = None

    @staticmethod
    def _lt(a: Comparable | None, b: Comparable | None) -> bool:
        if a is None and b is None:
            return False
        if a is None:
            return True
        if b is None:
            return False
        return a < b

    def add(self, element: T) -> _Node[T]:
        if element == self.value:
            return self
        elif self._lt(element, self.value):
            if self.left is None:
                self.left = _Node(element)
            else:
                self.left.add(element)
        else:
            if self.right is None:
                self.right = _Node(element)
            else:
                self.right.add(element)
        return self

    def member(self, element: T) -> bool:
        if element == self.value:
            return True
        elif self._lt(element, self.value):
            return self.left.member(element) if self.left else False
        else:
            return self.right.member(element) if self.right else False

    def size(self) -> int:
        left_size = self.left.size() if self.left else 0
        right_size = self.right.size() if self.right else 0
        return 1 + left_size + right_size

    def to_list(self) -> list[T]:
        result: list[T] = []
        self._in_order(result)
        return result

    def _in_order(self, result: list[T]) -> None:
        if self.left:
            self.left._in_order(result)
        result.append(self.value)
        if self.right:
            self.right._in_order(result)

    def remove(self, element: T) -> _Node[T] | None:
        if self._lt(element, self.value):
            if self.left:
                self.left = self.left.remove(element)
        elif self._lt(self.value, element):
            if self.right:
                self.right = self.right.remove(element)
        else:
            if self.left is None:
                return self.right
            elif self.right is None:
                return self.left
            successor = self.right
            while successor.left:
                successor = successor.left
            self.value = successor.value
            self.right = self.right.remove(successor.value)
        return self


class BinaryTree(Generic[T]):
    def __init__(self) -> None:
        self._root: _Node[T] | None = None

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

    def _in_order(self, res: list[T]) -> None:
        if self._root:
            self._root._in_order(res)

    def to_list(self) -> list[T]:
        return self._root.to_list() if self._root else []

    def from_list(self, lst: Iterable[T]) -> None:
        self._root = None
        for elem in lst:
            self.add(elem)

    def filter(self, predicate: Callable[[T], bool]) -> None:
        kept = [v for v in self.to_list() if predicate(v)]
        self.from_list(kept)

    def map(self, func: Callable[[T], T]) -> None:
        new_values = {func(v) for v in self.to_list()}
        self.from_list(new_values)

    def reduce(self, func: Callable[[U, T], U], initial: U) -> U:
        result = initial
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
        return self.to_list() == other.to_list()
