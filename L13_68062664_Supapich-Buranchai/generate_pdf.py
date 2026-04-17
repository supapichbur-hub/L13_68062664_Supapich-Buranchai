# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

# Register Thai font
for fp in [
    r"C:\Windows\Fonts\THSarabunNew.ttf",
    r"C:\Windows\Fonts\Tahoma.ttf",
    r"C:\Windows\Fonts\tahoma.ttf",
]:
    if os.path.exists(fp):
        pdfmetrics.registerFont(TTFont("Thai", fp))
        FONT = "Thai"
        break
else:
    FONT = "Helvetica"

W, H = A4
CW = W - 4 * cm  # content width


def style(name, **kw):
    defaults = dict(fontName=FONT, fontSize=11, leading=16, textColor=colors.HexColor("#212121"))
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)


def section_header(text):
    t = Table([[Paragraph(text, style("sh", fontSize=12, textColor=colors.white))]],
              colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#1565c0")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def code_block(lines):
    rows = []
    for line in lines:
        safe = (line
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace(" ", "&nbsp;"))
        rows.append([Paragraph(safe, ParagraphStyle(
            "c", fontName="Courier", fontSize=8.5, leading=12,
            textColor=colors.HexColor("#212121")))])
    t = Table(rows, colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f5f5f5")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#bdbdbd")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 8),
        ("TOPPADDING", (0, 1), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -2), 1),
    ]))
    return t


def result_table():
    TH = style("th", fontSize=10, textColor=colors.white, alignment=TA_CENTER)
    TD = style("td", fontSize=10, alignment=TA_CENTER)

    col_w = [2.8*cm, 4.8*cm, 1.8*cm, 4.0*cm, 2.0*cm, 1.8*cm]
    header = [Paragraph(t, TH) for t in
              ["รหัสประชากร", "ชื่อประชากร", "อายุ", "วันที่เพิ่มข้อมูล", "แก้ไข", "ลบ"]]

    data_rows = [
        ("1", "บุญศิริ",                      "40", "March 17, 2025"),
        ("2", "ปัญณภพ",                       "15", "March 17, 2025"),
        ("3", "วราภรณ์",                      "45", "March 17, 2025"),
        ("4", "พิกญา",                        "41", "March 17, 2025"),
        ("5", "เอกชัย",                       "65", "March 26, 2025"),
        ("6", "พิมพ์วิสาข์",                  "39", "March 26, 2025"),
        ("7", "นายราเวิน ไดลัน อาร์เนสัน",   "20", "April 16, 2025"),
    ]

    def btn(label, color):
        t = Table([[Paragraph(label, style("b", fontSize=9, textColor=colors.white,
                                           alignment=TA_CENTER))]], colWidths=[1.5*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(color)),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        return t

    rows = [header]
    for r in data_rows:
        rows.append([Paragraph(r[0], TD), Paragraph(r[1], TD),
                     Paragraph(r[2], TD), Paragraph(r[3], TD),
                     btn("แก้ไข", "#ffc107"), btn("ลบ", "#dc3545")])

    t = Table(rows, colWidths=col_w)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1565c0")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#bdbdbd")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e0e0e0")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        # Highlight last row (student's own entry)
        ("BACKGROUND", (0, 7), (-1, 7), colors.HexColor("#fff9c4")),
    ]))
    return t


def main():
    out = r"C:\Users\ilike\Downloads\lab11\Assignment11_นายราเวิน_ไดลัน_อาร์เนสัน.pdf"
    doc = SimpleDocTemplate(out, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    S = []

    # ── Header bar ──
    hdr = Table([[Paragraph("ICT12367  |  Assignment 11  |  รับส่งข้อมูลจากแบบฟอร์ม",
                             style("hd", fontSize=14, textColor=colors.white,
                                   alignment=TA_CENTER))]],
                colWidths=[CW])
    hdr.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#1a237e")),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    S.append(hdr)
    S.append(Spacer(1, 0.3*cm))

    # ── Student info ──
    S.append(Paragraph("ชื่อ: นายราเวิน ไดลัน อาร์เนสัน",
                        style("s1", fontSize=13, alignment=TA_CENTER,
                              textColor=colors.HexColor("#1a237e"))))
    S.append(Paragraph(
        "รายวิชา: ICT12367 การใช้กรอบงานสำหรับการพัฒนาเว็บแอปพลิเคชันเพื่อความมั่นคงปลอดภัย",
        style("s2", fontSize=11, alignment=TA_CENTER)))
    S.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1565c0"),
                         spaceAfter=10))

    # ── 1. models.py ──
    S.append(section_header("1. models.py  —  เพิ่มฟิลด์ created_date (DateField)"))
    S.append(Spacer(1, 0.2*cm))
    S.append(code_block([
        "from django.db import models",
        "",
        "class Person(models.Model):",
        "    name         = models.CharField(max_length=100)",
        "    age          = models.IntegerField()",
        "    created_date = models.DateField(auto_now_add=True)",
        "",
        "    def __str__(self):",
        "        return self.name",
    ]))
    S.append(Spacer(1, 0.4*cm))

    # ── 2. views.py ──
    S.append(section_header("2. views.py  —  รับค่าจากฟอร์มและบันทึกลงฐานข้อมูล"))
    S.append(Spacer(1, 0.2*cm))
    S.append(code_block([
        "from django.shortcuts import render, redirect",
        "from django.http import HttpResponse",
        "from myapp.models import Person",
        "",
        "def index(request):",
        "    all_person = Person.objects.all()",
        "    return render(request, \"index.html\", {\"all_person\": all_person})",
        "",
        "def form(request):",
        "    if request.method == \"POST\":",
        "        # รับข้อมูลจากฟอร์ม",
        "        name = request.POST.get(\"name\")",
        "        age  = request.POST.get(\"age\")",
        "",
        "        # บันทึกข้อมูลลงฐานข้อมูล",
        "        person = Person.objects.create(",
        "            name=name,",
        "            age=age",
        "        )",
        "",
        "        # เปลี่ยนเส้นทางไปหน้าแรก",
        "        return redirect(\"/\")",
        "    else:",
        "        # แสดงฟอร์ม",
        "        return render(request, \"form.html\")",
    ]))
    S.append(Spacer(1, 0.4*cm))

    # ── 3. index.html ──
    S.append(section_header("3. index.html  —  แสดงตารางพร้อมคอลัมน์วันที่เพิ่มข้อมูล"))
    S.append(Spacer(1, 0.2*cm))
    S.append(code_block([
        "{% block content %}",
        "    <h2 style=\"color: blueviolet;\" class=\"text-center\">ยินดีต้อนรับเข้าสู่ประชากร</h2>",
        "    <table class=\"table table-hover\">",
        "        <thead>",
        "            <tr>",
        "                <th scope=\"col\">รหัสประชากร</th>",
        "                <th scope=\"col\">ชื่อประชากร</th>",
        "                <th scope=\"col\">อายุ</th>",
        "                <th scope=\"col\">วันที่เพิ่มข้อมูล</th>",
        "                <th scope=\"col\">แก้ไข</th>",
        "                <th scope=\"col\">ลบ</th>",
        "            </tr>",
        "        </thead>",
        "        <tbody>",
        "            {% for person in all_person %}",
        "            <tr>",
        "                <th scope=\"row\">{{person.id}}</th>",
        "                <td>{{person.name}}</td>",
        "                <td>{{person.age}}</td>",
        "                <td>{{person.created_date|date:\"F d, Y\"}}</td>",
        "                <td><a href=\"#\" class=\"btn btn-warning btn-sm\">แก้ไข</a></td>",
        "                <td><a href=\"#\" class=\"btn btn-danger btn-sm\">ลบ</a></td>",
        "            </tr>",
        "            {% endfor %}",
        "        </tbody>",
        "    </table>",
        "{% endblock %}",
    ]))
    S.append(Spacer(1, 0.5*cm))

    # ── 4. Result ──
    S.append(section_header("4. ผลลัพธ์  —  ตารางแสดงข้อมูลพร้อมวันที่เพิ่มข้อมูล"))
    S.append(Spacer(1, 0.3*cm))

    # Title bar mock
    tb = Table([[Paragraph("ยินดีต้อนรับสู่เว็บไซต์ของรายวิชา ICT12367",
                            style("tb", fontSize=12, textColor=colors.white,
                                  alignment=TA_CENTER))]],
               colWidths=[CW])
    tb.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#212121")),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    S.append(tb)
    S.append(Spacer(1, 0.3*cm))
    S.append(result_table())

    doc.build(S)
    print("PDF saved successfully.")


if __name__ == "__main__":
    main()
