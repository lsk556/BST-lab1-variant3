class BinaryTree(object):
    def __init__(self):
        """
        Initialize an empty binary search tree node
        Author: linsk
        """
        self.value = None
        self.left = None
        self.right = None

    def add(self, element):
        """
        Insert an element into the BST, automatically avoid duplicates
        Author: linsk
        :param element: the element to be added into the tree
        """
        if self.value is None:
            self.value = element
            return

        if element == self.value:
            return
        elif element < self.value:
            if self.left is None:
                self.left = BinaryTree()
            self.left.add(element)
        else:
            if self.right is None:
                self.right = BinaryTree()
            self.right.add(element)

    def remove(self, element):
        """
        Remove the specified element from the BST
        Author: linsk
        :param element: the element to be removed
        """
        # 1. Return directly if the tree is empty
        if self.value is None:
            return
        # 2. If target is smaller than current node, search left subtree
        if element < self.value:
            # Check if left subtree exists
            if self.left:
                self.left = self._remove_recursive(self.left ,element)
        # 3. If target is larger than current node, search right subtree
        elif element > self.value:
            # Check if right subtree exists
            if self.right:
                self.right = self._remove_recursive(self.right ,element)
        else:
        # 4. Found the target node, perform deletion
            self._replace_with_successor()

    def _remove_recursive(self, node, element):
        """
        Internal recursive helper method for deletion
        Author: linsk
        :param node: current subtree node being processed
        :param element: the element to be removed
        :return: the modified subtree after deletion
        """
        # 1， Check if current node is null
        if self.value is None:
            return None
        # 2. Search left subtree if target is smaller
        if element < node.value:
            node.left = self._remove_recursive(node.left, element)
        # 3. Search right subtree if target is larger
        elif element > node.value:
            node.right = self._remove_recursive(node.right, element)
        # 4. Found target node, perform deletion
        else:
            return node._replace_with_successor()
        # 5. Target not found, return original node
        return node

    def _replace_with_successor(self):
        """
        Internal helper to replace current node with its successor
        Handle three cases: leaf node, one child, two children
        Author: linsk
        :return: modified node after replacement
        """
        # 1. Current node is a leaf node
        if self.left is None and self.right is None:
            self.value = None
            return None
        # 2. Current node only has right child
        if self.value is None:
            self.value = self.right.value
            self.left = self.right.left
            self.right = self.right.right
            return self
        # 3. Current node only has left child
        if self.right is None:
            self.value = self.left.value
            self.right = self.left.right
            self.left = self.left.left
            return self

        # 4. Current node has two children, replace with successor node
        successor_node = self.right
        while successor_node.left:
            successor_node = successor_node.left
        self.value = successor_node.value
        self.right = self._remove_recursive(self.right, successor_node.value)
        return self

    def member(self, element):
        """
        Check if the element exists in the BST
        Author: linsk
        :param element: the element to search
        :return: True if exists, False otherwise
        """
        if self.value is None:
            return False
        if element == self.value:
            return True
        elif element < self.value:
            return self.left.member(element) if self.left else False
        else:
            return self.right.member(element) if self.right else False

    def size(self):
        """
        Calculate the total number of elements in the tree
        Author: linsk
        :return: integer representing tree size
        """
        if self.value is None:
            return 0
        left_size = self.left.size() if self.left else 0
        right_size = self.right.size() if self.right else 0
        return left_size + right_size + 1

    def to_list(self):
        """
        Convert BST to a sorted list using in-order traversal
        Author: linsk
        :return: sorted list of tree elements
        """
        res = []
        self._in_order(res)
        return res

    def _in_order(self, res):
        """
        Internal helper for in-order traversal
        Author: linsk
        :param res: list to store traversal result
        """
        if self.left:
            self.left._in_order(res)
        if self.value is not None:
            res.append(self.value)
        if self.right:
            self.right._in_order(res)

    def filter(self, element):
        return -1

    def map(self, element):
        return -1

    def reduce(self):
        return -1

    def empty(self):
        return -1

    def concat(self):
        return -1

    def __iter__(self):
        return self

    def __next__(self):
        if self.value is None:
            raise StopIteration


