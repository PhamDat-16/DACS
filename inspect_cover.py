import docx
import sys

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document(r'C:\Users\LENOVO\Downloads\BAO_CAO_DACS.docx')
for i, p in enumerate(doc.paragraphs[:32]):
    print(f"{i:02d}: '{p.text}'")

