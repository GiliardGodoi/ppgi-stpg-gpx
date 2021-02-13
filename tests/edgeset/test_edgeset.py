from random import choice, choices, sample
from itertools import count
import unittest
from typing import Generator, Iterator

from ga4stpg.edgeset import EdgeSet, UEdge


class TestEdgeSet(unittest.TestCase):

    def test_init_empty(self):
        edset = EdgeSet()
        self.assertFalse(len(edset))

    def test_init_with_list_of_tuples(self):
        A = count(0, step=2)
        B = count(1, step=2)

        items = list((next(A), next(B)) for _ in range(200))

        self.assertIsInstance(items, list)
        self.assertTrue(all(isinstance(item, tuple) for item in items))

        result = EdgeSet(items)

        self.assertIsInstance(result, EdgeSet)
        self.assertEqual(len(result), 200)
        self.assertIsInstance(result._edges, set)

    def test_init_with_list_of_edges(self):
        A = count(0, step=2)
        B = count(1, step=2)

        items = list(UEdge(next(A), next(B)) for _ in range(200))

        self.assertIsInstance(items, list)
        self.assertTrue(all(isinstance(item, UEdge) for item in items))

        result = EdgeSet(items)

        self.assertIsInstance(result, EdgeSet)
        self.assertEqual(len(result), 200)
        self.assertIsInstance(result._edges, set)
        self.assertTrue(all(isinstance(edge, UEdge) for edge in result))

    def test_init_with_tuple_of_tuples(self):
        A = count(0, step=2)
        B = count(1, step=2)

        items = tuple((next(A), next(B)) for _ in range(200))

        self.assertIsInstance(items, tuple)
        self.assertTrue(all(isinstance(item, tuple) for item in items))

        result = EdgeSet(items)

        self.assertIsInstance(result, EdgeSet)
        self.assertEqual(len(result), 200)
        self.assertIsInstance(result._edges, set)

    def test_init_with_tuple_of_edges(self):
        A = count(0, step=2)
        B = count(1, step=2)

        items = tuple(UEdge(next(A), next(B)) for _ in range(200))

        self.assertIsInstance(items, tuple)
        self.assertTrue(all(isinstance(item, UEdge) for item in items))

        result = EdgeSet(items)

        self.assertIsInstance(result, EdgeSet)
        self.assertEqual(len(result), 200)
        self.assertIsInstance(result._edges, set)
        self.assertTrue(all(isinstance(edge, UEdge) for edge in result))

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
        A = count(0, step=2)
        B = count(1, step=2)

        items = set([UEdge(next(A), next(B)) for _ in range(200)])

        self.assertIsInstance(items, set)
        self.assertTrue(all(isinstance(item, UEdge) for item in items))

        result = EdgeSet(items)

        self.assertIsInstance(result, EdgeSet)
        self.assertEqual(len(result), 200)
        self.assertIsInstance(result._edges, set)
        self.assertTrue(all(isinstance(edge, UEdge) for edge in result))

    def test_init_with_edgeset(self):
        A = count(0, step=2)
        B = count(1, step=2)

        items = [ (next(A), next(B)) for _ in range(200)]

        result = EdgeSet(items)

        other = EdgeSet(result)

        self.assertFalse(other is result)
        self.assertFalse(other._edges is result._edges)
        self.assertEqual(result, other)
        self.assertEqual(other._edges, result._edges)
        self.assertEqual(len(result), len(other))

    def test_contains(self):
        A = count(0, step=2)
        B = count(1, step=2)

        items = [ (next(A), next(B)) for _ in range(200)]
        result = EdgeSet(items)

        self.assertTrue(hasattr(result, "__contains__"))
        self.assertTrue(UEdge(8, 9) in result)
        self.assertTrue(UEdge(9, 8) in result)

        self.assertFalse(UEdge(8, 7) in result)
        self.assertFalse(UEdge(7, 8) in result)

    def test_if_is_iterable(self):
        A = count(0, step=2)
        B = count(1, step=2)

        items = [ (next(A), next(B)) for _ in range(200)]

        result = EdgeSet(items)

        self.assertTrue(hasattr(result, '__iter__'))

        self.assertIsInstance(iter(result), Iterator)

        total = 0

        for _ in result:
            total += 1

        self. assertEqual(len(result), total)

        total_again = 0
        for _ in result:
            total_again += 1

        self.assertEqual(total, total_again)

    def test_len_property(self):
        A = count(0, step=2)
        B = count(1, step=2)

        items = [ (next(A), next(B)) for _ in range(200)]

        result = EdgeSet(items)
        self.assertTrue(hasattr(result, '__len__'))

        with self.subTest("How many edges?"):
            self.assertEqual(len(result), 200)

        with self.subTest("How many edges? len(items)"):
            self.assertEqual(len(result), len(items))

    def test_sub_operand(self):
        A = count(0, step=2)
        B = count(1, step=2)

        one = EdgeSet(UEdge(next(A), next(B)) for _ in range(200))
        self.assertEqual(len(one), 200)

        self.assertTrue(hasattr(one, "__sub__"))

        C = count(200, step=2)
        D = count(201, step=2)

        two = EdgeSet(UEdge(next(C), next(D)) for _ in range(200))
        self.assertEqual(len(two), 200)

        three = one - two

        self.assertIsInstance(three, EdgeSet)
        self.assertEqual(len(three), 100)

        A = count(0, step=2)
        B = count(1, step=2)

        three_expected = EdgeSet(UEdge(next(A), next(B)) for _ in range(100))

        self.assertEqual(three, three_expected)

    def test_and_operand(self):
        A = count(0, step=2)
        B = count(1, step=2)

        one = EdgeSet(UEdge(next(A), next(B)) for _ in range(200))
        self.assertEqual(len(one), 200)

        self.assertTrue(hasattr(one, "__and__"))

        C = count(200, step=2)
        D = count(201, step=2)

        two = EdgeSet(UEdge(next(C), next(D)) for _ in range(200))
        self.assertEqual(len(two), 200)

        three = one & two

        self.assertIsInstance(three, EdgeSet)
        self.assertEqual(len(three), 100)

        four = two & one
        self.assertEqual(len(four), len(three))
        self.assertIsInstance(four, EdgeSet)

        self.assertEqual(three, four)

    def test_xor_operand(self):
        A = count(0, step=2)
        B = count(1, step=2)

        one = EdgeSet(UEdge(next(A), next(B)) for _ in range(200))
        self.assertEqual(len(one), 200)

        self.assertTrue(hasattr(one, "__xor__"))

        C = count(200, step=2)
        D = count(201, step=2)

        two = EdgeSet(UEdge(next(C), next(D)) for _ in range(200))
        self.assertEqual(len(two), 200)

        three = one ^ two

        self.assertIsInstance(three, EdgeSet)
        self.assertEqual(len(three), 200)

        four = two ^ one
        self.assertEqual(three, four)
        self.assertIsInstance(four, EdgeSet)

        E = count(0, step=2)
        F = count(1, step=2)

        five  = EdgeSet(UEdge(next(E), next(F)) for _ in range(100))
        six   = EdgeSet((next(E), next(F)) for _ in range(100))
        items = [(next(E), next(F)) for _ in range(100)]
        for item in items:
            five.add(item)

        self.assertEqual(len(five), 200)

        self.assertEqual(three, five)
        self.assertEqual(four, five)

        seven = six & five
        self.assertEqual(len(seven), 0)
        self.assertFalse(seven)
        self.assertIsInstance(seven, EdgeSet)

    def test_or_operand(self):
        A = count(0, step=2)
        B = count(1, step=2)

        one = EdgeSet(UEdge(next(A), next(B)) for _ in range(200))
        self.assertEqual(len(one), 200)

        self.assertTrue(hasattr(one, "__or__"))

        C = count(200, step=2)
        D = count(201, step=2)

        two = EdgeSet(UEdge(next(C), next(D)) for _ in range(200))
        self.assertEqual(len(two), 200)

        three = one | two

        self.assertIsInstance(three, EdgeSet)
        self.assertEqual(len(three), 300)

        four = two | one
        self.assertEqual(len(four), len(three))
        self.assertIsInstance(four, EdgeSet)

        self.assertEqual(three, four)

        E = count(0, step=2)
        F = count(1, step=2)

        five = EdgeSet(UEdge(next(E), next(F)) for _ in range(300))
        self.assertEqual(three, five)
        self.assertEqual(four, five)

    def test_eq_operand(self):
        A = count(0, step=2)
        B = count(1, step=2)

        obj_1 = EdgeSet((next(A), next(B)) for _ in range(200))
        self.assertTrue(hasattr(obj_1, '__eq__'))

        C = count(398, step=-2)
        D = count(399, step=-2)

        obj_2 = EdgeSet((next(C), next(D)) for _ in range(200))

        self.assertTrue(obj_2 == obj_1)
        self.assertTrue(obj_1 == obj_2)

        E = count(400, step=2)
        F = count(401, step=2)
        obj_3 = EdgeSet((next(E), next(F)) for _ in range(200))
        self.assertFalse(obj_1 == obj_3)
        self.assertFalse(obj_3 == obj_1)

    def test_not_equal_operand(self):
        A = count(0, step=2)
        B = count(1, step=2)

        obj_1 = EdgeSet((next(A), next(B)) for _ in range(200))
        self.assertTrue(hasattr(obj_1, '__ne__'))

        C = count(398, step=-2)
        D = count(399, step=-2)

        obj_2 = EdgeSet((next(C), next(D)) for _ in range(200))

        self.assertFalse(obj_2 != obj_1)
        self.assertFalse(obj_1 != obj_2)

        E = count(400, step=2)
        F = count(401, step=2)
        obj_3 = EdgeSet((next(E), next(F)) for _ in range(200))
        self.assertTrue(obj_1 != obj_3)
        self.assertTrue(obj_3 != obj_1)

    @unittest.skip("not implemented")
    def test_less_than_operand(self):
        raise NotImplementedError()

    @unittest.skip("not implemented")
    def test_greater_than_operand(self):
        raise NotImplementedError()

    @unittest.skip("not implemented")
    def test_greater_or_equal_opearand(self):
        raise NotImplementedError()

    @unittest.skip("not implemented")
    def test_less_or_equal_operand(self):
        raise NotImplementedError()

    def test_vertices_property(self):
        A = count(0, step=2)
        B = count(1, step=2)

        items = [(next(A), next(B)) for _ in range(200)]
        result = EdgeSet(items)

        self.assertTrue(hasattr(result, 'vertices'))
        self.assertIsInstance(result.vertices, Generator)

        C = count(0, step=2)
        D = count(1, step=2)
        aa = set(next(C) for _ in range(200))
        bb = set(next(D) for _ in range(200))

        cc = aa.union(bb)

        nodes = [v for v in result.vertices]

        self.assertEqual(len(nodes), len(cc))

    def test_vertices_after_add_a_new_edge(self):
        items = [
            (8, 6), (7, 4),(5,3), (2,1),
            (8, 7), (8, 4), (8, 5), (8, 2)
        ]

        result = EdgeSet(items)
        self.assertEqual(len(result), len(items))
        self.assertTrue(hasattr(result, 'vertices'))

        vertices = set([v for v in result.vertices])
        self.assertEqual(len(vertices), 8)

        result.add(47, 5)
        result.add(23, 4)
        vertices_b = set([v for v in result.vertices])
        self.assertEqual(len(vertices_b), 10)
        self.assertEqual(len(result), len(items) + 2)

    def test_add_an_edge(self):
        items = [(8, 9), (7, 4),(5,3), (2,1)]
        result = EdgeSet(items)
        edge = UEdge(40, 50)

        self.assertFalse(edge in result)
        self.assertEqual(len(result), len(items))
        self.assertTrue(hasattr(result, 'add'))

        result.add(edge)

        self.assertTrue(edge in result)
        self.assertEqual(len(result), len(items) + 1)

    def test_add_an_edge_as_args(self):
        items = [ (8, 9), (7, 4),(5,3), (2,1)]
        result = EdgeSet(items)
        self.assertTrue(hasattr(result, 'add'))

        edge = UEdge(40, 50)

        self.assertFalse(edge in result)
        self.assertEqual(len(result), len(items))

        result.add(50, 40)

        self.assertTrue(edge in result)
        self.assertEqual(len(result), len(items) + 1)

    def test_add_an_edge_as_list(self):
        items = [ (8, 9), (7, 4),(5,3), (2,1)]
        result = EdgeSet(items)
        self.assertTrue(hasattr(result, 'add'))

        edge = UEdge(40, 50)

        self.assertFalse(edge in result)
        self.assertEqual(len(result), len(items))

        result.add([50, 40])

        self.assertTrue(edge in result)
        self.assertEqual(len(result), len(items) + 1)

    def test_add_an_edge_as_tuple(self):
        items = [ (8, 9), (7, 4),(5,3), (2,1)]
        result = EdgeSet(items)
        self.assertTrue(hasattr(result, 'add'))

        edge = UEdge(40, 50)

        self.assertFalse(edge in result)
        self.assertEqual(len(result), len(items))

        result.add((50, 40))

        self.assertTrue(edge in result)
        self.assertEqual(len(result), len(items) + 1)

    def test_add_an_edge_as_set(self):
        items = [ (8, 9), (7, 4),(5,3), (2,1)]
        result = EdgeSet(items)
        self.assertTrue(hasattr(result, 'add'))

        edge = UEdge(40, 50)

        self.assertFalse(edge in result)
        self.assertEqual(len(result), len(items))

        result.add({40, 50})

        self.assertTrue(edge in result)
        self.assertEqual(len(result), len(items) + 1)

    def test_discard_method(self):
        items = [
            (8, 6), (7, 4), (5,3), (2, 1),
            (8, 7), (8, 4), (8, 5), (8, 2)
        ]

        result = EdgeSet(items)
        self.assertEqual(len(result), len(items))
        self.assertTrue(hasattr(result, 'discard'))

        with self.subTest("without exception: tuple"):
            result.discard((5, 8))
            self.assertEqual(len(result), len(items) - 1)

        with self.subTest("without exception: args"):
            result.discard(2, 1)
            self.assertEqual(len(result), len(items) - 2)

        with self.subTest("without exception: list"):
            result.discard([4, 7])
            self.assertEqual(len(result), len(items) - 3)

        with self.subTest("without exception: list"):
            result.discard(UEdge(7, 8))
            self.assertEqual(len(result), len(items) - 4)

        with self.subTest("without exception: alredy taken"):
            result.discard(UEdge(7, 8))
            self.assertEqual(len(result), len(items) - 4)

        with self.subTest("without exception: non exists previously"):
            result.discard(UEdge(7, 8))
            self.assertEqual(len(result), len(items) - 4)

    def test_remove_method(self):
        items = [
            (8, 6), (7, 4), (5,3), (2, 1),
            (8, 7), (8, 4), (8, 5), (8, 2)
        ]

        result = EdgeSet(items)
        self.assertEqual(len(result), len(items))
        self.assertTrue(hasattr(result, 'remove'))

        with self.subTest("without exception: tuple"):
            result.remove((5, 8))
            self.assertEqual(len(result), len(items) - 1)

        with self.subTest("without exception: args"):
            result.remove(2, 1)
            self.assertEqual(len(result), len(items) - 2)

        with self.subTest("without exception: list"):
            result.remove([4, 7])
            self.assertEqual(len(result), len(items) - 3)

        with self.subTest("without exception: list"):
            result.remove(UEdge(7, 8))
            self.assertEqual(len(result), len(items) - 4)

        with self.subTest("with exception"):
            with self.assertRaises(KeyError):
                result.remove((101, 105))

        with self.subTest("with exception: alredy removed"):
            with self.assertRaises(KeyError):
                result.remove((8, 5))

    @unittest.skip("not implemented")
    def test_issubset_method(self):
        raise NotImplementedError()

    @unittest.skip("not implemented")
    def test_issuperset_method(self):
        raise NotImplementedError()

    def test_clear_method(self):
        A = count(0, step=2)
        B = count(1, step=2)

        items = [ (next(A), next(B)) for _ in range(200)]

        result = EdgeSet(items)
        self.assertTrue(hasattr(result, 'clear'))

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
        self.assertTrue(hasattr(result, 'copy'))

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

    def test_apply_random_sample(self):
        A = count(0, step=2)
        B = count(1, step=2)

        items = list((next(A), next(B)) for _ in range(200))
        obj = EdgeSet(items)

        result = sample(list(obj), k=10)

        self.assertEqual(len(result), 10)

    def test_convert_to_set(self):
        A = count(0, step=2)
        B = count(1, step=2)

        edges = EdgeSet(UEdge(next(A), next(B)) for _ in range(200))

        result = set(edges)

        self.assertIsInstance(result, set)
        self.assertEqual(len(result), 200)

    def test_convert_to_list(self):
        A = count(0, step=2)
        B = count(1, step=2)

        edges = EdgeSet(UEdge(next(A), next(B)) for _ in range(200))

        result = list(edges)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 200)

    @unittest.skip("choice does not work")
    def test_if_choice_works(self):
        A = count(0, step=2)
        B = count(1, step=2)

        edges = EdgeSet(UEdge(next(A), next(B)) for _ in range(200))

        arbitrary_edge = choice(edges)

    @unittest.skip("choices does not work")
    def test_if_choices_works(self):
        A = count(0, step=2)
        B = count(1, step=2)

        edges = EdgeSet(UEdge(next(A), next(B)) for _ in range(200))

        arbitrary_edges = choices(edges, k=5)


    @unittest.skip("sample does not work")
    def test_if_random_sample_works(self):
        A = count(0, step=2)
        B = count(1, step=2)

        edges = EdgeSet(UEdge(next(A), next(B)) for _ in range(200))

        arbitrary = sample(edges, k=10)


if __name__ == '__main__':
    unittest.main()
