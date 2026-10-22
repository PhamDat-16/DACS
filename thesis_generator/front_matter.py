import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from thesis_generator.style_helper import (
    set_cell_background, set_cell_margins, set_table_borders,
    add_body_paragraph, add_bullet_item, add_table_data
)

def add_cover_page(doc, logo_path):
    """
    Trang bìa chính theo chuẩn Trường Đại học Phenikaa - Khoa Khoa học Máy tính
    Nhóm 4 - Đề tài Smart Parking System
    GVHD: ThS. Nguyễn Thị Thùy Liên
    Thành viên: Phạm Văn Đạt (Trưởng nhóm), Nguyễn Duy Bảo, Trần Tuấn Anh
    """
    # Header tổ chức
    p1 = doc.add_paragraph()
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_before = Pt(0)
    p1.paragraph_format.space_after = Pt(2)
    r1 = p1.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\nTRƯỜNG ĐẠI HỌC PHENIKAA\nKHOA KHOA HỌC MÁY TÍNH")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(13)
    r1.bold = True
    
    # Dòng kẻ phân cách nhỏ
    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line.paragraph_format.space_before = Pt(0)
    p_line.paragraph_format.space_after = Pt(14)
    r_l = p_line.add_run("-----------------------***-----------------------")
    r_l.font.name = 'Times New Roman'
    r_l.font.size = Pt(11)
    r_l.bold = True

    # Logo trường
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(4)
        p_logo.paragraph_format.space_after = Pt(18)
        run_logo = p_logo.add_run()
        run_logo.add_picture(logo_path, width=Inches(1.8))

    # Loại báo cáo
    p_type = doc.add_paragraph()
    p_type.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_type.paragraph_format.space_before = Pt(12)
    p_type.paragraph_format.space_after = Pt(8)
    r_t = p_type.add_run("BÁO CÁO ĐỒ ÁN HỌC PHẦN\nPHÁT TRIỂN ỨNG DỤNG HỆ THỐNG THÔNG TIN")
    r_t.font.name = 'Times New Roman'
    r_t.font.size = Pt(15)
    r_t.bold = True
    r_t.font.color.rgb = RGBColor(30, 58, 138)

    # Tên đề tài
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(16)
    r_title = p_title.add_run("ĐỀ TÀI:\nNGHIÊN CỨU, THIẾT KẾ VÀ XÂY DỰNG HỆ THỐNG QUẢN LÝ BÃI ĐỖ XE THÔNG MINH (SMART PARKING SYSTEM)\nTÍCH HỢP ĐIỀU HƯỚNG BẢN ĐỒ A* VÀ DỰ BÁO NHU CẦU RANDOM FOREST")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(15)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(185, 28, 28)

    # Mã học phần
    p_code = doc.add_paragraph()
    p_code.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_code.paragraph_format.space_before = Pt(4)
    p_code.paragraph_format.space_after = Pt(20)
    r_code = p_code.add_run("Mã lớp học phần: CSE702131-1-1-26(N01)")
    r_code.font.name = 'Times New Roman'
    r_code.font.size = Pt(12)
    r_code.italic = True

    # Khung thông tin Giảng viên & Nhóm 3 sinh viên
    table_info = doc.add_table(rows=6, cols=2)
    table_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_w = [Cm(6.2), Cm(9.8)]
    
    rows_info = [
        ("Giảng viên hướng dẫn:", "ThS. Nguyễn Thị Thùy Liên"),
        ("Nhóm sinh viên thực hiện:", "Nhóm 4"),
        ("Sinh viên 1 (Trưởng nhóm):", "Phạm Văn Đạt – MSV: 23017150"),
        ("Sinh viên 2 (Thành viên):", "Nguyễn Duy Bảo – MSV: [Bổ sung]"),
        ("Sinh viên 3 (Thành viên):", "Trần Tuấn Anh – MSV: [Bổ sung]"),
        ("Lớp chuyên ngành:", "K17 - Khoa học Máy tính")
    ]
    
    for idx, (label, val) in enumerate(rows_info):
        r_row = table_info.rows[idx]
        r_row.cells[0].width = col_w[0]
        r_row.cells[1].width = col_w[1]
        
        p_lbl = r_row.cells[0].paragraphs[0]
        p_lbl.paragraph_format.space_before = Pt(2)
        p_lbl.paragraph_format.space_after = Pt(2)
        r_l = p_lbl.add_run(label)
        r_l.font.name = 'Times New Roman'
        r_l.font.size = Pt(12)
        r_l.bold = True
        
        p_val = r_row.cells[1].paragraphs[0]
        p_val.paragraph_format.space_before = Pt(2)
        p_val.paragraph_format.space_after = Pt(2)
        r_v = p_val.add_run(val)
        r_v.font.name = 'Times New Roman'
        r_v.font.size = Pt(12)
        if idx in [0, 1, 2]:
            r_v.bold = True

    # Địa danh và năm thực hiện
    p_bottom = doc.add_paragraph()
    p_bottom.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bottom.paragraph_format.space_before = Pt(36)
    p_bottom.paragraph_format.space_after = Pt(0)
    r_b = p_bottom.add_run("HÀ NỘI – NĂM 2026")
    r_b.font.name = 'Times New Roman'
    r_b.font.size = Pt(12)
    r_b.bold = True

def add_table_of_contents_table(doc):
    """
    Tạo bảng Mục lục chi tiết toàn diện phản ánh đầy đủ các chương, mục, trang của đồ án
    """
    headers = ["NỘI DUNG / ĐỀ MỤC", "TRANG"]
    toc_data = [
        # Front Matter
        ("LỜI CẢM ƠN", "iii", True, 0),
        ("LỜI CAM ĐOAN", "iv", True, 0),
        ("PHÂN CÔNG NHIỆM VỤ ĐỒ ÁN (BẢNG P.1 & P.2)", "v", True, 0),
        ("DANH MỤC THUẬT NGỮ VÀ TỪ VIẾT TẮT", "vii", True, 0),
        ("DANH MỤC HÌNH VẼ", "viii", True, 0),
        ("DANH MỤC BẢNG BIỂU", "ix", True, 0),
        ("MỞ ĐẦU", "1", True, 0),

        # Chương 1
        ("CHƯƠNG 1: KHẢO SÁT HIỆN TRẠNG VÀ PHÂN TÍCH YÊU CẦU NGHIỆP VỤ", "3", True, 0),
        ("1.1. Khảo sát hiện trạng và tính cấp thiết của đề tài", "3", False, 1),
        ("1.1.1. Thực trạng các bãi giữ xe truyền thống và bán tự động tại Việt Nam", "3", False, 2),
        ("1.1.2. Tính cấp thiết của giải pháp bãi đỗ xe thông minh (Smart Parking System)", "5", False, 2),
        ("1.2. Mục tiêu, đối tượng và phạm vi nghiên cứu", "6", False, 1),
        ("1.2.1. Mục tiêu tổng quát và mục tiêu cụ thể", "6", False, 2),
        ("1.2.2. Đối tượng và phạm vi ứng dụng của hệ thống", "7", False, 2),
        ("1.3. Phân tích yêu cầu nghiệp vụ hệ thống (SRS)", "9", False, 1),
        ("1.3.1. Phân loại các nhóm tác nhân (Actors)", "9", False, 2),
        ("1.3.2. Yêu cầu chức năng chi tiết cho từng nhóm tác nhân", "10", False, 2),
        ("1.3.3. Yêu cầu phi chức năng và quy tắc nghiệp vụ đặc thù", "12", False, 2),
        ("1.4. Mô hình hóa chức năng bằng sơ đồ Use Case", "14", False, 1),
        ("1.4.1. Sơ đồ Use Case tổng quát", "14", False, 2),
        ("1.4.2. Đặc tả chi tiết các Use Case cốt lõi", "16", False, 2),

        # Chương 2
        ("CHƯƠNG 2: THIẾT KẾ KIẾN TRÚC VÀ CƠ SỞ DỮ LIỆU HỆ THỐNG", "18", True, 0),
        ("2.1. Thiết kế kiến trúc tổng thể hệ thống", "18", False, 1),
        ("2.1.1. Mô hình kiến trúc 3 tầng (Three-Tier Architecture)", "18", False, 2),
        ("2.1.2. Phân tích luồng truyền thông thời gian thực WebSocket", "20", False, 2),
        ("2.2. Thiết kế cơ sở dữ liệu quan hệ (ERD)", "22", False, 1),
        ("2.2.1. Sơ đồ thực thể liên kết (Entity-Relationship Diagram)", "22", False, 2),
        ("2.2.2. Đặc tả chi tiết các bảng dữ liệu chuẩn hóa 3NF", "24", False, 2),
        ("2.2.3. Ràng buộc toàn vẹn và chiến lược đánh chỉ mục (Indexing)", "27", False, 2),
        ("2.3. Thiết kế luồng xử lý và tương tác", "28", False, 1),
        ("2.3.1. Sơ đồ hoạt động (Activity Diagram) luồng đặt chỗ và Check-in/Check-out", "28", False, 2),
        ("2.3.2. Sơ đồ tuần tự (Sequence Diagram) xử lý giao dịch và mở barrier", "31", False, 2),
        ("2.4. Thiết kế giao diện người dùng và trải nghiệm (UI/UX)", "33", False, 1),
        ("2.4.1. Nguyên lý thiết kế giao diện Dark Cyber hiện đại", "33", False, 2),
        ("2.4.2. Thiết kế sơ đồ ma trận lưới bãi đỗ 2D (Parking Grid Matrix)", "35", False, 2),

        # Chương 3
        ("CHƯƠNG 3: NGHIÊN CỨU THUẬT TOÁN ĐIỀU HƯỚNG A* VÀ HỌC MÁY RANDOM FOREST", "38", True, 0),
        ("3.1. Nghiên cứu thuật toán tìm đường tối ưu A* (A-Star Search)", "38", False, 1),
        ("3.1.1. Cơ sở lý thuyết và hàm đánh giá heuristic f(n) = g(n) + h(n)", "38", False, 2),
        ("3.1.2. Lựa chọn hàm heuristic Manhattan cho ma trận lưới bãi đỗ 2D", "40", False, 2),
        ("3.1.3. Thiết kế cấu trúc dữ liệu Priority Queue (heapq) và xử lý vật cản", "42", False, 2),
        ("3.1.4. Đánh giá độ phức tạp thuật toán và tối ưu hóa thời gian thực", "43", False, 2),
        ("3.2. Nghiên cứu mô hình học máy Random Forest dự báo tỷ lệ lấp đầy", "44", False, 1),
        ("3.2.1. Đặt bài toán và cơ sở lý thuyết mô hình hồi quy Random Forest", "44", False, 2),
        ("3.2.2. Xây dựng pipeline dữ liệu: Khởi tạo 4.320 mẫu lịch sử và trích xuất đặc trưng", "46", False, 2),
        ("3.2.3. Quy trình huấn luyện, tinh chỉnh siêu tham số (Hyperparameter Tuning)", "48", False, 2),
        ("3.2.4. Đánh giá độ chính xác thực nghiệm (MAE, RMSE, R²) và đóng gói mô hình", "49", False, 2),

        # Chương 4
        ("CHƯƠNG 4: HIỆN THỰC HÓA VÀ CÀI ĐẶT HỆ THỐNG", "51", True, 0),
        ("4.1. Môi trường công nghệ và công cụ phát triển", "51", False, 1),
        ("4.2. Hiện thực hóa phân hệ Backend FastAPI", "53", False, 1),
        ("4.2.1. Cấu trúc mã nguồn module hóa chuẩn Clean Architecture", "53", False, 2),
        ("4.2.2. Cài đặt hệ thống bảo mật Authentication (Bcrypt & JWT)", "55", False, 2),
        ("4.2.3. Cài đặt nghiệp vụ Đặt chỗ và giải pháp SELECT FOR UPDATE chống Race Condition", "57", False, 2),
        ("4.2.4. Cài đặt máy chủ thời gian thực WebSocket ConnectionManager", "59", False, 2),
        ("4.2.5. Xây dựng hệ thống 28 REST API Endpoints", "60", False, 2),
        ("4.3. Hiện thực hóa phân hệ Frontend Vue 3 + Tailwind CSS", "62", False, 1),
        ("4.3.1. Cấu trúc thành phần (Component Hierarchy) và State Management (Pinia)", "62", False, 2),
        ("4.3.2. Hiện thực hóa ma trận bản đồ bãi đỗ 2D và tích hợp GSAP 3 điều hướng xe", "64", False, 2),
        ("4.3.3. Hiện thực hóa Cổng nhân viên (Staff Portal) và Trình quét mã QR Barrier", "66", False, 2),
        ("4.3.4. Hiện thực hóa Cổng quản trị viên (Admin Portal) và Biểu đồ dự báo AI", "68", False, 2),

        # Chương 5
        ("CHƯƠNG 5: KIỂM THỬ HỆ THỐNG, ĐÁNH GIÁ VÀ KẾT LUẬN", "70", True, 0),
        ("5.1. Kế hoạch và phương pháp kiểm thử", "70", False, 1),
        ("5.1.1. Kiểm thử đơn vị tự động (Unit Testing với Pytest)", "70", False, 2),
        ("5.1.2. Kiểm thử tương tranh đa luồng (Concurrency Stress Testing)", "73", False, 2),
        ("5.1.3. Kiểm thử giao diện đầu cuối (End-to-End Testing với Playwright)", "75", False, 2),
        ("5.2. Kết quả kiểm thử và phân tích hiệu năng", "76", False, 1),
        ("5.3. Kiểm thử tự động giao diện End-to-End với Playwright", "78", False, 1),
        ("5.4. Đánh giá hiệu năng và phân tích rủi ro hệ thống", "80", False, 1),
        ("5.4.1. Đánh giá các chỉ số hiệu năng (Performance Benchmarks)", "80", False, 2),
        ("5.4.2. Phân tích các rủi ro kỹ thuật và giải pháp khắc phục", "82", False, 2),
        ("5.5. Kết luận đề tài và hướng phát triển tương lai", "84", False, 1),
        ("5.5.1. Các kết quả chính đã đạt được của đề tài", "84", False, 2),
        ("5.5.2. Hạn chế còn tồn tại và phân tích lựa chọn giải pháp kỹ thuật", "85", False, 2),
        ("5.5.3. Định hướng nghiên cứu và mở rộng hệ thống (Tích hợp ANPR)", "86", False, 2),

        # Back Matter
        ("TÀI LIỆU THAM KHẢO", "87", True, 0),
        ("PHỤ LỤC A: BẢNG ĐẶC TẢ CHI TIẾT 28 RESTFUL APIS", "89", True, 0),
        ("PHỤ LỤC B: CẤU TRÚC CÂY THƯ MỤC MÃ NGUỒN DỰ ÁN", "92", True, 0),
        ("PHỤ LỤC C: HƯỚNG DẪN CÀI ĐẶT VÀ TRIỂN KHAI VẬN HÀNH DỰ ÁN", "95", True, 0)
    ]

    table = doc.add_table(rows=len(toc_data) + 1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table, color="D0D7DE", sz="4", val="single")

    col_widths = [Cm(14.2), Cm(2.3)]

    # Header
    hdr_row = table.rows[0]
    for c_idx, h_text in enumerate(headers):
        cell = hdr_row.cells[c_idx]
        cell.width = col_widths[c_idx]
        set_cell_background(cell, "E2E8F0")
        set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 1 else WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.08
        r = p.add_run(h_text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10.5)
        r.bold = True

    # Rows
    for r_idx, (title, page, is_bold, level) in enumerate(toc_data):
        row = table.rows[r_idx + 1]
        
        # Cột 1: Tiêu đề
        cell0 = row.cells[0]
        cell0.width = col_widths[0]
        set_cell_margins(cell0, top=50, bottom=50, left=100, right=100)
        p0 = cell0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(0)
        p0.paragraph_format.line_spacing = 1.08
        
        indent_str = "    " * level
        r0 = p0.add_run(f"{indent_str}{title}")
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(10)
        r0.bold = is_bold
        if level == 0 and not is_bold:
            r0.bold = True
            
        # Cột 2: Số trang
        cell1 = row.cells[1]
        cell1.width = col_widths[1]
        set_cell_margins(cell1, top=50, bottom=50, left=100, right=100)
        p1 = cell1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(0)
        p1.paragraph_format.line_spacing = 1.08
        r1 = p1.add_run(page)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10)
        r1.bold = is_bold

def add_list_of_figures_table(doc):
    """
    Tạo Bảng Danh mục hình vẽ
    """
    headers = ["KÝ HIỆU HÌNH", "TÊN / MÔ TẢ NỘI DUNG HÌNH VẼ", "TRANG"]
    lof_data = [
        ("Hình 1.1", "Thực trạng ùn tắc giao thông tại các bãi đỗ xe truyền thống đô thị", "4"),
        ("Hình 2.1", "Sơ đồ Use Case tổng quát hệ thống Smart Parking System (Customer, Staff, Admin)", "15"),
        ("Hình 2.2", "Sơ đồ kiến trúc phân tầng hệ thống Smart Parking System (Frontend, FastAPI, PostgreSQL)", "19"),
        ("Hình 2.3", "Sơ đồ thực thể liên kết (ERD) cơ sở dữ liệu quan hệ chuẩn hóa 6 bảng", "23"),
        ("Hình 3.1", "Minh họa nguyên lý thuật toán tìm đường tối ưu A* né vật cản trên lưới 2D", "40"),
        ("Hình 3.2", "Kiến trúc mô hình rừng ngẫu nhiên (Random Forest Regressor 200 Trees) dự báo tỷ lệ lấp đầy", "46"),
        ("Hình 4.1", "Giao diện tổng quan hệ thống Smart Parking System thời gian thực", "52"),
        ("Hình 4.2", "Minh họa giao diện xác thực, bảo mật và phân quyền vai trò người dùng (JWT Bearer)", "56"),
        ("Hình 4.3", "Hộp thoại đặt giữ chỗ ô đỗ kèm vé điện tử mã QR Code động", "58"),
        ("Hình 4.4", "Bảng điều khiển phân hệ vận hành và quản trị hệ thống bãi xe (Admin Portal)", "64"),
        ("Hình 4.5", "Giao diện phân hệ Cổng nhân viên (Staff Portal) và quét mã QR Barrier", "66")
    ]
    add_table_data(doc, "Danh mục", "Danh mục hình vẽ trong báo cáo đồ án", headers, lof_data, col_widths=[2.8, 11.2, 2.5])

def add_list_of_tables_table(doc):
    """
    Tạo Bảng Danh mục bảng biểu
    """
    headers = ["KÝ HIỆU BẢNG", "TÊN / MÔ TẢ NỘI DUNG BẢNG BIỂU", "TRANG"]
    lot_data = [
        ("Bảng P.1", "Danh mục các hạng mục công việc chính của đồ án", "v"),
        ("Bảng P.2", "Bảng phân công chi tiết nhiệm vụ thành viên theo mẫu BAO_CAO_DACS", "vi"),
        ("Bảng T.1", "Bảng danh mục thuật ngữ và ký hiệu viết tắt trong đồ án", "vii"),
        ("Bảng 1.1", "So sánh đặc điểm bãi đỗ xe truyền thống với Smart Parking System", "5"),
        ("Bảng 1.2", "Ma trận phân quyền các nhóm tác nhân trong hệ thống", "10"),
        ("Bảng 2.1", "Đặc tả cấu trúc bảng users", "24"),
        ("Bảng 2.2", "Đặc tả cấu trúc bảng parking_lots", "24"),
        ("Bảng 2.3", "Đặc tả cấu trúc bảng parking_slots", "25"),
        ("Bảng 2.4", "Đặc tả cấu trúc bảng bookings", "26"),
        ("Bảng 2.5", "Đặc tả cấu trúc bảng sessions", "27"),
        ("Bảng 2.6", "Đặc tả cấu trúc bảng occupancy_history", "27"),
        ("Bảng 3.1", "Các đặc trưng trích xuất phục vụ huấn luyện mô hình Random Forest", "47"),
        ("Bảng 3.2", "Kết quả đánh giá thực nghiệm các mô hình học máy dự báo lấp đầy", "49"),
        ("Bảng 4.1", "Danh sách các công nghệ cốt lõi sử dụng trong đồ án", "51"),
        ("Bảng 5.1", "Danh sách 11 ca kiểm thử đơn vị tự động Pytest", "72"),
        ("Bảng 5.2", "Kết quả thực nghiệm kiểm thử tương tranh đặt chỗ đa luồng", "74"),
        ("Bảng 5.3", "Đánh giá mức độ hoàn thành các mục tiêu đồ án đã đề ra", "81"),
        ("Bảng A.1", "Đặc tả chi tiết các tham số và phản hồi của 28 RESTful APIs", "89")
    ]
    add_table_data(doc, "Danh mục", "Danh mục bảng biểu trong báo cáo đồ án", headers, lot_data, col_widths=[2.8, 11.2, 2.5])

def add_preamble_pages(doc):
    """
    Các trang Lời cảm ơn, Lời cam đoan, Phân công nhiệm vụ, Mục lục, Danh mục viết tắt, Danh mục hình vẽ & bảng biểu
    """
    # 1. LỜI CẢM ƠN
    p_ty = doc.add_paragraph()
    p_ty.paragraph_format.page_break_before = True
    p_ty.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ty.paragraph_format.space_before = Pt(18)
    p_ty.paragraph_format.space_after = Pt(12)
    r = p_ty.add_run("LỜI CẢM ƠN")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.bold = True

    add_body_paragraph(doc, "Lời đầu tiên, toàn thể nhóm sinh viên chúng em xin gửi lời cảm ơn chân thành và sâu sắc nhất tới toàn thể các Quý Thầy, Cô giáo thuộc Khoa Khoa học Máy tính – Trường Đại học Phenikaa, những người đã tận tâm truyền đạt tri thức quý báu, định hướng tư duy khoa học và truyền ngọn lửa đam mê công nghệ cho chúng em trong suốt quá trình học tập và rèn luyện tại trường.")
    add_body_paragraph(doc, "Đặc biệt, nhóm chúng em xin bày tỏ lòng biết ơn sâu sắc tới Giảng viên hướng dẫn – ThS. Nguyễn Thị Thùy Liên, người đã trực tiếp giảng dạy và đồng hành cùng nhóm trong học phần Phát triển ứng dụng Hệ thống thông tin (Mã lớp: CSE702131-1-1-26(N01)). Cô đã dành nhiều thời gian quý báu theo sát, tận tình hướng dẫn, đưa ra những nhận xét chuyên môn xác đáng, những lời khuyên thực tế quý báu để nhóm chúng em hoàn thiện đề tài 'Nghiên cứu, thiết kế và xây dựng Hệ thống quản lý bãi đỗ xe thông minh (Smart Parking System) tích hợp điều hướng bản đồ A* và dự báo nhu cầu Random Forest'.")
    add_body_paragraph(doc, "Mặc dù cả nhóm đã dành nhiều tâm huyết và nỗ lực nghiên cứu, bám sát các chuẩn mực kỹ thuật công nghệ thông tin hiện đại, song do giới hạn về thời gian và kinh nghiệm thực tiễn, báo cáo đồ án khó tránh khỏi những thiếu sót nhất định. Nhóm chúng em rất mong nhận được những góp ý, chỉ bảo quý báu từ cô giáo ThS. Nguyễn Thị Thùy Liên và quý Thầy Cô trong Hội đồng để sản phẩm ứng dụng và năng lực kỹ thuật của từng thành viên ngày càng hoàn thiện hơn nữa.")
    
    p_sign1 = doc.add_paragraph()
    p_sign1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sign1.paragraph_format.space_before = Pt(16)
    p_sign1.paragraph_format.space_after = Pt(2)
    r_s1 = p_sign1.add_run("Hà Nội, ngày 14 tháng 10 năm 2026\nNhóm sinh viên thực hiện (Nhóm 4)\n\n\nPhạm Văn Đạt (Trưởng nhóm)\nNguyễn Duy Bảo\nTrần Tuấn Anh")
    r_s1.font.name = 'Times New Roman'
    r_s1.font.size = Pt(12)
    r_s1.italic = True

    # 2. LỜI CAM ĐOAN
    p_cd = doc.add_paragraph()
    p_cd.paragraph_format.page_break_before = True
    p_cd.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cd.paragraph_format.space_before = Pt(18)
    p_cd.paragraph_format.space_after = Pt(12)
    r = p_cd.add_run("LỜI CAM ĐOAN")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.bold = True

    add_body_paragraph(doc, "Chúng em xin cam đoan đề tài nghiên cứu 'Nghiên cứu, thiết kế và xây dựng Hệ thống quản lý bãi đỗ xe thông minh (Smart Parking System)' là công trình nghiên cứu và xây dựng thực tế của tập thể Nhóm 4 dưới sự định hướng chuyên môn của Giảng viên hướng dẫn ThS. Nguyễn Thị Thùy Liên.")
    add_body_paragraph(doc, "Toàn bộ số liệu, thuật toán, kiến trúc hệ thống, mã nguồn Backend FastAPI, Frontend Vue 3 và kết quả thực nghiệm mô phỏng thuật toán A*, mô hình học máy Random Forest được trình bày trong báo cáo này là hoàn toàn trung thực, phản ánh chính xác quá trình cài đặt thực tế của dự án.")
    add_body_paragraph(doc, "Các tài liệu tham khảo, bài báo khoa học, thư viện mã nguồn mở và công cụ được sử dụng đều có nguồn gốc trích dẫn rõ ràng theo đúng tiêu chuẩn học thuật. Nhóm chúng em xin hoàn toàn chịu trách nhiệm trước Nhà trường và Khoa nếu có bất kỳ sự gian lận hoặc sao chép trái phép nào.")

    p_sign2 = doc.add_paragraph()
    p_sign2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sign2.paragraph_format.space_before = Pt(16)
    p_sign2.paragraph_format.space_after = Pt(2)
    r_s2 = p_sign2.add_run("Hà Nội, ngày 14 tháng 10 năm 2026\nĐại diện nhóm cam đoan\n\n\nPhạm Văn Đạt (Trưởng nhóm)")
    r_s2.font.name = 'Times New Roman'
    r_s2.font.size = Pt(12)
    r_s2.italic = True

    # 3. PHÂN CÔNG NHIỆM VỤ ĐỒ ÁN (Chuẩn BAO_CAO_DACS - Nhóm 4)
    p_assign = doc.add_paragraph()
    p_assign.paragraph_format.page_break_before = True
    p_assign.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_assign.paragraph_format.space_before = Pt(18)
    p_assign.paragraph_format.space_after = Pt(12)
    r = p_assign.add_run("PHÂN CÔNG NHIỆM VỤ ĐỒ ÁN")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.bold = True

    add_body_paragraph(doc, "Bảng tổng hợp phân chia các hạng mục công việc chính của đồ án:")
    
    # Bảng 1: Danh sách công việc
    headers_t1 = ["Danh sách các công việc / nhiệm vụ", "Mô tả tóm tắt công việc"]
    rows_t1 = [
        ["Công việc 1", "Khảo sát hiện trạng, phân tích yêu cầu nghiệp vụ (SRS) và mô hình hóa Use Case"],
        ["Công việc 2", "Thiết kế kiến trúc hệ thống 3 tầng và cơ sở dữ liệu quan hệ PostgreSQL 6 bảng chuẩn 3NF"],
        ["Công việc 3", "Nghiên cứu và cài đặt thuật toán tìm đường tối ưu A* né vật cản kết hợp hoạt ảnh GSAP 3"],
        ["Công việc 4", "Nghiên cứu và huấn luyện mô hình Machine Learning Random Forest Regressor 200 trees dự báo lấp đầy"],
        ["Công việc 5", "Hiện thực hóa Backend FastAPI (28 REST APIs, WebSocket, khóa SELECT FOR UPDATE chống Double-booking)"],
        ["Công việc 6", "Hiện thực hóa Frontend Vue 3 + Tailwind CSS (3 Cổng Customer, Staff, Admin, Barrier QR)"],
        ["Công việc 7", "Xây dựng bộ kiểm thử tự động Pytest (11 Unit Tests), kiểm thử đa luồng tương tranh và E2E Playwright"]
    ]
    add_table_data(doc, "Bảng P.1", "Danh mục các hạng mục công việc chính của đồ án", headers_t1, rows_t1, col_widths=[5.5, 11.0])

    add_body_paragraph(doc, "Bảng phân công chi tiết nhiệm vụ và đánh giá đóng góp của từng thành viên Nhóm 4:")

    # Bảng 2: Phân công 3 thành viên Nhóm 4 theo mẫu BAO_CAO_DACS
    headers_t2 = ["TT", "Mã sinh viên", "Họ và tên", "Nhiệm vụ phân công", "Nội dung đã thực hiện", "Đánh giá"]
    rows_t2 = [
        [
            "1",
            "23017150",
            "Phạm Văn Đạt\n(Trưởng nhóm)",
            "Backend & Kiến trúc Hệ thống\n(Công việc 2, 5, 7)",
            "Thiết kế kiến trúc 3 tầng, CSDL PostgreSQL 6 bảng, Auth JWT/Bcrypt, 28 REST APIs, Khóa SELECT FOR UPDATE chống Double-booking, WebSocket Server, kiểm thử Pytest.",
            "Hoàn thành 100%\n(Đóng góp 35%)"
        ],
        [
            "2",
            "[Bổ sung]",
            "Nguyễn Duy Bảo\n(Thành viên)",
            "Frontend UI/UX & Tương tác\n(Công việc 1, 6)",
            "Xây dựng giao diện Vue 3 + Tailwind CSS Dark Cyber, Sơ đồ ma trận lưới bãi đỗ 2D ParkingGrid, Diễn hoạt xe chạy GSAP 3, Modal đặt chỗ & vé QR, Biểu đồ AI tương tác, E2E Playwright.",
            "Hoàn thành 100%\n(Đóng góp 33%)"
        ],
        [
            "3",
            "[Bổ sung]",
            "Trần Tuấn Anh\n(Thành viên)",
            "Thuật toán & Machine Learning\n(Công việc 3, 4)",
            "Cài đặt thuật toán tìm đường tối ưu A* (astar.py, grid.py, heapq, Manhattan), Pipeline sinh 4.320 mẫu dữ liệu lịch sử, Huấn luyện mô hình Random Forest 200 trees (MAE 0.058), Service navigation.",
            "Hoàn thành 100%\n(Đóng góp 32%)"
        ]
    ]
    add_table_data(doc, "Bảng P.2", "Bảng phân công chi tiết nhiệm vụ thành viên theo mẫu BAO_CAO_DACS", headers_t2, rows_t2, col_widths=[0.8, 2.2, 3.2, 3.4, 4.8, 2.1])

    # 4. MỤC LỤC
    p_toc = doc.add_paragraph()
    p_toc.paragraph_format.page_break_before = True
    p_toc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc.paragraph_format.space_before = Pt(18)
    p_toc.paragraph_format.space_after = Pt(12)
    r = p_toc.add_run("MỤC LỤC")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.bold = True

    add_body_paragraph(doc, "Dưới đây là mục lục chi tiết toàn bộ báo cáo đồ án học phần Hệ thống quản lý bãi đỗ xe thông minh (Smart Parking System):")
    add_table_of_contents_table(doc)

    # 5. DANH MỤC THUẬT NGỮ VÀ TỪ VIẾT TẮT
    p_abbr = doc.add_paragraph()
    p_abbr.paragraph_format.page_break_before = True
    p_abbr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abbr.paragraph_format.space_before = Pt(18)
    p_abbr.paragraph_format.space_after = Pt(12)
    r = p_abbr.add_run("DANH MỤC THUẬT NGỮ VÀ TỪ VIẾT TẮT")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.bold = True

    abbr_headers = ["Ký hiệu viết tắt", "Tên đầy đủ tiếng Anh", "Ý nghĩa / Diễn giải tiếng Việt"]
    abbr_data = [
        ["API", "Application Programming Interface", "Giao diện lập trình ứng dụng kết nối Frontend và Backend"],
        ["ASGI", "Asynchronous Server Gateway Interface", "Tiêu chuẩn máy chủ bất đồng bộ dành cho Python web framework"],
        ["CRUD", "Create, Read, Update, Delete", "Bốn thao tác cơ bản trong quản trị dữ liệu (Thêm, Đọc, Sửa, Xóa)"],
        ["CSS", "Cascading Style Sheets", "Ngôn ngữ định dạng giao diện hiển thị cho các trang web"],
        ["DB / DBMS", "Database / Database Management System", "Cơ sở dữ liệu / Hệ quản trị cơ sở dữ liệu"],
        ["DOM", "Document Object Model", "Mô hình đối tượng tài liệu giao diện web"],
        ["ERD", "Entity Relationship Diagram", "Sơ đồ thực thể liên kết dùng để mô hình hóa cơ sở dữ liệu"],
        ["FK", "Foreign Key", "Khóa ngoại tham chiếu giữa các thực thể bảng trong CSDL"],
        ["GSAP", "GreenSock Animation Platform", "Thư viện JavaScript chuyên nghiệp xử lý hoạt ảnh và chuyển động mượt mà"],
        ["HTTP / HTTPS", "Hypertext Transfer Protocol (Secure)", "Giao thức truyền tải siêu văn bản mạng (bảo mật SSL/TLS)"],
        ["IoT", "Internet of Things", "Mạng lưới vạn vật kết nối Internet"],
        ["JSON", "JavaScript Object Notation", "Định dạng trao đổi dữ liệu dạng chuỗi văn bản phổ biến"],
        ["JWT", "JSON Web Token", "Chuẩn mã hóa thông tin xác thực an toàn không lưu trạng thái (Stateless)"],
        ["MAE", "Mean Absolute Error", "Sai số tuyệt đối trung bình dùng để đánh giá mô hình học máy"],
        ["ML", "Machine Learning", "Học máy - Một nhánh của Trí tuệ nhân tạo (AI)"],
        ["MSE", "Mean Squared Error", "Sai số bình phương trung bình trong bài toán hồi quy"],
        ["ORM", "Object-Relational Mapping", "Kỹ thuật ánh xạ bảng CSDL thành các đối tượng ngôn ngữ lập trình"],
        ["PK", "Primary Key", "Khóa chính định danh duy nhất cho từng bản ghi dữ liệu"],
        ["Pydantic", "Data validation library for Python", "Thư viện xác thực kiểu dữ liệu mạnh mẽ của hệ sinh thái Python"],
        ["REST", "Representational State Transfer", "Kiến trúc thiết kế dịch vụ web chuẩn mực"],
        ["RFID", "Radio Frequency Identification", "Công nghệ nhận dạng tự động bằng sóng vô tuyến"],
        ["RMSE", "Root Mean Squared Error", "Căn bậc hai sai số bình phương trung bình"],
        ["SPS", "Smart Parking System", "Hệ thống quản lý bãi đỗ xe thông minh"],
        ["SPA", "Single Page Application", "Ứng dụng web tải một trang đơn lẻ mang lại trải nghiệm mượt mà"],
        ["SQL", "Structured Query Language", "Ngôn ngữ truy vấn dữ liệu có cấu trúc"],
        ["SSR", "Server-Side Rendering", "Kết xuất giao diện phía máy chủ"],
        ["UI / UX", "User Interface / User Experience", "Giao diện người dùng / Trải nghiệm người dùng"],
        ["UML", "Unified Modeling Language", "Ngôn ngữ mô hình hóa thống nhất trong công nghệ phần mềm"],
        ["UVicorn", "Lightning-fast ASGI server", "Máy chủ web ASGI hiệu năng cực cao dành cho FastAPI"],
        ["WebSocket", "Full-duplex Communication Protocol", "Giao thức truyền thông hai chiều thời gian thực giữa máy khách và máy chủ"]
    ]
    add_table_data(doc, "Bảng T.1", "Bảng danh mục thuật ngữ và ký hiệu viết tắt trong đồ án", abbr_headers, abbr_data, col_widths=[2.8, 5.2, 8.5])

    # 6. DANH MỤC HÌNH VẼ
    p_lof = doc.add_paragraph()
    p_lof.paragraph_format.page_break_before = True
    p_lof.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lof.paragraph_format.space_before = Pt(18)
    p_lof.paragraph_format.space_after = Pt(12)
    r = p_lof.add_run("DANH MỤC HÌNH VẼ")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.bold = True

    add_body_paragraph(doc, "Danh mục tổng hợp toàn bộ các hình vẽ, sơ đồ kiến trúc và ảnh chụp giao diện hệ thống:")
    add_list_of_figures_table(doc)
    
    # 7. DANH MỤC BẢNG BIỂU
    p_lot = doc.add_paragraph()
    p_lot.paragraph_format.page_break_before = True
    p_lot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lot.paragraph_format.space_before = Pt(18)
    p_lot.paragraph_format.space_after = Pt(12)
    r = p_lot.add_run("DANH MỤC BẢNG BIỂU")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.bold = True

    add_body_paragraph(doc, "Danh mục tổng hợp toàn bộ các bảng số liệu, cấu trúc cơ sở dữ liệu và kết quả thực nghiệm:")
    add_list_of_tables_table(doc)
