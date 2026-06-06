using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using NguyenHoangNhat_1549_KiemTra.Data;
using NguyenHoangNhat_1549_KiemTra.ViewModels;

namespace NguyenHoangNhat_1549_KiemTra.Controllers;

[Authorize(Roles = "Admin")]
[Route("admin/dashboard")]
public class DashboardController : Controller
{
    private readonly ApplicationDbContext _context;
    private readonly UserManager<IdentityUser> _userManager;

    public DashboardController(ApplicationDbContext context, UserManager<IdentityUser> userManager)
    {
        _context = context;
        _userManager = userManager;
    }

    [HttpGet("")]
    public async Task<IActionResult> Index()
    {
        var students = await _userManager.GetUsersInRoleAsync(SeedData.StudentRole);
        var recentEnrollments = await _context.Enrollments
            .Include(e => e.Course)
            .Include(e => e.User)
            .AsNoTracking()
            .OrderByDescending(e => e.EnrollDate)
            .Take(5)
            .ToListAsync();

        var model = new DashboardViewModel
        {
            TotalCourses = await _context.Courses.CountAsync(),
            TotalCategories = await _context.Categories.CountAsync(),
            TotalStudents = students.Count,
            TotalEnrollments = await _context.Enrollments.CountAsync(),
            CoursesByCategory = await _context.Categories
                .AsNoTracking()
                .Select(category => new CategoryCourseStatViewModel
                {
                    CategoryName = category.Name,
                    CourseCount = category.Courses.Count
                })
                .OrderByDescending(category => category.CourseCount)
                .ThenBy(category => category.CategoryName)
                .ToListAsync(),
            TopCourses = await _context.Courses
                .AsNoTracking()
                .Select(course => new CourseEnrollmentStatViewModel
                {
                    CourseName = course.Name,
                    EnrollmentCount = course.Enrollments.Count
                })
                .OrderByDescending(course => course.EnrollmentCount)
                .ThenBy(course => course.CourseName)
                .Take(5)
                .ToListAsync(),
            RecentEnrollments = recentEnrollments
                .Select(enrollment => new RecentEnrollmentViewModel
                {
                    StudentName = enrollment.User?.UserName
                        ?? enrollment.User?.Email
                        ?? "Không rõ",
                    CourseName = enrollment.Course?.Name ?? "Không rõ",
                    EnrollDate = enrollment.EnrollDate
                })
                .ToList()
        };

        return View(model);
    }
}
