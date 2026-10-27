# Tài Liệu Kiến Trúc Kỹ Thuật Hệ Thống (System Architecture Document)

Dự án **KTGK_LapTrinhWeb** được xây dựng dựa trên nền tảng **ASP.NET Core Web Application** theo mô hình kiến trúc **Model-View-Controller (MVC)**. Tài liệu này mô tả chi tiết tổ chức kiến trúc, luồng xử lý dữ liệu và các thành phần cốt lõi của hệ thống.

---

## 1. Mô Hình Tổng Quan (High-Level Architecture)

Hệ thống hoạt động theo mô hình Client-Server hướng MVC truyền thống, trong đó:
- **Client (Trình duyệt Web)**: Gửi các yêu cầu HTTP (GET, POST, PUT, DELETE) và hiển thị kết quả HTML/CSS/JS do máy chủ render.
- **ASP.NET Core Web Server (Kestrel / IIS Integration)**: Tiếp nhận request, đưa qua pipeline các middleware để lọc, routing, xác thực và chuyển tiếp đến Controller phù hợp.
- **MVC Layer**:
  - **Controller**: Tiếp nhận dữ liệu đầu vào, tương tác với tầng dữ liệu/nghiệp vụ, lựa chọn View thích hợp và truyền dữ liệu View.
  - **Model / ViewModel**: Định nghĩa cấu trúc dữ liệu, quy tắc ràng buộc (validation attributes), trạng thái hiển thị.
  - **View**: Engine Razor (`.cshtml`) nhận dữ liệu từ Controller và kết xuất thành HTML tĩnh trả về cho Client.

---

## 2. Luồng Xử Lý HTTP Request (Request Processing Lifecycle)

```
[ Client Browser ]
        │  ▲
 HTTP   │  │  HTTP
Request │  │ Response
        ▼  │
┌────────────────────────────────────────────────────────┐
│ ASP.NET Core Middleware Pipeline                       │
│  ├── Static Files Middleware (wwwroot)                 │
│  ├── Routing Middleware                                │
│  ├── Authentication / Authorization (Nếu có)          │
│  └── Endpoint Routing Middleware                       │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│ MVC Controller Pipeline                                │
│  ├── Model Binding & Model Validation (Data Annotations)
│  ├── Action Execution                                  │
│  │     └── Business / Data Processing                  │
│  └── Action Result Execution                           │
│        ├── Razor View Engine (.cshtml Rendering)       │
│        └── JSON / Status Result Generation             │
└────────────────────────────────────────────────────────┘
```

### Các giai đoạn chi tiết:
1. **Tiếp nhận Request**: Yêu cầu từ Client đi vào Web Server Kestrel.
2. **Middleware Pipeline**:
   - Nếu là tài nguyên tĩnh (tại `wwwroot` như `.css`, `.js`, `.png`), `Static Files Middleware` phục vụ trực tiếp và kết thúc request.
   - Nếu là request điều hướng, `Routing Middleware` đối chiếu URL pattern với Route Table đã đăng ký (mặc định: `{controller=Home}/{action=Index}/{id?}`).
3. **Model Binding & Validation**:
   - ASP.NET Core tự động trích xuất tham số từ `RouteData`, `QueryString`, `Form Body`, hoặc `Header` và ánh xạ vào các tham số phương thức hoặc model.
   - Bộ xác thực kiểm tra các Data Annotation (`[Required]`, `[Range]`,...). Kết quả được lưu tại thuộc tính `ModelState.IsValid`.
4. **Action Invocation**: Action của Controller thực hiện logic, chuẩn bị dữ liệu và quyết định trả về kết quả (View, Redirect, PartialView hoặc JsonResult).
5. **View Rendering**: Razor Engine nạp layout (`_Layout.cshtml`), chèn nội dung view con, giải quyết Tag Helpers và sinh HTML hoàn chỉnh.
6. **HTTP Response**: Mã phản hồi kèm nội dung HTML được trả về Client.

---

## 3. Cấu Trúc Thư Mục Dự Án (Project Structure)

Dự án được phân cấp rõ ràng theo chuẩn ASP.NET Core MVC:

```
KTGK_LapTrinhWeb/
├── Controllers/                 # Bộ điều hướng tiếp nhận yêu cầu và xử lý hành vi
│   └── HomeController.cs        # Controller mặc định điều phối trang chủ và trang phụ
├── Models/                      # Định nghĩa dữ liệu nghiệp vụ và ViewModels
│   └── ErrorViewModel.cs        # Model chứa thông báo lỗi hệ thống
├── Views/                       # Giao diện hiển thị Razor (.cshtml)
│   ├── Home/                    # Các View thuộc HomeController
│   │   ├── Index.cshtml         # Trang chủ
│   │   └── Privacy.cshtml       # Trang chính sách
│   ├── Shared/                  # Giao diện dùng chung cho toàn bộ dự án
│   │   ├── _Layout.cshtml       # Layout khung chính (header, footer, nav)
│   │   ├── _Layout.cshtml.css   # CSS scoped dành riêng cho Layout
│   │   ├── _ValidationScriptsPartial.cshtml # Script xác thực client-side
│   │   └── Error.cshtml         # Giao diện hiển thị lỗi
│   ├── _ViewImports.cshtml      # Khai báo namespace & Tag Helpers toàn cục cho Views
│   └── _ViewStart.cshtml        # Cấu hình Layout mặc định cho mọi View
├── wwwroot/                     # Tài nguyên tĩnh công khai (Static Web Assets)
│   ├── css/                     # Tập tin định dạng giao diện hệ thống
│   │   └── site.css
│   ├── js/                      # Mã nguồn kịch bản JavaScript client-side
│   │   └── site.js
│   └── lib/                     # Thư viện JavaScript/CSS bên thứ ba
│       ├── bootstrap/           # Framework giao diện người dùng
│       ├── jquery/              # Thư viện xử lý DOM
│       ├── jquery-validation/   # Thư viện kiểm thực dữ liệu client
│       └── jquery-validation-unobtrusive/ # Tích hợp unobtrusive validation ASP.NET
├── Properties/
│   └── launchSettings.json      # Cấu hình môi trường chạy (ports, IIS Express, Kestrel)
├── tests/                       # Thư mục chứa các kịch bản kiểm thử (Tests / Validation)
│   └── test_feature_validation_helper.py
├── appsettings.json             # File cấu hình ứng dụng chính (Connection strings, App settings)
├── appsettings.Development.json # File cấu hình ghi đè cho môi trường Development
├── Program.cs                   # Điểm khởi đầu ứng dụng (Host builder, DI container, Middleware)
├── CONTRIBUTING.md              # Quy chuẩn đóng góp và phát triển
└── README.md                    # Tài liệu giới thiệu và hướng dẫn tổng quan
```

---

## 4. Quản Lý Cấu Hình & Môi Trường (Configuration Management)

- **Cấu hình phân cấp**: ASP.NET Core sử dụng hệ thống cấu hình hợp nhất (Configuration Providers). Thứ tự ưu tiên nạp cấu hình:
  1. `appsettings.json` (cấu hình cơ sở).
  2. `appsettings.{Environment}.json` (ghi đè theo môi trường: Development, Staging, Production).
  3. Environment Variables (biến môi trường hệ thống).
  4. Command-line arguments (tham số dòng lệnh khi khởi chạy).
- **Môi trường cục bộ**: Cấu hình URL và cổng dịch vụ được khai báo tại `Properties/launchSettings.json`. Không lưu trữ mật khẩu, chuỗi kết nối nhạy cảm trực tiếp lên git repository.

---

## 5. Cơ Chế Xác Thực Dữ Liệu (Validation Pipeline)

Hệ thống bảo vệ dữ liệu theo cơ chế phòng thủ 2 lớp (Two-Layer Validation):

### 5.1. Client-Side Validation
- Tận dụng `jquery.validate.js` và `jquery.validate.unobtrusive.js`.
- Khi Razor Engine render các thuộc tính có Data Annotations, nó tự động sinh các thuộc tính HTML5 `data-val-*`.
- Trình duyệt sẽ chặn submit form ngay tại client nếu dữ liệu chưa hợp lệ mà không cần gửi request lên server, giảm tải cho hệ thống.

### 5.2. Server-Side Validation
- Vì client-side validation có thể bị vô hiệu hóa hoặc vượt qua bởi các công cụ như Postman/curl, server-side validation là lớp bắt buộc:
  ```csharp
  [HttpPost]
  [ValidateAntiForgeryToken]
  public IActionResult Create(StudentViewModel model)
  {
      if (!ModelState.IsValid)
      {
          // Dữ liệu không hợp lệ: Render lại form kèm thông báo lỗi
          return View(model);
      }

      // Xử lý logic khi dữ liệu hợp lệ
      return RedirectToAction(nameof(Index));
  }
  ```

---

## 6. Định Hướng Phát Triển & Mở Rộng Hệ Thống (Extensibility)

Khi hệ thống phát triển quy mô lớn hơn, kiến trúc được khuyến nghị nâng cấp theo các mẫu thiết kế:
1. **Service Layer**: Tách toàn bộ nghiệp vụ phức tạp ra khỏi Controller, đưa vào các Services độc lập (`IStudentService`, `StudentService`).
2. **Repository & Unit of Work**: Sử dụng Entity Framework Core cùng Repository Pattern để trừu tượng hóa tầng truy xuất cơ sở dữ liệu.
3. **Automated Testing**: Mở rộng các kịch bản kiểm thử trong thư mục `tests/` bao gồm Unit Tests, Integration Tests cho Controllers và Services.
