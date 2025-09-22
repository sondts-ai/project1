# Ứng dụng thuật toán leo đồi ngẫu nhiên cho bài toán xếp thời khoá biểu khoa Công nghệ Thông tin Trường Đại học Kiến Trúc Hà Nội

## Giới thiệu
Bài toán xếp thời khoá biểu là một trong những bài toán tối ưu hoá kinh điển trong lĩnh vực Trí tuệ nhân tạo và Nghiên cứu vận hành. 
Mục tiêu là sắp xếp các môn học, giảng viên, lớp học và phòng học vào các khung thời gian sao cho hạn chế tối đa xung đột (ví dụ: một giảng viên bị xếp dạy 2 lớp cùng lúc, một lớp bị trùng lịch, hoặc một phòng bị nhiều lớp chiếm cùng thời điểm).

Trong đề tài này, chúng tôi áp dụng **thuật toán leo đồi ngẫu nhiên (Randomized Hill Climbing)** để tìm kiếm nghiệm gần tối ưu cho bài toán.

## Thuật toán sử dụng
- **Khởi tạo**: Tạo một thời khoá biểu ngẫu nhiên ban đầu.
- **Láng giềng**: Tạo nghiệm mới bằng cách thay đổi ngẫu nhiên một hoặc vài phần tử trong lịch.
- **Đánh giá**: Tính chi phí (số lượng xung đột trong lịch).
- **Chấp nhận nghiệm**:
  - Nếu nghiệm mới tốt hơn → chấp nhận.
  - Nếu nghiệm mới tệ hơn → có xác suất nhỏ vẫn chấp nhận (để thoát khỏi cực trị địa phương).
- **Lặp lại** cho đến khi đạt được lịch khả thi (không có xung đột) hoặc hết số vòng lặp.

## Công nghệ
- Ngôn ngữ: Python 3
- Thư viện: 
  - `random` để sinh lịch và biến đổi ngẫu nhiên
  - `pandas` để hiển thị bảng thời khoá biểu
  - `streamlit` để xây dựng giao diện web trực quan

## Cấu trúc dự án
```
├── app.py         # Mã nguồn chính chạy Streamlit
├── README.md      # Mô tả dự án
```

## Hướng dẫn chạy
1. Cài đặt các thư viện cần thiết:
   ```bash
   pip install streamlit pandas
   ```
2. Chạy ứng dụng:
   ```bash
   streamlit run app.py
   ```
3. Mở trình duyệt tại địa chỉ `http://localhost:8501` để sử dụng.

## Kết quả mong đợi
Ứng dụng sẽ hiển thị một bảng thời khoá biểu đã được tối ưu hoá, giảm thiểu tối đa xung đột nhờ vào thuật toán leo đồi ngẫu nhiên.

## Hướng phát triển
- Kết hợp với **giải thuật mô phỏng luyện kim (Simulated Annealing)** để cải thiện khả năng thoát khỏi cực trị địa phương.
- Bổ sung ràng buộc mềm (ví dụ: ưu tiên giảng viên dạy buổi sáng).
- Cho phép người dùng nhập dữ liệu thực tế từ file Excel/CSV.

---