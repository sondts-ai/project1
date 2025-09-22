import random
import streamlit as st
import pandas as pd

def tao_thoi_gian(so_ngay=6, so_ca=4):
    tg = []
    for thu in range(2, 2 + so_ngay): 
        for ca in range(1, so_ca + 1): 
            tg.append(f"T{thu}-Ca{ca}")
    return tg

def tinh_xung_dot(lich, giang_vien, lop_hoc):
    xung_dot = 0
    da_dung = {}
    for mh, (phong, tg) in lich.items():
        gv = giang_vien.get(mh, "Unknown GV")
        lop = lop_hoc.get(mh, "Unknown Lop")

        if (phong, tg) in da_dung: 
            xung_dot += 1
        else: 
            da_dung[(phong, tg)] = mh

        if (gv, tg) in da_dung: 
            xung_dot += 1
        else: 
            da_dung[(gv, tg)] = mh

        if (lop, tg) in da_dung: 
            xung_dot += 1
        else: 
            da_dung[(lop, tg)] = mh
    return xung_dot

def tao_lich_ngau_nhien(mon_hoc, phong_hoc, thoi_gian):
    lich = {}
    for mh in mon_hoc:
        phong = random.choice(phong_hoc)
        tg = random.choice(thoi_gian)
        lich[mh] = (phong, tg)
    return lich

def tao_lang_gieng(lich, mon_hoc, phong_hoc, thoi_gian):
    new_lich = lich.copy()
    mh = random.choice(mon_hoc)
    new_lich[mh] = (random.choice(phong_hoc), random.choice(thoi_gian))
    return new_lich

def hill_climbing_stochastic(mon_hoc, giang_vien, lop_hoc, phong_hoc, thoi_gian, max_iter=1000, patience=50):
    lich = tao_lich_ngau_nhien(mon_hoc, phong_hoc, thoi_gian)
    cost = tinh_xung_dot(lich, giang_vien, lop_hoc)

    for _ in range(max_iter):
        improved = False
        for _ in range(patience):  # số lần thử hàng xóm trong mỗi vòng lặp
            neighbor = tao_lang_gieng(lich, mon_hoc, phong_hoc, thoi_gian)
            new_cost = tinh_xung_dot(neighbor, giang_vien, lop_hoc)
            if new_cost < cost:  # nhận hàng xóm tốt hơn
                lich, cost = neighbor, new_cost
                improved = True
                break
        if not improved:  # không tìm thấy hàng xóm tốt hơn
            break
        if cost == 0:
            break

    return lich, cost

st.title("📅 Lập lịch học bằng Stochastic Hill Climbing")

if "ds_mon" not in st.session_state:
    st.session_state.ds_mon = []

with st.form("them_mon", clear_on_submit=True):
    mh = st.text_input("Tên môn")
    gv = st.text_input("Giảng viên")
    lop = st.text_input("Lớp")
    so_buoi = st.number_input("Số buổi", min_value=1, step=1, value=1)
    if st.form_submit_button("➕ Thêm môn") and mh and gv and lop:
        st.session_state.ds_mon.append((mh, gv, lop, so_buoi))
if st.session_state.ds_mon:
    st.subheader("📘 Danh sách môn đã nhập")
    st.table(pd.DataFrame(st.session_state.ds_mon, columns=["Môn học", "Giảng viên", "Lớp", "Số buổi"]))
    if st.button("🗑️ Xoá tất cả"):
        st.session_state.ds_mon = []
        st.rerun()
if st.button("🚀 Chạy tối ưu lịch") and st.session_state.ds_mon:
    mon_hoc, giang_vien, lop_hoc = [], {}, {}
    for mh, gv, lop, so_buoi in st.session_state.ds_mon:
        for j in range(1, so_buoi + 1):
            slot = f"{mh}_{j}"
            mon_hoc.append(slot)
            giang_vien[slot] = gv
            lop_hoc[slot] = lop
    phong_hoc = [f"P{i:03}" for i in range(1, 31)]
    thoi_gian = tao_thoi_gian()

    best_schedule, best_cost = hill_climbing_stochastic(
        mon_hoc, giang_vien, lop_hoc, phong_hoc, thoi_gian,
        max_iter=2000, patience=50
    )
    st.subheader("📌 Kết quả")
    st.write(f"🔍 Số xung đột: {best_cost}")
    if best_cost == 0:
        st.success("✅ Không có xung đột!")
    else:
        st.warning("⚠️ Còn xung đột, hãy thử chạy lại.")

    df = pd.DataFrame([
        {"Thời gian": tg, "Phòng": phong, "Môn": mh, "GV": giang_vien[mh], "Lớp": lop_hoc[mh]}
        for mh, (phong, tg) in best_schedule.items()
    ])
    st.subheader("📌 Lịch chi tiết")
    st.dataframe(df.sort_values(by="Thời gian"), use_container_width=True)
