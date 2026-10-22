with open('view_2533.txt', 'r', encoding='utf-8') as f:
    t = f.read()

import re
matches = re.findall(r'^\s*(\d+):\s*(.*)$', t, re.MULTILINE)
for m in matches[:10]:
    print(m[0], m[1].encode('ascii', 'replace').decode('ascii'))
