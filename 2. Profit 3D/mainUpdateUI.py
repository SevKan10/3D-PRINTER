import customtkinter as ctk
import json
from tkinter import messagebox

ctk.set_appearance_mode("system")  # "light", "dark", "system"
ctk.set_default_color_theme("blue")  # Có thể dùng "green", "dark-blue", v.v.

def tinh_tien_in():
    try:
        loai_nhua = combo_loai.get()
        khoi_luong = float(entry_khoi_luong.get())
        gio = int(entry_gio.get())
        phut = int(entry_phut.get())
        thoi_gian = gio + phut / 60
    except ValueError:
        messagebox.showerror("Lỗi nhập liệu", "Vui lòng nhập đúng định dạng số.")
        return

    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file 'config.json'")
        return
    except json.JSONDecodeError:
        messagebox.showerror("Lỗi", "File 'config.json' bị lỗi định dạng.")
        return

    loi_nhuan_phan_tram = config.get("loi_nhuan", 25)
    cong_suat_watt = config.get("cong_suat_watt", 310)
    tien_cong_moi_gio = config.get("tien_cong_moi_gio", 10000)
    hao_mon_moi_gio = config.get("hao_mon_moi_gio", 5000)
    gia_nhua_raw = config.get("gia_nhua", {})
    gia_dien = config.get("gia_dien", {})

    gia_nhua = {k: v / 1000 for k, v in gia_nhua_raw.items()}

    if loai_nhua not in gia_nhua:
        messagebox.showerror("Lỗi", f"Không tìm thấy giá cho loại nhựa '{loai_nhua}' trong config.")
        return

    def tinh_tien_dien(kwh):
        bac1 = gia_dien.get("bac1", 1984)
        bac2 = gia_dien.get("bac2", 2050)
        bac3 = gia_dien.get("bac3", 2380)
        bac4 = gia_dien.get("bac4", 2998)

        if kwh <= 50:
            return kwh * bac1
        elif kwh <= 100:
            return 50 * bac1 + (kwh - 50) * bac2
        elif kwh <= 200:
            return 50 * bac1 + 50 * bac2 + (kwh - 100) * bac3
        else:
            return 50 * bac1 + 50 * bac2 + 100 * bac3 + (kwh - 200) * bac4

    cong_suat_kw = cong_suat_watt / 1000
    dien_tieu_thu = cong_suat_kw * thoi_gian

    tien_nhua = gia_nhua[loai_nhua] * khoi_luong
    tien_dien = tinh_tien_dien(dien_tieu_thu)
    tien_hao_mon = thoi_gian * hao_mon_moi_gio
    tien_cong = thoi_gian * tien_cong_moi_gio

    tong_chi_phi = tien_nhua + tien_dien + tien_hao_mon + tien_cong

    T = 1 + loi_nhuan_phan_tram / 100
    Tt = loi_nhuan_phan_tram
    gia_ban = tong_chi_phi * T

    ket_qua = f"""\n\
Thời gian in: {gio} giờ {phut} phút
Tiền nhựa: {round(tien_nhua):,} VNĐ
Tiền điện: {round(tien_dien):,} VNĐ
Hao mòn máy: {round(tien_hao_mon):,} VNĐ
Tiền công: {round(tien_cong):,} VNĐ
----------------------------
Tổng chi phí: {round(tong_chi_phi):,} VNĐ
Giá bán ({Tt}% lời): {round(gia_ban):,} VNĐ
Tổng lời: {round(gia_ban - tong_chi_phi):,} VNĐ
"""
    text_kq.configure(state="normal")
    text_kq.delete("1.0", "end")
    text_kq.insert("end", ket_qua)
    text_kq.configure(state="disabled")

# === GUI ===
app = ctk.CTk()
app.title("Tính tiền in 3D")
app.geometry("460x560")
app.resizable(False, False)

ctk.CTkLabel(app, text="Chọn loại nhựa:").pack(pady=(10, 0))
combo_loai = ctk.CTkComboBox(app, values=["PLA", "PLA+", "ABS", "PETG"])
combo_loai.set("PLA")
combo_loai.pack(pady=5)

ctk.CTkLabel(app, text="Khối lượng nhựa cần in (g):").pack()
entry_khoi_luong = ctk.CTkEntry(app, placeholder_text="VD: 150")
entry_khoi_luong.pack(pady=5)

ctk.CTkLabel(app, text="Thời gian in:").pack()
frame_time = ctk.CTkFrame(app)
frame_time.pack(pady=5)

entry_gio = ctk.CTkEntry(frame_time, width=60, placeholder_text="Giờ")
entry_gio.pack(side="left", padx=5)
entry_phut = ctk.CTkEntry(frame_time, width=60, placeholder_text="Phút")
entry_phut.pack(side="left", padx=5)

ctk.CTkButton(app, text="Tính tiền", command=tinh_tien_in).pack(pady=15)

text_kq = ctk.CTkTextbox(app, height=200, width=420, font=("Consolas", 11))
text_kq.pack(pady=5)
text_kq.configure(state="disabled")

app.mainloop()
