import os
import sys
import shutil
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.abspath(r"D:\smart-parking-system")
BAO_CAO_DIR = os.path.join(PROJECT_DIR, "bao_cao_de_xuat")
os.makedirs(BAO_CAO_DIR, exist_ok=True)
USER_DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads")

LOGO_PATH = os.path.join(PROJECT_DIR, "extracted_media", "word", "media", "image1.png")

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=120, right=120):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="000000", sz="8", val="single"):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'</w:tblBorders>'
        )
        tblPr[0].append(borders)

def add_header_table(doc, topic_text="Đề tài: Smart Parking System – Hệ thống quản lý bãi đỗ xe thông minh"):
    table = doc.add_table(rows=1, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table, color="000000", sz="8", val="single")

    widths = [Cm(3.8), Cm(9.6), Cm(4.2)]

    # Cột 1: Logo
    cell0 = table.rows[0].cells[0]
    cell0.width = widths[0]
    set_cell_margins(cell0, top=120, bottom=120, left=120, right=120)
    p0 = cell0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists(LOGO_PATH):
        r_logo = p0.add_run()
        r_logo.add_picture(LOGO_PATH, width=Inches(1.2))
    else:
        r_txt = p0.add_run("PHENIKAA\nUNIVERSITY")
        r_txt.font.name = 'Times New Roman'
        r_txt.font.size = Pt(10)
        r_txt.bold = True

    # Cột 2: Tiêu đề biên bản
    cell1 = table.rows[0].cells[1]
    cell1.width = widths[1]
    set_cell_margins(cell1, top=120, bottom=120, left=120, right=120)
    p1 = cell1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.line_spacing = 1.15
    p1.paragraph_format.space_before = Pt(2)
    p1.paragraph_format.space_after = Pt(2)

    r1_1 = p1.add_run("BIÊN BẢN HỌP NHÓM VÀ BÁO CÁO TIẾN ĐỘ CÔNG VIỆC\n")
    r1_1.font.name = 'Times New Roman'
    r1_1.font.size = Pt(11)
    r1_1.bold = True

    r1_2 = p1.add_run("(Học phần: Phát triển ứng dụng Hệ thống thông tin)\n")
    r1_2.font.name = 'Times New Roman'
    r1_2.font.size = Pt(9.5)
    r1_2.italic = True

    r1_3 = p1.add_run(topic_text)
    r1_3.font.name = 'Times New Roman'
    r1_3.font.size = Pt(10)
    r1_3.bold = True

    # Cột 3: Mã số BM
    cell2 = table.rows[0].cells[2]
    cell2.width = widths[2]
    set_cell_margins(cell2, top=120, bottom=120, left=120, right=120)
    p2 = cell2.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p2.paragraph_format.line_spacing = 1.15
    p2.paragraph_format.space_before = Pt(2)
    p2.paragraph_format.space_after = Pt(2)

    r2_1 = p2.add_run("Mã số: BM.CNTT.01.06\nLần ban hành: 01")
    r2_1.font.name = 'Times New Roman'
    r2_1.font.size = Pt(9.5)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(6)

def add_signature_table(doc, leader_name="Phạm Văn Đạt", instructor_name="ThS. Nguyễn Thị Thùy Liên"):
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table, color="FFFFFF", sz="0", val="none")

    widths = [Cm(8.8), Cm(8.8)]

    # Cột 1: Giảng viên
    c0 = table.rows[0].cells[0]
    c0.width = widths[0]
    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0.paragraph_format.line_spacing = 1.15
    r0 = p0.add_run(f"GIẢNG VIÊN HƯỚNG DẪN\n\n\n\n\n{instructor_name}\n(Ký và ghi rõ họ tên)")
    r0.font.name = 'Times New Roman'
    r0.font.size = Pt(11)
    r0.bold = True

    # Cột 2: Nhóm trưởng
    c1 = table.rows[0].cells[1]
    c1.width = widths[1]
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.line_spacing = 1.15
    r1 = p1.add_run(f"NHÓM TRƯỞNG\n\n\n\n\n{leader_name}\n(Ký và ghi rõ họ tên)")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(11)
    r1.bold = True

def add_heading_section(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.bold = True
    return p

def add_bullet(doc, text, bold_prefix=""):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.left_indent = Cm(0.6)
    r_sym = p.add_run("• ")
    r_sym.font.name = 'Times New Roman'
    r_sym.font.size = Pt(10.5)
    r_sym.bold = True
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(10.5)
        r_pre.bold = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10.5)
    return p

def add_dash_bullet(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.left_indent = Cm(0.6)
    r_sym = p.add_run("– ")
    r_sym.font.name = 'Times New Roman'
    r_sym.font.size = Pt(10.5)
    r_sym.bold = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10.5)
    return p

# ==============================================================================
# TẠO FILE BÁO CÁO TIẾN ĐỘ ĐỢT 3 CHUẨN MẪU BM.CNTT.01.06 (GIỐNG HỆT ĐỢT 2)
# ==============================================================================
def create_dot_3():
    print("-> Đang tạo Báo cáo tiến độ Đợt 3 chuẩn mẫu BM.CNTT.01.06 (giống hệt Đợt 2) ...")
    doc = Document()
    for s in doc.sections:
        s.top_margin = Cm(1.70)
        s.bottom_margin = Cm(1.70)
        s.left_margin = Cm(1.80)
        s.right_margin = Cm(1.80)
        s.page_width = Cm(21.0)
        s.page_height = Cm(29.7)

    add_header_table(doc, "Đề tài: Smart Parking System – Hệ thống quản lý bãi đỗ xe thông minh")

    add_heading_section(doc, "1. Thời gian và địa điểm")
    add_bullet(doc, "19h30 – 21h30, ngày 22/10/2026.", bold_prefix="Thời gian: ")
    add_bullet(doc, "Họp trực tuyến qua ứng dụng Google Meet kết hợp kiểm thử trực tiếp trên môi trường máy chủ cục bộ.", bold_prefix="Địa điểm: ")

    add_heading_section(doc, "2. Thành phần tham dự")
    add_bullet(doc, "Đầy đủ các thành viên trong nhóm nghiên cứu đề tài (Nhóm 4):")
    add_bullet(doc, "Phạm Văn Đạt – Trưởng nhóm / Chủ tọa cuộc họp (MSV: 23017150).")
    add_bullet(doc, "Nguyễn Duy Bảo – Kỹ sư Giao diện & Trải nghiệm người dùng / Thư ký cuộc họp (MSV: 23017133).")
    add_bullet(doc, "Trần Tuấn Anh – Kỹ sư Thuật toán & Trí tuệ nhân tạo / Thành viên (MSV: 23017118).")

    add_heading_section(doc, "3. Nội dung chi tiết")
    add_bullet(doc, "Đánh giá tiến độ hoàn thành các hạng mục chuyển tiếp từ Tuần 8 sang Tuần 9 của đồ án Smart Parking System: Mô hình học máy (Machine Learning) Random Forest Regressor đã được huấn luyện với 200 Decision Trees, đạt sai số thấp MAE = 0.058 và được đóng gói thành file Singleton model .joblib nạp sẵn vào FastAPI.")
    add_bullet(doc, "Tích hợp toàn diện Client-Server và kiểm tra chuẩn hóa API: Rà soát toàn bộ 28 RESTful API endpoints, xác nhận 100% các điểm gọi API từ giao diện Frontend Vue 3 / GSAP 3 đều kết nối đồng bộ và phản hồi chuẩn xác.")
    add_bullet(doc, "Báo cáo kết quả kiểm thử tự động toàn diện (QA): Chạy bộ kiểm thử tự động Pytest đạt tuyệt đối 24/24 ca kiểm thử PASSED 100% (bao gồm A* né vật cản, Machine Learning Engine, Concurrency Stress Test 50 workers chứng minh triệt tiêu xung đột Double-booking, quản lý hồ sơ xe và vé tháng cư dân).")
    add_bullet(doc, "Khắc phục triệt để lỗi thời gian của vé tháng mẫu tĩnh (Time-bomb Bug): Gia hạn vé mẫu PASS-8801 đến ngày 31/12/2027 và bổ sung cơ chế thiết lập ngày động (Dynamic Date Test Isolation) trong fixture Pytest, bảo đảm bộ test vĩnh viễn không bị flaky do thời gian trôi qua.")
    add_bullet(doc, "Đóng gói công cụ khởi chạy tự động 1-Click (run_web.bat): Tự động bật đồng thời Backend FastAPI (port 8000), Frontend Web Server (port 3000) và tự động mở trình duyệt web localhost:3000 phục vụ demo nghiệm thu nhanh chóng.")
    add_bullet(doc, "Hoàn thiện trọn bộ hồ sơ đồ án phục vụ bảo vệ trước Hội đồng: Báo cáo thuyết minh toàn diện 85+ trang chuẩn mẫu Phenikaa (BAO_CAO_DACS), Kế hoạch 10 tuần, 2 Biên bản họp nhóm trước, Tuyển tập 50 câu hỏi & trả lời bảo vệ đồ án, Kịch bản thuyết trình và slide PowerPoint.")

    add_heading_section(doc, "3.1. Thời gian thực hiện")
    add_bullet(doc, "Giai đoạn Đợt 3 (Tuần 8 – Tuần 9): từ 12/10/2026 đến 22/10/2026 (Hoàn thành 100% khối lượng đề tài, chuẩn bị nghiệm thu ở Tuần 10).")

    add_heading_section(doc, "3.2. Đánh giá tiến độ công việc")

    # Bảng đánh giá chi tiết 7 cột (y hệt đợt 2)
    headers_t2 = ["TT", "Mã sinh viên", "Họ và tên", "Nhiệm vụ phân công", "Nội dung đã/đang thực hiện", "Đánh giá tiến độ", "Ghi chú"]
    rows_t2 = [
        [
            "1",
            "23017150",
            "Phạm Văn Đạt",
            "Backend Core – Concurrency Lock – Dynamic Test Fixture – 1-Click Launcher (run_web.bat)",
            "Tối ưu hóa các API Backend; khắc phục triệt để lỗi hết hạn dữ liệu vé tháng mẫu trên đĩa và trong test suite; chạy stress test 50 workers chứng minh triệt tiêu Double-booking; đóng gói script run_web.bat kích hoạt đồng thời Backend, Frontend và mở trình duyệt tự động; hoàn thiện báo cáo thuyết minh đồ án.",
            "Hoàn thành 100%",
            "Đã đưa 24/24 unit test đạt Passed 100%; hệ thống ổn định tuyệt đối, sẵn sàng nghiệm thu."
        ],
        [
            "2",
            "23017133",
            "Nguyễn Duy Bảo",
            "Frontend UI/UX – GSAP 3 Animation – QR Scanner – API Integration",
            "Hoàn thiện giao diện Dark Cyber trên Vue 3 và Tailwind CSS; tối ưu hóa diễn hoạt xe ảo bám lộ trình A* bằng GSAP 3; kết nối đồng bộ 18 API endpoints với Backend; hoàn thiện modal quét mã QR barrier, xuất hóa đơn điện tử và giao diện đăng ký vé tháng cư dân; chuẩn bị slide PowerPoint thuyết trình.",
            "Hoàn thành 100%",
            "Giao diện trực quan, mượt mà, hiệu ứng chuyển động ấn tượng và phản hồi nhanh."
        ],
        [
            "3",
            "23017118",
            "Trần Tuấn Anh",
            "A* Pathfinding Optimization – Random Forest Regressor – Model Joblib – QA Defense",
            "Tối ưu hóa hàm Heuristic Manhattan và hàng đợi heapq cho thuật toán A* (độ trễ < 5ms); hoàn thiện pipeline 4.320 mẫu lịch sử, huấn luyện mô hình Random Forest 200 cây quyết định đạt sai số MAE = 0.058, R² = 0.912; tích hợp nạp model .joblib vào API dự báo 24h; hoàn thiện Bộ 50 câu hỏi & trả lời phản biện đồ án.",
            "Hoàn thành 100%",
            "Mô hình AI có độ chính xác cao; tài liệu phản biện đầy đủ dẫn chứng khoa học và thực nghiệm."
        ]
    ]

    t2 = doc.add_table(rows=len(rows_t2) + 1, cols=len(headers_t2))
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t2, color="000000", sz="8", val="single")

    col_w2 = [Cm(1.0), Cm(2.2), Cm(3.0), Cm(3.8), Cm(4.6), Cm(2.2), Cm(2.4)]

    for c_idx, heading in enumerate(headers_t2):
        cell = t2.rows[0].cells[c_idx]
        cell.width = col_w2[c_idx]
        set_cell_background(cell, "E7E6E6")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(heading)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9.5)
        r.bold = True

    for r_idx, r_vals in enumerate(rows_t2):
        row = t2.rows[r_idx + 1]
        for c_idx, val in enumerate(r_vals):
            cell = row.cells[c_idx]
            cell.width = col_w2[c_idx]
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            if c_idx in [0, 1, 5]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.0)
            if c_idx == 5:
                r.bold = True
                r.font.color.rgb = RGBColor(21, 128, 61)

    p_sp_t2 = doc.add_paragraph()
    p_sp_t2.paragraph_format.space_after = Pt(4)

    add_heading_section(doc, "4. Kế hoạch công việc sau cuộc họp")
    add_bullet(doc, "Tiếp tục duy trì môi trường chạy ổn định trên file run_web.bat, kiểm tra lại các trường hợp biên của cơ sở dữ liệu trước buổi báo cáo với giảng viên hướng dẫn.")
    add_bullet(doc, "Rà soát in ấn và đóng quyển Báo cáo thuyết minh đồ án chuẩn mẫu Phenikaa (BAO_CAO_DACS_Smart_Parking_System.docx) cùng toàn bộ hồ sơ nghiệm thu.")
    add_bullet(doc, "Tổng duyệt kịch bản thuyết trình slide (thời lượng 15 - 20 phút), phân chia thứ tự trình bày giữa 3 thành viên: Đạt (Tổng quan, Kiến trúc, Backend, Database), Bảo (Giao diện Vue 3, GSAP, Demo vận hành), Tuấn Anh (Thuật toán A*, Mô hình AI Random Forest, Đánh giá kết quả).")
    add_bullet(doc, "Luyện tập trả lời các câu hỏi phản biện chuyên sâu từ Hội đồng dựa trên Tuyển tập 50 câu hỏi & trả lời đã biên soạn.")

    add_heading_section(doc, "5. Kết luận cuộc họp")
    p_conclusion = doc.add_paragraph()
    p_conclusion.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_conclusion.paragraph_format.space_before = Pt(0)
    p_conclusion.paragraph_format.space_after = Pt(8)
    p_conclusion.paragraph_format.line_spacing = 1.15
    r_c = p_conclusion.add_run("Nhóm 4 đã hoàn thành 100% khối lượng công việc theo đúng Đề xuất dự án và Kế hoạch 10 tuần đã cam kết với Khoa và Giảng viên hướng dẫn. Hệ thống Smart Parking System vận hành mượt mà, ổn định, thuật toán A* và mô hình học máy Random Forest hoạt động chính xác cao, toàn bộ các chức năng đã được kiểm thử chặt chẽ với 24/24 unit test đạt chuẩn. Toàn nhóm tự tin, đoàn kết và sẵn sàng bước vào buổi bảo vệ đồ án trước Hội đồng nghiệm thu đạt kết quả cao nhất.")
    r_c.font.name = 'Times New Roman'
    r_c.font.size = Pt(10.5)

    p_sp_sig = doc.add_paragraph()
    p_sp_sig.paragraph_format.space_after = Pt(8)

    add_signature_table(doc, leader_name="Phạm Văn Đạt", instructor_name="ThS. Nguyễn Thị Thùy Liên")

    # Lưu thành nhiều tên file để người dùng dễ tìm
    target_names = [
        "BaoCaoTienDo-Dot3.docx",
        "Bien_ban_hop_nhom_SmartParking_Tuan_8_9_22-10-2026.docx",
        "BaoCaoTienDo_Dot3_SmartParking.docx"
    ]

    for fname in target_names:
        p_root = os.path.join(PROJECT_DIR, fname)
        p_bao_cao = os.path.join(BAO_CAO_DIR, fname)
        p_dl = os.path.join(USER_DOWNLOADS, fname)

        doc.save(p_root)
        shutil.copy2(p_root, p_bao_cao)
        try:
            shutil.copy2(p_root, p_dl)
        except Exception as e:
            print(f"Notice copy {fname} to Downloads: {e}")
        print(f"SUCCESS: Saved {fname} at root, bao_cao_de_xuat, and Downloads!")

    # Đồng thời tạo file BaoCaoTienDo-Dot2.docx nếu người dùng muốn đối chiếu
    dot2_source = os.path.join(BAO_CAO_DIR, "Bien_ban_hop_nhom_SmartParking_Tuan_6_7_30-09-2026.docx")
    if os.path.exists(dot2_source):
        shutil.copy2(dot2_source, os.path.join(PROJECT_DIR, "BaoCaoTienDo-Dot2.docx"))
        shutil.copy2(dot2_source, os.path.join(BAO_CAO_DIR, "BaoCaoTienDo-Dot2.docx"))
        try:
            shutil.copy2(dot2_source, os.path.join(USER_DOWNLOADS, "BaoCaoTienDo-Dot2.docx"))
        except Exception:
            pass
        print("SUCCESS: Copied exact Dot 2 file to BaoCaoTienDo-Dot2.docx!")

if __name__ == "__main__":
    create_dot_3()
