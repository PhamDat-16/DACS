for step_id in [261, 275, 277]:
    print(f'=== STEP {step_id} ===')
    with open(f'step_{step_id}.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    for l in text.splitlines()[:25]:
        print(l.encode('ascii', 'replace').decode('ascii'))
