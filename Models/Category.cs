using System.ComponentModel.DataAnnotations;

namespace NguyenHoangNhat_1549_KiemTra.Models;

public class Category
{
    public int Id { get; set; }

    [Required]
    public string Name { get; set; } = string.Empty;

    public ICollection<Course> Courses { get; set; } = new List<Course>();
}
