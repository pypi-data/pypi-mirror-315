import sys
import unittest
from python_dependency_resolver import DependencyResolver
from python_dependency_resolver.exceptions import CircularReferenceException, MissingReferenceException


class DependencyResolverTestCase(unittest.TestCase):
    """
        v ----------------|
        A <-- B <-- C <-- D
              ^     ^
              |--E--|
    """

    def test_resolve(self):
        tree = {
            'A': [],
            'B': ['A'],
            'C': ['B', 'A'],
            'D': ['C', 'A'],
            'E': ['C', 'B'],
            'F': ['G'],
            'G': []
        }

        dependency_resolver = DependencyResolver()
        r = dependency_resolver.resolve(tree)
        self.assertEqual(r[0], ['A', 'B', 'C', 'D', 'E', 'G', 'F'])
        self.assertEqual(r[1], [])

    """
                <-- A  
        D <-- C
                <-- B
    """
    def test_resolve_graph(self):
        tree = {
            'A': ['C'],
            'B': ['C'],
            'C': ['D'],
            'D': [],
        }

        dependency_resolver = DependencyResolver()
        r = dependency_resolver.resolve(tree)
        self.assertEqual(r[0], ['D', 'C', 'A', 'B'])

    def test_missing_dependency(self):
        tree = {
            'A': [],
            'B': ['A'],
            'C': ['B', 'A'],
            'D': ['C', 'A'],
            'E': ['C', 'B'],
            'F': 'G',
            # 'G': []
        }

        dependency_resolver = DependencyResolver()
        with self.assertRaises(MissingReferenceException) as e:
            dependency_resolver.resolve(tree)
        self.assertEqual(str(e.exception), 'Missing reference detected: G')

        dependency_resolver = DependencyResolver(raise_errors=False)
        r = dependency_resolver.resolve(tree)
        self.assertEqual(r[0], ['A', 'B', 'C', 'D', 'E', 'F'])
        self.assertEqual(r[1], ['G'])

    """
         < ------|
        A        B
        |------ >
    """
    def test_circular_dependency(self):
        tree = {
            'A': ['B'],
            'B': ['A'],
        }

        dependency_resolver = DependencyResolver()
        with self.assertRaises(CircularReferenceException) as e:
            dependency_resolver.resolve(tree)
        self.assertEqual(str(e.exception), 'Circular reference detected: B -> A')

        dependency_resolver = DependencyResolver(raise_errors=False)
        r = dependency_resolver.resolve(tree)
        self.assertEqual(r[0], ['A', 'B'])
        self.assertEqual(r[1], ['B'])

    def test_wrong_node_type(self):
        dependency_resolver = DependencyResolver()
        with self.assertRaises(Exception) as e:
            dependency_resolver.resolve(None)
        self.assertEqual(str(e.exception), '`node` me be a dict.')


    def test_maximum_recursion(self):
        n = 10 ** 4
        sys.setrecursionlimit(int(10000))

        tree = {}
        for i in range(1, n):
            tree[str(i)] = (str(i+1),)
        tree[str(n)] = ()

        dependency_resolver = DependencyResolver()
        with self.assertRaises(Exception) as e:
            dependency_resolver.resolve(tree)
        self.assertEqual(str(e.exception), 'You have to increase your `recursionlimit`(current: 10000): import sys; sys.setrecursionlimit(10100)')
