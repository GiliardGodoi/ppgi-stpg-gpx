from random import randint
from itertools import count
import unittest
from typing import Generator, Iterator

from ga4stpg.edgeset import EdgeSet, UEdge


class TestEdgeSet(unittest.TestCase):

    def test_init_empty(self):
        edset = EdgeSet()
        self.assertFalse(len(edset))

    def test_init_with_list_of_tuples(self):
        raise NotImplementedError()

    def test_init_with_list_of_edges(self):
        raise NotImplementedError()

    def test_init_with_tuple_of_tuples(self):
        raise NotImplementedError()

    def test_init_with_tuple_of_edges(self):
        raise NotImplementedError()

    def test_init_with_set_of_tuples(self):
        A = count(0, step=2)
        B = count(1, step=2)

        items = {(next(A), next(B)) for _ in range(200)}

        self.assertIsInstance(items, set)
        self.assertTrue(all(isinstance(item, tuple) for item in items))

        result = EdgeSet(items)

        self.assertIsInstance(result, EdgeSet)
        self.assertEqual(len(result), 200)
        self.assertIsInstance(result._edges, set)


    def test_init_with_set_of_edges(self):
        raise NotImplementedError()

    def init_with_edgeset(self):
        raise NotImplementedError()

    def test_contains(self):
        raise NotImplementedError()

    def test_if_is_iterable(self):
        raise NotImplementedError()

    def test_len_property(self):
        A = count(0, step=2)
        B = count(1, step=2)

        items = [ (next(A), next(B)) for _ in range(200)]

        result = EdgeSet(items)

        with self.subTest("How many edges?"):
            self.assertEqual(len(result), 200)

        with self.subTest("How many edges? len(items)"):
            self.assertEqual(len(result), len(items))

    def test_sub_operand(self):
        raise NotImplementedError()

    def test_and_operand(self):
        raise NotImplementedError()

    def test_xor_operand(self):
        raise NotImplementedError()

    def test_or_operand(self):
        raise NotImplementedError()

    def test_eq_operand(self):
        raise NotImplementedError()

    def test_not_equal_operand(self):
        raise NotImplementedError()

    def test_less_than_operand(self):
        raise NotImplementedError()

    def test_greater_than_operand(self):
        raise NotImplementedError()

    def test_greater_or_equal_opearand(self):
        raise NotImplementedError()

    def test_less_or_equal_operand(self):
        raise NotImplementedError()

    def test_vertices_property(self):
        raise NotImplementedError()

    def test_add_method(self):
        raise NotImplementedError()

    def test_discard_method(self):
        raise NotImplementedError()

    def test_remove_method(self):
        raise NotImplementedError()

    def test_issubset_method(self):
        raise NotImplementedError()

    def test_issuperset_method(self):
        raise NotImplementedError()

    def test_clear_method(self):
        A = count(0, step=2)
        B = count(1, step=2)

        items = [ (next(A), next(B)) for _ in range(200)]

        result = EdgeSet(items)

        with self.subTest("Has it elements?"):
            self.assertTrue(result)
            self.assertTrue(len(result))
            self.assertEqual(len(result), 200)

        result.clear()

        with self.subTest("There isn't elements anymore."):
            self.assertFalse(result)
            self.assertFalse(len(result))
            self.assertEqual(len(result), 0)

    def test_copy_method(self):
        A = count(0, step=2)
        B = count(1, step=2)

        items = [ (next(A), next(B)) for _ in range(200)]

        result = EdgeSet(items)

        copied = result.copy()

        with self.subTest("test instance returned"):
            self.assertIsInstance(copied, EdgeSet)

        with self.subTest("have they same lenght?"):
            self.assertEqual(len(result), len(copied))

        with self.subTest("are they equal?"):
            self.assertTrue(result == copied)
            self.assertTrue(copied == result)

        with self.subTest("are they the same?"):
            self.assertFalse(copied is result)
            self.assertFalse(result is copied)

        with self.subTest("have they the same edges?"):
            self.assertEqual(result._edges, copied._edges)



if __name__ == '__main__':
    unittest.main()