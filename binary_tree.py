class _Node:
    __slots__ = ('value', 'left', 'right')

    def __init__(self, value):
        """
        Initialize an empty binary search tree node
        Author: linsk
        """
        self.value = value
        self.left = None
        self.right = None

    @staticmethod
    def _lt(a, b):
        # Custom less than comparator, in order to solve None.
        if a is None and b is None:
            return False
        if a is None:
            return True
        if b is None:
            return False
        return a < b

    def add(self, element):
        """
        Insert an element into the BST, automatically avoid duplicates
        Author: linsk
        :param element: the element to be added into the tree
        """
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

    def member(self, element):
        """
        Check if the element exists in the BST
        Author: linsk
        :param element: the element to search
        :return: True if exists, False otherwise
        """
        if element == self.value:
            return True
        elif self._lt(element, self.value):
            return self.left.member(element) if self.left else False
        else:
            return self.right.member(element) if self.right else False

    def size(self):
        """
        Calculate the total number of elements in the tree
        Author: linsk
        :return: integer representing tree size
        """
        # left_size = 0
        # if self.left is not None:
        #     left_size = self.left.size()
        left_size = self.left.size() if self.left else 0
        right_size = self.right.size() if self.right else 0
        return 1 + left_size + right_size

    def to_list(self):
        """
        Convert BST to a sorted list using in-order traversal
        Author: linsk
        :return: sorted list of tree elements
        """
        result = []
        self._in_order(result)
        return result

    def _in_order(self, result):
        """
        Internal helper for in-order traversal
        Author: linsk
        :param res: list to store traversal result
        """
        if self.left:
            self.left._in_order(result)
        result.append(self.value)
        if self.right:
            self.right._in_order(result)

    def remove(self, element):
        """
        remove the element.
        Author: Daybreakxia
        """
        if self._lt(element, self.value):
            if self.left:
                self.left = self.left.remove(element)  # Iteration
        elif self._lt(self.value, element):
            if self.right:
                self.right = self.right.remove(element)
        else:
            if self.left is None:
                return self.right  # return the right subtree
            elif self.right is None:
                return self.left
            # so we need find successor
            successor = self.right
            while successor.left:
                successor = successor.left
            self.value = successor.value
            self.right = self.right.remove(successor.value)
        return self


class BinaryTree:
    def __init__(self):
        self._root = None

    def add(self, element):
        if self._root is None:
            self._root = _Node(element)
        else:
            self._root.add(element)

    def member(self, element):
        return self._root.member(element) if self._root else False

    def size(self):
        return self._root.size() if self._root else 0

    def remove(self, element):
        if self._root:
            self._root = self._root.remove(element)

    def _in_order(self, res):
        if self._root:
            self._root._in_order(res)

    def to_list(self):
        return self._root.to_list() if self._root else []

    def from_list(self, lst):
        self._root = None
        for elem in lst:
            self.add(elem)

    def filter(self, predicate):
        kept = [v for v in self.to_list() if predicate(v)]
        self.from_list(kept)

    def map(self, func):
        new_values = {func(v) for v in self.to_list()}
        self.from_list(new_values)

    def reduce(self, func, initial):
        result = initial
        for v in self.to_list():
            result = func(result, v)
        return result

    @classmethod
    def empty(cls):
        return cls()

    def concat(self, other):
        for elem in other.to_list():
            self.add(elem)

    def __iter__(self):
        return iter(self.to_list())

    def __str__(self):
        return "{" + ", ".join(str(v) for v in self.to_list()) + "}"
