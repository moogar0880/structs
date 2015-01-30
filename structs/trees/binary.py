# -*- coding: utf-8 -*-
"""This module contains a collection of Binary Tree type data structures"""

from .base import Node, Tree

__author__ = 'Jon Nappi'
__all__ = ['BinaryTree', 'BinarySearchTree']


class BinaryNode(Node):
    """A data node used to store data at a specific key value pair in a
    :class:`~structs.trees.binary.BinaryTree`. This class also handles tracking
    child and parent :class:`BinaryNode`'s.
    """

    def __init__(self, key, value, left=None, right=None, parent=None):
        """Create a new :class:`BinaryNode` instance to store *value* at *key*.
        Also handle registering this node as a child of *parent* and a parent
        of *left* and *right*

        :param key: The key to store *value* at
        :param value: The actual data stored in this :class:`BinaryNode`
        :param left: The left child to be stored at this node with a key that
            is logically less than this :class:`BinaryNode`
        :param right: The right child to be stored at this node with a key that
            is logically greater than this :class:`BinaryNode`
        :param parent: The :class:`BinaryNode` that has this
            :class:`BinaryNode` as a child
        """
        super().__init__(key, value, parent=parent)
        self.left_child, self.right_child = left, right

    def has_left_child(self):
        """Determine if this :class:`BinaryNode` has a left child

        :return: :const:`True` if `left_child` is not :const:`None`, otherwise
            :const:`False`
        """
        return self.left_child is not None

    def has_right_child(self):
        """Determine if this :class:`BinaryNode` has a right child

        :return: :const:`True` if `right_child` is not :const:`None`, otherwise
            :const:`False`
        """
        return self.right_child is not None

    def is_left_child(self):
        """Determine if this :class:`BinaryNode` is it's parent's left child

        :return: :const:`True` if this :class:`BinaryNode` is it's parent's
        left child, otherwise :const:`False`
        """
        return self.parent and self.parent.left_child == self

    def is_right_child(self):
        """Determine if this :class:`BinaryNode` is it's parent's right child

        :return: :const:`True` if this :class:`BinaryNode` is it's parent's
        right child, otherwise :const:`False`
        """
        return self.parent and self.parent.right_child == self

    def has_both_children(self):
        """Determine if this :class:`BinaryNode` has both of it's child nodes

        :return: :const:`True` if this :class:`BinaryNode` has both of it's
            child nodes, otherwise :const:`False`
        """
        return self.right_child is not None and self.left_child is not None

    def update(self, key, value, left=None, right=None):
        """Convenience method to update all of the values stored in this
        :class:`BinaryNode`

        :param key: The key that this :class:`BinaryNode` is stored at
        :param value: The value stored in this :class:`BinaryNode`
        :param left: The left child of this :class:`BinaryNode`
        :param right: The right child of this :class:`BinaryNode`
        """
        self.key = key
        self.data = value
        self.left_child = left or self.left_child
        self.right_child = right or self.right_child
        if self.has_left_child():
            self.left_child.parent = self
        if self.has_right_child():
            self.right_child.parent = self

    @property
    def children(self):
        """An immutable collection of the children in this :class:`BinaryNode`
        """
        return tuple([self.left_child, self.right_child])

    def splice_out(self):
        """Remove this :class:`BinaryNode` from it's containing
        :class:`~structs.trees.binary.BinaryTree` and handle rearranging
        it's connected :class:`BinaryNode`'s accordingly
        """
        if self.is_leaf():
            if self.is_left_child():
                self.parent.left_child = None
            else:
                self.parent.right_child = None
        elif self.has_children():
            if self.has_left_child():
                if self.is_left_child():
                    self.parent.left_child = self.left_child
                else:
                    self.parent.right_child = self.left_child
                self.left_child.parent = self.parent
            else:
                if self.is_left_child():
                    self.parent.left_child = self.right_child
                else:
                    self.parent.right_child = self.right_child
                self.right_child.parent = self.parent

    def find_successor(self):
        """Find the next greatest :class:`BinaryNode` under this
        :class:`BinaryNode` and return it. If no such :class:`BinaryNode`
        exists, return :const:`None`

        :return: The :class:`BinaryNode` that is the next greatest to this
            :class:`BinaryNode` in it's containing
            :class:`~structs.trees.binary.BinaryTree` or :const:`None`
        """
        successor = None
        if self.has_right_child():
            successor = self.right_child.find_min()
        else:
            if self.parent:
                if self.is_left_child():
                    successor = self.parent
                else:
                    successor = self.parent.find_successor()
        return successor
    find_max = find_successor

    def find_min(self):
        """Find the next lowest :class:`BinaryNode` under this
        :class:`BinaryNode` and return it. If no such :class:`BinaryNode`
        exists, return :const:`None`

        :return: The :class:`BinaryNode` that is the next lowest to this
            :class:`BinaryNode` in it's containing
            :class:`~structs.trees.binary.BinaryTree` or :const:`None`
        """
        current = self
        while current.has_left_child():
            current = current.left_child
        return current

    def __str__(self):
        """Dump the string contents of this :class:`BinaryNode`'s data"""
        return str(self.data)

    __repr__ = __str__


class BinaryTree(Tree):
    """A :class:`~structs.trees.base.Tree` based data structure in which each
    :class:`~structs.trees.base.Node` has at most two children.
    """

    #: The maximum number of children each node can have
    max_size = 2

    #: The type of node used in this :class:`Tree`
    node_type = BinaryNode

    def _get(self, key, current_node):
        """Search for the :class:`~structs.trees.base.Node` stored at *key*.
        Because Binary Tree's aren't sorted in any way, we have to perform a
        traversal of (potentially) the entire tree to find the node we're
        looking for

        :param key: The key our target Node is stored at
        :param current_node: The current node in our traversal
        """
        for node in self.in_order:
            if node.key == key:
                return node
        return None

    def _put(self, key, value, current_node):
        """Insert a new node with data of *value* at *key*. Insert into the
        next open child slot that we can find in the tree

        :param key: The key to store the new node at
        :param value: The data for the new node
        :param current_node: The current node we're trying to insert at
        """
        if not current_node.has_left_child():
            current_node.left_child = self.node_type(key, value,
                                                     parent=current_node)
        elif not current_node.has_right_child():
            current_node.right_child = self.node_type(key, value,
                                                      parent=current_node)
        else:
            for node in current_node.children:
                self._put(key, value, node)  # Order doesn't matter

    def _delete(self, current_node):
        """Since there's no specific logic required when removing from an
        unsorted tree, we can just splice our the node we're looking to remove

        :param current_node: The node to remove
        """
        current_node.splice_out()


class BinarySearchTree(BinaryTree):
    """A Binary Search Tree is a sorted Binary Tree in which each node has a
    comparable key (and an associated value) and satisfies the restriction that
    the key in any node is larger than the keys in all nodes in that node's
    left sub-tree and smaller than the keys in all nodes in that node's right
    sub-tree.
    """

    def _get(self, key, current_node):
        """Overriden abstract method to handle the logical retrieval of nodes
        from this :class:`~structs.trees.binary.BinarySearchTree`. If we don't
        find a :class:`BinaryNode` at *key*, return :const:`None`. If we find a
        :class:`BinaryNode`, return it. Otherwise continue searching down to
        the left if our current key is less than *current_node*'s key,
        otherwise recurse to the right

        :param key: The key to search for
        :param current_node: The current :class:`BinaryNode` we're attempting
            to retrieve from
        """
        if not current_node:
            return None
        elif current_node.key == key:
            return current_node
        elif key < current_node.key:
            return self._get(key, current_node.left_child)
        else:
            return self._get(key, current_node.right_child)

    def _put(self, key, value, current_node):
        """Overriden abstract method to handle the logical insertions of new
        nodes into this :class:`~structs.trees.binary.BinarySearchTree`. Until
        we find the right place to insert our key value pair, recurse down to
        the left if *key* is less than *current_node*'s key attribute,
        otherwise recurse to the right

        :param key: The key to search for
        :param value: The data to be inserted into the :class:`Tree`
        :param current_node: The current :class:`BinaryNode` we're attempting
            to retrieve from
        """
        if key < current_node.key:
            if current_node.has_left_child():
                self._put(key, value, current_node.left_child)
            else:
                current_node.left_child = self.node_type(key, value,
                                                         parent=current_node)
        else:
            if current_node.has_right_child():
                self._put(key, value, current_node.right_child)
            else:
                current_node.right_child = self.node_type(key, value,
                                                          parent=current_node)

    def _delete(self, node):
        """Overriden abstract method to handle the logical removal of nodes
        from this :class:`~structs.trees.binary.BinarySearchTree`

        :param node: The :class:`BinaryNode` to remove from this
            :class:`~structs.trees.binary.BinarySearchTree`
        """
        if node == self.root and self.root.is_leaf():
            self.root = None
        elif node.is_leaf():  # leaf
            self._delete_leaf(node)
        elif node.has_both_children():  # interior
            self._delete_full_node(node)
        else:  # this node has one child
            if node.has_left_child():
                self._delete_left_child(node)
            else:
                self._delete_right_child(node)

    @staticmethod
    def _delete_leaf(node):
        """Handle the removal of a leaf node

        :param node: The node to remove. This method can only successfully be
            called on a leaf node
        """
        if node == node.parent.left_child:
            node.parent.left_child = None
        else:
            node.parent.right_child = None

    @staticmethod
    def _delete_full_node(node):
        """Handle the removal of a node with two children

        :param node: The node to remove. This method can only succesfully be
            called on a node with two children
        """
        succ = node.find_successor()
        succ.splice_out()
        node.key = succ.key
        node.data = succ.data

    @staticmethod
    def _delete_left_child(node):
        """Handle the removal of a node that only has a left child

        :param node: The node to remove. This method can only successfully be
            called on a node that only has a left child
        """
        if node.is_left_child():
            node.left_child.parent = node.parent
            node.parent.left_child = node.left_child
        elif node.is_right_child():
            node.left_child.parent = node.parent
            node.parent.right_child = node.left_child
        else:
            node.update(node.left_child.key,
                        node.left_child.data,
                        node.left_child.left_child,
                        node.left_child.right_child)

    @staticmethod
    def _delete_right_child(node):
        """Handle the removal of a node that only has a right child

        :param node: The node to remove. This method can only successfully be
            called on a node that only has a right child
        """
        if node.is_left_child():
            node.right_child.parent = node.parent
            node.parent.left_child = node.right_child
        elif node.is_right_child():
            node.right_child.parent = node.parent
            node.parent.right_child = node.right_child
        else:
            node.update(node.right_child.key,
                        node.right_child.data,
                        node.right_child.left_child,
                        node.right_child.right_child)
