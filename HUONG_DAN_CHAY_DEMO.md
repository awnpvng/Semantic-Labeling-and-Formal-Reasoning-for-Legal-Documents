# 🚀 Hướng Dẫn Chạy Demo

## Cách 1: Sử dụng Script PowerShell (Khuyến nghị)

### Bước 1: Mở PowerShell trong thư mục dự án
```powershell
cd d:\code_nam_3\ngu_nghia_hoc\CS229_Privacy_Semantic-main
```

### Bước 2: Chạy script
```powershell
.\run_demo.ps1
```

Script sẽ tự động:
- ✅ Kiểm tra dependencies
- ✅ Cài đặt nếu thiếu
- ✅ Khởi động server
- ✅ Hiển thị URL để truy cập

### Bước 3: Mở trình duyệt
Truy cập: **http://127.0.0.1:8000**

### Bước 4: Dừng server
Nhấn `Ctrl + C` trong PowerShell để dừng server

---

## Cách 2: Chạy Thủ Công

### Bước 1: Mở Terminal/PowerShell
```powershell
cd d:\code_nam_3\ngu_nghia_hoc\CS229_Privacy_Semantic-main
```

### Bước 2: Kiểm tra dependencies (chỉ cần làm 1 lần)
```powershell
pip install -r requirements.txt
```

### Bước 3: Khởi động server
```powershell
python -m uvicorn demo.main:app --reload --port 8000
```

### Bước 4: Mở trình duyệt
Truy cập: **http://127.0.0.1:8000**

### Bước 5: Dừng server
Nhấn `Ctrl + C` trong terminal

---

## 📝 Lưu Ý

### Nếu gặp lỗi "Module not found"
```powershell
pip install -r requirements.txt
```

### Nếu port 8000 đã được sử dụng
Thay đổi port trong lệnh:
```powershell
python -m uvicorn demo.main:app --reload --port 8001
```
Sau đó truy cập: http://127.0.0.1:8001

### Nếu muốn chạy không reload (production mode)
```powershell
python -m uvicorn demo.main:app --port 8000
```

---

## 🎯 Các Tính Năng Demo

| Tab | Chức năng |
|-----|-----------|
| **Tổng Quan** | Thống kê dự án, đoạn văn Privacy Policy |
| **WSD** | Tra cứu từ, so sánh MFS vs BERT+SVM |
| **Tri Thức** | Knowledge Base (Prolog), FOL |
| **Truy Vấn** | Thực thi 8 câu truy vấn Prolog |
| **WordNet** | Xem synonyms và hypernyms |

---

## 🔧 Troubleshooting

### Lỗi: Python không được nhận diện
Đảm bảo Python đã được cài đặt và thêm vào PATH:
```powershell
python --version
```

### Lỗi: pip không hoạt động
Thử sử dụng:
```powershell
python -m pip install -r requirements.txt
```

### Lỗi: Permission denied khi chạy script
Cho phép thực thi PowerShell script:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề, kiểm tra:
1. Python version >= 3.8
2. Tất cả dependencies đã được cài đặt
3. Port 8000 không bị chiếm bởi ứng dụng khác
