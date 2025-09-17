# 📅 Ứng dụng Xếp Lịch Học - Khoa CNTT (Hill Climbing)

Ứng dụng này được xây dựng bằng **Python** và **Streamlit** để mô phỏng bài toán **xếp lịch học** cho khoa CNTT, sử dụng **thuật toán leo đồi ngẫu nhiên (Random Hill Climbing)**.  
Ứng dụng sẽ tự động phân bổ **môn học - giảng viên - lớp - phòng học - thời gian** sao cho hạn chế tối đa **xung đột** (giảng viên/lớp/phòng bị trùng giờ).

---

## 🚀 Tính năng
- Sinh ngẫu nhiên thời khóa biểu cho các môn học.
- Đánh giá số lượng xung đột trong lịch.
- Sử dụng **Hill Climbing** để cải thiện và tối ưu lịch.
- Giao diện trực quan với **Streamlit**:
  - Cho phép chỉnh số lần lặp (`iterations`) của thuật toán.
  - Hiển thị bảng lịch học kết quả.
  - Thông báo khi tìm được lịch không còn xung đột.

---

## 🛠️ Cài đặt

### 1. Clone dự án
```bash
git clone https://github.com/ten-ban/repo-xep-lich.git
cd repo-xep-lich
```

### 2. Tạo môi trường ảo (khuyến nghị)
```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
```

### 3. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

File `requirements.txt` gồm:
```
streamlit
```

---

## ▶️ Chạy ứng dụng
```bash
streamlit run app.py
```

Sau đó mở trình duyệt tại [http://localhost:8501](http://localhost:8501).

---

## 📂 Cấu trúc dự án
```
.
├── app.py          # File chính chứa thuật toán + UI
├── README.md       # Tài liệu mô tả dự án
└── requirements.txt
```

---

## 📖 Thuật toán sử dụng
- **Random Hill Climbing**:
  - Bắt đầu với một lịch ngẫu nhiên.
  - Lặp lại nhiều lần:
    - Sinh một "láng giềng" (neighbor) bằng cách đổi ngẫu nhiên phòng/thời gian cho một môn.
    - Nếu lịch mới tốt hơn (ít xung đột hơn), chấp nhận thay thế.
  - Dừng khi tìm được lịch **không xung đột** hoặc đạt số vòng lặp tối đa.

---



Ứng dụng sẽ hiển thị bảng lịch học tối ưu và số xung đột:

| Môn học       | Giảng viên | Lớp   | Phòng | Thời gian |
|---------------|------------|-------|-------|-----------|
| AI            | Thầy A     | CNTT1 | P101  | T2-Sáng   |
| DL            | Thầy B     | CNTT1 | P103  | T3-Chiều  |
| ...           | ...        | ...   | ...   | ...       |

---

