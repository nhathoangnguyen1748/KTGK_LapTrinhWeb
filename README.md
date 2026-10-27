# KTGK_LapTrinhWeb - Dự Án ASP.NET Core MVC

[![.NET](https://img.shields.io/badge/.NET-ASP.NET%20Core%20MVC-512BD4?logo=dotnet)](https://dotnet.microsoft.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

Dự án Web ứng dụng được phát triển bằng nền tảng **ASP.NET Core MVC**, tuân thủ các quy chuẩn thiết kế phần mềm hiện đại, kiến trúc phân tầng rõ ràng và tích hợp cơ chế xác thực dữ liệu chặt chẽ từ máy khách đến máy chủ.

---

## 📚 Mục Lục
- [1. Tính Năng & Công Nghệ](#1-tính-năng--công-nghệ)
- [2. Kiến Trúc Dự Án](#2-kiến-trúc-dự-án)
- [3. Cấu Trúc Thư Mục](#3-cấu-trúc-thư-mục)
- [4. Yêu Cầu Hệ Thống & Cài Đặt](#4-yêu-cầu-hệ-thống--cài-đặt)
- [5. Hướng Dẫn Khởi Chạy](#5-hướng-dẫn-khởi-chạy)
- [6. Kiểm Thử (Testing)](#6-kiểm-thử-testing)
- [7. Quy Chuẩn Đóng Góp (Contributing)](#7-quy-chuẩn-đóng-góp-contributing)
- [8. Bản Quyền & Giấy Phép](#8-bản-quyền--giấy-phép)

---

## 1. Tính Năng & Công Nghệ

### Công Nghệ Sử Dụng:
- **Backend**: C#, ASP.NET Core MVC (Model-View-Controller pattern).
- **Frontend**: Razor View Engine, HTML5, CSS3, JavaScript.
- **Thư viện UI & Utilities**: Bootstrap 5, jQuery.
- **Client-Side Validation**: jQuery Validation & jQuery Validation Unobtrusive.
- **Dependency Injection**: Tích hợp sẵn trong ASP.NET Core Service Container.
- **Kiểm thử**: Bộ kịch bản kiểm thử tự động tại thư mục `tests/`.

---

## 2. Kiến Trúc Dự Án

Hệ thống hoạt động theo mô hình **Model-View-Controller (MVC)** với các nguyên tắc:
1. **Controller**: Đóng vai trò điều hướng, tiếp nhận HTTP Request, xử lý xác thực đầu vào và điều phối dữ liệu.
2. **Model / ViewModel**: Đại diện cho thực thể dữ liệu và các ràng buộc dữ liệu (Data Annotations).
3. **View**: Định dạng và kết xuất giao diện trực quan thông qua Razor Engine.
4. **Middleware Pipeline**: Quản lý tài nguyên tĩnh (`wwwroot`), routing, xử lý ngoại lệ và bảo mật.

👉 **Xem chi tiết tài liệu kiến trúc kỹ thuật tại:** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## 3. Cấu Trúc Thư Mục

```
KTGK_LapTrinhWeb/
├── Controllers/          # Các Controller tiếp nhận và xử lý Request
├── Models/               # Định nghĩa Model thực thể và ViewModel
├── Views/                # Các file giao diện Razor (.cshtml)
│   ├── Home/             # Giao diện theo từng Controller
│   └── Shared/           # Giao diện dùng chung (_Layout, Partials)
├── wwwroot/              # Tài nguyên tĩnh công khai (CSS, JS, Libs)
│   ├── css/              # Stylesheet hệ thống
│   ├── js/               # Kịch bản JavaScript
│   └── lib/              # Thư viện ngoài (Bootstrap, jQuery,...)
├── Properties/           # Cấu hình môi trường khởi chạy (launchSettings.json)
├── docs/                 # Tài liệu kỹ thuật chi tiết
│   └── ARCHITECTURE.md   # Tài liệu kiến trúc hệ thống
├── tests/                # Bộ kịch bản kiểm thử
├── appsettings.json      # File cấu hình ứng dụng
├── CONTRIBUTING.md       # Hướng dẫn quy chuẩn đóng góp & code
└── README.md             # Tài liệu tổng quan dự án
```

---

## 4. Yêu Cầu Hệ Thống & Cài Đặt

Trước khi bắt đầu, hãy đảm bảo máy tính đã cài đặt:
- [.NET SDK](https://dotnet.microsoft.com/download) (Khuyến nghị bản tương thích với dự án, ví dụ: .NET 6.0, 7.0 hoặc 8.0 trở lên).
- Trình biên dịch: Visual Studio 2022, Visual Studio Code (kèm C# Dev Kit), hoặc JetBrains Rider.
- [Git](https://git-scm.com/).

---

## 5. Hướng Dẫn Khởi Chạy

### Bước 1: Sao chép mã nguồn
```bash
git clone https://github.com/nhathoangnguyen1748/KTGK_LapTrinhWeb.git
cd KTGK_LapTrinhWeb
```

### Bước 2: Khôi phục dependencies
```bash
dotnet restore
```

### Bước 3: Biên dịch dự án
```bash
dotnet build
```

### Bước 4: Khởi chạy dự án
```bash
dotnet run
```

Sau khi khởi chạy thành công, mở trình duyệt và truy cập vào URL hiển thị trên terminal (thường là `https://localhost:5001` hoặc `http://localhost:5000` tùy theo `launchSettings.json`).

---

## 6. Kiểm Thử (Testing)

Dự án tích hợp các kịch bản kiểm thử nhằm đảm bảo tính toàn vẹn của hệ thống:
```bash
# Chạy các bài kiểm thử .NET (nếu có dự án test xUnit/NUnit)
dotnet test

# Chạy kịch bản kiểm thử tính năng hỗ trợ
python3 -m unittest discover tests/
```

---

## 7. Quy Chuẩn Đóng Góp (Contributing)

Chúng tôi luôn chào đón mọi đóng góp phát triển hệ thống! Xin vui lòng đọc kỹ quy tắc trước khi gửi Pull Request:
- **Quy chuẩn commit**: Chuẩn [Conventional Commits](https://www.conventionalcommits.org/) (`feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`).
- **Quy trình nhánh**: Làm việc trên nhánh `feature/*` hoặc `bugfix/*` tách từ `develop`.
- **Quy chuẩn mã nguồn**: Tuân thủ quy tắc đặt tên C# (PascalCase, camelCase) và cấu trúc Skinny Controller.

👉 **Xem hướng dẫn chi tiết tại:** [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 8. Bản Quyền & Giấy Phép

Dự án được phân phối dưới giấy phép MIT License. Chi tiết xem tại tập tin `LICENSE` (nếu có).
