import random
import streamlit as st

# ==========================
# HÀM TẠO DANH SÁCH THỜI GIAN (T2-T7, 4 ca/ngày)
# ==========================
def tao_thoi_gian():
    tg = []
    for thu in range(2, 8):  # T2 -> T7
        for ca in range(1, 5):  # 4 ca mỗi ngày
            tg.append(f"T{thu}-Ca{ca}")
    return tg

# ==========================
# STREAMLIT UI
# ==========================
st.title("📅 Xếp lịch học - Khoa CNTT (Hill Climbing)")

st.sidebar.header("Nhập dữ liệu đầu vào")

# Nhập môn học
mon_hoc_input = st.sidebar.text_area("Danh sách môn học (mỗi môn 1 dòng)", 
                                     "AI\nDL\nCSDL\nML\nPython\nToán rời rạc")
mon_hoc = [mh.strip() for mh in mon_hoc_input.split("\n") if mh.strip()]

# Nhập giảng viên (dạng: Môn=GV)
gv_input = st.sidebar.text_area("Danh sách giảng viên (Môn=GV, mỗi dòng 1 cặp)", 
                                "AI=Thầy A\nDL=Thầy B\nCSDL=Cô C\nML=Thầy D\nPython=Cô E\nToán rời rạc=Thầy F")
giang_vien = {}
for line in gv_input.split("\n"):
    if "=" in line:
        mh, gv = line.split("=", 1)
        giang_vien[mh.strip()] = gv.strip()

# Nhập lớp (dạng: Môn=Lớp)
lop_input = st.sidebar.text_area("Danh sách lớp (Môn=Lớp, mỗi dòng 1 cặp)", 
                                 "AI=CNTT1\nDL=CNTT1\nCSDL=CNTT2\nML=CNTT2\nPython=CNTT3\nToán rời rạc=CNTT3")
lop_hoc = {}
for line in lop_input.split("\n"):
    if "=" in line:
        mh, lop = line.split("=", 1)
        lop_hoc[mh.strip()] = lop.strip()

# Phòng học
phong_hoc_input = st.sidebar.text_area("Danh sách phòng học (mỗi phòng 1 dòng)", 
                                       "P101\nP102\nP103\nP201\nP202\nP203")
phong_hoc = [p.strip() for p in phong_hoc_input.split("\n") if p.strip()]

# Thời gian
thoi_gian = tao_thoi_gian()

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
        gv = giang_vien.get(mh, "Unknown GV")
        lop = lop_hoc.get(mh, "Unknown Lop")

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
# CHẠY THUẬT TOÁN
# ==========================
so_lan = st.slider("Số lần lặp tối đa", min_value=100, max_value=5000, value=1000, step=100)
run_button = st.button("Chạy thuật toán")

if run_button:
    best_schedule, best_cost = hill_climbing(so_lan)
    
    st.subheader("✅ Lịch học tối ưu tìm được:")
    st.table([
        {
            "Môn học": mh,
            "Giảng viên": giang_vien.get(mh, "Unknown"),
            "Lớp": lop_hoc.get(mh, "Unknown"),
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
