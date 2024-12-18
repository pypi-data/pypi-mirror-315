import sys

from python_dependency_resolver.exceptions import CircularReferenceException, \
    MissingReferenceException, \
    RecursionLimitException


VERSION = (1, 0, 4)

def get_version():
    return ".".join(map(str, VERSION))


__version__ = get_version()


class DependencyResolver:
    RATE_RECURSION_LIMIT = 1.01
    """
        For the recursion limit, we're applying an arbitrary safe rate.
    """

    def __init__(self, **kwargs):
        """
            :param raise_errors: This class raises an exception if it meets an :class:`~python_dependency_resolver.exceptions.CircularReferenceException`  or an :class:`~python_dependency_resolver.exceptions.MissingReferenceException`. You can disable it.
            :type raise_errors: bool, default True
        """
        self.raise_errors = kwargs.get('raise_errors', True)


    def resolve(self, node, resolved=None, unresolved=None):
        """
            :param node: A dict containing your dependencies tree
            :type node: dict

            :exception: :class:`~Exception`
        """

        if not isinstance(node, dict):
            raise Exception('`node` me be a dict.')

        recommended_recursion_limit = len(node.keys()) * self.RATE_RECURSION_LIMIT
        if recommended_recursion_limit > sys.getrecursionlimit():
            raise RecursionLimitException(node, recommended_recursion_limit, sys.getrecursionlimit())

        if resolved is None:
            resolved = []

        if unresolved is None:
            unresolved = []

        for n in node.keys():
            self.__resolver(n, node, resolved, unresolved)
        return [resolved, unresolved]

    def __resolver(self, n, node, resolved=None, unresolved=None):
        unresolved.append(n)

        if n not in node.keys():
            if self.raise_errors:
                raise MissingReferenceException(n)
            return

        for e in node[n]:
            if e not in resolved:
                if e in unresolved:
                    if self.raise_errors:
                        raise CircularReferenceException(n, e)
                    # avoid infinite loop
                    return
                self.__resolver(e, node, resolved, unresolved)

        if n not in resolved:
            resolved.append(n)
        unresolved.remove(n)
