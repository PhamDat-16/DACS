with open('target_time_validation.txt', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
print('Total lines in target_time_validation:', len(lines))
print('First 15 lines:')
for l in lines[:15]:
    print(l[:80].encode('ascii', 'replace').decode('ascii'))
print('---')
print('Last 15 lines:')
for l in lines[-15:]:
    print(l[:80].encode('ascii', 'replace').decode('ascii'))
