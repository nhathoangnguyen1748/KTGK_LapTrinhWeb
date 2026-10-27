using System;
using System.Globalization;
using System.Text;
using System.Text.RegularExpressions;

namespace KTGK_LapTrinhWeb.Models
{
    public static class StringHelper
    {
        /// <summary>
        /// Định dạng số tiền thành chuỗi tiền tệ Việt Nam Đồng (VND).
        /// Ví dụ: 100000 -> "100.000 ₫"
        /// </summary>
        /// <param name="amount">Số tiền cần định dạng.</param>
        /// <returns>Chuỗi tiền tệ đã định dạng kèm ký hiệu ₫.</returns>
        public static string FormatCurrencyVnd(decimal amount)
        {
            var culture = new CultureInfo("vi-VN");
            return $"{amount.ToString("#,##0", culture)} ₫";
        }

        /// <summary>
        /// Rút gọn chuỗi văn bản theo độ dài tối đa và gắn kèm dấu ba chấm "...".
        /// Trả về string.Empty nếu chuỗi null, rỗng hoặc maxLength <= 0.
        /// </summary>
        /// <param name="text">Chuỗi văn bản cần rút gọn.</param>
        /// <param name="maxLength">Độ dài tối đa của chuỗi.</param>
        /// <returns>Chuỗi đã rút gọn hoặc chuỗi ban đầu nếu ngắn hơn maxLength.</returns>
        public static string Truncate(string text, int maxLength)
        {
            if (string.IsNullOrEmpty(text) || maxLength <= 0)
            {
                return string.Empty;
            }

            if (text.Length <= maxLength)
            {
                return text;
            }

            return text.Substring(0, maxLength) + "...";
        }

        /// <summary>
        /// Chuyển đổi chuỗi văn bản thành slug URL-friendly.
        /// Trả về string.Empty nếu đầu vào là null, rỗng hoặc chỉ chứa khoảng trắng.
        /// </summary>
        /// <param name="text">Chuỗi văn bản cần chuyển đổi.</param>
        /// <returns>Chuỗi slug chuẩn hóa hoặc string.Empty.</returns>
        public static string Slugify(string text)
        {
            // Guard clause: xử lý null, rỗng hoặc chuỗi chỉ chứa khoảng trắng
            if (string.IsNullOrWhiteSpace(text))
            {
                return string.Empty;
            }

            // Chuyển sang chữ thường
            string str = text.ToLowerInvariant();

            // Tách dấu tiếng Việt bằng Unicode FormD
            string normalized = str.Normalize(NormalizationForm.FormD);
            StringBuilder sb = new StringBuilder();

            foreach (char c in normalized)
            {
                UnicodeCategory uc = CharUnicodeInfo.GetUnicodeCategory(c);
                if (uc != UnicodeCategory.NonSpacingMark)
                {
                    sb.Append(c);
                }
            }

            string result = sb.ToString().Normalize(NormalizationForm.FormC);

            // Thay thế ký tự đặc thù tiếng Việt đ/Đ
            result = Regex.Replace(result, "[đĐ]", "d");

            // Loại bỏ các ký tự không phải chữ cái thường, số, khoảng trắng hoặc dấu gạch ngang
            result = Regex.Replace(result, @"[^a-z0-9\s-]", "");

            // Thay thế khoảng trắng bằng dấu gạch ngang
            result = Regex.Replace(result, @"\s+", "-");

            // Loại bỏ các ký tự gạch ngang liên tiếp '--' thành '-'
            result = Regex.Replace(result, @"-+", "-");

            // Xóa gạch ngang ở đầu và cuối chuỗi
            return result.Trim('-');
        }
    }
}
