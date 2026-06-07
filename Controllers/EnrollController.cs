using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using NguyenHoangNhat_1549_KiemTra.Data;
using NguyenHoangNhat_1549_KiemTra.Models;

namespace NguyenHoangNhat_1549_KiemTra.Controllers;

[Authorize(Roles = "STUDENT")]
[Route("enroll")]
public class EnrollController : Controller
{
    private readonly ApplicationDbContext _context;
    private readonly UserManager<IdentityUser> _userManager;

    public EnrollController(ApplicationDbContext context, UserManager<IdentityUser> userManager)
    {
        _context = context;
        _userManager = userManager;
    }

    [HttpPost("{courseId:int}")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(int courseId)
    {
        var userId = _userManager.GetUserId(User);

        if (string.IsNullOrEmpty(userId))
        {
            return Challenge();
        }

        var courseExists = await _context.Courses.AnyAsync(c => c.Id == courseId);
        var alreadyEnrolled = await _context.Enrollments.AnyAsync(e => e.UserId == userId && e.CourseId == courseId);

        if (courseExists && !alreadyEnrolled)
        {
            _context.Enrollments.Add(new Enrollment
            {
                UserId = userId,
                CourseId = courseId,
                EnrollDate = DateTime.Now
            });

            await _context.SaveChangesAsync();
        }

        await UpdateEnrollmentSessionCountAsync(userId);

        return RedirectToAction("Index", "Home");
    }

    [HttpPost("cancel/{courseId:int}")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Cancel(int courseId)
    {
        var userId = _userManager.GetUserId(User);

        if (string.IsNullOrEmpty(userId))
        {
            return Challenge();
        }

        var enrollment = await _context.Enrollments
            .FirstOrDefaultAsync(e => e.UserId == userId && e.CourseId == courseId);

        if (enrollment is not null)
        {
            _context.Enrollments.Remove(enrollment);
            await _context.SaveChangesAsync();
        }

        await UpdateEnrollmentSessionCountAsync(userId);

        return RedirectToAction("Index", "Home");
    }

    [HttpGet("my-courses")]
    public async Task<IActionResult> MyCourses()
    {
        var userId = _userManager.GetUserId(User);

        if (string.IsNullOrEmpty(userId))
        {
            return Challenge();
        }

        var enrollments = await _context.Enrollments
            .Include(e => e.Course)
            .ThenInclude(c => c!.Category)
            .Where(e => e.UserId == userId)
            .OrderByDescending(e => e.EnrollDate)
            .AsNoTracking()
            .ToListAsync();

        return View(enrollments);
    }

    private async Task UpdateEnrollmentSessionCountAsync(string userId)
    {
        var enrolledCourseCount = await _context.Enrollments
            .CountAsync(enrollment => enrollment.UserId == userId);

        HttpContext.Session.SetInt32(SessionKeys.EnrolledCourseCount, enrolledCourseCount);
    }
}
