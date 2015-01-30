# -*- coding: utf-8 -*-
"""This module contains an abstract base class for all Tree type data
structures with a basic implemented Tree API and several abstract methods that
must be implemented by all inheriting base classes
"""

from abc import ABCMeta, abstractmethod
from collections import Sized, Iterable, Container

__author__ = 'Jon Nappi'
__all__ = ['Node', 'Tree']


class Node:
    """A data node used to store data at a specific key value pair in a
    :class:`~structs.trees.base.Tree`. This class also handles tracking child 
    and parent :class:`Node`'s.
    """
    children = []

    def __init__(self, key, value, parent=None):
        """Create a new :class:`Node` instance to store *value* at *key*. Also 
        handle registering this :class:`Node` as a child of *parent* and a 
        parent of any of it's child :class:`Node`'s 

        :param key: The key to store *value* at
        :param value: The actual data stored in this :class:`Node`
        :param parent: The :class:`Node` that has this :class:`Node` as a 
            child
        """
        self.key, self.data = key, value
        self.parent = parent

    def is_root(self):
        """Determine if this :class:`Node` is the root of it's containing
        :class:`~structs.trees.base.Tree`

        :return: :const:`True` if this :class:`Node` is the root of it's
            containing :class:`~structs.trees.base.Tree`, otherwise
            :const:`False`
        """
        return not self.parent

    def is_leaf(self):
        """Determine if this :class:`Node` is a leaf node of it's containing
        :class:`~structs.trees.base.Tree`

        :return: :const:`True` if this :class:`Node` is a leaf, otherwise
            :const:`False`
        """
        return not any(self.children)

    def has_children(self):
        """Determine if this :class:`Node` has child nodes

        :return: :const:`True` if this :class:`Node` has child nodes,
            otherwise :const:`False`
        """
        return len(self.children) > 0

    def __eq__(self, other):
        """Determine equivalence between this Node and any other node

        :param other: The object to compare to, will be :const:`False` if
            *other* is not an instance of :class:`Node`
        :return: :const:`False` if *other* is not an instance of :class:`Node`
            or if `other.data` is not equal to our `data`. :const:`True`
            otherwise
        """
        if not isinstance(other, Node):
            return False
        return self.data == other.data

    def __ne__(self, other):
        """Return the opposite of the result of our __eq__ method"""
        return not self.__eq__(other)

    def __gt__(self, other):
        return self.key > other.key

    def __ge__(self, other):
        return self.key >= other.key

    def __lt__(self, other):
        return self.key < other.key

    def __le__(self, other):
        return self.key <= other.key


class Tree(Sized, Iterable, Container, metaclass=ABCMeta):
    """Abstract base Tree type"""

    max_size = 0
    children = []
    node_type = Node

    def __init__(self):
        """Create a new :class:`~structs.trees.base.Tree` instance"""
        super().__init__()
        self.root = None
        self.size = 0

    def put(self, key, value):
        """Insert the provided key value pair into this :class:`Tree`. If this
        :class:`Tree` has no `root` yet, the key value pair will be stored as
        this :class:`Tree`'s root node. If this :class:`Tree` does have a root
        node, then the private `_put` method starts an insertion at `root`

        :param key: The key to insert *value* into the :class:`Tree`
        :param value: The data to be inserted into the :class:`Tree`
        """
        if self.root:
            self._put(key, value, self.root)
        else:
            self.root = self.node_type(key, value)
        self.size += 1

    @abstractmethod
    def _put(self, key, value, current_node):
        """Abstract method is to be implemented by all inheriting subclasses,
        so the specific implementation will vary depending on the type of
        :class:`Tree`.

        :param key: The key to insert *value* into the :class:`Tree`
        :param value: The data to be inserted into the :class:`Tree`
        :param current_node: The current `node_type` to attempt inserting
            *value* into
        """
        pass

    def __setitem__(self, key, value):
        """Handle inserting *value* into *key* using `instance[key] = value`
        notation. For specifics see :meth:`Tree.put`.
        """
        self.put(key, value)

    def get(self, key, default=None):
        """Retrieve the *value* stored at *key* if it exists in this
        :class:`Tree`, otherwise return *default*

        :param key: The key to search for
        :param default: The default value to return if *key* isn't in this
            :class:`Tree`
        """
        if self.root is not None:
            res = self._get(key, self.root)
            if res:
                return res
            else:
                return default
        return default

    @abstractmethod
    def _get(self, key, current_node):
        """Abstract method is to be implemented by all inheriting subclasses,
        so the specific implementation will vary depending on the type of
        :class:`Tree`.

        :param key: The key to search for
        :param current_node: The current `node_type` to retrieving from
        """
        pass

    def __getitem__(self, key):
        """Handle retrieving the value stored at *key* using `instance[key]`
        notation. For specifics see :meth:`Tree.get`.
        """
        return self.get(key)

    def __contains__(self, key):
        """Determine whether a value is already stored at *key* in this
        :class:`Tree`

        :param key: The key to search for
        :return: :const:`True`, if *key* is in this :class:`Tree`,
            :const:`False` otherwise
        """
        return self._get(key, self.root) is not None

    def delete(self, key):
        """Attempting deleting the node stored at *key* from this :class:`Tree`

        :param key: The key to delete from this :class:`Tree`
        :raises: KeyError if *key* not in :class:`Tree`
        """
        if self.size > 1:
            node_to_remove = self._get(key, self.root)
            if node_to_remove is not None:
                self._delete(node_to_remove)
                self.size -= 1
            else:
                raise KeyError('Error, key not in tree')
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size -= 1
        else:
            raise KeyError('Error, key not in tree')

    @abstractmethod
    def _delete(self, current_node):
        """Abstract method is to be implemented by all inheriting subclasses,
        so the specific implementation will vary depending on the type of
        :class:`Tree`.

        :param current_node: The current `node_type` to retrieving from
        """
        pass

    def __delitem__(self, key):
        """Handle removing the value stored at *key* using `del instance[key]`
        notation. For specifics see :meth:`Tree.delete`.
        """
        self.delete(key)

    @property
    def length(self):
        """The current length of this :class:`Tree`"""
        return self.size

    def __len__(self):
        """The current length of this :class:`Tree`"""
        return self.size

    def __iter__(self):
        """Default iterator returns the in_order representation of this
        :class:`Tree`
        """
        return self.in_order

    @property
    def preorder(self):
        """A generator containing the preorder representation of this
        :class:`Tree`
        """
        return (node for node in self.get_preorder(self.root))

    def get_preorder(self, node):
        """Recursively build the preorder representation of this :class:`Tree`

        :param node: The current node we're at in our recursive traversal
        """
        if node is not None:
            lt = [n for n in node.children if n is not None and n < node]
            gt = [n for n in node.children if n is not None and n > node]
            yield node
            for n in lt:
                for data in self.get_preorder(n):
                    yield data
            for n in gt:
                for data in self.get_preorder(n):
                    yield data

    @property
    def in_order(self):
        """A generator containing the in order representation of this
        :class:`Tree`
        """
        return (node for node in self.get_in_order(self.root))

    def get_in_order(self, node):
        """Recursively build the in order representation of this :class:`Tree`

        :param node: The current node we're at in our recursive traversal
        """
        if node is not None:
            lt = [n for n in node.children if n is not None and n < node]
            gt = [n for n in node.children if n is not None and n > node]
            for n in lt:
                for data in self.get_in_order(n):
                    yield data
            yield node
            for n in gt:
                for data in self.get_in_order(n):
                    yield data

    @property
    def postorder(self):
        """A generator containing the postorder representation of this
        :class:`Tree`
        """
        return (node for node in self.get_postorder(self.root))

    def get_postorder(self, node):
        """Recursively build the postorder representation of this :class:`Tree`

        :param node: The current node we're at in our recursive traversal
        """
        if node is not None:
            lt = [n for n in node.children if n is not None and n < node]
            gt = [n for n in node.children if n is not None and n > node]
            for n in lt:
                for data in self.get_postorder(n):
                    yield data
            for n in gt:
                for data in self.get_postorder(n):
                    yield data
            yield node

    @property
    def levelorder(self):
        """A generator containing the levelorder representation of this
        :class:`Tree`
        """
        return (node for node in self.get_level_order(self.root))

    def get_level_order(self, node, more=None):
        """Recursively build the level order representation of this
        :class:`Tree`

        :param node: The current node we're at in our recursive traversal
        """
        if node is not None:
            if more is None:
                more = []
            more += [n for n in node.children if n is not None]
            yield node
        if more:
            for data in self.get_level_order(more[0], more[1:]):
                yield data

    def __iadd__(self, other):
        """Concatenate this :class:`Tree` and another :class:`Tree` instance
        together. *other* will be iterated over in `in order` format and
        inserted node by node into this :class:`Tree`
        """
        if not isinstance(other, Tree):
            msg = 'Cannot concatenate Tree and {}'.format(type(other))
            raise TypeError(msg)
        for node in other.in_order:
            self.put(node.key, node.data)
        return self
