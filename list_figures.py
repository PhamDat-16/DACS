import docx
import sys

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document('Bao_cao_do_an_Smart_Parking_System.docx')
for i, p in enumerate(doc.paragraphs):
    if 'Hình ' in p.text:
        print(f"{i}: {p.text}")

