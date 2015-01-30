# -*- coding: utf-8 -*-
import unittest
from structs.trees.binary import BinaryTree, BinaryNode

__author__ = 'Jon Nappi'


class BinaryNodeTests(unittest.TestCase):
    def setUp(self):
        self.tree = BinaryTree()

    def tearDown(self):
        self.tree = None

    def test_is_root(self):
        self.tree.put(0, 'Root')
        self.tree.put(1, 'Not Root')

        self.assertTrue(self.tree.get(0).is_root())
        self.assertFalse(self.tree.get(1).is_root())

    def test_eq(self):
        self.tree.put(0, 'Root')
        self.tree.put(1, 'Not Root')

        self.assertEqual(self.tree.root, self.tree[0])
        self.assertNotEqual(self.tree.root, self.tree[1])

    def test_ne(self):
        self.tree.put(0, 'Root')
        self.tree.put(1, 'Not Root')

        self.assertNotEqual(self.tree.root, self.tree[1])
        self.assertEqual(self.tree.root, self.tree[0])

    def test_str(self):
        self.tree.put(0, 'Root')
        self.assertEqual(str(self.tree.get(0)), 'Root')

    def test_node_update(self):
        self.tree.put(0, 'Root')
        self.assertEqual(self.tree.root.data, 'Root')
        self.tree.root.update(0, 'New Root')
        self.assertEqual(self.tree.root.data, 'New Root')

    def test_update_with_children(self):
        self.tree[3] = 'Root'  # Has two children
        self.tree[4] = 'Blue'
        self.tree[6] = 'Green'
        self.tree[2] = 'Maroon'

        self.assertEqual(self.tree[3].data, 'Root')
        self.tree.get(3).update(3, 'New Root')
        self.assertEqual(self.tree[3].data, 'New Root')

    def test_splice_leaf(self):
        self.tree[3] = 'Root'
        self.tree[5] = 'Blue'
        self.tree[6] = 'Green'   # is right leaf
        self.tree[4] = 'Maroon'  # is left leaf

        self.tree[4].splice_out()
        self.assertNotIn(4, self.tree)
        self.tree[6].splice_out()
        self.assertNotIn(6, self.tree)

    def test_splice_edges(self):
        self.tree[3] = 'Root'
        self.tree[2] = 'Left Parent'
        self.tree[1] = 'Left Child'
        self.tree[5] = 'Right Parent'
        self.tree[4] = 'Right Child'

        self.tree.get(2).splice_out()
        self.assertEqual(self.tree.root.left_child, self.tree.get(1))

        self.tree.get(5).splice_out()
        self.assertEqual(self.tree.root.right_child, self.tree.get(4))

        self.tree[2] = 'Right Left Child'
        self.tree.get(1).splice_out()
        self.assertEqual(self.tree.root.left_child, self.tree.get(2))

    def test_find_max(self):
        self.tree[5] = 'Root'
        self.tree[3] = 'Left Child'
        self.tree[7] = 'Right child'

        self.assertEqual(self.tree.get(3).find_max(), self.tree.root)
        self.assertEqual(self.tree.get(7).find_max(), self.tree.get(7))


class BinaryTreeTests(unittest.TestCase):
    def setUp(self):
        self.tree = BinaryTree()

    def tearDown(self):
        self.tree = None

    def test_init(self):
        self.assertIsNone(self.tree.root)
        self.assertEqual(self.tree.size, 0)

    def test_put_root(self):
        self.tree.put(0, 'Root')

        self.assertEqual(self.tree.root, self.tree.get(0))
        self.assertEqual(self.tree.root, self.tree[0])

    def test_put(self):
        self.tree.put(0, 'Root')
        self.tree.put(1, 'Not Root')

        new_node = self.tree.get(1)
        self.assertIn(new_node, self.tree.root.children)
        self.assertEqual(self.tree.root, new_node.parent)

    def test_put_left(self):
        self.tree[3] = 'Root'
        self.tree[2] = 'Left 1'
        self.tree[1] = 'Left 2'
        self.assertIn(1, self.tree)

    def test_items(self):
        self.tree[0] = 'Root'
        self.assertEqual(self.tree.root, self.tree[0])

    def test_get(self):
        self.tree.put(0, 'Root')
        self.assertEqual(self.tree.root, self.tree.get(0))

    def test_get_default(self):
        self.tree.put(0, 'Root')
        self.assertIsNone(self.tree.get(1))
        self.assertEqual(self.tree.get(12, 'Default'), 'Default')

    def test_get_empty_default(self):
        self.assertEqual(self.tree.get(12, 24), 24)

    def test_contains(self):
        self.tree.put(0, 'Root')
        self.assertTrue(0 in self.tree)

    def test_delete(self):
        self.tree.put(0, 'Root')
        self.tree.put(1, 'Not Root')
        self.tree.put(2, 'Not Root 2')
        self.tree.delete(1)

        self.assertNotIn(1, self.tree)
        self.assertEqual(self.tree.size, 2)

        with self.assertRaises(KeyError):
            self.tree.delete(3)

    def test_delete_one(self):
        self.tree.put(0, 'Root')
        self.tree.delete(0)

        self.assertEqual(self.tree.size, 0)
        self.assertIsNone(self.tree.root)

    def test_delete_missing(self):
        with self.assertRaises(KeyError):
            self.tree.delete(12)

    def test_del(self):
        self.tree.put(0, 'Root')
        del self.tree[0]

    def test_remove_root(self):
        self.tree.put(0, 'Root')
        self.tree.delete(self.tree.root.key)

    def test_remove_leaf(self):
        self.tree[3] = 'Root'
        self.tree[4] = 'Blue'
        self.tree[6] = 'Green'
        self.tree[2] = 'Maroon'  # Leaf node

        self.assertEqual(len(self.tree), 4)
        self.tree.delete(self.tree.get(2).key)
        self.assertEqual(len(self.tree), 3)

    def test_remove_two_children(self):
        self.tree[3] = 'Root'  # Has two children
        self.tree[4] = 'Blue'
        self.tree[6] = 'Green'
        self.tree[2] = 'Maroon'

        self.assertEqual(len(self.tree), 4)
        self.tree.delete(self.tree.root.key)
        self.assertEqual(len(self.tree), 3)

    def test_has_one_child(self):
        self.tree[3] = 'Root'
        self.tree[4] = 'Blue'  # Has one child
        self.tree[6] = 'Green'
        self.tree[2] = 'Maroon'

        self.assertEqual(len(self.tree), 4)
        self.tree.delete(self.tree.get(4).key)
        self.assertEqual(len(self.tree), 3)

    def test_lengths(self):
        self.assertEqual(self.tree.length, 0)
        self.assertEqual(len(self.tree), 0)

        self.tree.put(0, 'Root')
        self.assertEqual(self.tree.length, 1)
        self.assertEqual(len(self.tree), 1)

    def test_preorder(self):
        self.tree[3] = 'Root'
        self.tree[4] = 'Blue'
        self.tree[6] = 'Green'
        self.tree[2] = 'Maroon'

        data = [node.data for node in self.tree.preorder]
        self.assertEqual(data, ['Root', 'Maroon', 'Blue', 'Green'])

    def test_inorder(self):
        self.tree[3] = 'Root'
        self.tree[4] = 'Blue'
        self.tree[6] = 'Green'
        self.tree[2] = 'Maroon'

        data = [node.data for node in self.tree.in_order]
        self.assertEqual(data, ['Maroon', 'Root', 'Blue', 'Green'])

    def test_postorder(self):
        self.tree[3] = 'Root'
        self.tree[4] = 'Blue'
        self.tree[6] = 'Green'
        self.tree[2] = 'Maroon'

        data = [node.data for node in self.tree.postorder]
        self.assertEqual(data, ['Maroon', 'Green', 'Blue', 'Root'])

    def test_levelorder(self):
        self.tree[3] = 'Root'
        self.tree[4] = 'Blue'
        self.tree[6] = 'Green'
        self.tree[2] = 'Maroon'

        data = [node.data for node in self.tree.levelorder]
        self.assertEqual(data, ['Root', 'Maroon', 'Blue', 'Green'])

    def test_iter(self):
        self.tree.put(0, 'Root')
        self.tree.put(1, 'Not Root')

        for index, item in enumerate(self.tree):
            if index == 0:
                self.assertEqual(self.tree.root, item)
            else:
                self.assertEqual(self.tree.get(1), item)

    def test_iadd(self):
        self.tree.put(0, 'Root')
        self.tree.put(1, 'Not Root')

        tree2 = BinaryTree()
        tree2.put(3, 'Another Not Root')

        self.tree += tree2

        self.assertIn(3, self.tree)
        self.assertEqual(self.tree.get(3).data, 'Another Not Root')

        with self.assertRaises(TypeError):
            self.tree += 5
