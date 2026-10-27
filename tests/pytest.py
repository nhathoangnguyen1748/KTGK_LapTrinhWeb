"""
Fallback pytest module shim for environments without pytest installed.
"""
class _PytestRaisesContext:
    def __init__(self, expected_exc):
        self.expected_exc = expected_exc
        self.value = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            raise AssertionError(f"Expected exception {self.expected_exc}, but none was raised.")
        self.value = exc_val
        return issubclass(exc_type, self.expected_exc)

    def __str__(self):
        return str(self.value)


def raises(expected_exc):
    return _PytestRaisesContext(expected_exc)


class _PytestMark:
    def __getattr__(self, name):
        return lambda *args, **kwargs: (lambda f: f)

    def __call__(self, *args, **kwargs):
        return lambda f: f


mark = _PytestMark()


def fixture(*args, **kwargs):
    return lambda f: f


def approx(expected, rel=None, abs=None):
    return expected


def fail(msg=""):
    raise AssertionError(msg)


def skip(msg=""):
    import unittest
    raise unittest.SkipTest(msg)
