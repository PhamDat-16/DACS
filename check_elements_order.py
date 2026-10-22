import docx
import sys

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document(r'C:\Users\LENOVO\Downloads\BAO_CAO_DACS.docx')
for i, el in enumerate(doc._body._element):
    tag = el.tag.split('}')[-1]
    if tag == 'p':
        p_text = el.xpath('.//w:t')
        t = ''.join([node.text for node in p_text]) if p_text else ''
        if t.strip():
            print(f"{i:02d} [P]: {t[:60]}")
    elif tag == 'tbl':
        # print first row of table
        t_text = el.xpath('.//w:t')
        header = ' | '.join([node.text for node in t_text[:6]])
        print(f"{i:02d} [TABLE]: {header}")

