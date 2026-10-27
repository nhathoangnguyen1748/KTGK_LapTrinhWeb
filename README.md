# KTGK_LapTrinhWeb - Đồ Án ASP.NET Core MVC

Dự án Kiểm tra giữa kỳ (KTGK) môn **Lập trình Web**, được xây dựng trên nền tảng **ASP.NET Core MVC**. Dự án mô phỏng ứng dụng web hoàn chỉnh với mô hình kiến trúc MVC, tích hợp giao diện người dùng tương tác và xử lý dữ liệu backend.

---

## 📌 Mục lục
- [Giới thiệu](#-giới-thiệu)
- [Công nghệ sử dụng](#-công-nghệ-sử-dụng)
- [Cấu trúc thư mục & Kiến trúc MVC](#-cấu-trúc-thư-mục--kiến-trúc-mvc)
- [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
- [Hướng dẫn cài đặt và chạy đồ án](#-hướng-dẫn-cài-đặt-và-chạy-đồ-án)
  - [1. Clone mã nguồn](#1-clone-mã-nguồn)
  - [2. Cấu hình chuỗi kết nối cơ sở dữ liệu](#2-cấu-hình-chuỗi-kết-nối-cơ-sở-dữ-liệu)
  - [3. Khởi tạo Cơ sở Dữ liệu (Migrations)](#3-khởi-tạo-cơ-sở-dữ-liệu-migrations)
  - [4. Build và Chạy ứng dụng](#4-build-và-chạy-ứng-dụng)
- [Cấu hình môi trường & Port](#-cấu-hình-môi-trường--port)
- [Đóng góp & Giấy phép](#-đóng-góp--giấy-phép)

---

## 📖 Giới thiệu

`KTGK_LapTrinhWeb` là đồ án thực hành kiến trúc ứng dụng web hướng đối tượng, xử lý luồng nghiệp vụ thông qua mô hình Model-View-Controller (MVC) của Microsoft:
- **Tách bạch mối quan tâm (Separation of Concerns)** giữa dữ liệu (Model), giao diện (View) và logic điều hướng (Controller).
- **Trải nghiệm giao diện thân thiện (UI/UX)**: Tối ưu hiển thị responsive, tích hợp CSS/JS tùy biến và kiểm tra hợp lệ dữ liệu (Client-side & Server-side Validation).

---

## 💻 Công nghệ sử dụng

- **Backend**:
  - Ngôn ngữ: C#
  - Framework: .NET (ASP.NET Core MVC)
  - ORM: Entity Framework Core
- **Frontend**:
  - Razor View Engine (`.cshtml`)
  - HTML5, CSS3, JavaScript
  - Thư viện: Bootstrap, jQuery, jQuery Validation & Unobtrusive Validation
- **Cơ sở dữ liệu**:
  - Microsoft SQL Server / SQL Server LocalDB

---

## 🏛 Cấu trúc thư mục & Kiến trúc MVC

Dự án tuân thủ chuẩn cấu trúc của ứng dụng ASP.NET Core MVC:

```text
KTGK_LapTrinhWeb/
├── Controllers/                 # Điều khiển luồng request và trả về View/Data
│   └── HomeController.cs        # Controller mặc định xử lý trang chủ và các tác vụ chung
├── Models/                      # Thực thể dữ liệu (Entities) và ViewModels
│   └── ErrorViewModel.cs        # Model xử lý và truyền dữ liệu lỗi
├── Views/                       # Giao diện hiển thị (Razor Views)
│   ├── Home/                    # Các View thuộc HomeController (Index, Privacy, ...)
│   ├── Shared/                  # Giao diện dùng chung
│   │   ├── _Layout.cshtml       # Master layout chính cho toàn ứng dụng
│   │   ├── _Layout.cshtml.css   # Scoped CSS cho Layout
│   │   └── _ValidationScriptsPartial.cshtml
│   ├── _ViewImports.cshtml      # Import namespaces và tag helpers cho toàn bộ Views
│   └── _ViewStart.cshtml        # Cấu hình layout mặc định cho Views
├── wwwroot/                     # Tài nguyên tĩnh (Static Files)
│   ├── css/                     # File stylesheet tùy biến (site.css)
│   ├── js/                      # File JavaScript tùy biến (site.js)
│   └── lib/                     # Thư viện client bên thứ ba (Bootstrap, jQuery, v.v.)
├── Properties/
│   └── launchSettings.json      # Cấu hình môi trường dev, profile và ports
├── appsettings.json             # Cấu hình chính (Connection Strings, App Settings)
├── appsettings.Development.json # Cấu hình ghi đè cho môi trường Development
├── Program.cs                   # Điểm khởi động (Entry point), cấu hình DI container và Middleware pipeline
└── README.md                    # Tài liệu hướng dẫn đồ án
```

### Chi tiết các thành phần chính:
1. **Controllers**: Tiếp nhận HTTP requests từ client, gọi tầng dữ liệu/nghiệp vụ và chọn View phù hợp để hiển thị dữ liệu cho người dùng.
2. **Models**: Chứa các lớp đại diện cho cấu trúc dữ liệu trong cơ sở dữ liệu, tham số nghiệp vụ và các ViewModels phục vụ hiển thị/nhập liệu.
3. **Views**: Các file `.cshtml` kết hợp giữa mã HTML và cú pháp C# Razor để sinh mã HTML trả về trình duyệt.
4. **wwwroot**: Chứa mã nguồn client tĩnh (CSS, JavaScript, hình ảnh, vendor libraries) được phục vụ trực tiếp tới client.
5. **Program.cs**: Cấu hình các dịch vụ (Services / Dependency Injection), chuỗi kết nối DbContext và thiết lập Middleware (Routing, StaticFiles, Authentication/Authorization).

---

## ⚙ Yêu cầu hệ thống

Trước khi chạy dự án, hãy đảm bảo máy tính đã cài đặt các công cụ sau:
- [.NET SDK](https://dotnet.microsoft.com/download) (Khuyên dùng .NET 8.0 SDK hoặc phiên bản tương thích)
- [Visual Studio 2022](https://visualstudio.microsoft.com/) (với workload *ASP.NET and web development*) hoặc [Visual Studio Code](https://code.visualstudio.com/) (với extension C# Dev Kit)
- [Microsoft SQL Server](https://www.microsoft.com/en-us/sql-server) hoặc SQL Server Express / LocalDB

Kiểm tra phiên bản .NET SDK bằng dòng lệnh:
```bash
dotnet --version
```

---

## 🚀 Hướng dẫn cài đặt và chạy đồ án

### 1. Clone mã nguồn
Mở terminal và clone repository về máy cục bộ:
```bash
git clone https://github.com/nhathoangnguyen1748/KTGK_LapTrinhWeb.git
cd KTGK_LapTrinhWeb
```

### 2. Cấu hình chuỗi kết nối cơ sở dữ liệu
Mở file `appsettings.json` và cấu hình chuỗi kết nối phù hợp với SQL Server cục bộ của bạn:
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\mssqllocaldb;Database=KTGK_LapTrinhWeb_Db;Trusted_Connection=True;MultipleActiveResultSets=true"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*"
}
```
*(Lưu ý: Điều chỉnh `Server` hoặc thông tin đăng nhập `User Id`/`Password` nếu bạn dùng SQL Server Authentication)*.

### 3. Khởi tạo Cơ sở Dữ liệu (Migrations)
Nếu đồ án có sử dụng Entity Framework Core Migrations, thực thi lệnh sau để cập nhật database:
```bash
# Cài đặt công cụ dotnet-ef (nếu chưa có)
dotnet tool install --global dotnet-ef

# Cập nhật schema vào database
dotnet ef database update
```

### 4. Build và Chạy ứng dụng

#### Lựa chọn A: Sử dụng .NET CLI (Khuyên dùng)
1. Restore các package NuGet:
   ```bash
   dotnet restore
   ```
2. Biên dịch dự án:
   ```bash
   dotnet build
   ```
3. Chạy ứng dụng:
   ```bash
   dotnet run
   ```

#### Lựa chọn B: Sử dụng Visual Studio 2022
1. Mở file giải pháp (`.sln`) hoặc thư mục dự án bằng Visual Studio 2022.
2. Đợi Visual Studio tự động khôi phục các NuGet Packages.
3. Nhấn **F5** (hoặc nút **Start Debugging** / **Start Without Debugging** - `Ctrl + F5`).

---

## 🌐 Cấu hình môi trường & Port

Sau khi khởi chạy ứng dụng thành công, terminal sẽ thông báo địa chỉ truy cập cục bộ (được cấu hình trong `Properties/launchSettings.json`):
- **HTTPS**: `https://localhost:7xxx` hoặc `https://localhost:5001`
- **HTTP**: `http://localhost:5xxx` hoặc `http://localhost:5000`

Mở trình duyệt web và truy cập vào đường dẫn trên để trải nghiệm ứng dụng.

---

## 👨‍💻 Đóng góp & Giấy phép

- **Tác giả đồ án**: [nhathoangnguyen1748](https://github.com/nhathoangnguyen1748)
- **Môn học**: Lập trình Web - Kiểm tra giữa kỳ (KTGK)
- **Mục đích**: Học tập, nghiên cứu và phát triển kỹ năng lập trình web ASP.NET Core MVC.
