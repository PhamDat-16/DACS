with open('view_2525.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'^\s*(\d+):\s*(.*)$', text, re.MULTILINE)
print('view_2525 range:', matches[0][0], 'to', matches[-1][0])
for m in matches[-50:]:
    print(m[0], m[1].encode('ascii', 'replace').decode('ascii'))
