using System.Security.Claims;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using NguyenHoangNhat_1549_KiemTra.Data;
using NguyenHoangNhat_1549_KiemTra.ViewModels;

namespace NguyenHoangNhat_1549_KiemTra.Controllers;

[Route("account")]
public class AccountController : Controller
{
    private readonly SignInManager<IdentityUser> _signInManager;
    private readonly UserManager<IdentityUser> _userManager;

    public AccountController(SignInManager<IdentityUser> signInManager, UserManager<IdentityUser> userManager)
    {
        _signInManager = signInManager;
        _userManager = userManager;
    }

    [HttpGet("register")]
    public IActionResult Register()
    {
        return View();
    }

    [HttpPost("register")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Register(RegisterViewModel model)
    {
        if (!ModelState.IsValid)
        {
            return View(model);
        }

        var user = new IdentityUser
        {
            UserName = model.UserName.Trim(),
            Email = model.Email.Trim(),
            EmailConfirmed = true
        };

        var result = await _userManager.CreateAsync(user, model.Password);

        if (result.Succeeded)
        {
            await _userManager.AddToRoleAsync(user, SeedData.StudentRole);
            await _signInManager.SignInAsync(user, isPersistent: false);
            return Redirect("/home");
        }

        foreach (var error in result.Errors)
        {
            ModelState.AddModelError(string.Empty, error.Description);
        }

        return View(model);
    }

    [HttpGet("login")]
    public async Task<IActionResult> Login(string? returnUrl = null)
    {
        return View(await BuildLoginViewModelAsync(returnUrl));
    }

    [HttpPost("login")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Login(LoginViewModel model)
    {
        if (!ModelState.IsValid)
        {
            return View(await BuildLoginViewModelAsync(model.ReturnUrl, model));
        }

        var result = await _signInManager.PasswordSignInAsync(
            model.UserName.Trim(),
            model.Password,
            model.RememberMe,
            lockoutOnFailure: false);

        if (result.Succeeded)
        {
            return RedirectToLocal(model.ReturnUrl);
        }

        ModelState.AddModelError(string.Empty, "Đăng nhập không thành công");
        return View(await BuildLoginViewModelAsync(model.ReturnUrl, model));
    }

    [Authorize]
    [HttpPost("logout")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Logout()
    {
        await _signInManager.SignOutAsync();
        return Redirect("/home");
    }

    [HttpPost("external-login")]
    [ValidateAntiForgeryToken]
    public IActionResult ExternalLogin(string provider, string? returnUrl = null)
    {
        var redirectUrl = Url.Action(nameof(ExternalLoginCallback), "Account", new { returnUrl });
        var properties = _signInManager.ConfigureExternalAuthenticationProperties(provider, redirectUrl);

        return Challenge(properties, provider);
    }

    [HttpGet("external-login-callback")]
    public async Task<IActionResult> ExternalLoginCallback(string? returnUrl = null, string? remoteError = null)
    {
        if (remoteError is not null)
        {
            ModelState.AddModelError(string.Empty, $"Lỗi Google: {remoteError}");
            return View("Login", await BuildLoginViewModelAsync(returnUrl));
        }

        var info = await _signInManager.GetExternalLoginInfoAsync();

        if (info is null)
        {
            return RedirectToAction(nameof(Login));
        }

        var externalResult = await _signInManager.ExternalLoginSignInAsync(
            info.LoginProvider,
            info.ProviderKey,
            isPersistent: false,
            bypassTwoFactor: true);

        if (externalResult.Succeeded)
        {
            return RedirectToLocal(returnUrl);
        }

        var email = info.Principal.FindFirstValue(ClaimTypes.Email);

        if (string.IsNullOrWhiteSpace(email))
        {
            ModelState.AddModelError(string.Empty, "Tài khoản Google không có địa chỉ thư điện tử.");
            return View("Login", await BuildLoginViewModelAsync(returnUrl));
        }

        var user = await _userManager.FindByEmailAsync(email);

        if (user is null)
        {
            user = new IdentityUser
            {
                UserName = email,
                Email = email,
                EmailConfirmed = true
            };

            var createResult = await _userManager.CreateAsync(user);

            if (!createResult.Succeeded)
            {
                foreach (var error in createResult.Errors)
                {
                    ModelState.AddModelError(string.Empty, error.Description);
                }

                return View("Login", await BuildLoginViewModelAsync(returnUrl));
            }

            await _userManager.AddToRoleAsync(user, SeedData.StudentRole);
        }

        var addLoginResult = await _userManager.AddLoginAsync(user, info);

        if (!addLoginResult.Succeeded && addLoginResult.Errors.Any(e => e.Code != "LoginAlreadyAssociated"))
        {
            foreach (var error in addLoginResult.Errors)
            {
                ModelState.AddModelError(string.Empty, error.Description);
            }

            return View("Login", await BuildLoginViewModelAsync(returnUrl));
        }

        await _signInManager.SignInAsync(user, isPersistent: false);
        return RedirectToLocal(returnUrl);
    }

    [HttpGet("access-denied")]
    public IActionResult AccessDenied()
    {
        return View();
    }

    private async Task<LoginViewModel> BuildLoginViewModelAsync(string? returnUrl, LoginViewModel? model = null)
    {
        model ??= new LoginViewModel();
        model.ReturnUrl = returnUrl ?? "/home";
        model.ExternalLogins = (await _signInManager.GetExternalAuthenticationSchemesAsync()).ToList();

        return model;
    }

    private IActionResult RedirectToLocal(string? returnUrl)
    {
        if (!string.IsNullOrWhiteSpace(returnUrl) && Url.IsLocalUrl(returnUrl))
        {
            return LocalRedirect(returnUrl);
        }

        return Redirect("/home");
    }
}
