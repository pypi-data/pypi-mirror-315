class CircularReferenceException(Exception):
    def __init__(self, n, e):
        self.node = n
        self.edge = e
        message = 'Circular reference detected: %s -> %s' % (n, e)
        super().__init__(message)


class MissingReferenceException(Exception):
    def __init__(self, n):
        self.node = n
        message = 'Missing reference detected: %s' % (n)
        super().__init__(message)

class RecursionLimitException(Exception):
    def __init__(self, n, recommended_recursion_limit, current_recursion_limit):
        self.node = n
        message = 'You have to increase your `recursionlimit`(current: %s): import sys; sys.setrecursionlimit(%s)' % (
            current_recursion_limit,
            int(recommended_recursion_limit)
        )
        super().__init__(message)