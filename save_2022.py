with open(r'C:\Users\LENOVO\.gemini\antigravity\brain\34425343-ff1b-46ef-a476-294ad3a89c79\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    import json
    lines = f.readlines()

for idx in [2021, 2022]:
    obj = json.loads(lines[idx])
    tc = obj.get('tool_calls', [])
    content = str(obj.get('content', ''))
    print(idx, len(tc), len(content))
    if content:
        with open('step_2022.txt', 'w', encoding='utf-8') as out:
            out.write(content)
        print('Wrote step_2022.txt, len:', len(content))
