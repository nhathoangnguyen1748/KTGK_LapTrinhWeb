import os
import re
import unittest

class TestValidationHelperFeature(unittest.TestCase):
    def setUp(self):
        self.helper_path = os.path.join("Models", "ValidationHelper.cs")
        self.email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$")
        self.phone_pattern = re.compile(r"^(?:0|\+84)(?:3|5|7|8|9)\d{8}$")

    def test_file_exists(self):
        """Kiểm tra file ValidationHelper.cs tồn tại trong thư mục Models."""
        self.assertTrue(os.path.exists(self.helper_path), f"File {self.helper_path} không tồn tại.")

    def test_file_contains_required_methods(self):
        """Kiểm tra ValidationHelper.cs định nghĩa đầy đủ các phương thức tiện ích."""
        with open(self.helper_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("class ValidationHelper", content)
        self.assertIn("IsValidEmail", content)
        self.assertIn("IsValidPhoneNumber", content)

    def test_email_validation_valid(self):
        """Kiểm tra các định dạng email hợp lệ."""
        valid_emails = [
            "student@hutech.edu.vn",
            "nhubcode@gmail.com",
            "user.name+tag@sub.example.com",
            "contact_123@domain.org",
        ]
        for email in valid_emails:
            self.assertTrue(bool(self.email_pattern.match(email)), f"Email {email} phải hợp lệ.")

    def test_email_validation_invalid(self):
        """Kiểm tra các định dạng email không hợp lệ."""
        invalid_emails = [
            "",
            "   ",
            "plainaddress",
            "@missingusername.com",
            "username@.com",
            "username@domain",
            "user@domain..com",
        ]
        for email in invalid_emails:
            self.assertFalse(bool(self.email_pattern.match(email.strip())), f"Email {email} không được hợp lệ.")

    def test_phone_validation_valid(self):
        """Kiểm tra các số điện thoại hợp lệ (đầu số 03, 05, 07, 08, 09 và +84)."""
        valid_phones = [
            "0912345678",
            "0389998888",
            "0771234567",
            "0855566677",
            "0561234567",
            "+84912345678",
            "+84389998888",
            "0912-345-678",
            "0912.345.678",
        ]
        for phone in valid_phones:
            cleaned = re.sub(r"[\s.-]", "", phone.strip())
            self.assertTrue(bool(self.phone_pattern.match(cleaned)), f"Số điện thoại {phone} phải hợp lệ.")

    def test_phone_validation_invalid(self):
        """Kiểm tra các số điện thoại không hợp lệ."""
        invalid_phones = [
            "",
            "   ",
            "0123456789",    # Đầu 01 không còn hợp lệ tại VN
            "091234567",     # 9 số (thiếu số)
            "09123456789",   # 11 số (thừa số)
            "abcdefghij",    # Ký tự chữ
            "0283899999",    # Số cố định
            "+1800123456",   # Mã quốc gia ngoài VN
        ]
        for phone in invalid_phones:
            cleaned = re.sub(r"[\s.-]", "", phone.strip())
            self.assertFalse(bool(self.phone_pattern.match(cleaned)), f"Số điện thoại {phone} không được hợp lệ.")

if __name__ == "__main__":
    unittest.main()
