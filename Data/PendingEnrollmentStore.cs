using Microsoft.AspNetCore.Http;

namespace NguyenHoangNhat_1549_KiemTra.Data;

public static class PendingEnrollmentStore
{
    public static HashSet<int> GetPendingCourseIds(HttpContext context)
    {
        var value = context.Session.GetString(SessionKeys.PendingCourseIds);

        if (string.IsNullOrWhiteSpace(value))
        {
            value = context.Request.Cookies[SessionKeys.PendingCourseCookie];

            if (!string.IsNullOrWhiteSpace(value))
            {
                context.Session.SetString(SessionKeys.PendingCourseIds, value);
            }
        }

        return ParseCourseIds(value);
    }

    public static void SavePendingCourseIds(HttpContext context, IEnumerable<int> courseIds)
    {
        var ids = courseIds
            .Where(id => id > 0)
            .Distinct()
            .OrderBy(id => id)
            .ToList();

        if (ids.Count == 0)
        {
            Clear(context);
            return;
        }

        var value = string.Join(",", ids);
        context.Session.SetString(SessionKeys.PendingCourseIds, value);
        context.Response.Cookies.Append(
            SessionKeys.PendingCourseCookie,
            value,
            new CookieOptions
            {
                HttpOnly = true,
                IsEssential = true,
                SameSite = SameSiteMode.Lax,
                Expires = DateTimeOffset.Now.AddDays(7)
            });
    }

    public static void Clear(HttpContext context)
    {
        context.Session.Remove(SessionKeys.PendingCourseIds);
        context.Response.Cookies.Delete(SessionKeys.PendingCourseCookie);
    }

    private static HashSet<int> ParseCourseIds(string? value)
    {
        if (string.IsNullOrWhiteSpace(value))
        {
            return [];
        }

        return value
            .Split(',', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)
            .Select(item => int.TryParse(item, out var id) ? id : 0)
            .Where(id => id > 0)
            .ToHashSet();
    }
}
