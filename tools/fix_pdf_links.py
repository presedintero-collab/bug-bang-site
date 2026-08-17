from pathlib import Path
import re
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]

PATTERN = re.compile(
    r'href=(?P<q>["\'])(?:https://twistphysics\.org/|/)?assets/files/(?P<file>[^"\']+\.pdf)(?P=q)',
    re.IGNORECASE,
)

changed = []
for path in sorted(ROOT.glob('*.html')):
    if path.name == 'pdf-viewer.html':
        continue
    text = path.read_text(encoding='utf-8', errors='replace')

    def repl(match):
        filename = match.group('file')
        viewer = 'pdf-viewer.html?file=' + quote('assets/files/' + filename, safe='/-_.()')
        return f'href="{viewer}"'

    new_text, count = PATTERN.subn(repl, text)
    if count:
        path.write_text(new_text, encoding='utf-8')
        changed.append((path.name, count))

print('PDF viewer links updated:', sum(c for _, c in changed))
for name, count in changed:
    print(f'  {name}: {count}')
