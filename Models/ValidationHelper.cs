using System;
using System.Text.RegularExpressions;

namespace KTGK_LapTrinhWeb.Models
{
    /// <summary>
    /// Helper tiện ích cung cấp các phương thức xác thực dữ liệu cho ViewModels và Models.
    /// </summary>
    public static class ValidationHelper
    {
        private static readonly Regex EmailRegex = new Regex(
            @"^[a-zA-Z0-9._%+-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$",
            RegexOptions.Compiled | RegexOptions.IgnoreCase);

        private static readonly Regex PhoneRegex = new Regex(
            @"^(?:0|\+84)(?:3|5|7|8|9)\d{8}$",
            RegexOptions.Compiled);

        /// <summary>
        /// Kiểm tra tính hợp lệ của định dạng email.
        /// </summary>
        /// <param name="email">Chuỗi email cần kiểm tra.</param>
        /// <returns>True nếu email đúng định dạng; ngược lại là False.</returns>
        public static bool IsValidEmail(string email)
        {
            if (string.IsNullOrWhiteSpace(email))
            {
                return false;
            }

            return EmailRegex.IsMatch(email.Trim());
        }

        /// <summary>
        /// Kiểm tra tính hợp lệ của số điện thoại (hỗ trợ đầu số Việt Nam 0x và +84x).
        /// </summary>
        /// <param name="phoneNumber">Chuỗi số điện thoại cần kiểm tra.</param>
        /// <returns>True nếu số điện thoại hợp lệ; ngược lại là False.</returns>
        public static bool IsValidPhoneNumber(string phoneNumber)
        {
            if (string.IsNullOrWhiteSpace(phoneNumber))
            {
                return false;
            }

            // Loại bỏ khoảng trắng, dấu gạch nối và dấu chấm trước khi kiểm tra
            string sanitized = Regex.Replace(phoneNumber.Trim(), @"[\s.-]", "");

            return PhoneRegex.IsMatch(sanitized);
        }
    }
}
