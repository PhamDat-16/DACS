import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Đặt màu nền cho ô trong bảng"""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Đặt lề trong cho ô bảng"""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="CCCCCC", sz="4", val="single"):
    """Đặt viền thanh mảnh cho toàn bộ bảng"""
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

def setup_document_styles(doc):
    """Cấu hình kích thước trang A4 và lề chuẩn học thuật Việt Nam"""
    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(3.5)   # Chuẩn 3.5cm để đóng gáy đồ án
        section.right_margin = Cm(2.5)

    # Cấu hình Default Style
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(13)
    font.color.rgb = RGBColor(0, 0, 0)
    style.paragraph_format.line_spacing = 1.3
    style.paragraph_format.space_after = Pt(4)
    style.paragraph_format.space_before = Pt(0)

def add_chapter_heading(doc, text):
    """Tiêu đề chương (Heading 1) - Cỡ 14pt, Đậm, In hoa, Căn giữa, Ngắt trang trước"""
    p = doc.add_paragraph()
    p.paragraph_format.page_break_before = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.line_spacing = 1.3
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.bold = True
    return p

def add_section_heading(doc, text):
    """Tiêu đề mục lớn (Heading 2) - Cỡ 13pt, Đậm, Căn trái"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.3
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13)
    run.bold = True
    return p

def add_subsection_heading(doc, text):
    """Tiêu đề mục con (Heading 3) - Cỡ 13pt, Đậm, Nghiêng, Căn trái"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.3
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13)
    run.bold = True
    run.italic = True
    return p

def add_body_paragraph(doc, text, first_indent=True, bold_prefix=""):
    """Đoạn văn nội dung - Căn đều 2 bên (Justify), thụt đầu dòng 1.27cm chuẩn học thuật"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.line_spacing = 1.3
    if first_indent:
        p.paragraph_format.first_line_indent = Cm(1.27)
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(13)
        r_pre.bold = True
        
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13)
    return p

def add_bullet_item(doc, text, bold_prefix="", level=1):
    """Mục danh sách gạch đầu dòng"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.line_spacing = 1.25
    p.paragraph_format.left_indent = Cm(1.27 * level)
    
    symbol = "–  " if level == 1 else "•  "
    r_sym = p.add_run(symbol)
    r_sym.font.name = 'Times New Roman'
    r_sym.font.size = Pt(13)
    r_sym.bold = True
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(13)
        r_pre.bold = True
        
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13)
    return p

def add_image_figure(doc, fig_id, fig_title, image_path=None, note_instructions=""):
    """Thêm hình ảnh thực tế nếu tồn tại, hoặc tạo khung placeholder nếu chưa có ảnh"""
    if image_path and os.path.exists(image_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(10)
        p_img.paragraph_format.space_after = Pt(4)
        run = p_img.add_run()
        run.add_picture(image_path, width=Inches(5.8))
        
        # Caption bên dưới hình
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(12)
        r_cap = p_cap.add_run(f"{fig_id}: {fig_title}")
        r_cap.font.name = 'Times New Roman'
        r_cap.font.size = Pt(11)
        r_cap.italic = True
        r_cap.bold = True
        return p_img
    else:
        # Tạo khung placeholder chuyên nghiệp
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        
        cell = table.rows[0].cells[0]
        cell.width = Cm(15.0)
        set_cell_background(cell, "F8FAFC")
        set_cell_margins(cell, top=200, bottom=200, left=200, right=200)
        
        # Viền nét đứt cho khung dán ảnh
        tcPr = cell._element.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="dashed" w:sz="6" w:space="0" w:color="94A3B8"/>'
            f'<w:left w:val="dashed" w:sz="6" w:space="0" w:color="94A3B8"/>'
            f'<w:bottom w:val="dashed" w:sz="6" w:space="0" w:color="94A3B8"/>'
            f'<w:right w:val="dashed" w:sz="6" w:space="0" w:color="94A3B8"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        
        r1 = p.add_run(f"[{fig_id.upper()}: DÁN ẢNH TẠI ĐÂY]\n")
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        r1.bold = True
        r1.font.color.rgb = RGBColor(30, 58, 138)
        
        r2 = p.add_run(f"👉 Hướng dẫn: {note_instructions}\n")
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(10)
        r2.italic = True
        r2.font.color.rgb = RGBColor(100, 116, 139)
        
        r3 = p.add_run("------------------------------------------------------------------------------------------\n(Khung ảnh chừa trống theo yêu cầu - Bạn bấm dán ảnh đè vào khung này)")
        r3.font.name = 'Times New Roman'
        r3.font.size = Pt(9.5)
        r3.font.color.rgb = RGBColor(148, 163, 184)
        p.paragraph_format.space_after = Pt(14)
        
        # Caption bên dưới hình
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(4)
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run(f"{fig_id}: {fig_title}")
        r_cap.font.name = 'Times New Roman'
        r_cap.font.size = Pt(11)
        r_cap.italic = True
        r_cap.bold = True
        return table

def add_table_data(doc, table_id, table_title, headers, rows_data, col_widths=None):
    """Tạo bảng dữ liệu chuẩn phong cách học thuật"""
    # Caption phía trên bảng
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_cap.paragraph_format.space_before = Pt(8)
    p_cap.paragraph_format.space_after = Pt(3)
    r_cap = p_cap.add_run(f"{table_id}: {table_title}")
    r_cap.font.name = 'Times New Roman'
    r_cap.font.size = Pt(11.5)
    r_cap.bold = True
    
    table = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table, color="94A3B8", sz="4", val="single")
    
    # Tiêu đề cột
    hdr_row = table.rows[0]
    for idx, heading in enumerate(headers):
        cell = hdr_row.cells[idx]
        set_cell_background(cell, "1E3A8A") # Xanh đậm trang trọng
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(heading)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        run.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        
    # Các dòng dữ liệu
    for r_idx, row in enumerate(rows_data):
        row_cells = table.rows[r_idx + 1].cells
        bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            cell = row_cells[c_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx > 0 else WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(str(val))
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10.5)
            
    if col_widths:
        for row in table.rows:
            for idx, w in enumerate(col_widths):
                row.cells[idx].width = Cm(w)
                
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(4)
    return table

def add_code_snippet(doc, title, code_text):
    """Tạo khung chứa đoạn mã nguồn minh họa"""
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(6)
    p_title.paragraph_format.space_after = Pt(2)
    r_t = p_title.add_run(f"Đoạn mã: {title}")
    r_t.font.name = 'Times New Roman'
    r_t.font.size = Pt(10.5)
    r_t.bold = True
    
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.rows[0].cells[0]
    cell.width = Cm(15.0)
    set_cell_background(cell, "F1F5F9")
    set_table_borders(table, color="CBD5E1", sz="4", val="single")
    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
    
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.1
    
    run = p.add_run(code_text.strip())
    run.font.name = 'Consolas'
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(15, 23, 42)
    
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(4)
    return table

