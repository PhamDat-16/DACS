with open('rc_857.txt', 'r', encoding='utf-8') as f:
    rc = f.read()

print('rc_857 length:', len(rc))
print('Starts with:')
print(rc[:300].encode('ascii', 'replace').decode('ascii'))
print('Ends with:')
print(rc[-300:].encode('ascii', 'replace').decode('ascii'))
