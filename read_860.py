with open('step_860.txt', 'r', encoding='utf-8') as f:
    text = f.read()

for l in text.splitlines()[:20]:
    print(l.encode('ascii', 'replace').decode('ascii'))
