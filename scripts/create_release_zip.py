import os
import sys
import zipfile
import shutil
import time

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ZIP_NAME = "smart-parking-system.zip"
OUTPUT_ZIP = os.path.join("d:\\", ZIP_NAME)
DOWNLOADS_ZIP = os.path.join(os.path.expanduser("~"), "Downloads", ZIP_NAME)

EXCLUDE_DIRS = {
    'venv', '.venv', '.git', '__pycache__', '.pytest_cache',
    '_archive_unrelated_files', '.vscode', '.agent', '.agents',
    '.gemini', 'html-ppt-skill', 'node_modules', '.cache'
}

EXCLUDE_EXTS = {'.pyc', '.pyo', '.pyd', '.tmp'}

def should_exclude(rel_path):
    parts = rel_path.replace('\\', '/').split('/')
    for p in parts:
        if p in EXCLUDE_DIRS:
            return True
        if p.startswith('.edge_'):
            return True
    
    filename = parts[-1]
    if filename.startswith('~$'):
        return True
    if filename.endswith('.zip'):
        return True
    if filename == 'create_release_zip.py':
        return True
    _, ext = os.path.splitext(filename)
    if ext.lower() in EXCLUDE_EXTS:
        return True
    return False

def make_zip():
    print(f"[*] Bắt đầu đóng gói dự án từ: {ROOT_DIR}")
    start_time = time.time()
    
    file_count = 0
    total_size = 0
    
    with zipfile.ZipFile(OUTPUT_ZIP, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for root, dirs, files in os.walk(ROOT_DIR):
            # Lọc bỏ các thư mục không cần thiết để không duyệt sâu
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.edge_')]
            
            for f in files:
                abs_path = os.path.join(root, f)
                rel_path = os.path.relpath(abs_path, ROOT_DIR)
                
                if should_exclude(rel_path):
                    continue
                
                arcname = os.path.join("smart-parking-system", rel_path)
                zf.write(abs_path, arcname)
                file_count += 1
                total_size += os.path.getsize(abs_path)
                
    zip_size = os.path.getsize(OUTPUT_ZIP)
    duration = time.time() - start_time
    
    print(f"[+] Đã đóng gói thành công {file_count} tệp tin trong {duration:.2f} giây.")
    print(f"[+] Dung lượng gốc: {total_size / (1024*1024):.2f} MB -> Dung lượng nén ZIP: {zip_size / (1024*1024):.2f} MB")
    print(f"[+] Đường dẫn tệp ZIP tại ổ D: {OUTPUT_ZIP}")
    
    # Sao chép sang thư mục Downloads của người dùng
    try:
        shutil.copy2(OUTPUT_ZIP, DOWNLOADS_ZIP)
        print(f"[+] Đã sao chép sang thư mục Downloads: {DOWNLOADS_ZIP}")
    except Exception as e:
        print(f"[!] Không thể sao chép sang Downloads: {e}")

if __name__ == "__main__":
    make_zip()
