with open('step_2623.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'^\s*(\d+):\s*(.*)$', text, re.MULTILINE)
print('step_2623 range:', matches[0][0], 'to', matches[-1][0])
for m in matches[:10]:
    print(m[0], m[1][:60].encode('ascii', 'replace').decode('ascii'))
print('---')
for m in matches[-10:]:
    print(m[0], m[1][:60].encode('ascii', 'replace').decode('ascii'))
