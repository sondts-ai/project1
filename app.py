import random
import sys

# ==========================
# TẠO THỜI GIAN (T2–T7, 4 ca/ngày)
# ==========================
def tao_thoi_gian():
    tg = []
    for thu in range(2, 8):  # T2 -> T7
        for ca in range(1, 5):  # 4 ca/ngày
            tg.append(f"T{thu}-Ca{ca}")
    return tg

# ==========================
# HÀM ĐÁNH GIÁ
# ==========================
def tinh_xung_dot(lich, giang_vien, lop_hoc):
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
# TẠO LỊCH NGẪU NHIÊN
# ==========================
def tao_lich_ngau_nhien(mon_hoc, phong_hoc, thoi_gian):
    return {
        mh: (random.choice(phong_hoc), random.choice(thoi_gian))
        for mh in mon_hoc
    }

# ==========================
# TẠO LÁNG GIỀNG
# ==========================
def tao_lang_gieng(lich, mon_hoc, phong_hoc, thoi_gian):
    new_lich = lich.copy()
    mh = random.choice(mon_hoc)
    new_lich[mh] = (random.choice(phong_hoc), random.choice(thoi_gian))
    return new_lich

# ==========================
# THUẬT TOÁN LEO ĐỒI
# ==========================
def hill_climbing(mon_hoc, giang_vien, lop_hoc, phong_hoc, thoi_gian, max_iter=1000):
    lich = tao_lich_ngau_nhien(mon_hoc, phong_hoc, thoi_gian)
    cost = tinh_xung_dot(lich, giang_vien, lop_hoc)

    for _ in range(max_iter):
        neighbor = tao_lang_gieng(lich, mon_hoc, phong_hoc, thoi_gian)
        new_cost = tinh_xung_dot(neighbor, giang_vien, lop_hoc)

        if new_cost < cost:
            lich, cost = neighbor, new_cost

        if cost == 0:
            break

    return lich, cost

# ==========================
# CHẠY Ở CONSOLE
# ==========================
def run_console():
    print("📌 Chạy chế độ console\n")

    # Nhập môn học
    mon_hoc = input("Nhập danh sách môn học (cách nhau bởi dấu phẩy, mặc định: AI,DL,CSDL,ML,Python,Toán rời rạc): ")
    if not mon_hoc.strip():
        mon_hoc = ["AI", "DL", "CSDL", "ML", "Python", "Toán rời rạc"]
    else:
        mon_hoc = [mh.strip() for mh in mon_hoc.split(",")]

    # Nhập giảng viên
    giang_vien = {}
    for mh in mon_hoc:
        gv = input(f"Nhập giảng viên cho môn {mh}: ")
        giang_vien[mh] = gv if gv.strip() else f"GV_{mh}"

    # Nhập lớp
    lop_hoc = {}
    for mh in mon_hoc:
        lop = input(f"Nhập lớp cho môn {mh}: ")
        lop_hoc[mh] = lop if lop.strip() else f"Lop_{mh}"

    # Nhập phòng học
    phong_input = input("Nhập danh sách phòng học (cách nhau bởi dấu phẩy, mặc định: P101,P102,P103,P201,P202,P203): ")
    if not phong_input.strip():
        phong_hoc = ["P101", "P102", "P103", "P201", "P202", "P203"]
    else:
        phong_hoc = [p.strip() for p in phong_input.split(",")]

    # Thời gian
    thoi_gian = tao_thoi_gian()

    # Chạy hill climbing
    lich, cost = hill_climbing(mon_hoc, giang_vien, lop_hoc, phong_hoc, thoi_gian, max_iter=2000)

    print("\n✅ Lịch học tối ưu:")
    for mh, (phong, tg) in lich.items():
        print(f"{mh:<15} | {giang_vien[mh]:<10} | {lop_hoc[mh]:<8} | {phong:<5} | {tg}")

    print(f"\n🔍 Số xung đột: {cost}")
    if cost == 0:
        print("🎉 Tìm được lịch không xung đột!")
    else:
        print("⚠️ Vẫn còn xung đột, có thể chạy lại hoặc tăng số lần lặp.")

# ==========================
# MAIN
# ==========================
if __name__ == "__main__":
    if "streamlit" in sys.argv[0]:  # Nếu chạy bằng streamlit
        import streamlit as st

        st.title("📅 Xếp lịch học - Hill Climbing")

        # Sidebar input
        mon_hoc_input = st.sidebar.text_area("Môn học", "AI\nDL\nCSDL\nML\nPython\nToán rời rạc")
        mon_hoc = [mh.strip() for mh in mon_hoc_input.split("\n") if mh.strip()]

        gv_input = st.sidebar.text_area("Giảng viên (Môn=GV)", 
                                        "AI=Thầy A\nDL=Thầy B\nCSDL=Cô C\nML=Thầy D\nPython=Cô E\nToán rời rạc=Thầy F")
        giang_vien = {mh.strip(): gv.strip() for mh, gv in (line.split("=") for line in gv_input.split("\n") if "=" in line)}

        lop_input = st.sidebar.text_area("Lớp (Môn=Lớp)", 
                                         "AI=CNTT1\nDL=CNTT1\nCSDL=CNTT2\nML=CNTT2\nPython=CNTT3\nToán rời rạc=CNTT3")
        lop_hoc = {mh.strip(): lop.strip() for mh, lop in (line.split("=") for line in lop_input.split("\n") if "=" in line)}

        phong_hoc_input = st.sidebar.text_area("Phòng học", "P101\nP102\nP103\nP201\nP202\nP203")
        phong_hoc = [p.strip() for p in phong_hoc_input.split("\n") if p.strip()]

        thoi_gian = tao_thoi_gian()

        so_lan = st.slider("Số lần lặp tối đa", 100, 5000, 1000, 100)
        run_button = st.button("Chạy thuật toán")

        if run_button:
            best_schedule, best_cost = hill_climbing(mon_hoc, giang_vien, lop_hoc, phong_hoc, thoi_gian, max_iter=so_lan)
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
                st.warning("⚠️ Vẫn còn xung đột, có thể chạy lại hoặc tăng số lần lặp.")
    else:
        run_console()
