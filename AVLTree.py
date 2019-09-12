'''
PROJECT 5 - AVL Trees
Name: Jack Thomas Brooks
PID: A51452865
'''

import random as r      # To use for testing

class Node:
    # DO NOT MODIFY THIS CLASS #
    __slots__ = 'value', 'parent', 'left', 'right', 'height'

    def __init__(self, value, parent=None, left=None, right=None):
        """
        Initialization of a node
        :param value: value stored at the node
        :param parent: the parent node
        :param left: the left child node
        :param right: the right child node
        """
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right
        self.height = 0

    def __eq__(self, other):
        """
        Determine if the two nodes are equal
        :param other: the node being compared to
        :return: true if the nodes are equal, false otherwise
        """
        if type(self) is not type(other):
            return False
        return self.value == other.value

    def __str__(self):
        """String representation of a node by its value"""
        return str(self.value)

    def __repr__(self):
        """String representation of a node by its value"""
        return str(self.value)

class AVLTree:

    def __init__(self):
        # DO NOT MODIFY THIS FUNCTION #
        """
        Initializes an empty Binary Search Tree
        """
        self.root = None    # The root Node of the tree
        self.size = 0       # The number of Nodes in the tree

    def __eq__(self, other):
        # DO NOT MODIFY THIS FUNCTION #
        """
        Describe equality comparison for BSTs ('==')
        :param other: BST being compared to
        :return: True if equal, False if not equal
        """
        if self.size != other.size:
            return False
        if self.root != other.root:
            return False
        if self.root is None or other.root is None:
            return True  # Both must be None

        if self.root.left is not None and other.root.left is not None:
            r1 = self._compare(self.root.left, other.root.left)
        else:
            r1 = (self.root.left == other.root.left)
        if self.root.right is not None and other.root.right is not None:
            r2 = self._compare(self.root.right, other.root.right)
        else:
            r2 = (self.root.right == other.root.right)

        result = r1 and r2
        return result

    def _compare(self, t1, t2):
        # DO NOT MODIFY THIS FUNCTION #
        """
        Recursively compares two trees, used in __eq__.
        :param t1: root node of first tree
        :param t2: root node of second tree
        :return: True if equal, False if nott
        """
        if t1 is None or t2 is None:
            return t1 == t2
        if t1 != t2:
            return False
        result = self._compare(t1.left, t2.left) and self._compare(t1.right, t2.right)
        return result

    def visual(self):
        """
        Returns a visual representation of the AVL Tree in terms of levels
        :return: None
        """
        root = self.root
        if not root:
            print("Empty tree.")
            return
        bfs_queue = []
        track = {}
        bfs_queue.append((root, 0, root.parent))
        h = self.height(self.root)
        for i in range(h+1):
            track[i] = []
        while bfs_queue:
            node = bfs_queue.pop(0)
            track[node[1]].append(node)
            if node[0].left:
                bfs_queue.append((node[0].left, node[1] + 1, node[0]))
            if node[0].right:
                bfs_queue.append((node[0].right, node[1] + 1, node[0]))
        for i in range(h+1):
            print(f"Level {i}: ", end='')
            for node in track[i]:
                print(tuple([node[0], node[2]]), end=' ')
            print()

    ### Implement/Modify the functions below ###

    def insert(self, node, value):
        """
        Inserts a node with the passed in value into the tree if apppropriate
        :param node: The root of the tree or one of its subtrees to insert the node into
        :param value: Value of a node to be inserted
        :return: Nothing
        """
        if node is None:
            new_node = Node(value)
            self.root = new_node
            self.root.parent = None
            self.size += 1
            return
        if node.value == value:
            return
        if value < node.value:
            if (node.left is None):
                new_node = Node(value)
                self.set_child(node, "left", new_node)
                self.size += 1
                self.rebalance(node)
                return
            else:
                self.insert(node.left, value)
        else:
            if node.right is None:
                new_node = Node(value)
                self.set_child(node, "right", new_node)
                self.size += 1
                self.rebalance(node)
                return
            else:
                self.insert(node.right, value)
        self.rebalance(node)

    def remove(self, node, value):
        """
        Removes a node with the given value in the tree if appropriate
        :param node: The root of the tree or one of its subtrees to remove the node from
        :param value: Value of a node to be removed
        :return: Root of the tree or subtree
        """
        if node is None or value is None:
            return None
        if node.left is None and node.right is None:
            if node.value == value:
                if self.root == node:
                    self.root = None
                node = None
                self.size -= 1
                return Node(value)
            return node
        if node.value == value:
            if node.left is not None and node.right is not None:
                node_left = node.left
                substitute_node = self.remove(node_left.right, value)
                if node.left.left is not None:
                    node_left.left.parent = node
                if substitute_node is None:
                    node.value = node_left.value
                    node.left = node_left.left
                else:
                    node_left.right = None
                    node.value = substitute_node.value
                    self.update_height(node_left)
            elif node.left is None:
                node.value = node.right.value
                node.right = node.right.right
            else:
                node.value = node.left.value
                node.left = node.left.left
            self.size -= 1
        else:
            if value > node.value:
                next_node = self.remove(node.right, value)
                if next_node is not None and next_node.value == value:
                    node.right = None
            else:
                next_node = self.remove(node.left, value)
                if next_node is not None and next_node.value == value:
                    node.left = None
        self.rebalance(node)
        return node

    def search(self, node, value):
        """
        Searches for a node with the passed in value within a tree
        :param node: The root of the tree or one of its subtrees to search
        :param value: Value of a node to be removed
        :return: Node with the given value if found or its potential parent, None if not found
        """
        if node is None or value is None:
            return None
        while (node is not None):
            if value == node.value:
                return node
            elif value > node.value:
                if node.right is None:
                    return node
                node = node.right
            elif value < node.value:
                if node.left is None:
                    return node
                node = node.left

    def inorder(self, node):
        """
        Performs an inorder traversal of the tree rooted at the given node and yields each node
        :param node: Root of the tree or one of its subtrees
        :return: None if the tree or subtree is None
        """
        if node is None:
            return None
        if node.left is not None:
            yield from self.inorder(node.left)
        yield node
        if node.right is not None:
            yield from self.inorder(node.right)

    def preorder(self, node):
        """
        Performs a preorder traversal of the tree rooted at the given node and yields each node
        :param node: Root of the tree or one of its subtrees
        :return: None if the tree or subtree is None
        """
        if node is None:
            return None
        yield node
        if node.left is not None:
            yield from self.preorder(node.left)
        if node.right is not None:
            yield from self.preorder(node.right)

    def postorder(self, node):
        """
        Performs a postorder traversal of the tree rooted at the given node and yields each node
        :param node: Root of the tree or one of its subtrees
        :return: None if the tree or subtree is None
        """
        if node is None:
            return None
        if node.left is not None:
            yield from self.postorder(node.left)
        if node.right is not None:
            yield from self.postorder(node.right)
        yield node

    def depth(self, value):
        """
        Finds the depth of the node with the given value in the tree
        :param value: A value associated with a node whose depth is to be found
        :return: -1 if the value is None or the node is not found, the depth of the node otherwise
        """
        if value is None:
            return -1
        node = self.root
        node_depth = -1
        while node is not None:
            if value == node.value:
                node_depth += 1
                return node_depth
            elif value > node.value:
                node = node.right
            elif value < node.value:
                node = node.left
            node_depth += 1
        return -1

    def height(self, node):
        """
        Finds the height of the node passed in
        :param node: A node within the tree whose height is to be found
        :return: -1 if the node is None or the tree is empty, the height of the node otherwise
        """
        if node is None or self.root is None:
            return -1
        else:
            return node.height

    def min(self, node):
        """
        Finds the node with the minimum value of the node passed in
        :param node: A node within the tree whose minimum value is to be found
        :return: None if the node is None or the tree is empty, otherwise the node with the minimum value
        """
        if self.size == 0 or node is None:
            return None
        if node.left is None:
            return node
        else:
            node = self.min(node.left)
        return node

    def max(self, node):
        """
        Finds the node with the maximum value of the node passed in
        :param node: A node within the tree whose maximum value is to be found
        :return: None if the node is None or the tree is empty, otherwise the node with the maximum value
        """
        if self.size == 0 or node is None:
            return None
        if node.right is None:
            return node
        else:
            node = self.max(node.right)
        return node

    def get_size(self):
        """
        Finds the size of the tree
        :return: Number of nodes in tree (the tree's size)
        """
        return self.size

    def update_height(self, node):
        """
        Updates the height of a given node within the tree
        :param node: A node whose height is to be updated
        :return: Nothing
        """
        leftHeight = -1
        if node.left is not None:
            leftHeight = node.left.height
        rightHeight = -1
        if node.right is not None:
            rightHeight = node.right.height
        node.height = max(leftHeight, rightHeight) + 1

    def set_child(self, parent, whichChild, child):
        """
        Takes in a parent node, either "left" or "right" indicating where its child should be set, and the parent's
        child node
        :param parent: Parent of node that is to be set in place
        :param whichChild: "left" or "right" depending on where child is to be set
        :param child: A node to be set in place at a given spot relative to its parent
        :return: False if place to set node is not "left" or "right", True otherwise
        """
        if whichChild != "left" and whichChild != "right":
            return False
        if whichChild == "left":
            parent.left = child
        else:
            parent.right = child
        if child is not None:
            child.parent = parent
        self.update_height(parent)
        return True

    def replace_child(self, parent, currentChild, newChild):
        """

        :param parent: Parent of node that is to replace its child
        :param currentChild: The parent's current child node
        :param newChild: Node to replace parent's current child node
        :return: True
        """
        if parent.left == currentChild:
            self.set_child(parent, "left", newChild)
        elif (parent.right == currentChild):
            self.set_child(parent, "right", newChild)

        return True

    def get_balance(self, node):
        """
        Finds the height balance of a node within the tree
        :param node: A node within the tree whose height balance is to be found
        :return: The node's height balance
        """

        leftHeight = -1
        if (node.left is not None):
            leftHeight = node.left.height
        rightHeight = -1
        if (node.right is not None):
            rightHeight = node.right.height
        return leftHeight - rightHeight

    def left_rotate(self, root):
        """
        Rotates left on the root node passed in
        :param root: A node within the tree that is to be rotated left on
        :return: Root passed in
        """
        rightLeftChild = root.right.left
        if (root.parent is not None):
            self.replace_child(root.parent, root, root.right)
        else:
            self.root = root.right
            self.root.parent = None
        self.set_child(root.right, "left", root)
        self.set_child(root, "right", rightLeftChild)
        return root

    def right_rotate(self, root):
        """
        Rotates right on the root node passed in
        :param root: A node within the tree that is to be rotated right on
        :return: Root passed in
        """
        leftRightChild = root.left.right
        if (root.parent is not None):
            self.replace_child(root.parent, root, root.left)
        else:
            self.root = root.left
            self.root.parent = None

        self.set_child(root.left, "right", root)
        self.set_child(root, "left", leftRightChild)
        return root

    def rebalance(self, node):
        """
        Rebalances a tree rooted at the passed in node so its height balance never surpasses an absolute value of 2
        :param node: Root of the tree or one of its subtrees to be rebalanced
        :return: Rebalanced version of node passed in
        """

        self.update_height(node)
        balance = self.get_balance(node)
        if balance == -2:
            if self.get_balance(node.right) == 1:
                self.right_rotate(node.right)
            self.left_rotate(node)
            self.update_height(node.parent)
        elif balance == 2:
            if self.get_balance(node.left) == -1:
                self.left_rotate(node.left)
            self.right_rotate(node)
            self.update_height(node.parent)
        return node

def repair_tree(tree):
    """
    "Repairs" a tree with two out of place values by swapping them
    :param tree: A tree with two out of place values
    :return: Nothing
    """
    if tree is None or tree.get_size() == 1:
        return
    first_node_val = None
    second_node_val = None
    counter = 0
    for node in tree.inorder(tree.root):
        if second_node_val is None:
            if first_node_val is None:
                first_node_val = node.value
            if node.value < first_node_val:
                second_node_val = node.value
                counter += 1
                continue
            first_node_val = node.value
        else:
            if node.value < second_node_val:
                second_node_val = node.value
                counter += 1
                break
    if counter == 2:
        for node in tree.inorder(tree.root):
            if node.value == first_node_val:
                node.value = second_node_val
            elif node.value == second_node_val:
                node.value = first_node_val
                continue
