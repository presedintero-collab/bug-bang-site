from pathlib import Path
from urllib.parse import urlsplit
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SITE_HOSTS = {'twistphysics.org', 'www.twistphysics.org'}
TARGET_RE = re.compile(r'\s+target\s*=\s*(?:"[^"]*"|\'[^\']*\'|[^\s>]+)', re.I)
FORMTARGET_RE = re.compile(r'\s+formtarget\s*=\s*(?:"[^"]*"|\'[^\']*\'|[^\s>]+)', re.I)
HREF_RE = re.compile(r'\bhref\s*=\s*(["\'])(.*?)\1', re.I | re.S)
ANCHOR_RE = re.compile(r'<a\b[^>]*>', re.I | re.S)
BASE_RE = re.compile(r'<base\b[^>]*>', re.I | re.S)


def is_internal(href: str) -> bool:
    href = href.strip()
    if not href or href.startswith(('#', 'mailto:', 'tel:', 'javascript:', 'data:')):
        return not href.startswith(('mailto:', 'tel:', 'javascript:', 'data:'))
    parsed = urlsplit(href)
    if not parsed.scheme and not parsed.netloc:
        return True
    return parsed.netloc.lower() in SITE_HOSTS


def clean_anchor(match: re.Match) -> str:
    tag = match.group(0)
    href_match = HREF_RE.search(tag)
    if not href_match or not is_internal(href_match.group(2)):
        return tag
    return TARGET_RE.sub('', tag)


def clean_html(path: Path) -> None:
    text = path.read_text(encoding='utf-8', errors='replace')
    text = ANCHOR_RE.sub(clean_anchor, text)
    text = BASE_RE.sub(lambda m: TARGET_RE.sub('', m.group(0)), text)
    text = FORMTARGET_RE.sub('', text)

    marker = 'id="same-tab-internal-links"'
    if marker not in text:
        runtime_guard = (
            '<script id="same-tab-internal-links">'
            'document.addEventListener("DOMContentLoaded",function(){'
            'document.querySelectorAll("a[target]").forEach(function(a){'
            'var h=a.getAttribute("href")||"";'
            'try{var u=new URL(h,window.location.href);'
            'if(u.origin===window.location.origin){a.removeAttribute("target");}}'
            'catch(e){a.removeAttribute("target");}'
            '});});</script>'
        )
        text = text.replace('</body>', runtime_guard + '</body>', 1)

    path.write_text(text, encoding='utf-8')


def audit() -> dict:
    internal_new_tab = []
    base_targets = []
    window_open_hits = []

    for path in sorted(ROOT.glob('*.html')):
        text = path.read_text(encoding='utf-8', errors='replace')
        for base in BASE_RE.findall(text):
            if TARGET_RE.search(base):
                base_targets.append(path.name)
        for tag in ANCHOR_RE.findall(text):
            href_match = HREF_RE.search(tag)
            if href_match and is_internal(href_match.group(2)) and TARGET_RE.search(tag):
                internal_new_tab.append({'file': path.name, 'href': href_match.group(2)})
        if re.search(r'window\.open\s*\(', text, re.I):
            window_open_hits.append(path.name)

    report_path = ROOT / 'MIGRATION_REPORT.json'
    report = {}
    if report_path.exists():
        try:
            report = json.loads(report_path.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            report = {}
    report['internal_new_tab_references'] = internal_new_tab
    report['base_target_references'] = base_targets
    report['window_open_pages'] = window_open_hits
    report['navigation_status'] = 'same-tab-corrected' if not internal_new_tab and not base_targets else 'navigation-audit-failed'
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return report


def main() -> None:
    for path in sorted(ROOT.glob('*.html')):
        clean_html(path)
    report = audit()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report['navigation_status'] != 'same-tab-corrected':
        raise SystemExit('Navigation audit failed')


if __name__ == '__main__':
    main()
