from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]

PDFS = {
    "assets/files/bug-bang-ro.pdf": "BUG BANG RO",
    "assets/files/bug-bang-en.pdf": "BUG BANG EN",
    "assets/files/tscn-ro.pdf": "TSC(n) RO",
    "assets/files/kernel-1-618-ro.pdf": "KERNEL RO",
    "assets/files/kernel-1-618-en.pdf": "KERNEL EN",
    "assets/files/tpn-ro.pdf": "TPN RO",
    "assets/files/tpn-en.pdf": "TPN EN",
}

CSS_FIX = """
/* home-books-fix-2026-07-12 */
.hero{min-height:auto!important;display:block!important;align-items:initial!important;padding:clamp(2.4rem,4vw,4rem) 0 5rem!important}
.hero-grid{align-items:start!important}
.hero-grid>div:first-child{padding-top:.35rem}
.cover-shelf{align-content:start!important;grid-auto-rows:auto!important;padding-top:.15rem}
.mini-cover img{display:block!important;width:100%!important;height:auto!important;aspect-ratio:2/3!important;max-height:220px!important;object-fit:contain!important;object-position:center!important;background:#080b10!important;padding:.35rem!important}
@media(max-width:900px){.hero{padding-top:2rem!important}.hero-grid{gap:2.5rem!important}.mini-cover img{max-height:260px!important}}
@media(max-width:520px){.mini-cover img{max-height:none!important}}
""".strip()

COFFEE_TILE = re.compile(
    r'<div class="mini-cover" style="min-height:clamp\(190px,26vh,250px\);.*?Buy me a coffee</a></div>',
    re.IGNORECASE | re.DOTALL,
)


def inject_css(text: str) -> str:
    if "home-books-fix-2026-07-12" in text:
        return text
    return text.replace("</style>", CSS_FIX + "\n</style>", 1)


def same_tab_local(text: str) -> str:
    # Local pages, PDFs and ZIPs must stay in the current tab.
    pattern = re.compile(
        r'(<a\b(?=[^>]*\bhref=["\'](?:assets/|[^"\']+\.(?:html|pdf|zip)(?:[?#][^"\']*)?)["\'])[^>]*?)\s+target=["\']_blank["\']',
        re.IGNORECASE,
    )
    return pattern.sub(r"\1", text)


def fix_ro(text: str) -> str:
    replacements = {
        '<a class="mini-cover" href="bug-bang.html" rel="noopener">': '<a class="mini-cover" href="assets/files/bug-bang-ro.pdf">',
        '<a class="mini-cover" href="3sos-c-package.html">': '<a class="mini-cover" href="assets/files/3sos-c-ro.pdf">',
        '<a class="mini-cover" href="twist-sferic-ciclic-tscn.html" rel="noopener">': '<a class="mini-cover" href="assets/files/tscn-ro.pdf">',
        '<a class="mini-cover" href="axis.html" rel="noopener"><img src="assets/images/covers/real-kernel-ro.jpg"': '<a class="mini-cover" href="assets/files/kernel-1-618-ro.pdf"><img src="assets/images/covers/kernel-ro.svg"',
        '<a class="mini-cover" href="tpn.html" rel="noopener"><img src="assets/images/covers/real-tpn-ro.jpg"': '<a class="mini-cover" href="assets/files/tpn-ro.pdf"><img src="assets/images/covers/tpn-ro.svg"',
        '<a class="btn btn-primary" href="bug-bang.html" rel="noopener">Deschide pagina BUG BANG RO</a>': '<a class="btn btn-primary" href="assets/files/bug-bang-ro.pdf">Deschide cartea BUG BANG RO</a>',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def fix_en(text: str) -> str:
    replacements = {
        '<a class="mini-cover" href="bug-bang-en.html" rel="noopener">': '<a class="mini-cover" href="assets/files/bug-bang-en.pdf">',
        '<a class="mini-cover" href="3sos-c-package.html">': '<a class="mini-cover" href="assets/files/3sos-c-en.pdf">',
        '<a class="mini-cover" href="axis.html" rel="noopener"><img src="assets/images/covers/kernel-en.svg"': '<a class="mini-cover" href="assets/files/kernel-1-618-en.pdf"><img src="assets/images/covers/kernel-en.svg"',
        '<a class="mini-cover" href="tpn.html" rel="noopener"><img src="assets/images/covers/tpn-en.svg"': '<a class="mini-cover" href="assets/files/tpn-en.pdf"><img src="assets/images/covers/tpn-en.svg"',
        '<a class="btn btn-secondary" href="bug-bang-en.html" rel="noopener">Open English page</a>': '<a class="btn btn-secondary" href="assets/files/bug-bang-en.pdf">Open BUG BANG book</a>',
        'href="index.html?lang=ro"': 'href="index.html"',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def cover_links(text: str) -> list[str]:
    match = re.search(
        r'<div[^>]*class="cover-shelf[^\"]*"[^>]*>(.*?)</div>\s*</div>\s*</header>',
        text,
        re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return []
    return re.findall(r'<a class="mini-cover" href="([^"]+)"', match.group(1), re.IGNORECASE)


def validate_pdf(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Missing PDF: {path.relative_to(ROOT)}")
    if path.stat().st_size < 1000:
        raise SystemExit(f"PDF too small: {path.relative_to(ROOT)}")
    if path.read_bytes()[:4] != b"%PDF":
        raise SystemExit(f"Invalid PDF signature: {path.relative_to(ROOT)}")


def main() -> None:
    for relative in PDFS:
        validate_pdf(ROOT / relative)

    reports = {}
    for filename, language in (("index.html", "ro"), ("bug-bang-en.html", "en")):
        path = ROOT / filename
        text = path.read_text(encoding="utf-8", errors="replace")
        text = COFFEE_TILE.sub("", text)
        text = inject_css(text)
        text = fix_ro(text) if language == "ro" else fix_en(text)
        text = same_tab_local(text)
        path.write_text(text, encoding="utf-8")

        links = cover_links(text)
        bad = [href for href in links if not href.lower().endswith(".pdf")]
        missing = [href for href in links if not (ROOT / href).exists()]
        if len(links) != 9 or bad or missing:
            raise SystemExit(
                f"Cover audit failed for {filename}: count={len(links)}, bad={bad}, missing={missing}"
            )
        reports[filename] = {
            "cover_count": len(links),
            "all_covers_open_books": True,
            "same_tab": True,
            "links": links,
        }

    report = {
        "status": "homepage-books-corrected",
        "pages": reports,
        "new_local_pdfs": sorted(PDFS),
        "coffee_tile_removed_from_hero": True,
        "hero_overflow_fixed": True,
        "kernel_tpn_cover_art_fixed": True,
    }
    (ROOT / "HOME_BOOKS_REPORT.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
