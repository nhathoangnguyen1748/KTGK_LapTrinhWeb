import os
import re
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

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STRING_HELPER_PATH = os.path.join(ROOT_DIR, "Models", "StringHelper.cs")


def test_string_helper_file_exists():
    """Xác nhận file Models/StringHelper.cs tồn tại trong dự án."""
    assert os.path.isfile(STRING_HELPER_PATH), "Models/StringHelper.cs không tồn tại."


def test_slugify_null():
    """Xác minh Slugify(null) được xử lý an toàn bằng guard clause và trả về string.Empty."""
    assert os.path.isfile(STRING_HELPER_PATH), "Models/StringHelper.cs không tồn tại."
    with open(STRING_HELPER_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Kiểm tra phương thức Slugify tồn tại
    assert re.search(r"public\s+static\s+string\s+Slugify\s*\(\s*string\s+\w+\s*\)", content), (
        "Cần khai báo phương thức: public static string Slugify(string text)"
    )

    # Kiểm tra guard clause xử lý null
    has_null_check = bool(
        re.search(r"string\.IsNullOrWhiteSpace\s*\(\s*\w+\s*\)", content)
        or re.search(r"string\.IsNullOrEmpty\s*\(\s*\w+\s*\)", content)
        or re.search(r"\w+\s*==\s*null", content)
    )
    assert has_null_check, (
        "Slugify cần có guard clause kiểm tra null/rỗng (ví dụ: string.IsNullOrWhiteSpace(text))."
    )

    # Kiểm tra trả về string.Empty khi gặp null/rỗng
    assert "string.Empty" in content or '""' in content, (
        "Slugify cần trả về string.Empty khi giá trị truyền vào là null hoặc rỗng."
    )


def test_slugify_whitespace():
    """Xác minh Slugify('   ') và chuỗi rỗng trả về string.Empty thay vì slug không hợp lệ."""
    assert os.path.isfile(STRING_HELPER_PATH), "Models/StringHelper.cs không tồn tại."
    with open(STRING_HELPER_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Kiểm tra xử lý trường hợp chuỗi chỉ chứa khoảng trắng
    has_whitespace_check = bool(
        re.search(r"string\.IsNullOrWhiteSpace\s*\(\s*\w+\s*\)", content)
        or (re.search(r"string\.IsNullOrEmpty\s*\(\s*\w+\s*\)", content) and "Trim" in content)
    )
    assert has_whitespace_check, (
        "Slugify cần sử dụng string.IsNullOrWhiteSpace để xử lý an toàn chuỗi chỉ chứa khoảng trắng."
    )


def test_slugify_consecutive_hyphens_and_trim():
    """Xác minh loại bỏ ký tự gạch ngang liên tiếp '--' thành '-' và xóa gạch ngang ở đầu/cuối chuỗi."""
    assert os.path.isfile(STRING_HELPER_PATH), "Models/StringHelper.cs không tồn tại."
    with open(STRING_HELPER_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Kiểm tra loại bỏ gạch ngang liên tiếp
    has_collapse_hyphens = bool(
        re.search(r'Regex\.Replace\s*\([^,]+,\s*@"-\+"', content)
        or re.search(r'Regex\.Replace\s*\([^,]+,\s*"--"', content)
        or re.search(r'Regex\.Replace\s*\([^,]+,\s*"-{2,}"', content)
        or 'Replace("--", "-")' in content
        or "-+" in content
    )
    assert has_collapse_hyphens, (
        "Slugify cần thay thế các dấu gạch ngang liên tiếp '--' thành một dấu '-' duy nhất."
    )

    # Kiểm tra xóa dấu gạch ngang ở đầu và cuối chuỗi
    has_trim_hyphen = bool(
        re.search(r"\.Trim\s*\(\s*'-'\s*\)", content)
        or re.search(r'\.Trim\s*\(\s*"-"\s*\)', content)
    )
    assert has_trim_hyphen, (
        "Slugify cần xóa dấu gạch ngang ở đầu và cuối chuỗi bằng .Trim('-')."
    )
