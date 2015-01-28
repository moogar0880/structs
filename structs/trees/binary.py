# -*- coding: utf-8 -*-
"""This module contains a collection of Binary Tree type data structures"""

from .base import Node, Tree

__author__ = 'Jon Nappi'
__all__ = ['BinaryTree']


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
        return self.right_child and self.left_child

    def update(self, key, value, left, right):
        """Convenience method to update all of the values stored in this
        :class:`BinaryNode`

        :param key: The key that this :class:`BinaryNode` is stored at
        :param value: The value stored in this :class:`BinaryNode`
        :param left: The left child of this :class:`BinaryNode`
        :param right: The right child of this :class:`BinaryNode`
        """
        self.key = key
        self.data = value
        self.left_child = left
        self.right_child = right
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
        succ = None
        if self.has_right_child():
            succ = self.right_child.find_min()
        else:
            if self.parent:
                if self.is_left_child():
                    succ = self.parent
                else:
                    self.parent.right_child = None
                    succ = self.parent.find_successor()
                    self.parent.right_child = self
        return succ

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
    max_size = 2
    node_type = BinaryNode

    def _get(self, key, current_node):
        """Overriden abstract method to handle the logical retrieval of nodes
        from this :class:`~structs.trees.binary.BinaryTree`. If we don't find a
        :class:`BinaryNode` at *key*, return :const:`None`. If we find a
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
        nodes into this :class:`~structs.trees.binary.BinaryTree`. Until we
        find the right place to insert our key value pair, recurse down to the
        left if *key* is less than *current_node*'s key attribute, otherwise
        recurse to the right

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

    def remove(self, node):
        """Overriden abstract method to handle the logical removal of nodes 
        from this :class:`~structs.trees.binary.BinaryTree`
        
        :param node: The :class:`BinaryNode` to remove from this 
            :class:`~structs.trees.binary.BinaryTree`
        """
        if node.is_leaf():  # leaf
            if node == node.parent.left_child:
                node.parent.left_child = None
            else:
                node.parent.right_child = None
        elif node.has_both_children():  # interior
            succ = node.find_successor()
            succ.splice_out()
            node.key = succ.key
            node.data = succ.data
        else:  # this node has one child
            if node.has_left_child():
                if node.is_left_child():
                    node.left_child.parent = node.parent
                    node.parent.left_child = node.left_child
                elif node.isright_child():
                    node.left_child.parent = node.parent
                    node.parent.right_child = node.left_child
                else:
                    node.update(node.left_child.key,
                                node.left_child.data,
                                node.left_child.left_child,
                                node.left_child.right_child)
            else:
                if node.is_left_child():
                    node.right_child.parent = node.parent
                    node.parent.left_child = node.right_child
                elif node.isright_child():
                    node.right_child.parent = node.parent
                    node.parent.right_child = node.right_child
                else:
                    node.update(node.right_child.key,
                                node.right_child.data,
                                node.right_child.left_child,
                                node.right_child.right_child)
