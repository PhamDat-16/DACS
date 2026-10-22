with open('step_2627.txt', 'w', encoding='utf-8') as out:
    with open(r'C:\Users\LENOVO\.gemini\antigravity\brain\34425343-ff1b-46ef-a476-294ad3a89c79\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
        import json
        lines = f.readlines()
    obj = json.loads(lines[2627])
    out.write(obj.get('content', ''))
print('Wrote step_2627.txt')
