using System.ComponentModel.DataAnnotations;

namespace NguyenHoangNhat_1549_KiemTra.ViewModels;

public class RegisterViewModel
{
    [Required(ErrorMessage = "Nhập tên đăng nhập")]
    [Display(Name = "Tên đăng nhập")]
    public string UserName { get; set; } = string.Empty;

    [Required(ErrorMessage = "Nhập địa chỉ thư điện tử")]
    [EmailAddress(ErrorMessage = "Địa chỉ thư điện tử không hợp lệ")]
    [Display(Name = "Thư điện tử")]
    public string Email { get; set; } = string.Empty;

    [Required(ErrorMessage = "Nhập mật khẩu")]
    [Display(Name = "Mật khẩu")]
    [DataType(DataType.Password)]
    [MinLength(6, ErrorMessage = "Mật khẩu tối thiểu 6 ký tự")]
    public string Password { get; set; } = string.Empty;
}
