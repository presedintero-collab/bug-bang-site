import zipfile,re,shutil,json
from pathlib import Path
from urllib.parse import urlsplit,unquote
src=Path('backup.zip'); out=Path('site'); domain='https://www.twistgeometry.org'
shutil.rmtree(out,ignore_errors=True); out.mkdir()
with zipfile.ZipFile(src) as z:
 for i in z.infolist():
  if i.is_dir(): continue
  n=i.filename.replace('\\','/'); t=None
  if n.startswith('pages/'):
   b=n[6:]; b='newpage.html' if b=='newpage' else ('google-sitemap.xml' if b=='google-sitemap' else b); t=out/b if b else None
  elif n.startswith('fragments/'): t=out/n
  else:
   c=n.lstrip('/'); m='cdn.websumo.com/assets/'
   if c.startswith(m): t=out/'assets'/c[len(m):]
  if t: t.parent.mkdir(parents=True,exist_ok=True); t.write_bytes(z.read(i))

def localize(u):
 if not u or u.startswith(('#','mailto:','tel:','javascript:','data:')): return u
 for pre in ('https://cdn.websitepublisher.ai/custom/wid23603/','//cdn.websitepublisher.ai/custom/wid23603/','https://cdn.websumo.com/assets/','//cdn.websumo.com/assets/'):
  if u.startswith(pre):
   rel=u[len(pre):].split('?',1)[0].split('#',1)[0]
   return 'assets/'+rel if (out/'assets'/unquote(rel)).exists() else u
 p=urlsplit(u)
 if p.scheme in ('http','https') and p.netloc.lower() in ('bug-bang-theory.org','www.bug-bang-theory.org'):
  q=unquote(p.path.lstrip('/')) or 'index.html'; q=q+'.html' if not Path(q).suffix and (out/(q+'.html')).exists() else q; return q
 if p.scheme or p.netloc:return u
 q=unquote(p.path); q=q.lstrip('/') or 'index.html'
 if q.startswith(('images/','files/')) and (out/'assets'/q).exists(): q='assets/'+q
 if not Path(q).suffix and (out/(q+'.html')).exists(): q+='.html'
 return q+('?' + p.query if p.query else '')+('#'+p.fragment if p.fragment else '')
attr=re.compile(r'\b(href|src|action)\s*=\s*(["\'])([^"\']*)\2',re.I)
cdn=re.compile(r'(?:https:)?//cdn\.(?:websitepublisher\.ai/custom/wid23603|websumo\.com/assets)/[^\s"\'<>]+',re.I)
for f in out.glob('*.html'):
 s=f.read_text('utf-8','replace')
 s=re.sub(r'<!--\s*WPE-DEBUG.*?-->','',s,flags=re.I|re.S)
 s=re.sub(r'<script\b[^>]*wpe/loader\.js[^>]*>\s*</script>','',s,flags=re.I)
 s=attr.sub(lambda m:f'{m.group(1)}={m.group(2)}{localize(m.group(3))}{m.group(2)}',s)
 s=cdn.sub(lambda m:localize(m.group(0)),s)
 s=re.sub(r'hostname\s*=\s*(["\'])//www\.bug-bang-theory\.org\1\s*;','hostname = window.location.host;',s,flags=re.I)
 can=domain+('/' if f.name=='index.html' else '/'+f.name)
 s=re.sub(r'<link\b[^>]*rel=["\']canonical["\'][^>]*>',f'<link rel="canonical" href="{can}">',s,count=1,flags=re.I)
 for n in ('robots','googlebot'):
  pat=rf'<meta\b[^>]*name=["\']{n}["\'][^>]*>'; tag=f'<meta name="{n}" content="noindex, nofollow">'
  s=re.sub(pat,tag,s,count=1,flags=re.I) if re.search(pat,s,re.I) else s.replace('</head>',tag+'</head>',1)
 if 'bug-bang-migration' not in s:s=s.replace('</head>','<meta name="bug-bang-migration" content="github-ready-2026-07-12"></head>',1)
 f.write_text(s,encoding='utf-8')
(out/'404.html').write_text('<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><title>404 — BUG BANG</title><h1>404</h1><p><a href="index.html">BUG BANG</a></p>',encoding='utf-8')
pages=sorted(f.name for f in out.glob('*.html') if f.name not in {'404.html','admin-upload.html','bug-bang.html'})
(out/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{domain+("/" if n=="index.html" else "/"+n)}</loc></url>\n' for n in pages)+'</urlset>\n')
(out/'robots.txt').write_text(f'User-agent: *\nDisallow: /\nSitemap: {domain}/sitemap.xml\n');(out/'.nojekyll').write_text('')
missing=[]
for f in out.glob('*.html'):
 for u in re.findall(r'\b(?:href|src|action)=["\']([^"\']+)',f.read_text('utf-8','replace'),re.I):
  if not u.startswith(('#','http:','https:','mailto:','tel:','javascript:','data:','//')) and not (out/unquote(urlsplit(u).path)).exists(): missing.append([f.name,u])
report={'pages':len(list(out.glob('*.html'))),'assets':len([p for p in (out/'assets').rglob('*') if p.is_file()]),'missing_local_references':missing,'status':'preview-noindex'}
(out/'MIGRATION_REPORT.json').write_text(json.dumps(report,indent=2)); print(report)
if missing: raise SystemExit(2)
