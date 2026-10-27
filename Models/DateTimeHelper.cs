using System;
using System.Globalization;

namespace KTGK_LapTrinhWeb.Models
{
    /// <summary>
    /// Helper class providing Vietnamese relative time and datetime formatting methods.
    /// </summary>
    public static class DateTimeHelper
    {
        /// <summary>
        /// Calculates relative time distance in Vietnamese compared to the current time (DateTime.Now).
        /// - Under 1 minute: "Vừa xong"
        /// - Under 60 minutes: "X phút trước"
        /// - Under 24 hours: "X giờ trước"
        /// - Under 30 days: "X ngày trước"
        /// - Otherwise: "dd/MM/yyyy"
        /// </summary>
        /// <param name="dt">Target datetime</param>
        /// <returns>Vietnamese relative time string</returns>
        public static string ToRelativeTimeVietnamese(DateTime dt)
        {
            return ToRelativeTimeVietnamese(dt, DateTime.Now);
        }

        /// <summary>
        /// Calculates relative time distance in Vietnamese compared to a specified reference time.
        /// </summary>
        /// <param name="dt">Target datetime</param>
        /// <param name="now">Reference datetime</param>
        /// <returns>Vietnamese relative time string</returns>
        public static string ToRelativeTimeVietnamese(DateTime dt, DateTime now)
        {
            TimeSpan span = now - dt;

            if (span.TotalSeconds < 60)
            {
                return "Vừa xong";
            }

            if (span.TotalMinutes < 60)
            {
                int minutes = (int)span.TotalMinutes;
                return $"{minutes} phút trước";
            }

            if (span.TotalHours < 24)
            {
                int hours = (int)span.TotalHours;
                return $"{hours} giờ trước";
            }

            if (span.TotalDays < 30)
            {
                int days = (int)span.TotalDays;
                return $"{days} ngày trước";
            }

            return dt.ToString("dd/MM/yyyy", CultureInfo.InvariantCulture);
        }

        /// <summary>
        /// Formats date to standard Vietnamese format "dd/MM/yyyy HH:mm".
        /// </summary>
        /// <param name="dt">Target datetime</param>
        /// <returns>Formatted datetime string</returns>
        public static string FormatVietnameseDate(DateTime dt)
        {
            return dt.ToString("dd/MM/yyyy HH:mm", CultureInfo.InvariantCulture);
        }
    }
}
