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
tape_catalog = json.loads((ROOT / 'tapes.json').read_text())
tape_pairs = tape_catalog['pairs']
tape_specs = tape_catalog['tapes']
pair_members = [key for pair in tape_pairs for key in pair]
if (
    any(len(pair) != 2 for pair in tape_pairs)
    or len(pair_members) != len(set(pair_members))
    or set(pair_members) != set(tape_specs)
    or not any(a == tape_catalog['firstPair'] for a, _ in tape_pairs)
):
    raise ValueError('Each title tape must belong to exactly one weekly pair.')
registry = {
    'assets': assets, 'badges': badges,
    'tapes': {key: tape_catalog[key] for key in ('firstWeek', 'firstPair', 'pairs')},
}
tape_css = '\n'.join(
    f'[data-tape="{key}"]{{--tape-pattern:url("{data(ROOT / "assets/textures/tapes" / spec["file"])}");'
    f'--tape-size:{spec.get("size", "28px 18px")};--tape-base:{spec["color"]};--tape-ink:{spec["text"]}}}'
    for key, spec in tape_specs.items()
)
textures = {
    'plaster': 'tuscan-wash.webp',
    'fiber': 'card-fiber.webp',
    'week-waves': 'week-waves.svg',
    'marker': 'marker.svg',
    'chat-xuan': 'chat-xuan.webp',
    'chat-sand': 'chat-sand.webp',
    'chat-joy': 'chat-joy.webp',
}
variables = ':root{' + ''.join(
    f'--journal-{name}:url("{data(ROOT / "assets/textures" / file)}");' for name, file in textures.items()
) + '}'

source = (ROOT / 'base-v9.html').read_text()
dog = re.search(r'^const dog = "(data:image/[^"]+)";', source, re.M)[1]
source, brand_count = re.subn(r'(<div class="brand"><img src=")[^"]+', lambda m: m[1] + dog, source)
if brand_count != 1:
    raise ValueError('Expected one desktop brand mark in the v9 prototype.')
# Keep the original v9 source intact. Both task lists use the same orderRow()
# handle, so one replacement gives them the same single-colour drawn paw.
paw = (
    '<g fill="none" stroke="currentColor" stroke-width="1.45" '
    'stroke-linecap="round" stroke-linejoin="round">'
    '<ellipse cx="5.4" cy="10" rx="1.45" ry="1.85" transform="rotate(-20 5.4 10)"/>'
    '<ellipse cx="9.2" cy="6.9" rx="1.5" ry="2.05" transform="rotate(-8 9.2 6.9)"/>'
    '<ellipse cx="14.1" cy="6.8" rx="1.5" ry="2.1" transform="rotate(9 14.1 6.8)"/>'
    '<ellipse cx="18.4" cy="9.8" rx="1.4" ry="1.8" transform="rotate(21 18.4 9.8)"/>'
    '<path d="M7.4 16.7c.1-1.3 1.4-2.1 2.4-3.3.7-.8 1.2-1.5 2.2-1.5 '
    '1.1 0 1.8 1.1 2.5 1.9 1 .9 2.1 1.5 2.1 2.7 '
    '.1 1.7-1.2 2.5-2.8 2.4-.9 0-1.3-.4-2.1-.4 '
    '-1 0-1.5.5-2.5.5-1.5.1-2.7-.8-2.8-2.3z"/>'
    '</g>'
)
if source.count('const icons = {') != 1 or source.count('icon("hand")') != 1:
    raise ValueError('Expected one icon registry and one shared drag handle.')
source = source.replace('const icons = {', 'const icons = {"paw": ' + json.dumps(paw) + ',', 1)
source = source.replace('icon("hand")', 'icon("paw")', 1)
source = source.replace('右边的小手', '右边的狗爪')
journal_css = (ROOT / 'journal.css').read_text()
style = '\n'.join((variables, tape_css, journal_css))
code = 'const JOURNAL_LIBRARY=' + json.dumps(registry, ensure_ascii=False) + ';\n' + (ROOT / 'journal.js').read_text()
result = source.replace('</style>', style + '\n</style>', 1).replace('</body>', '<script>\n' + code + '\n</script>\n</body>')
(ROOT / 'dist').mkdir(exist_ok=True)
for name in ('dist/index.html', 'little-days-h5-journal.html'):
    (ROOT / name).write_text(result)


def asset_tiles(kind, group=None):
    return ''.join(
        f'<article data-kind="{kind}" data-group="{asset.get("group", "original")}">'
        f'<img loading="lazy" src="{asset["src"]}" alt=""><h3>{html.escape(asset["label"])}</h3></article>'
        for asset in assets if asset['kind'] == kind and asset.get('group') == group
    )


def section(title, tiles, id=""):
    section_id = f' id="{id}"' if id else ""
    return f'<section{section_id}><h2>{title}</h2><div class="grid">{tiles}</div></section>'


drawing_grids = ''.join(
    section(title, asset_tiles('doodle', group), 'drawings' if group == 'girl' else '')
    for group, title in (
        ('girl', '活动人物 · 小女孩'), ('cloud', '活动人物 · 云朵头'),
        ('objects', '日常物件'), ('animals', '动物'), ('food', '美食'), ('replace', '重画的四枚小图'),
    )
)
tape_tiles = ''.join(
    f'<article class="tape-set"><p>第 {index} 组</p><div class="materials">'
    + ''.join(
        f'<span class="swatch" data-tape="{key}"><i aria-hidden="true"></i>'
        f'{tape_specs[key]["label"]} · {tape_specs[key]["pattern"]}</span>'
        for key in pair
    ) + '</div></article>'
    for index, pair in enumerate(tape_pairs, 1)
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
{tape_css}
{journal_css}
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
article[data-kind="collage"]>img{{height:180px}}
h3{{font-size:15px;margin:6px 0 2px}}
article p{{font-size:13px;margin:0}}
.badge-view{{display:flex;align-items:center;gap:21px;min-height:89px}}
.materials{{display:grid;grid-template-columns:1fr 1fr;gap:11px;margin-top:9px}}
.tape-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px}}
.swatch{{display:grid;gap:6px;font-size:13px}}
.swatch i{{display:block;height:24px;background:var(--tape-background);background-blend-mode:normal,multiply,normal;clip-path:var(--tape-edge)}}
.corner-sample{{height:100px;position:relative;max-width:320px;padding:16px;background:var(--journal-fiber) 0 0 / 230px,#fffbf0}}
nav{{margin-top:15px;display:flex;flex-wrap:wrap;gap:8px 16px}}
.reference-grid{{grid-template-columns:repeat(auto-fit,minmax(95px,1fr))}}
.reference-grid article{{padding:8px 2px;text-align:center}}
.reference-grid h3{{font-size:12px}}
.reference-icon{{display:block;width:70px;height:70px;margin:auto;background-image:url("{atlas}");
background-size:{reference['columns'] * 70}px {reference['rows'] * 70}px;background-repeat:no-repeat}}
</style>
<main>
<header><img src="{dog}" alt="" width="51" height="51"><h1>小日子 · 手账素材库</h1></header>
<p>每周按本机记录选拼贴与小图，再换一组标题胶带。</p>
<nav aria-label="素材分类"><a href="#drawings">手绘小图</a><a href="#tapes">胶带</a><a href="#collages">拼贴</a><a href="#reference">53 张参考</a><a href="little-days-h5-journal.html#diary">打开日记</a></nav>
{drawing_grids}
<section id="tapes">
<h2>手账胶带 · {len(tape_specs)} 卷</h2>
<div class="tape-grid">{tape_tiles}</div>
<h2>固定角贴</h2>
<div class="corner-sample">绿格在后，砖红格在前<span class="corner-tape corner-tape-bottom" aria-hidden="true"><i></i><i></i></span></div>
</section>
<section id="collages">
<h2>原创拼贴 · 4 张</h2><div class="grid">{asset_tiles('collage')}</div>
<h2>分支拼贴 · 36 张</h2><p>摄影与拼贴同页的 10 张已单独裁出拼贴。</p><div class="grid">{asset_tiles('collage', 'photos')}</div>
</section>
<section id="reference">
<h2>参考小图 · {len(reference['icons'])} 张</h2>
<p>按原图顺序逐张收录。</p>
<div class="grid reference-grid">{reference_tiles}</div>
</section>
<h2>纸质徽章</h2><div class="grid">{badge_tiles}</div>
</main></html>"""
(ROOT / 'gallery.html').write_text(gallery)
(ROOT / 'dist/gallery.html').write_text(gallery.replace('href="little-days-h5-journal.html#diary"', 'href="index.html#diary"'))
print(f'Built {len(assets)} rotating assets, {len(reference["icons"])} reference doodles and 2 badges. Offline app {len(result.encode()):,} bytes.')
