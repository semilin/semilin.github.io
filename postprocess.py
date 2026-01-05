from pathlib import Path

for p in Path('./docs/').rglob('*'):
    if not p.suffix == '.html': continue
    print(p)
    with open(p, 'r') as f:
        t = f.read()
        t = t.replace('.html', '')
    with open(p, 'w') as f: f.write(t)
        
