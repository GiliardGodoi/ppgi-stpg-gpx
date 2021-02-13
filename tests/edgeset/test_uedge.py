import unittest
from typing import Generator, Iterator

from ga4stpg.edgeset import UEdge


class TestUndiretedEdge(unittest.TestCase):

    def test_init_with_args(self):
        with self.subTest("Tuple with two values"):
            tt = (3, 56)
            try:
                UEdge(*tt)
            except Exception:
                self.fail(f"faild when trying init with {tt}")

        with self.subTest("tuple with two values and weight"):
            tt = (49, 56)
            try:
                UEdge(*tt, weight=3)
            except Exception:
                self.fail("faild when trying init with {tt} and weight=3")

        with self.subTest("Tuple with tree values"):
            ttt = (34, 90, 10)
            with self.assertRaises(TypeError):
                UEdge(*ttt)

        with self.subTest("passing tree values"):
            with self.assertRaises(TypeError):
                UEdge(22, 11, 33)

    def test_init_with_extreme_arguments(self):
        with self.subTest("init with one positional argument"):
            with self.assertRaises(TypeError) as context:
                UEdge(4)
            self.assertTrue(" missing 1 required positional argument" in str(context.exception))

        with self.subTest("init with one positional argument and weigth"):
            with self.assertRaises(TypeError) as context:
                UEdge(70, weigth=10)
            self.assertTrue(" missing 1 required positional argument" in str(context.exception))

        with self.subTest("init with one positional argument: a tuple"):
            with self.assertRaises(TypeError):
                UEdge((4, 3))

    @unittest.skip("list support > operator")
    def test_init_with_list(self):
        with self.assertRaises(TypeError):
            UEdge([3, 23, 1], [90, 10, 2])

    def test_init_with_set(self):
        with self.assertRaises(TypeError):
            UEdge(set(3), set(90))

    def test_init_with_dict(self):
        with self.assertRaises(TypeError):
            UEdge({4: 0}, {3 : 60})

    def test_init_with_typeerror(self):
        with self.assertRaises(TypeError):
            UEdge(7, 'G')

    def test_they_are_equal(self):

        A = UEdge('T', 'U')
        B = UEdge('U', 'T')

        with self.subTest("edges with character vertice"):
            self.assertTrue(hasattr(A, '__eq__'))
            self.assertFalse(A is B)
            self.assertTrue(A == B)
            self.assertFalse(A != B)

        C = UEdge(4, 9)
        D = UEdge(9, 4)
        with self.subTest("Edge with number vertices"):
            self.assertFalse(C is D)
            self.assertTrue(C == D)
            self.assertFalse(C != D)

        E = UEdge(8, 7)
        F = UEdge(9, 4)
        with self.subTest("test with they are different"):
            self.assertFalse(E is F)
            self.assertFalse(E == F)
            self.assertTrue(E != F)

        with self.subTest("mixing edges types"):
            self.assertTrue(A != D)
            self.assertTrue(C != B)
            self.assertFalse(C != F)

    def test_there_is_a_vertice(self):

        R = UEdge('A', 'B')

        self.assertTrue(hasattr(R, '__contains__'))
        self.assertTrue('A' in R)
        self.assertTrue('B' in R)
        self.assertFalse('R' in R)

        S = UEdge(50, 100)
        self.assertTrue(50 in S)
        self.assertTrue(100 in S)
        self.assertFalse(5 in S)
        self.assertFalse(10 in S)

    def test_is_hash_possible(self):

        W = UEdge(8, 3)
        self.assertTrue(hasattr(W, '__hash__'))

        M = UEdge(3, 8)

        try:
            _ = hash(W)
        except Exception:
            self.fail("it raised an exception when try hashing")

        self.assertTrue(hash(W) == hash(M))
        self.assertTrue(W == M)

        self.assertFalse(W is M)
        self.assertFalse(M is W)

    def test_if_return_vertices(self):

        P = UEdge(90, 403)

        self.assertTrue(hasattr(P, 'vertices'))
        self.assertFalse(hasattr(P, 'vertice'))

        nodes = set()
        for v in P.vertices:
            nodes.add(v)

        self.assertIsInstance(P.vertices, Generator)

        self.assertEqual(nodes, set([90, 403]))
        self.assertEqual(len(nodes), 2)

        again = set()
        for u in P.vertices :
            again.add(u)

        self.assertEqual(nodes, again)

    def test_if_is_iterable(self):

        Q = UEdge(90, 88)

        one = set()
        for w in Q:
            one.add(w)

        self.assertTrue(hasattr(Q, '__iter__'))
        self.assertIsInstance(iter(Q), Iterator)

        other = set()
        for x in Q.vertices:
            other.add(x)

        self.assertEqual(one, other)
        self.assertTrue(Q._edge)
        self.assertTrue(len(Q._edge) == 2)

    def test_getitem(self):

        O = UEdge(3, 1)

        self.assertTrue(hasattr(O, "__getitem__"))
        self.assertEqual(O[0], 1)
        self.assertEqual(O[1], 3)

        with self.assertRaises(IndexError):
            O[3]

    def test_weigth_property(self):

        with self.subTest("with weight property"):
            M = UEdge(4, 3, weight=50)

            self.assertTrue(hasattr(M, "_weight"))
            self.assertTrue(hasattr(M, '__len__'))
            self.assertTrue(len(M), 50)

        with self.subTest("without weight property"):
            N = UEdge(11, 27)
            self.assertTrue(hasattr(N, '__len__'))
            self.assertFalse(hasattr(N, '_weight'))

            with self.assertRaises(AttributeError) as context:
                len(N)

            self.assertTrue('_weight' in str(context.exception))

if __name__ == '__main__':
    unittest.main()
