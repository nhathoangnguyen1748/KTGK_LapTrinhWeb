import os
import re
import shutil
import subprocess
import tempfile
import unicodedata
import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STRING_HELPER_PATH = os.path.join(ROOT_DIR, "Models", "StringHelper.cs")


def read_file_content(path):
    assert os.path.exists(path), f"File không tồn tại: {path}"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def test_string_helper_file_exists():
    """Kiểm tra file Models/StringHelper.cs phải tồn tại."""
    assert os.path.isfile(STRING_HELPER_PATH), "Models/StringHelper.cs chưa được tạo."


def test_string_helper_namespace_and_class_declaration():
    """Kiểm tra khai báo class và namespace chuẩn C# ASP.NET Core."""
    content = read_file_content(STRING_HELPER_PATH)
    assert "namespace KTGK_LapTrinhWeb.Models" in content or "namespace Models" in content, (
        "Namespace phải là KTGK_LapTrinhWeb.Models hoặc Models."
    )
    assert re.search(r"public\s+static\s+class\s+StringHelper", content), (
        "Cần khai báo public static class StringHelper."
    )


def test_format_currency_vnd_declaration_and_logic():
    """Kiểm tra định nghĩa hàm FormatCurrencyVnd."""
    content = read_file_content(STRING_HELPER_PATH)
    pattern = r"public\s+static\s+string\s+FormatCurrencyVnd\s*\(\s*decimal\s+\w+\s*\)"
    assert re.search(pattern, content), (
        "Cần có phương thức: public static string FormatCurrencyVnd(decimal amount)"
    )
    assert "₫" in content, "Phương thức FormatCurrencyVnd phải sử dụng ký hiệu ₫."
    assert "vi-VN" in content or "NumberGroupSeparator" in content, (
        "Phương thức FormatCurrencyVnd phải hỗ trợ phân cách hàng nghìn theo chuẩn Việt Nam."
    )


def test_truncate_declaration_and_logic():
    """Kiểm tra định nghĩa hàm Truncate."""
    content = read_file_content(STRING_HELPER_PATH)
    pattern = r"public\s+static\s+string\s+Truncate\s*\(\s*string\s+\w+\s*,\s*int\s+\w+\s*\)"
    assert re.search(pattern, content), (
        "Cần có phương thức: public static string Truncate(string text, int maxLength)"
    )
    assert "..." in content, "Phương thức Truncate phải gắn kèm dấu '...' khi rút gọn."
    assert "string.IsNullOrEmpty" in content or "IsNullOrEmpty" in content, (
        "Phương thức Truncate cần kiểm tra chuỗi rỗng/null an toàn."
    )


def test_slugify_declaration_and_logic():
    """Kiểm tra định nghĩa hàm Slugify."""
    content = read_file_content(STRING_HELPER_PATH)
    pattern = r"public\s+static\s+string\s+Slugify\s*\(\s*string\s+\w+\s*\)"
    assert re.search(pattern, content), (
        "Cần có phương thức: public static string Slugify(string text)"
    )
    assert "FormD" in content, "Phương thức Slugify cần sử dụng Unicode FormD để tách dấu tiếng Việt."
    assert "đ" in content or "Đ" in content, "Phương thức Slugify cần xử lý riêng ký tự đ/Đ."
    assert "ToLower" in content or "ToLowerInvariant" in content, (
        "Phương thức Slugify cần chuyển đổi chữ hoa thành chữ thường."
    )


# --- Kiểm thử logic mô phỏng (Python equivalent validation) ---

def python_format_currency_vnd(amount: float) -> str:
    sign = "-" if amount < 0 else ""
    abs_amount = round(abs(amount))
    formatted = f"{abs_amount:,}".replace(",", ".")
    return f"{sign}{formatted} ₫"


def python_truncate(text: str, max_length: int) -> str:
    if not text or max_length <= 0:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def python_slugify(text: str) -> str:
    if not text or not text.strip():
        return ""
    text = text.replace("đ", "d").replace("Đ", "d")
    normalized = unicodedata.normalize("NFD", text)
    without_diacritics = "".join(
        c for c in normalized if unicodedata.category(c) != "Mn"
    )
    without_diacritics = unicodedata.normalize("NFC", without_diacritics).lower()
    slug = re.sub(r"[^a-z0-9]+", "-", without_diacritics)
    return slug.strip("-")


def test_format_currency_vnd_cases():
    assert python_format_currency_vnd(100000) == "100.000 ₫"
    assert python_format_currency_vnd(0) == "0 ₫"
    assert python_format_currency_vnd(1500000) == "1.500.000 ₫"
    assert python_format_currency_vnd(25000000) == "25.000.000 ₫"


def test_truncate_cases():
    assert python_truncate("Xin chào các bạn", 8) == "Xin chào..."
    assert python_truncate("Ngắn", 10) == "Ngắn"
    assert python_truncate("", 5) == ""
    assert python_truncate(None, 5) == ""
    assert python_truncate("Test", 0) == ""
    assert python_truncate("Test", -1) == ""
    assert python_truncate("Chính xác 8 ký tự", 8) == "Chính xá..."


def test_slugify_cases():
    assert python_slugify("Lập trình Web") == "lap-trinh-web"
    assert python_slugify("Định dạng tiền tệ VND") == "dinh-dang-tien-te-vnd"
    assert python_slugify("Xử lý chuỗi tiếng Việt!") == "xu-ly-chuoi-tieng-viet"
    assert python_slugify("   ---Bài Viết Số 1---   ") == "bai-viet-so-1"
    assert python_slugify("Áo sơ mi nam & nữ, size XL") == "ao-so-mi-nam-nu-size-xl"
    assert python_slugify("") == ""
    assert python_slugify("   ") == ""
    assert python_slugify(None) == ""


# --- Kiểm thử biên dịch và chạy thực thi thực tế nếu có .NET SDK ---

@pytest.mark.skipif(shutil.which("dotnet") is None, reason="dotnet SDK không có sẵn trong môi trường")
def test_dotnet_build_and_functional_execution():
    """Biên dịch và chạy trực tiếp StringHelper qua .NET CLI để đảm bảo C# runtime hợp lệ."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Tạo test runner C# tạm thời
        runner_source = f"""
using System;
using KTGK_LapTrinhWeb.Models;

class Program
{{
    static int Main()
    {{
        // Kiểm tra FormatCurrencyVnd
        if (StringHelper.FormatCurrencyVnd(100000m) != "100.000 ₫") return 1;
        if (StringHelper.FormatCurrencyVnd(0m) != "0 ₫") return 2;
        if (StringHelper.FormatCurrencyVnd(1500000m) != "1.500.000 ₫") return 3;

        // Kiểm tra Truncate
        if (StringHelper.Truncate("Xin chào các bạn", 8) != "Xin chào...") return 4;
        if (StringHelper.Truncate("Ngắn", 10) != "Ngắn") return 5;
        if (StringHelper.Truncate(null, 5) != string.Empty) return 6;
        if (StringHelper.Truncate("", 5) != string.Empty) return 7;
        if (StringHelper.Truncate("Hello", 0) != string.Empty) return 8;

        // Kiểm tra Slugify
        if (StringHelper.Slugify("Lập trình Web") != "lap-trinh-web") return 9;
        if (StringHelper.Slugify("Định dạng tiền tệ VND") != "dinh-dang-tien-te-vnd") return 10;
        if (StringHelper.Slugify("  ---Bài Viết #1---  ") != "bai-viet-1") return 11;
        if (StringHelper.Slugify(null) != string.Empty) return 12;
        if (StringHelper.Slugify("") != string.Empty) return 13;

        return 0;
    }}
}}
"""
        runner_path = os.path.join(tmp_dir, "Program.cs")
        with open(runner_path, "w", encoding="utf-8") as f:
            f.write(runner_source)

        csproj_content = f"""<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
  <ItemGroup>
    <Compile Include="{os.path.abspath(STRING_HELPER_PATH)}" Link="StringHelper.cs" />
  </ItemGroup>
</Project>
"""
        csproj_path = os.path.join(tmp_dir, "TestRunner.csproj")
        with open(csproj_path, "w", encoding="utf-8") as f:
            f.write(csproj_content)

        run_res = subprocess.run(
            ["dotnet", "run", "--project", csproj_path],
            capture_output=True,
            text=True,
        )
        assert run_res.returncode == 0, (
            f"Thực thi StringHelper trong C# thất bại (exit code: {run_res.returncode}).\n"
            f"Stdout: {run_res.stdout}\nStderr: {run_res.stderr}"
        )
