# Hướng Dẫn Đóng Góp (Contributing Guide) - KTGK_LapTrinhWeb

Cảm ơn bạn đã quan tâm và mong muốn đóng góp cho dự án **KTGK_LapTrinhWeb**! Tài liệu này cung cấp các nguyên tắc, quy chuẩn mã nguồn và quy trình làm việc nhằm đảm bảo chất lượng và tính nhất quán của toàn bộ hệ thống.

---

## 1. Nguyên Tắc Chung
- Tôn trọng các thành viên trong đội ngũ phát triển.
- Luôn kiểm tra mã nguồn, chạy build và unit test trước khi gửi Pull Request.
- Giữ các thay đổi có phạm vi rõ ràng, tập trung giải quyết một vấn đề cụ thể (Single Responsibility).

---

## 2. Quy Trình Phân Nhánh (Branching Strategy)

Dự án áp dụng mô hình Git Feature Branching:

- **`main`**: Nhánh chính thức, chứa mã nguồn ổn định nhất (Production-ready). Không commit trực tiếp lên `main`.
- **`develop`**: Nhánh tích hợp các tính năng mới trước khi release.
- **Nhánh phụ**: Phải được tạo từ `develop` (hoặc `main` nếu là hotfix khẩn cấp) theo quy tắc đặt tên:
  - Tính năng mới: `feature/<ten-tinh-nang>` (Ví dụ: `feature/student-management`)
  - Sửa lỗi: `bugfix/<ma-loi-hoac-mo-ta>` (Ví dụ: `bugfix/fix-login-validation`)
  - Bản vá khẩn cấp: `hotfix/<noi-dung>` (Ví dụ: `hotfix/security-patch`)
  - Tài liệu: `docs/<noi-dung>` (Ví dụ: `docs/update-architecture`)
  - Tái cấu trúc mã nguồn: `refactor/<noi-dung>`

---

## 3. Quy Chuẩn Commit (Conventional Commits)

Các thông điệp commit phải tuân thủ chuẩn **Conventional Commits** với cấu trúc:

```
<type>(<scope>): <mô tả ngắn gọn bằng tiếng Việt hoặc tiếng Anh>

[Tùy chọn: Mô tả chi tiết nội dung thay đổi]

[Tùy chọn: Liên kết issue, ví dụ: Closes #6]
```

### Các Type được chấp thuận:
- `feat`: Tính năng mới cho người dùng hoặc hệ thống.
- `fix`: Sửa lỗi phát sinh.
- `docs`: Cập nhật hoặc bổ sung tài liệu kỹ thuật (README, CONTRIBUTING, XML docs).
- `style`: Thay đổi định dạng code (khoảng trắng, formatting, dấu chấm phẩy) không ảnh hưởng logic.
- `refactor`: Tái cấu trúc mã nguồn (không sửa lỗi, không thêm tính năng mới).
- `perf`: Cải thiện hiệu năng xử lý.
- `test`: Thêm mới hoặc chỉnh sửa các bài kiểm thử.
- `chore`: Cập nhật file cấu hình, dependencies, script build không tác động mã nguồn chính.

### Ví dụ hợp lệ:
```bash
git commit -m "feat(student): bổ sung chức năng thêm mới sinh viên"
git commit -m "fix(validation): xử lý lỗi kiểm tra định dạng email sinh viên"
git commit -m "docs(architecture): cập nhật sơ đồ luồng dữ liệu MVC"
git commit -m "chore(deps): nâng cấp thư viện jquery-validation"
```

---

## 4. Quy Chuẩn Viết Code (Coding Conventions)

### 4.1. Ngôn ngữ C# & ASP.NET Core
- **PascalCase**: Đặt tên cho `Class`, `Interface` (bắt đầu bằng chữ `I`), `Method`, `Property`, `Namespace`, `Enum`.
  ```csharp
  public interface IStudentService { }
  public class StudentController : Controller
  {
      public int TotalCount { get; set; }
      public IActionResult GetDetails(int id) { }
  }
  ```
- **camelCase**: Dùng cho biến cục bộ (local variables), tham số phương thức (parameters).
  ```csharp
  public void ProcessOrder(int orderId, string customerName)
  {
      var currentStatus = "Pending";
  }
  ```
- **_camelCase**: Dùng cho các private fields, readonly fields.
  ```csharp
  private readonly ILogger<HomeController> _logger;
  private readonly IConfiguration _configuration;
  ```
- **Async/Await**: Các tác vụ I/O, truy vấn database hoặc HTTP calls bắt buộc dùng `async/await`, tên phương thức kết thúc bằng hậu tố `Async`.
  ```csharp
  public async Task<IActionResult> IndexAsync()
  ```
- **Dependency Injection**: Tiêm phụ thuộc (DI) qua Constructor (Constructor Injection), không khởi tạo thủ công (`new`) các dịch vụ đã đăng ký trong container.

### 4.2. Kiến Trúc MVC & Clean Code
- **Controller**: Giữ Controller mỏng (Skinny Controller). Controller chỉ nhận request, kích hoạt validation, gọi service/xử lý và trả về View/JSON. Không viết logic nghiệp vụ phức tạp trực tiếp trong Controller.
- **ViewModel/Model**: Sử dụng ViewModel cho dữ liệu hiển thị trên View. Áp dụng Data Annotations (`[Required]`, `[StringLength]`, `[RegularExpression]`) để kiểm thực dữ liệu.
- **Views**:
  - Hạn chế viết mã C# phức tạp trong View (`.cshtml`).
  - Tận dụng Tag Helpers của ASP.NET Core (`asp-action`, `asp-controller`, `asp-for`, `asp-validation-for`).
  - Đặt các layout dùng chung tại `Views/Shared/`.

### 4.3. Quản lý Tài nguyên Tĩnh (Static Assets)
- Mọi file CSS, JavaScript và thư viện bên thứ ba phải đặt tại `wwwroot/`.
- File CSS dùng riêng cho view hoặc layout cần phân chia theo module, tránh viết inline style trong `.cshtml`.
- Các file JavaScript phải được đóng gói theo dạng module hoặc hàm có namespace để tránh xung đột biến toàn cục (`global scope`).

---

## 5. Quy Trình Tạo Pull Request (PR)

1. **Đồng bộ mã nguồn**: Cập nhật nhánh nhánh làm việc với nhánh `develop` mới nhất trước khi mở PR:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout feature/ten-tinh-nang
   git rebase develop
   ```
2. **Kiểm tra cục bộ**:
   - Dự án build thành công không có warning/error: `dotnet build`
   - Chạy toàn bộ test suite thành công: `dotnet test`
3. **Mở Pull Request trên GitHub**:
   - Đặt tiêu đề PR theo chuẩn: `[Loại] Tên tóm tắt thay đổi` (Ví dụ: `[Feature] Quản lý thông tin môn học`).
   - Điền đầy đủ thông tin vào template PR: Mục đích thay đổi, danh sách file sửa đổi, hướng dẫn kiểm thử.
   - Gắn nhãn (Labels) và gán Reviewer liên quan.
4. **Xử lý Review**:
   - Phản hồi và khắc phục các góp ý từ Reviewer.
   - Khi có ít nhất 1 phê duyệt (Approval) và tất cả bài kiểm tra CI pass, tiến hành Merge (Squash and Merge hoặc Rebase Merge theo chính sách kho chứa).

---

## 6. Hướng Dẫn Cài Đặt Môi Trường Cục Bộ

1. Cài đặt **.NET SDK** (khuyến nghị phiên bản 8.0 hoặc phiên bản tương thích của dự án).
2. Clone repository:
   ```bash
   git clone https://github.com/nhathoangnguyen1748/KTGK_LapTrinhWeb.git
   cd KTGK_LapTrinhWeb
   ```
3. Phục hồi dependencies:
   ```bash
   dotnet restore
   ```
4. Build ứng dụng:
   ```bash
   dotnet build
   ```
5. Khởi chạy ứng dụng:
   ```bash
   dotnet run
   ```
   Ứng dụng sẽ khả dụng tại địa chỉ hiển thị trong terminal (mặc định cấu hình tại `Properties/launchSettings.json`).
