using System.Diagnostics;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using NguyenHoangNhat_1549_KiemTra.Data;
using NguyenHoangNhat_1549_KiemTra.Models;
using NguyenHoangNhat_1549_KiemTra.ViewModels;

namespace NguyenHoangNhat_1549_KiemTra.Controllers
{
    public class HomeController : Controller
    {
        private const int PageSize = 5;
        private readonly ApplicationDbContext _context;
        private readonly UserManager<IdentityUser> _userManager;

        public HomeController(ApplicationDbContext context, UserManager<IdentityUser> userManager)
        {
            _context = context;
            _userManager = userManager;
        }

        public async Task<IActionResult> Index(string? search, int page = 1)
        {
            return View(await BuildCourseListAsync(search, page));
        }

        [HttpGet("/courses")]
        public async Task<IActionResult> Courses(string? search, int page = 1)
        {
            return View("Index", await BuildCourseListAsync(search, page));
        }

        public IActionResult Privacy()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }

        private async Task<CourseListViewModel> BuildCourseListAsync(string? search, int page)
        {
            var query = _context.Courses
                .Include(c => c.Category)
                .AsNoTracking();

            if (!string.IsNullOrWhiteSpace(search))
            {
                query = query.Where(c => c.Name.Contains(search));
            }

            var totalItems = await query.CountAsync();
            var totalPages = Math.Max(1, (int)Math.Ceiling(totalItems / (double)PageSize));
            page = Math.Clamp(page, 1, totalPages);

            var courses = await query
                .OrderBy(c => c.Name)
                .Skip((page - 1) * PageSize)
                .Take(PageSize)
                .ToListAsync();

            var enrolledCourseIds = new HashSet<int>();

            if (User.Identity?.IsAuthenticated == true && User.IsInRole(SeedData.StudentRole))
            {
                var userId = _userManager.GetUserId(User);

                if (!string.IsNullOrEmpty(userId))
                {
                    enrolledCourseIds = await _context.Enrollments
                        .Where(e => e.UserId == userId)
                        .Select(e => e.CourseId)
                        .ToHashSetAsync();
                }
            }

            return new CourseListViewModel
            {
                Courses = courses,
                Search = search,
                CurrentPage = page,
                TotalPages = totalPages,
                EnrolledCourseIds = enrolledCourseIds
            };
        }
    }
}
