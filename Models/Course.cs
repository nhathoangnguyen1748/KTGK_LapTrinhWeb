using System.ComponentModel.DataAnnotations;

namespace NguyenHoangNhat_1549_KiemTra.Models;

public class Course
{
    public int Id { get; set; }

    [Required]
    public string Name { get; set; } = string.Empty;

    [Required]
    public string Image { get; set; } = "/images/course-default.svg";

    [Range(1, 10)]
    public int Credits { get; set; }

    [Required]
    public string Lecturer { get; set; } = string.Empty;

    public int CategoryId { get; set; }
    public Category? Category { get; set; }

    public ICollection<Enrollment> Enrollments { get; set; } = new List<Enrollment>();
}
