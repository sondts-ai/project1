# 📅 Ứng dụng thuật toán Hill Climbing cho bài toán xếp thời khóa biểu

## 🚀 Giới thiệu
Đây là một ứng dụng minh họa cách sử dụng **thuật toán Hill Climbing** để giải bài toán **xếp thời khóa biểu**.  
Ứng dụng được xây dựng bằng **Python** và **Streamlit**, cho phép người dùng nhập danh sách môn học, giảng viên, lớp học và số buổi học, sau đó tự động tối ưu để tạo ra một lịch học với số xung đột thấp nhất.

---

## ⚙️ Cách hoạt động
- Người dùng nhập:
  - Tên môn học
  - Giảng viên phụ trách
  - Lớp học
  - Số buổi (một môn có thể chiếm nhiều buổi khác nhau)
- Hệ thống sinh ngẫu nhiên lịch ban đầu.
- Thuật toán **Hill Climbing** sẽ tìm kiếm lịch tốt hơn bằng cách thay đổi dần (neighbor search) để **giảm số xung đột**:
  - Xung đột phòng (2 môn học cùng phòng cùng thời gian).
  - Xung đột giảng viên (GV bị trùng giờ).
  - Xung đột lớp học (lớp bị học 2 môn cùng giờ).
- Kết quả được hiển thị trực quan bằng bảng lịch.

---

## 🛠️ Cài đặt
### 1. Clone project
```bash
git clone https://github.com/your-repo/timetable-hillclimbing.git
cd timetable-hillclimbing
```

### 2. Tạo môi trường ảo (khuyến khích)
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

File `requirements.txt`:
```
streamlit
pandas
```

---

## ▶️ Chạy ứng dụng
```bash
streamlit run app.py
```

Ứng dụng sẽ mở trên trình duyệt mặc định tại địa chỉ:
```
http://localhost:8501
```

---

## 📊 Minh họa giao diện
- Nhập danh sách môn học, giảng viên, lớp học, số buổi.
- Nhấn **🚀 Chạy tối ưu lịch** để hệ thống sinh ra lịch học.
- Bảng kết quả sẽ hiển thị:
  - Số lượng xung đột
  - Lịch học chi tiết được sắp xếp theo thời gian

---

## 🧮 Thuật toán Hill Climbing
- **Khởi tạo:** sinh ngẫu nhiên một lịch học.
- **Đánh giá:** tính số xung đột.
- **Tìm kiếm láng giềng:** thay đổi ngẫu nhiên lịch của một môn học.
- **Chấp nhận:** nếu lịch mới có ít xung đột hơn thì cập nhật.
- **Dừng:** khi đạt lịch không có xung đột hoặc hết số vòng lặp cho phép.

---

## 📌 Ghi chú
- Do Hill Climbing có thể rơi vào **cực trị địa phương**, kết quả đôi khi vẫn còn xung đột. Có thể chạy lại nhiều lần để tìm lịch tốt hơn.
- Có thể mở rộng thêm các thuật toán khác như: **Simulated Annealing**, **Genetic Algorithm** để cải thiện chất lượng kết quả.

---