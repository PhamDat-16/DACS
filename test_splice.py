with open('frontend/index.html', 'r', encoding='utf-8') as f:
    curr = f.read()

pos_trunc = curr.find('... [truncated for diff preview]')
print('pos_trunc in curr:', pos_trunc)

with open('rc_857.txt', 'r', encoding='utf-8') as f:
    rc = f.read()

needle = "models: ['Evo 200 / Lite', 'Feliz S"
pos_needle = rc.find(needle)
print('pos_needle in rc:', pos_needle)

# In curr, the line before truncation is:
# "            models: ['Evo 200 / Lite', 'Feliz S\n"
# So from curr[:pos_trunc] we replace with rc from that point!
line_start_in_curr = curr.rfind("models: ['Evo 200 / Lite', 'Feliz S", 0, pos_trunc)
print('line_start_in_curr:', line_start_in_curr)

part1 = curr[:line_start_in_curr]
part2 = rc[pos_needle:]

print('part1 ends with:', repr(part1[-100:]))
print('part2 starts with:', repr(part2[:100]))
print('part2 ends with:', repr(part2[-100:]))
