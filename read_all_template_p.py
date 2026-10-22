import docx
import sys

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document(r'C:\Users\LENOVO\Downloads\BAO_CAO_DACS.docx')
for i, p in enumerate(doc.paragraphs):
    print(f"{i:02d} [{p.style.name}]: '{p.text}'")

