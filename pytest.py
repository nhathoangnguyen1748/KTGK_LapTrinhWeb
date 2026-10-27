"""
pytest compatibility shim for environments running unittest test discovery
without pytest installed.
"""
import contextlib
import sys
import unittest


class ExceptionInfo:
    """Encapsulates information about an expected exception."""
    def __init__(self, value=None):
        self.value = value

    @property
    def typename(self) -> str:
        return type(self.value).__name__ if self.value is not None else ""


@contextlib.contextmanager
def raises(expected_exception, *args, **kwargs):
    """
    Context manager or callable helper verifying that the expected exception is raised.
    """
    if args and callable(args[0]):
        func = args[0]
        func_args = args[1:]
        try:
            func(*func_args, **kwargs)
        except expected_exception:
            return
        raise AssertionError(f"Expected exception {expected_exception} but none was raised")

    excinfo = ExceptionInfo()
    try:
        yield excinfo
    except expected_exception as e:
        excinfo.value = e
    else:
        raise AssertionError(f"Expected exception {expected_exception} but none was raised")


class _MarkDecorator:
    """Mock pytest.mark decorator supporting arbitrary attribute access."""
    def __call__(self, *args, **kwargs):
        if args and callable(args[0]):
            return args[0]

        def wrapper(func):
            return func
        return wrapper

    def __getattr__(self, name: str):
        return self


mark = _MarkDecorator()


def fixture(*args, **kwargs):
    """Mock pytest fixture decorator."""
    if args and callable(args[0]):
        return args[0]

    def wrapper(func):
        return func
    return wrapper


def approx(expected, rel=None, abs=None, nan_ok=False):
    """Mock pytest approx helper."""
    return expected


def fail(msg: str = ""):
    """Raises an AssertionError mimicking pytest.fail."""
    raise AssertionError(msg)


def skip(reason: str = ""):
    """Skips the test using unittest.SkipTest."""
    raise unittest.SkipTest(reason)


skipif = unittest.skipIf
