"""Build the offline journal prototype and its asset gallery."""
from pathlib import Path
import base64
import html
import json
import mimetypes
import re

ROOT = Path(__file__).resolve().parents[1]


def data(path):
    mime = mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
    return f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode()


manifest = json.loads((ROOT / 'manifest.json').read_text())
assets = [{**asset, 'src': data(ROOT / asset['path'])} for asset in manifest['assets']]
badges = {name: data(ROOT / 'assets/badges' / f'{name}.svg') for name in ('crown', 'rose')}
registry = {'assets': assets, 'badges': badges}
textures = {
    'plaster': 'tuscan-wash.webp',
    'fiber': 'card-fiber.webp',
    'week-waves': 'week-waves.svg',
    'marker': 'marker.svg',
}
variables = ':root{' + ''.join(
    f'--journal-{name}:url("{data(ROOT / "assets/textures" / file)}");' for name, file in textures.items()
) + '}'

source = (ROOT / 'base-v9.html').read_text()
dog = re.search(r'^const dog = "(data:image/[^"]+)";', source, re.M)[1]
source, brand_count = re.subn(r'(<div class="brand"><img src=")[^"]+', lambda m: m[1] + dog, source)
if brand_count != 1:
    raise ValueError('Expected one desktop brand mark in the v9 prototype.')
style = variables + '\n' + (ROOT / 'journal.css').read_text()
code = 'const JOURNAL_LIBRARY=' + json.dumps(registry, ensure_ascii=False) + ';\n' + (ROOT / 'journal.js').read_text()
result = source.replace('</style>', style + '\n</style>', 1).replace('</body>', '<script>\n' + code + '\n</script>\n</body>')
(ROOT / 'dist').mkdir(exist_ok=True)
for name in ('dist/index.html', 'little-days-h5-journal.html'):
    (ROOT / name).write_text(result)


def asset_tiles(kind):
    return ''.join(
        f'<article data-kind="{kind}"><img src="{asset["src"]}" alt=""><h3>{html.escape(asset["label"])}</h3></article>'
        for asset in assets if asset['kind'] == kind
    )


badge_tiles = ''.join(
    f'<article><div class="badge-view"><img src="{badges[key]}" alt="" width="84" height="84">'
    f'<img src="{badges[key]}" alt="" width="26" height="26"></div><h3>{label}</h3><p>{description}</p></article>'
    for key, label, description in (
        ('crown', '小皇冠', '只留中间一颗红点'), ('rose', '细长玫瑰', '纸质圆章')
    )
)
reference_dir = ROOT / 'assets/reference'
reference = json.loads((reference_dir / 'reference-doodles.json').read_text())
atlas = data(reference_dir / reference['atlas'])
reference_tiles = ''.join(
    f'<article data-reference="{item["id"]}"><span class="reference-icon" aria-hidden="true" '
    f'style="background-position:{-item["column"] * 70}px {-item["row"] * 70}px"></span>'
    f'<h3>{html.escape(item["label"])}</h3></article>'
    for item in reference['icons']
)

gallery = f"""<!doctype html>
<html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>小日子 · 手账素材库</title>
<style>
{variables}
{(ROOT / 'journal.css').read_text().split('body.journal-on', 1)[0]}
*{{box-sizing:border-box}}
body{{margin:0;background:#efe6d7 var(--journal-plaster) center top / 620px;color:#384a3a;font:16px/1.6 -apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif}}
main{{max-width:1080px;margin:auto;padding:34px 20px 60px}}
header{{display:flex;align-items:center;gap:14px}}
header img{{object-fit:contain}}
h1{{font-size:clamp(24px,6vw,34px);margin:0}}
h2{{margin:34px 0 16px;font-size:clamp(20px,4.5vw,26px)}}
p{{color:#5c6557}}
a{{color:#3d5840;text-underline-offset:3px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(148px,1fr));gap:13px}}
article,.materials{{padding:16px;background:var(--journal-fiber) 0 0 / 285px,#fffcf3;clip-path:var(--paper-edge);min-width:0}}
article>img{{width:100%;height:135px;object-fit:contain}}
h3{{font-size:15px;margin:6px 0 2px}}
article p{{font-size:13px;margin:0}}
.badge-view{{display:flex;align-items:center;gap:21px;min-height:89px}}
.materials{{display:flex;flex-wrap:wrap;align-items:center;gap:14px}}
.materials span{{display:inline-block;padding:4px 12px;clip-path:var(--tape-edge);color:#36483b}}
.yellow{{background:var(--tape-yellow);background-blend-mode:normal,normal,multiply}}
.lilac{{background:var(--tape-lilac);background-blend-mode:normal,normal,multiply}}
.orange{{background:var(--tape-orange);background-blend-mode:normal,multiply}}
.reference-grid{{grid-template-columns:repeat(auto-fit,minmax(95px,1fr))}}
.reference-grid article{{padding:8px 2px;text-align:center}}
.reference-grid h3{{font-size:12px}}
.reference-icon{{display:block;width:70px;height:70px;margin:auto;background-image:url("{atlas}");
background-size:{reference['columns'] * 70}px {reference['rows'] * 70}px;background-repeat:no-repeat}}
</style>
<main>
<header><img src="{dog}" alt="" width="51" height="51"><h1>小日子 · 手账素材库</h1></header>
<p>每周按本机记录选择一张拼贴和一个小图案。<br><a href="little-days-h5-journal.html#diary">看日记里的使用效果</a></p>
<h2>胶带拼贴</h2><div class="grid">{asset_tiles('collage')}</div>
<h2>手绘小图案</h2><div class="grid">{asset_tiles('doodle')}</div>
<h2>纸张、胶带与徽章</h2>
<div class="materials"><span class="yellow">鹅黄点纹</span><span class="lilac">淡紫格纹</span><span class="orange">暖橙斜纹</span>托斯卡纳灰泥与手工纸</div>
<div class="grid" style="margin-top:13px">{badge_tiles}</div>
<h2>参考图全套 · {len(reference['icons'])} 个</h2>
<p>按原图顺序收录，可逐个查看。日记的每周轮换使用上方原创素材。</p>
<div class="grid reference-grid">{reference_tiles}</div>
</main></html>"""
(ROOT / 'gallery.html').write_text(gallery)
(ROOT / 'dist/gallery.html').write_text(gallery.replace('href="little-days-h5-journal.html#diary"', 'href="index.html#diary"'))
print(f'Built {len(assets)} rotating assets, {len(reference["icons"])} reference doodles and 2 badges. Offline app {len(result.encode()):,} bytes.')
