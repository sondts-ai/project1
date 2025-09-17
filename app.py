import random
import streamlit as st

# ==========================
# DỮ LIỆU GIẢ ĐỊNH
# ==========================
mon_hoc = ["AI", "DL", "CSDL", "ML", "Python", "Toán rời rạc"]
giang_vien = {
    "AI": "Thầy A",
    "DL": "Thầy B",
    "CSDL": "Cô C",
    "ML": "Thầy D",
    "Python": "Cô E",
    "Toán rời rạc": "Thầy F",
}
lop_hoc = {
    "AI": "CNTT1",
    "DL": "CNTT1",
    "CSDL": "CNTT2",
    "ML": "CNTT2",
    "Python": "CNTT3",
    "Toán rời rạc": "CNTT3",
}
phong_hoc = ["P101", "P102", "P103","P201","P202","P203"]
thoi_gian = ["T2-Sáng", "T2-Chiều", "T3-Sáng", "T3-Chiều", "T4-Sáng", "T4-Chiều"]

# ==========================
# TẠO LỊCH NGẪU NHIÊN
# ==========================
def tao_lich_ngau_nhien():
    return {
        mh: (random.choice(phong_hoc), random.choice(thoi_gian))
        for mh in mon_hoc
    }

# ==========================
# HÀM ĐÁNH GIÁ
# ==========================
def tinh_xung_dot(lich):
    xung_dot = 0
    da_dung = {}

    for mh, (phong, tg) in lich.items():
        gv = giang_vien[mh]
        lop = lop_hoc[mh]

        # Kiểm tra phòng học trùng giờ
        if (phong, tg) in da_dung:
            xung_dot += 1
        else:
            da_dung[(phong, tg)] = mh

        # Kiểm tra giảng viên trùng giờ
        if (gv, tg) in da_dung:
            xung_dot += 1
        else:
            da_dung[(gv, tg)] = mh

        # Kiểm tra lớp trùng giờ
        if (lop, tg) in da_dung:
            xung_dot += 1
        else:
            da_dung[(lop, tg)] = mh

    return xung_dot

# ==========================
# TẠO LÁNG GIỀNG
# ==========================
def tao_lang_gieng(lich):
    new_lich = lich.copy()
    mh = random.choice(mon_hoc)
    new_lich[mh] = (random.choice(phong_hoc), random.choice(thoi_gian))
    return new_lich

# ==========================
# THUẬT TOÁN LEO ĐỒI NGẪU NHIÊN
# ==========================
def hill_climbing(max_iter=1000):
    lich = tao_lich_ngau_nhien()
    cost = tinh_xung_dot(lich)

    for _ in range(max_iter):
        neighbor = tao_lang_gieng(lich)
        new_cost = tinh_xung_dot(neighbor)

        if new_cost < cost:
            lich, cost = neighbor, new_cost

        if cost == 0:  # không còn xung đột
            break

    return lich, cost

# ==========================
# STREAMLIT UI
# ==========================
st.title("📅 Xếp lịch học - Khoa CNTT (Hill Climbing)")

so_lan = st.slider("Số lần lặp tối đa", min_value=100, max_value=5000, value=1000, step=100)
run_button = st.button("Chạy thuật toán")

if run_button:
    best_schedule, best_cost = hill_climbing(so_lan)
    
    st.subheader("✅ Lịch học tối ưu tìm được:")
    st.table([
        {
            "Môn học": mh,
            "Giảng viên": giang_vien[mh],
            "Lớp": lop_hoc[mh],
            "Phòng": phong,
            "Thời gian": tg
        }
        for mh, (phong, tg) in best_schedule.items()
    ])

    st.write(f"### 🔍 Số xung đột: {best_cost}")
    if best_cost == 0:
        st.success("🎉 Tìm được lịch không xung đột!")
    else:
        st.warning("⚠️ Vẫn còn xung đột. Bạn có thể chạy lại hoặc tăng số lần lặp.")
