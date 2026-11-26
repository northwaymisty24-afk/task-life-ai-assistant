"""Build an offline single-file prototype and an offline asset contact sheet."""
from pathlib import Path
import base64, json, mimetypes, html

ROOT=Path(__file__).resolve().parents[1]
def data(path):
    mime=mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
    return 'data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode()

collages=[
 ('tea-pause','慢慢喝杯茶',['rest','neutral']),
 ('sprout-notes','小小的新芽',['learning','neutral']),
 ('sunny-window','窗边的阳光',['outdoors','rest','neutral']),
 ('garden-pause','树下坐一会',['outdoors','learning','neutral'])]
doodles=[
 ('sun-friend','伸手接一点阳光',['outdoors','neutral']),
 ('little-reader','慢慢读',['learning','neutral']),
 ('tea-friend','茶歇小人',['rest','neutral']),
 ('gentle-stretch','伸个懒腰',['rest','neutral']),
 ('little-walker','出去走走',['outdoors','neutral']),
 ('resting-head','趴一会儿',['rest','neutral']),
 ('small-bloom','一朵小花',['outdoors','neutral']),
 ('bird-branch','枝头小鸟',['outdoors','neutral']),
 ('moon-cloud','月亮和云',['rest','neutral']),
 ('book-spark','书里的一点光',['learning','neutral'])]
assets=[]
for kind,items,ext in [('collage',collages,'webp'),('doodle',doodles,'svg')]:
    folder='collages' if kind=='collage' else 'doodles'
    for name,label,contexts in items:
        assets.append(dict(id=name,label=label,kind=kind,contexts=contexts,path=f'assets/{folder}/{name}.{ext}',enabled=True,origin='generated' if kind=='collage' else 'original-svg',version=1))
manifest={'version':1,'style':'C 底色 / C 胶带 / B 纸质圆章','rotation':'one collage + one doodle per browser-local Monday-based week','assets':assets}
manifest_file=ROOT/'manifest.json'
if manifest_file.exists():
    manifest=json.loads(manifest_file.read_text());assets=manifest['assets']
else:
    manifest_file.write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
registry={'assets':[{**a,'src':data(ROOT/a['path'])} for a in assets],
          'badges':{k:data(ROOT/f'assets/badges/{k}.svg') for k in ['crown','rose']}}
textures={'plaster':'plaster.svg','tape-sage':'tape-sage.svg','tape-coral':'tape-coral.svg','tape-blue':'tape-blue.svg','week-waves':'week-waves.svg'}
vars=':root{'+''.join(f'--journal-{k}:url("{data(ROOT/"assets/textures"/v)}");' for k,v in textures.items())
sun='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><g stroke="#b8a36a" fill="none" stroke-linecap="round"><circle cx="12" cy="12" r="4" fill="#ecd18a"/><path d="M12 1v3m0 16v3M1 12h3m16 0h3M4 4l2 2m12 12l2 2M4 20l2-2M18 6l2-2"/></g></svg>'
vars+='--journal-sun:url("data:image/svg+xml;base64,'+base64.b64encode(sun.encode()).decode()+'");}'
source=(ROOT/'base-v9.html').read_text()
style=vars+'\n'+(ROOT/'journal.css').read_text()
code='const JOURNAL_LIBRARY='+json.dumps(registry,ensure_ascii=False)+';\n'+(ROOT/'journal.js').read_text()
result=source.replace('</style>',style+'\n</style>',1).replace('</body>','<script>\n'+code+'\n</script>\n</body>')
(ROOT/'dist').mkdir(exist_ok=True)
for name in ['dist/index.html','little-days-h5-journal.html']:(ROOT/name).write_text(result)

tiles=[]
for a in assets:
    tiles.append(f'<article data-kind="{a["kind"]}"><img src="{data(ROOT/a["path"])}" alt="{html.escape(a["label"])}"><h3>{html.escape(a["label"])}</h3><p>{a["id"]} · {a["kind"]}</p></article>')
badges=''.join(f'<article><div class="badges"><img src="{registry["badges"][k]}" alt="{label}" width="96" height="96"><img src="{registry["badges"][k]}" alt="" width="26" height="26"></div><h3>{label}</h3><p>{desc}</p></article>' for k,label,desc in [('crown','小皇冠','只留中间一颗红点'),('rose','细长玫瑰','收窄花头，保留纸质圆章')])
collage_tiles=''.join(tile for a,tile in zip(assets,tiles) if a['kind']=='collage')
doodle_tiles=''.join(tile for a,tile in zip(assets,tiles) if a['kind']=='doodle')
gallery=f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>小日子 · 手账素材库</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#f6f0e6;color:#344d3e;font:16px/1.65 -apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif}}main{{max-width:1120px;margin:auto;padding:40px 24px}}h1{{font-size:34px;margin:0}}h2{{margin:30px 0 16px}}p{{color:#687163}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:18px}}article{{padding:20px;border:1px solid #ddd6c9;border-radius:18px;background:#fffdf7}}article>img{{width:100%;height:170px;object-fit:contain}}h3{{font-size:17px;margin:12px 0 4px}}article p{{font-size:12px;overflow-wrap:anywhere;margin:0}}.badges{{display:flex;align-items:center;justify-content:center;gap:35px;min-height:110px}}.badges img{{display:block}}.swatch{{height:160px;border-radius:16px;background:var(--journal-plaster);margin-top:18px}}{vars}</style><main><h1>小日子 · 手账素材库</h1><p>C 底色 · C 胶带 · B 纸质圆章<br>每周选一张拼贴和一个小图案；同一周固定，记录只在本机参与选择。</p><div class="swatch" aria-label="浅米色灰泥质感"></div><h2>日历周行旁的小徽章</h2><div class="grid">{badges}</div><h2>胶带拼贴</h2><div class="grid">{collage_tiles}</div><h2>儿童简笔小图案</h2><div class="grid">{doodle_tiles}</div><p>参考图仅用于研究材质、造型与配色。新增素材在 manifest 中登记后即可轮换；完整说明见 README。</p></main></html>'''
for name in ['gallery.html','dist/gallery.html']:(ROOT/name).write_text(gallery)
print(f'Built {len(assets)} rotating assets + 2 badges; offline app {len(result.encode()):,} bytes')
