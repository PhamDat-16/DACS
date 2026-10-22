import os
import sys
import shutil
import docx
from docx import Document

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from thesis_generator.style_helper import setup_document_styles
from thesis_generator.front_matter import add_cover_page, add_preamble_pages
from thesis_generator.chapter1 import add_chapter_1
from thesis_generator.chapter2 import add_chapter_2
from thesis_generator.chapter3 import add_chapter_3
from thesis_generator.chapter4 import add_chapter_4
from thesis_generator.chapter5 import add_chapter_5
from thesis_generator.back_matter import add_back_matter

def build_full_thesis():
    print("=== BAT DAU TONG HOP BAO CAO DO AN TOT NGHIEP SMART PARKING SYSTEM ===")
    
    doc = Document()
    setup_document_styles(doc)
    
    logo_path = os.path.join(os.getcwd(), "extracted_media", "word", "media", "image1.png")
    
    # 1. Trang bìa & Front Matter
    print("-> Đang tạo Trang bìa chuẩn Phenikaa...")
    add_cover_page(doc, logo_path)
    
    print("-> Đang tạo Lời cảm ơn, Lời cam đoan, Phân công nhiệm vụ (trống), Mục lục (trống), Danh mục viết tắt, Danh mục bảng biểu...")
    add_preamble_pages(doc)
    
    # 2. Các chương nội dung chính
    print("-> Đang tổng hợp Chương 1: Tổng quan và đặt vấn đề...")
    add_chapter_1(doc)
    
    print("-> Đang tổng hợp Chương 2: Phân tích yêu cầu và thiết kế hệ thống...")
    add_chapter_2(doc)
    
    print("-> Đang tổng hợp Chương 3: Thuật toán điều hướng A* và Mô hình học máy Random Forest...")
    add_chapter_3(doc)
    
    print("-> Đang tổng hợp Chương 4: Hiện thực hóa và xây dựng hệ thống...")
    add_chapter_4(doc)
    
    print("-> Đang tổng hợp Chương 5: Kiểm thử, đánh giá kết quả và kết luận...")
    add_chapter_5(doc)
    
    # 3. Tài liệu tham khảo & Phụ lục
    print("-> Đang tổng hợp Tài liệu tham khảo chuẩn IEEE và Phụ lục A, B, C...")
    add_back_matter(doc)
    
    # Lưu tệp báo cáo chính thức chuẩn BAO_CAO_DACS
    output_filename = "BAO_CAO_DACS_Smart_Parking_System.docx"
    doc_path = os.path.join(os.getcwd(), output_filename)
    doc.save(doc_path)
    print(f"==> Đã xuất báo cáo thành công tại: {doc_path}")
    
    # Sao chép vào thư mục Downloads của người dùng
    user_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    if os.path.exists(user_downloads):
        dl_target = os.path.join(user_downloads, output_filename)
        try:
            shutil.copy2(doc_path, dl_target)
            print(f"==> Đã sao chép bản sao vào Downloads: {dl_target}")
        except PermissionError:
            dl_alt = os.path.join(user_downloads, "BAO_CAO_DACS_Smart_Parking_System_Nhom4.docx")
            shutil.copy2(doc_path, dl_alt)
            print(f"==> Bản gốc trong Downloads đang mở. Đã lưu bản cập nhật vào: {dl_alt}")
        except Exception as e:
            print(f"Lưu ý bản copy trong Downloads: {e}")

if __name__ == "__main__":
    build_full_thesis()
