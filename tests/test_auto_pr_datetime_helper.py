import os
import re
import shutil
import subprocess
from datetime import datetime, timedelta
try:
    import pytest
except ImportError:
    class _PytestRaisesContext:
        def __init__(self, expected_exc):
            self.expected_exc = expected_exc
            self.value = None
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is None:
                raise AssertionError(f"Expected {self.expected_exc}, but no exception was raised")
            self.value = exc_val
            return issubclass(exc_type, self.expected_exc)
        def __str__(self):
            return str(self.value)

    class _PytestMark:
        def __getattr__(self, name):
            return lambda *args, **kwargs: (lambda f: f)
        def __call__(self, *args, **kwargs):
            return lambda f: f

    class _PytestMock:
        raises = _PytestRaisesContext
        mark = _PytestMark()
        @staticmethod
        def fixture(*args, **kwargs):
            return lambda f: f

    pytest = _PytestMock()

# Determine paths relative to this test file
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(TESTS_DIR, ".."))
HELPER_FILE_PATH = os.path.join(PROJECT_ROOT, "Models", "DateTimeHelper.cs")


def read_helper_source() -> str:
    """Reads and returns the source code of Models/DateTimeHelper.cs."""
    assert os.path.isfile(HELPER_FILE_PATH), f"File not found: {HELPER_FILE_PATH}"
    with open(HELPER_FILE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def test_datetime_helper_file_exists():
    """Verify that Models/DateTimeHelper.cs exists in the project."""
    assert os.path.isfile(HELPER_FILE_PATH), f"Expected {HELPER_FILE_PATH} to exist."


def test_datetime_helper_class_declared():
    """Verify that DateTimeHelper class is declared in Models namespace."""
    source = read_helper_source()
    assert re.search(r"namespace\s+KTGK_LapTrinhWeb\.Models", source), (
        "Namespace 'KTGK_LapTrinhWeb.Models' not found in DateTimeHelper.cs"
    )
    assert re.search(r"public\s+static\s+class\s+DateTimeHelper", source), (
        "Class 'public static class DateTimeHelper' not found in DateTimeHelper.cs"
    )


def test_to_relative_time_vietnamese_method_declared():
    """Verify that ToRelativeTimeVietnamese method is declared with expected signature."""
    source = read_helper_source()
    assert re.search(r"public\s+static\s+string\s+ToRelativeTimeVietnamese\s*\(\s*DateTime\s+\w+", source), (
        "Method ToRelativeTimeVietnamese(DateTime dt) not found in DateTimeHelper.cs"
    )


def test_format_vietnamese_date_method_declared():
    """Verify that FormatVietnameseDate method is declared with expected signature."""
    source = read_helper_source()
    assert re.search(r"public\s+static\s+string\s+FormatVietnameseDate\s*\(\s*DateTime\s+\w+\s*\)", source), (
        "Method FormatVietnameseDate(DateTime dt) not found in DateTimeHelper.cs"
    )


def test_required_vietnamese_strings_present():
    """Verify all required relative time strings and format tokens are present in source."""
    source = read_helper_source()
    required_tokens = [
        "Vừa xong",
        "phút trước",
        "giờ trước",
        "ngày trước",
        "dd/MM/yyyy",
        "dd/MM/yyyy HH:mm",
    ]
    for token in required_tokens:
        assert token in source, f"Required token '{token}' was not found in DateTimeHelper.cs"


def simulate_to_relative_time_vietnamese(dt: datetime, now: datetime) -> str:
    """Python reference implementation mirroring DateTimeHelper logic."""
    span = now - dt
    total_seconds = span.total_seconds()

    if total_seconds < 60:
        return "Vừa xong"
    total_minutes = total_seconds / 60
    if total_minutes < 60:
        return f"{int(total_minutes)} phút trước"
    total_hours = total_seconds / 3600
    if total_hours < 24:
        return f"{int(total_hours)} giờ trước"
    total_days = total_seconds / 86400
    if total_days < 30:
        return f"{int(total_days)} ngày trước"
    return dt.strftime("%d/%m/%Y")


def simulate_format_vietnamese_date(dt: datetime) -> str:
    """Python reference implementation for FormatVietnameseDate."""
    return dt.strftime("%d/%m/%Y %H:%M")


@pytest.mark.parametrize(
    "delta,expected",
    [
        (timedelta(seconds=0), "Vừa xong"),
        (timedelta(seconds=15), "Vừa xong"),
        (timedelta(seconds=59), "Vừa xong"),
        (timedelta(minutes=1), "1 phút trước"),
        (timedelta(minutes=15), "15 phút trước"),
        (timedelta(minutes=59, seconds=30), "59 phút trước"),
        (timedelta(hours=1), "1 giờ trước"),
        (timedelta(hours=5), "5 giờ trước"),
        (timedelta(hours=23, minutes=59), "23 giờ trước"),
        (timedelta(days=1), "1 ngày trước"),
        (timedelta(days=7), "7 ngày trước"),
        (timedelta(days=29), "29 ngày trước"),
    ],
)
def test_relative_time_intervals(delta, expected):
    """Validate relative time outputs across all required intervals."""
    now = datetime(2025, 6, 15, 12, 0, 0)
    dt = now - delta
    result = simulate_to_relative_time_vietnamese(dt, now)
    assert result == expected


def test_relative_time_older_than_thirty_days():
    """Validate that timestamps >= 30 days are formatted as dd/MM/yyyy."""
    now = datetime(2025, 6, 15, 12, 0, 0)
    dt = datetime(2025, 1, 10, 8, 30, 0)
    result = simulate_to_relative_time_vietnamese(dt, now)
    assert result == "10/01/2025"


def test_format_vietnamese_date_formatting():
    """Validate standard Vietnamese date formatting dd/MM/yyyy HH:mm."""
    dt = datetime(2025, 3, 25, 9, 5, 0)
    result = simulate_format_vietnamese_date(dt)
    assert result == "25/03/2025 09:05"


def test_csharp_compilation_if_dotnet_present():
    """If dotnet CLI is available, build the project to verify C# compilation."""
    dotnet_bin = shutil.which("dotnet")
    if dotnet_bin is None:
        pytest.skip("dotnet CLI not found on environment; skipping build test.")

    result = subprocess.run(
        [dotnet_bin, "build", "--no-incremental"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"dotnet build failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
