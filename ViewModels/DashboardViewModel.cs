namespace NguyenHoangNhat_1549_KiemTra.ViewModels;

public class DashboardViewModel
{
    public int TotalCourses { get; set; }
    public int TotalCategories { get; set; }
    public int TotalStudents { get; set; }
    public int TotalEnrollments { get; set; }

    public List<CategoryCourseStatViewModel> CoursesByCategory { get; set; } = [];
    public List<CourseEnrollmentStatViewModel> TopCourses { get; set; } = [];
    public List<RecentEnrollmentViewModel> RecentEnrollments { get; set; } = [];
}

public class CategoryCourseStatViewModel
{
    public string CategoryName { get; set; } = string.Empty;
    public int CourseCount { get; set; }
}

public class CourseEnrollmentStatViewModel
{
    public string CourseName { get; set; } = string.Empty;
    public int EnrollmentCount { get; set; }
}

public class RecentEnrollmentViewModel
{
    public string StudentName { get; set; } = string.Empty;
    public string CourseName { get; set; } = string.Empty;
    public DateTime EnrollDate { get; set; }
}
