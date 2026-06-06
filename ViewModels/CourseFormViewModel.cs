using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Mvc.Rendering;

namespace NguyenHoangNhat_1549_KiemTra.ViewModels;

public class CourseFormViewModel
{
    public int Id { get; set; }

    [Required(ErrorMessage = "Nhập tên học phần")]
    [Display(Name = "Tên học phần")]
    public string Name { get; set; } = string.Empty;

    [Display(Name = "Hình ảnh")]
    public string? Image { get; set; }

    [Range(1, 10, ErrorMessage = "Số tín chỉ từ 1 đến 10")]
    [Display(Name = "Số tín chỉ")]
    public int Credits { get; set; } = 3;

    [Required(ErrorMessage = "Nhập giảng viên")]
    [Display(Name = "Giảng viên")]
    public string Lecturer { get; set; } = string.Empty;

    [Display(Name = "Danh mục")]
    public int CategoryId { get; set; }

    public List<SelectListItem> Categories { get; set; } = [];
}
