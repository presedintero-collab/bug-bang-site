from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]

LINK_MAP = {
    '14KtULzxWly5vfo1aH8fd66MByqYQ5jiI': 'bug-bang.html',
    '1PQIS4HMxEfrb1xqVO7fUztpFQlvg3LOE': 'twist-sferic-ciclic-tscn.html',
    '19bTnZtVBYiHGRFfaPup5at6N0tU5Wtzy': 'axis.html',
    '1JGolfjVkp62bpnfnF3pFQxn6ED9SH0w4': 'tpn.html',
    '1OaxxZZNUzmNPi1-uCLPNTppnK2qN9Mig': 'bug-bang-en.html',
    '1C2p-5YDYse2wM3BTk1G7v-IEjAWr6Nov': 'axis.html',
    '12aoQzHaMDAMijT6N_lRp3WQJM5hbzxTm': 'tpn.html',
}

THUMB_MAP = {
    '14KtULzxWly5vfo1aH8fd66MByqYQ5jiI': 'assets/images/covers/bug-bang-ro.png',
    '1QfFTCvZrYuHI0k7bZtuYt4xcI6GnS73R': 'assets/images/covers/real-kernel-ro.jpg',
    '18YdSlPfZWbWV21RD6jhMj6cv9tgvOYxS': 'assets/images/covers/real-tpn-ro.jpg',
    '1OaxxZZNUzmNPi1-uCLPNTppnK2qN9Mig': 'assets/images/covers/bug-bang-en.png',
    '1tgf0TAY1HP0-z4qtN-CR7uk8c3IWQIvo': 'assets/images/covers/kernel-en.svg',
    '13cqHnHeQMh6Pc2A6DI3c3pXZiYOxi5kZ': 'assets/images/covers/tpn-en.svg',
}

INTERNAL_NO_INDEX = {
    '404.html',
    'admin-upload.html',
    'bug-bang.html',
    'documente.html',
    'home.html',
    'newpage.html',
}

FORBIDDEN = (
    'drive.google.com',
    'docs.google.com',
    'websitepublisher.ai',
    'bug-bang-theory.org',
    'twistgeometry.org',
    'cdn.websumo.com',
    'cdn.websitepublisher.ai',
)


def replace_drive_links(text: str) -> str:
    for file_id, destination in LINK_MAP.items():
        text = re.sub(
            r'https://drive\.google\.com/file/d/' + re.escape(file_id) + r'/view\?[^"\'\s<]*',
            destination,
            text,
        )
    for file_id, destination in THUMB_MAP.items():
        text = re.sub(
            r'https://drive\.google\.com/thumbnail\?id=' + re.escape(file_id) + r'&[^"\'\s<]*',
            destination,
            text,
        )
    return text


def clean_html(path: Path) -> None:
    text = path.read_text(encoding='utf-8', errors='replace')

    text = re.sub(
        r'\s*<!-- WebsitePublisher\.ai Powered-by Widget -->.*?(?=</body>)',
        '\n',
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    text = text.replace('https://www.twistgeometry.org', 'https://twistphysics.org')
    text = text.replace('https://twistgeometry.org', 'https://twistphysics.org')
    text = text.replace('https://www.bug-bang-theory.org', 'https://twistphysics.org')
    text = replace_drive_links(text)

    text = text.replace(
        'https://cdn.websitepublisher.ai/custom/wid23603/files/tpn-web-ro-complet-webopt.pdf',
        'tpn.html',
    )
    text = text.replace(
        'https://cdn.websitepublisher.ai/custom/wid23603/files/tpn-web-en-complete-webopt.pdf',
        'tpn.html',
    )
    text = text.replace(
        'https://cdn.websitepublisher.ai/custom/wid23603/',
        'https://twistphysics.org/assets/',
    )

    label_replacements = {
        'Deschide PDF-ul BUG BANG RO': 'Deschide pagina BUG BANG RO',
        'Open English PDF': 'Open English page',
        'Open the rebuilt English BUG BANG PDF': 'Open the English BUG BANG page',
        'Deschide PDF RO': 'Deschide pagina RO',
        'Descarcă PDF RO': 'Deschide pagina TPN RO',
        'Download PDF EN': 'Open TPN English section',
        'KERNEL 1.618 English PDF': 'KERNEL 1.618 English page',
        'TPN(n) English PDF': 'TPN(n) English page',
        'KERNEL 1.618 RO PDF': 'KERNEL 1.618 RO page',
        'TPN(n) RO PDF': 'TPN(n) RO page',
    }
    for old, new in label_replacements.items():
        text = text.replace(old, new)

    text = re.sub(r'>Deschide PDF<', '>Deschide pagina<', text)
    text = re.sub(r'>Open PDF<', '>Open page<', text)

    if path.name == 'index.html':
        text = text.replace(
            'Aceasta este pagina română separată. Pagina principală a site-ului este acum versiunea engleză.',
            'Aceasta este pagina principală în limba română. Versiunea engleză este disponibilă separat.',
        )
        text = text.replace(
            'href="index.html">Deschide pagina EN principală',
            'href="bug-bang-en.html">Deschide pagina EN',
        )
        text = text.replace(
            '<a href="index.html">EN principal</a>',
            '<a href="bug-bang-en.html">EN</a>',
        )

    if path.name == 'technical-library.html':
        text = text.replace(
            '<a href="index.html">EN</a>',
            '<a href="bug-bang-en.html">EN</a>',
        )

    if path.name == 'newpage.html':
        text = (
            '<!doctype html>\n'
            '<html lang="ro"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="robots" content="noindex, nofollow">'
            '<title>Pagină retrasă — BUG BANG</title>'
            '<meta http-equiv="refresh" content="0; url=index.html">'
            '<link rel="canonical" href="https://twistphysics.org/">'
            '</head><body><p>Această pagină veche a fost retrasă. '
            '<a href="index.html">Deschide BUG BANG</a>.</p></body></html>\n'
        )

    if path.name not in INTERNAL_NO_INDEX:
        text = re.sub(
            r'\s*<meta\s+name=["\']robots["\'][^>]*>',
            '',
            text,
            flags=re.IGNORECASE,
        )
        text = re.sub(
            r'\s*<meta\s+name=["\']googlebot["\'][^>]*>',
            '',
            text,
            flags=re.IGNORECASE,
        )

    path.write_text(text, encoding='utf-8')


def build_sitemaps() -> None:
    public_pages = sorted(
        path.name for path in ROOT.glob('*.html') if path.name not in INTERNAL_NO_INDEX
    )

    (ROOT / 'robots.txt').write_text(
        'User-agent: *\nAllow: /\n\nSitemap: https://twistphysics.org/sitemap.xml\n',
        encoding='utf-8',
    )

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    plain_urls = []
    for name in public_pages:
        url = 'https://twistphysics.org/' if name == 'index.html' else f'https://twistphysics.org/{name}'
        lines.append(f'  <url><loc>{url}</loc></url>')
        plain_urls.append(url)
    lines.append('</urlset>')
    xml = '\n'.join(lines) + '\n'

    for relative in ('sitemap.xml', 'google-sitemap.xml', 'assets/google-sitemap.xml'):
        target = ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(xml, encoding='utf-8')

    (ROOT / 'sitemap.txt').write_text('\n'.join(plain_urls) + '\n', encoding='utf-8')

    llms = ROOT / 'assets/llms.txt'
    if llms.exists():
        text = llms.read_text(encoding='utf-8', errors='replace')
        text = text.replace('https://www.bug-bang-theory.org', 'https://twistphysics.org')
        text = text.replace('https://www.twistgeometry.org', 'https://twistphysics.org')
        text = text.replace('https://twistgeometry.org', 'https://twistphysics.org')
        llms.write_text(text, encoding='utf-8')


def audit() -> dict:
    forbidden_hits = []
    missing_local = []
    attribute_pattern = re.compile(r'(?:href|src)=["\']([^"\']+)["\']', re.IGNORECASE)

    for path in sorted(ROOT.rglob('*')):
        if not path.is_file() or path.suffix.lower() not in {'.html', '.xml', '.txt'}:
            continue
        text = path.read_text(encoding='utf-8', errors='replace')
        for token in FORBIDDEN:
            if token in text:
                forbidden_hits.append({'file': str(path.relative_to(ROOT)), 'token': token})

        if path.suffix.lower() != '.html':
            continue
        for match in attribute_pattern.finditer(text):
            value = match.group(1)
            if value.startswith(('http://', 'https://', '//', '#', 'mailto:', 'tel:', 'data:', 'javascript:')):
                continue
            relative = value.split('#', 1)[0].split('?', 1)[0]
            if not relative:
                continue
            target = (path.parent / relative).resolve()
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                continue
            if not target.exists():
                missing_local.append({'file': path.name, 'reference': value})

    report = {
        'pages': len(list(ROOT.glob('*.html'))),
        'public_pages': len([p for p in ROOT.glob('*.html') if p.name not in INTERNAL_NO_INDEX]),
        'assets': 48,
        'forbidden_external_references': forbidden_hits,
        'missing_local_references': missing_local,
        'status': 'corrected-live' if not forbidden_hits and not missing_local else 'audit-failed',
    }
    (ROOT / 'MIGRATION_REPORT.json').write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + '\n',
        encoding='utf-8',
    )
    return report


def main() -> None:
    for path in sorted(ROOT.glob('*.html')):
        clean_html(path)

    test_file = ROOT / '_test-tree.txt'
    if test_file.exists():
        test_file.unlink()

    build_sitemaps()
    report = audit()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report['status'] != 'corrected-live':
        raise SystemExit('Migration audit failed')


if __name__ == '__main__':
    main()
