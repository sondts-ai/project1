import random
import streamlit as st
import pandas as pd

def tao_thoi_gian(so_ngay=6, so_ca=4):
    tg = []
    for thu in range(2, 2 + so_ngay): 
        for ca in range(1, so_ca + 1): 
            tg.append(f"T{thu}-Ca{ca}")
    return tg

def tinh_xung_dot(lich, giang_vien, lop_hoc, mon_phong):
    vi_pham = {
        "Trùng phòng": 0,"Trùng giảng viên": 0, "Trùng lớp": 0,"Sai loại phòng": 0
    }
    da_dung_phong = {}
    da_dung_gv = {}
    da_dung_lop = {}
    for mh, (phong, tg) in lich.items():
        gv = giang_vien[mh]
        lop = lop_hoc[mh]
        if (phong, tg) in da_dung_phong:
            vi_pham["Trùng phòng"] += 1
        else:
            da_dung_phong[(phong, tg)] = mh
        if (gv, tg) in da_dung_gv:
            vi_pham["Trùng giảng viên"] += 1
        else:
            da_dung_gv[(gv, tg)] = mh
        if (lop, tg) in da_dung_lop:
            vi_pham["Trùng lớp"] += 1
        else:
            da_dung_lop[(lop, tg)] = mh
        if mh in mon_phong:
            loai = mon_phong[mh]
            if loai == "may" and not phong.startswith("PM"):
                vi_pham["Sai loại phòng"] += 1
            if loai == "lythuyet" and not phong.startswith("LT"):
                vi_pham["Sai loại phòng"] += 1
    tong = sum(vi_pham.values())
    return vi_pham, tong

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

def hill_climbing_stochastic(mon_hoc, giang_vien, lop_hoc, mon_phong, phong_hoc, thoi_gian, max_iter=1000, patience=50):
    lich = tao_lich_ngau_nhien(mon_hoc, phong_hoc, thoi_gian)
    _, cost = tinh_xung_dot(lich, giang_vien, lop_hoc, mon_phong)
    for _ in range(max_iter):
        improved = False
        for _ in range(patience):
            neighbor = tao_lang_gieng(lich, mon_hoc, phong_hoc, thoi_gian)
            _, new_cost = tinh_xung_dot(neighbor, giang_vien, lop_hoc, mon_phong)
            if new_cost < cost:
                lich, cost = neighbor, new_cost
                improved = True
                break
        if not improved:
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
    loai_phong = st.selectbox("Loại phòng", ["may", "lythuyet"])
    if st.form_submit_button("➕ Thêm môn") and mh and gv and lop:
        st.session_state.ds_mon.append((mh, gv, lop, so_buoi, loai_phong))

if st.session_state.ds_mon:
    st.subheader("📘 Danh sách môn đã nhập")
    st.table(pd.DataFrame(st.session_state.ds_mon, columns=["Môn học", "Giảng viên", "Lớp", "Số buổi", "Loại phòng"]))
    if st.button("🗑️ Xoá tất cả"):
        st.session_state.ds_mon = []
        st.rerun()

if st.button("🚀 Chạy tối ưu lịch") and st.session_state.ds_mon:
    mon_hoc, giang_vien, lop_hoc, mon_phong = [], {}, {}, {}
    for mh, gv, lop, so_buoi, loai in st.session_state.ds_mon:
        for j in range(1, so_buoi + 1):
            slot = f"{mh}_{j}"
            mon_hoc.append(slot)
            giang_vien[slot] = gv
            lop_hoc[slot] = lop
            mon_phong[slot] = loai

    phong_hoc = [f"PM{i:03}" for i in range(1, 16)] + [f"LT{i:03}" for i in range(16, 31)]
    thoi_gian = tao_thoi_gian()

    best_schedule, best_cost = hill_climbing_stochastic(
        mon_hoc, giang_vien, lop_hoc, mon_phong, phong_hoc, thoi_gian,
        max_iter=2000, patience=50
    )

    st.subheader("📌 Kết quả")
    st.write(f"🔍 Số xung đột (tổng quan): {best_cost}")
    if best_cost == 0:
        st.success("✅ Không có xung đột!")
    else:
        st.warning("⚠️ Còn xung đột, hãy thử chạy lại.")

    vi_pham, tong = tinh_xung_dot(best_schedule, giang_vien, lop_hoc, mon_phong)
    st.subheader("📊 Đánh giá chi tiết")
    st.write(f"🔎 Tổng số vi phạm chi tiết: {tong}")
    st.table(pd.DataFrame(list(vi_pham.items()), columns=["Loại vi phạm", "Số lượng"]))

    df = pd.DataFrame([
        {"Thời gian": tg, "Phòng": phong, "Môn": mh, "GV": giang_vien[mh], "Lớp": lop_hoc[mh]}
        for mh, (phong, tg) in best_schedule.items()
    ])
    st.subheader("📌 Lịch chi tiết")
    st.dataframe(df.sort_values(by="Thời gian"), use_container_width=True)
