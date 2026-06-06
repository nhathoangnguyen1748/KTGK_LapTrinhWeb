using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Authentication;

namespace NguyenHoangNhat_1549_KiemTra.ViewModels;

public class LoginViewModel
{
    [Required(ErrorMessage = "Nhập tên đăng nhập")]
    [Display(Name = "Tên đăng nhập")]
    public string UserName { get; set; } = string.Empty;

    [Required(ErrorMessage = "Nhập mật khẩu")]
    [Display(Name = "Mật khẩu")]
    [DataType(DataType.Password)]
    public string Password { get; set; } = string.Empty;

    [Display(Name = "Ghi nhớ đăng nhập")]
    public bool RememberMe { get; set; }

    public string? ReturnUrl { get; set; }
    public IList<AuthenticationScheme> ExternalLogins { get; set; } = [];
}
