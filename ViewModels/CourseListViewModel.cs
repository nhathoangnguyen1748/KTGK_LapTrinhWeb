using NguyenHoangNhat_1549_KiemTra.Models;

namespace NguyenHoangNhat_1549_KiemTra.ViewModels;

public class CourseListViewModel
{
    public IReadOnlyList<Course> Courses { get; set; } = [];
    public string? Search { get; set; }
    public int CurrentPage { get; set; }
    public int TotalPages { get; set; }
    public HashSet<int> EnrolledCourseIds { get; set; } = [];
    public HashSet<int> PendingCourseIds { get; set; } = [];
}
