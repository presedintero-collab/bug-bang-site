from pathlib import Path
from urllib.request import Request, urlopen
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'https://project23603.websitepublisher.ai/bug-bang-en.html'
TARGET = ROOT / 'bug-bang-en.html'

req = Request(SOURCE, headers={'User-Agent': 'Mozilla/5.0'})
with urlopen(req, timeout=45) as response:
    text = response.read().decode('utf-8', errors='replace')

text = text.replace('https://project23603.websitepublisher.ai/', '/')
text = text.replace('https://cdn.websitepublisher.ai/custom/wid23603/images/', '/assets/images/')
text = text.replace('https://cdn.websitepublisher.ai/custom/wid23603/files/', '/assets/files/')
text = text.replace('https://www.bug-bang-theory.org/', 'https://twistphysics.org/bug-bang-en.html')
text = re.sub(r'<link rel="canonical"[^>]*>', '<link rel="canonical" href="https://twistphysics.org/bug-bang-en.html">', text, count=1, flags=re.I)
text = text.replace('<meta name="robots" content="noindex, nofollow">', '<meta name="robots" content="index, follow">')
text = re.sub(r'<script[^>]+cdn\.websitepublisher\.ai/wpe/loader\.js[^>]*></script>', '', text, flags=re.I)
text = re.sub(r'<script type="text/javascript">hostname\s*=.*?</script>', '', text, flags=re.I | re.S)
marker = '<!-- WebsitePublisher.ai Powered-by Widget -->'
if marker in text:
    text = text.split(marker, 1)[0].rstrip() + '\n</body>\n</html>\n'

TARGET.write_text(text, encoding='utf-8')
print(f'Synced {TARGET.name}: {len(text)} chars')
