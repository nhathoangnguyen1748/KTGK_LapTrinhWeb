using System;
using System.Globalization;
using System.Text;
using System.Text.RegularExpressions;

namespace KTGK_LapTrinhWeb.Models
{
    /// <summary>
    /// Tiện ích xử lý chuỗi và định dạng dữ liệu cho ứng dụng.
    /// </summary>
    public static class StringHelper
    {
        /// <summary>
        /// Định dạng tiền tệ Việt Nam (ví dụ 100000 -> "100.000 ₫").
        /// </summary>
        /// <param name="amount">Số tiền cần định dạng.</param>
        /// <returns>Chuỗi định dạng tiền tệ VND kèm ký hiệu ₫.</returns>
        public static string FormatCurrencyVnd(decimal amount)
        {
            var culture = new CultureInfo("vi-VN");
            var nfi = (NumberFormatInfo)culture.NumberFormat.Clone();
            nfi.NumberGroupSeparator = ".";
            nfi.CurrencyGroupSeparator = ".";
            nfi.CurrencySymbol = "₫";
            return $"{amount.ToString("#,##0", nfi)} ₫";
        }

        /// <summary>
        /// Rút gọn chuỗi an toàn nếu vượt quá maxLength, kèm dấu "...".
        /// </summary>
        /// <param name="text">Chuỗi văn bản cần rút gọn.</param>
        /// <param name="maxLength">Số lượng ký tự tối đa giữ lại.</param>
        /// <returns>Chuỗi đã rút gọn kèm "..." hoặc chuỗi ban đầu nếu không vượt quá maxLength.</returns>
        public static string Truncate(string text, int maxLength)
        {
            if (string.IsNullOrEmpty(text))
            {
                return string.Empty;
            }

            if (maxLength <= 0)
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
        /// Chuyển đổi tiêu đề tiếng Việt có dấu thành slug URL không dấu dạng kebab-case.
        /// </summary>
        /// <param name="text">Chuỗi tiêu đề tiếng Việt cần chuyển đổi.</param>
        /// <returns>Chuỗi slug không dấu dạng kebab-case.</returns>
        public static string Slugify(string text)
        {
            if (string.IsNullOrWhiteSpace(text))
            {
                return string.Empty;
            }

            // Xử lý riêng ký tự đ/Đ do Unicode FormD không tách dấu gạch ngang của chữ đ
            string slug = text.Replace('đ', 'd').Replace('Đ', 'd');

            // Chuẩn hóa FormD để tách dấu thanh/dấu phụ ra khỏi nguyên âm
            string normalizedString = slug.Normalize(NormalizationForm.FormD);
            var stringBuilder = new StringBuilder();

            foreach (char c in normalizedString)
            {
                var unicodeCategory = CharUnicodeInfo.GetUnicodeCategory(c);
                if (unicodeCategory != UnicodeCategory.NonSpacingMark)
                {
                    stringBuilder.Append(c);
                }
            }

            // Tái hợp chuỗi về FormC và chuyển thành chữ thường
            string cleanString = stringBuilder.ToString().Normalize(NormalizationForm.FormC).ToLowerInvariant();

            // Thay thế tất cả ký tự không phải chữ cái và số bằng dấu gạch ngang
            cleanString = Regex.Replace(cleanString, @"[^a-z0-9]+", "-");

            // Xóa các dấu gạch ngang thừa ở đầu và cuối chuỗi
            return cleanString.Trim('-');
        }
    }
}
