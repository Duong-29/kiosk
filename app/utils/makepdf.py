from fpdf import FPDF
import io, math
from datetime import datetime, date

def info_line(pdf, label, value):
    pdf.cell(60,10, txt=label, align="L")
    pdf.cell(0,10, txt=value, align="R", ln=True)

def round_like_js(value):
    return int(math.floor(float(value) + 0.5))

def to_str(value):
    if isinstance(value, (datetime, date)):
        return value.strftime("%Y-%m-%d %H:%M:%S") if isinstance(value, datetime) else value.strftime("%Y-%m-%d")
    return str(value)

def makePDF(info):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DEjaVu", "", "font/dejavu-sans.ttf", uni=True)
    pdf.set_font("DejaVu", size=14)

    pdf.set_font_size(23)
    pdf.cell(0, 10,"PHIẾU KHÁM BỆNH", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font_size(16)
    info_line(pdf, "Họ tên:", info[1])
    info_line(pdf, "Giới tính:", "Nam" if info[2] == 1 else "Nữ")
    info_line(pdf, "Ngày sinh:", to_str(info[3]))
    info_line(pdf, "CCCD:", info[0])
    info_line(pdf, "Bảo hiểm y tế:", "Có" if info[7] == 1 else "Không")
    info_line(pdf, "Phiếu áp dụng bảo hiểm y tế:", "Có" if info[13] == 1 else "Không")
    info_line(pdf, "Dịch vụ:", info[9])
    info_line(pdf, "Phòng khám:", info[10])
    info_line(pdf, "Địa chỉ phòng:", info[11])
    info_line(pdf, "Số phiếu đợi:", str(info[4]))
    info_line(pdf, "Bác sĩ:", info[12])
    info_line(pdf, "Thời gian đăng ký:", to_str(info[5]))
    info_line(pdf, "Giá dịch vụ:", str(f"{round_like_js(info[6] * 26181):,} VNĐ"))