with open(r'C:\Users\LENOVO\.gemini\antigravity\brain\34425343-ff1b-46ef-a476-294ad3a89c79\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    import json
    lines = f.readlines()

for idx in [1774, 1776, 2579]:
    obj = json.loads(lines[idx])
    content = str(obj.get('content', ''))
    with open(f'step_{idx}.txt', 'w', encoding='utf-8') as out:
        out.write(content)
    print(f'Wrote step_{idx}.txt, len: {len(content)}')
