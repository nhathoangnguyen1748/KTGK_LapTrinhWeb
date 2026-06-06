using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using NguyenHoangNhat_1549_KiemTra.Models;

namespace NguyenHoangNhat_1549_KiemTra.Data;

public static class SeedData
{
    public const string AdminRole = "Admin";
    public const string StudentRole = "STUDENT";

    private static readonly CourseSeed[] CourseSeeds =
    [
        new("ASP.NET Core MVC", "ASP.NET Core MVC", 3, "Nguyễn Văn A", "Lập trình"),
        new("Entity Framework Core", "Entity Framework Core", 3, "Trần Thị B", "Lập trình"),
        new("C# Cơ Bản", "C# Co Ban", 2, "Lê Văn C", "Lập trình"),
        new("Thiết Kế Cơ Sở Dữ Liệu", "Thiet Ke Database", 3, "Phạm Thị D", "Cơ sở dữ liệu"),
        new("SQL Server", "SQL Server", 3, "Hoàng Văn E", "Cơ sở dữ liệu"),
        new("Lập Trình Giao Diện Web", "Web Frontend", 3, "Đỗ Thị F", "Thiết kế"),
        new("JavaScript Nâng Cao", "JavaScript Nang Cao", 3, "Võ Văn G", "Lập trình"),
        new("RESTful API", "RESTful API", 3, "Đặng Thị H", "Lập trình"),
        new("Điện Toán Đám Mây", "Cloud Computing", 2, "Bùi Văn I", "Mạng máy tính"),
        new("An Toàn Mạng", "Network Security", 3, "Ngô Thị K", "Mạng máy tính"),
        new("Kiểm Thử Phần Mềm", "Software Testing", 2, "Vũ Văn L", "Lập trình"),
        new("Thiết Kế UI/UX", "UI/UX Design", 2, "Mai Thị M", "Thiết kế")
    ];

    public static async Task InitializeAsync(IServiceProvider services)
    {
        using var scope = services.CreateScope();
        var context = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
        var roleManager = scope.ServiceProvider.GetRequiredService<RoleManager<IdentityRole>>();
        var userManager = scope.ServiceProvider.GetRequiredService<UserManager<IdentityUser>>();

        await context.Database.EnsureCreatedAsync();
        await SeedRolesAsync(roleManager);
        await SeedUsersAsync(userManager);
        await SeedCoursesAsync(context);
    }

    private static async Task SeedRolesAsync(RoleManager<IdentityRole> roleManager)
    {
        foreach (var role in new[] { AdminRole, StudentRole })
        {
            if (!await roleManager.RoleExistsAsync(role))
            {
                await roleManager.CreateAsync(new IdentityRole(role));
            }
        }
    }

    private static async Task SeedUsersAsync(UserManager<IdentityUser> userManager)
    {
        await CreateUserAsync(userManager, "admin", "admin@example.com", "Admin@123", AdminRole);
        await CreateUserAsync(userManager, "student", "student@example.com", "Student@123", StudentRole);
    }

    private static async Task CreateUserAsync(
        UserManager<IdentityUser> userManager,
        string userName,
        string email,
        string password,
        string role)
    {
        var user = await userManager.FindByNameAsync(userName);

        if (user is null)
        {
            user = new IdentityUser
            {
                UserName = userName,
                Email = email,
                EmailConfirmed = true
            };

            var result = await userManager.CreateAsync(user, password);

            if (!result.Succeeded)
            {
                throw new InvalidOperationException(
                    $"Không thể tạo tài khoản mẫu {userName}: {string.Join(", ", result.Errors.Select(e => e.Description))}");
            }
        }

        if (!await userManager.IsInRoleAsync(user, role))
        {
            await userManager.AddToRoleAsync(user, role);
        }
    }

    private static async Task SeedCoursesAsync(ApplicationDbContext context)
    {
        await EnsureCategoriesAsync(context);

        var categories = await context.Categories.ToDictionaryAsync(c => c.Name, c => c.Id);
        var courses = await context.Courses.ToListAsync();

        foreach (var seed in CourseSeeds)
        {
            var course = courses.FirstOrDefault(c =>
                c.Name == seed.Name || c.Name == seed.OldName);

            if (course is null)
            {
                context.Courses.Add(new Course
                {
                    Name = seed.Name,
                    Credits = seed.Credits,
                    Lecturer = seed.Lecturer,
                    CategoryId = categories[seed.CategoryName],
                    Image = "/images/course-default.svg"
                });

                continue;
            }

            course.Name = seed.Name;
            course.Credits = seed.Credits;
            course.Lecturer = seed.Lecturer;
            course.CategoryId = categories[seed.CategoryName];
            course.Image = string.IsNullOrWhiteSpace(course.Image)
                ? "/images/course-default.svg"
                : course.Image;
        }

        await context.SaveChangesAsync();
    }

    private static async Task EnsureCategoriesAsync(ApplicationDbContext context)
    {
        var categories = await context.Categories.ToListAsync();
        var oldNames = new Dictionary<string, string>
        {
            ["Lap trinh"] = "Lập trình",
            ["Co so du lieu"] = "Cơ sở dữ liệu",
            ["Thiet ke"] = "Thiết kế",
            ["Mang may tinh"] = "Mạng máy tính"
        };

        foreach (var category in categories)
        {
            if (oldNames.TryGetValue(category.Name, out var newName))
            {
                category.Name = newName;
            }
        }

        var requiredCategoryNames = CourseSeeds
            .Select(c => c.CategoryName)
            .Distinct()
            .ToList();

        foreach (var categoryName in requiredCategoryNames)
        {
            if (categories.All(c => c.Name != categoryName))
            {
                context.Categories.Add(new Category { Name = categoryName });
            }
        }

        await context.SaveChangesAsync();
    }

    private sealed record CourseSeed(
        string Name,
        string OldName,
        int Credits,
        string Lecturer,
        string CategoryName);
}
