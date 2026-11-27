"""Editable project-native badges, doodles, tapes and a quiet plaster texture."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
INK='#4e5146'
def svg(body,box='0 0 120 120'):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{box}" fill="none" stroke="{INK}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{body}</svg>'
def write(kind,name,body,box='0 0 120 120'):
    p=ROOT/'assets'/kind/(name+'.svg');p.parent.mkdir(exist_ok=True,parents=True);p.write_text(svg(body,box))

# Paper discs remain simple enough to read at 24px. One jewel, a narrow rose.
disc='<path d="M32 2.8C48 2 61 15 61 31.8C62 48 48 62 32 61C15 62 2 48 3 32C2 15 15 2 32 2.8Z" fill="{color}" stroke="{edge}" stroke-width="1.2"/>'
write('badges','crown',disc.format(color='#e9ddee',edge='#a59aa9')+'<path d="M14 24L22 31L31.7 16.6L42 31L50.1 23.6L46.5 45.3Q31 47 17.7 44.8Z" fill="#f3d68d" stroke="#77704e" stroke-width="1.6"/><path d="M18.7 41.4Q32 42.4 46.4 41.4" stroke="#d2ae63"/><circle cx="14" cy="23.5" r="2.5" fill="#f3d68d" stroke="#77704e"/><circle cx="31.8" cy="15.8" r="2.8" fill="#f3d68d" stroke="#77704e"/><circle cx="50" cy="23.4" r="2.5" fill="#f3d68d" stroke="#77704e"/><circle cx="32" cy="35.5" r="2.6" stroke="none" fill="#cc806e"/>','0 0 64 64')
write('badges','rose',disc.format(color='#e1e7cf',edge='#a4ad90')+'<path d="M32 32Q31 41 32.6 51" stroke="#728461"/><path d="M32 43C23 44 20 38 20 36C26 35 30 38 32 43Z" fill="#a8b791" stroke="#748363"/><path d="M32 47C36 39 42 39 44 40C42 46 37 48 32 47Z" fill="#a8b791" stroke="#748363"/><path d="M31.5 34C26 32 23 26 24.8 22C22.8 17 27 12 31 14C35 10 39 14 39 18C43 21 39.3 28 36.8 30.3Z" fill="#dba196" stroke="#926f68" stroke-width="1.45"/><path d="M28.1 21.5C30 16.7 36.8 19.4 35.1 23.5C34.1 26.1 30 26.8 29.7 24M25.5 24C27.2 28.3 31.2 30 36.5 28" stroke="#a37870" stroke-width="1.25"/>','0 0 64 64')

head='<path d="M49 36C47 23 54 18 61 19C70 18 76 27 73 35C72 43 55 45 49 36Z" fill="#fffaf0"/><path d="M52 25Q62 19 71 28" stroke-width="3"/><path d="M57 33h.3M66 33h.3" stroke-width="2.5"/><path d="M59 37q3 2 5-.4"/>'
doodles={
'sun-friend':head+'<path d="M53 44Q48 60 48 77Q60 82 74 76L69 44M50 49L32 38L28 24M70 49L87 37L91 23M53 80L51 98L43 99M68 80L72 99L80 99"/><path d="M29 24l-4-4m4 4l1-6m60 6l5-4m-4 4v-7"/><circle cx="18" cy="57" r="8" fill="#f1d689" stroke="none"/><path d="M18 44v-4M18 70v4M5 57H1M31 57h4M8 47l-3-3M28 67l3 3" stroke="#c2a458"/>',
'little-reader':head+'<path d="M52 45Q44 56 43 71L60 77L80 69Q77 53 70 44M47 53L36 66L49 70M72 54L86 64L72 70M45 82L37 95L55 95M75 82L84 95H66"/><path d="M36 65L58 70L59 90L35 82ZM58 70L83 65L82 83L59 90Z" fill="#e0e7d2"/><path d="M41 72l10 3M66 75l10-3" stroke="#87937b"/>',
'tea-friend':head+'<path d="M53 44L46 79L74 78L69 44M49 52L36 60L47 67M71 51L82 61L71 67M51 81L48 99M69 80L75 99M35 68H87M40 69V98M84 69V98"/><path d="M53 54H67L66 67H54ZM67 56Q76 55 73 62L67 63" fill="#f0dfca"/><path d="M58 48q-4-4 0-8m6 8q4-4 0-8" stroke="#a9aca0"/>',
'gentle-stretch':head+'<path d="M53 44L48 76L72 76L68 44M52 46L35 33L35 14M69 46L84 32L82 14M53 79L45 101M68 79L77 101M35 14l-4-6m4 6l3-7m44 7l-4-5m4 5l4-6"/><path d="M89 57q7 3 8 11m-7 3q6 3 6 8" stroke="#c5a66c"/>',
'little-walker':head+'<path d="M54 44L49 73L70 76L69 44M51 51L34 65M69 51L83 58M52 75L40 98L31 98M67 77L79 92L87 92"/><path d="M90 39Q82 22 94 18Q105 14 110 27Q113 39 101 42L90 39ZM97 42V77" fill="#dfe6d4"/><path d="M16 105Q60 102 105 105" stroke="#b5bda8"/>',
'resting-head':'<path d="M42 53C37 39 45 26 59 26C75 23 83 39 77 53" fill="#fffaf0"/><path d="M43 37Q55 26 72 34" stroke-width="3"/><path d="M49 44q3 2 5 0m10 0q3 2 5 0"/><path d="M44 52C28 45 24 63 43 64L60 60C74 67 92 62 85 51C81 47 74 48 68 51"/><path d="M21 63L98 62L101 91L18 91ZM25 93V102M94 93V102" fill="#e7e9dd"/><path d="M44 73L70 72L68 84L43 85Z"/><path d="M88 24h6l-5 7h7m6-15h5l-4 5h5" stroke="#9da395"/>',
'small-bloom':'<path d="M61 49C52 39 39 44 44 55C31 58 38 71 49 68C50 80 65 83 69 70C81 78 88 65 77 58C87 47 72 36 66 47Z" fill="#ebc8bd"/><circle cx="61" cy="59" r="5" fill="#ead18b"/><path d="M61 78Q56 93 63 110M59 95C45 99 42 85 45 83Q57 81 59 95M61 101C74 103 81 89 77 87Q65 86 61 101" fill="#dfe6d1"/>',
'bird-branch':'<path d="M14 86Q61 78 104 86" stroke="#9ba98e"/><path d="M38 77C18 70 22 50 34 46C41 43 51 50 48 59L62 56L52 66C49 75 43 79 38 77Z" fill="#eee2c4"/><path d="M74 76C57 66 67 45 78 49C89 49 95 58 91 66L102 69L91 74C87 80 80 81 74 76Z" fill="#e4d5dd"/><path d="M35 54h.2M80 57h.2" stroke-width="3"/><path d="M31 64q8 7 13-2M73 67q8 6 13 0M35 78v7m7-7v7m36-7v7m7-7v7"/>',
'moon-cloud':'<path d="M73 22C45 23 40 54 66 63C46 75 23 56 29 38C34 24 49 16 73 22Z" fill="#f0d995"/><path d="M40 83C19 83 15 65 27 59C35 53 43 57 46 63C52 49 71 53 72 65C91 59 103 77 89 84Z" fill="#e4dce9"/><path d="M95 29v10m-5-5h10M14 42v7m-3-4h6" stroke="#b19d71"/>',
'book-spark':'<path d="M19 46Q42 40 59 49Q79 39 101 46L99 91Q79 87 61 97Q41 87 21 92Z" fill="#e1e7d5"/><path d="M59 49L61 97M28 54q15-2 22 2M29 63q14-1 22 3M72 56l20-3M72 67l18-3"/><path d="M72 14L75 22L84 25L75 29L72 37L68 29L59 25L68 22Z" fill="#edd48f" stroke="#b7a06c"/>'
}
for name,body in doodles.items(): write('doodles',name,body)

# Quiet irregular texture: page-wide scale, no dense lines, no stains.
texture='''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="900" viewBox="0 0 1200 900"><defs><filter id="plaster"><feTurbulence type="fractalNoise" baseFrequency=".008 .013" numOctaves="3" seed="23" stitchTiles="stitch"/><feColorMatrix type="matrix" values="0 0 0 0 .52 0 0 0 0 .45 0 0 0 0 .34 0 0 0 .12 0"/></filter><filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".63" numOctaves="2" seed="8" stitchTiles="stitch"/><feColorMatrix type="matrix" values="0 0 0 0 .61 0 0 0 0 .55 0 0 0 0 .43 0 0 0 .085 0"/></filter></defs><rect width="1200" height="900" fill="#f6f0e6"/><rect width="1200" height="900" filter="url(#plaster)"/><rect width="1200" height="900" filter="url(#grain)"/><g fill="none" stroke="#ad9d85" opacity=".055" stroke-width=".8"><path d="M-40 215C130 115 180 310 320 245S470 135 510 200M650 530C820 390 930 620 1100 530S1230 440 1260 480M200 680C340 555 430 760 570 695M700 140C840 75 900 245 1060 155"/><path d="M-40 220C130 120 180 315 320 250S470 140 510 205M650 535C820 395 930 625 1100 535S1230 445 1260 485"/></g><g stroke="#b6a58b" opacity=".14" stroke-width=".8"><path d="M122 83l7 3M404 350l-3 7M747 622l9-2M1036 178l2 7M922 810l7 3M259 812l4-6"/></g></svg>'''
(ROOT/'assets/textures/plaster.svg').write_text(texture)
wave='''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="300" viewBox="0 0 1000 300" preserveAspectRatio="none"><g fill="none" stroke="#a9b59c" stroke-width="1.1" opacity=".32"><path d="M-20 38C160 10 240 75 420 38S730 8 1020 40M-20 100C130 66 280 134 450 100S780 72 1020 102M-20 165C140 129 290 194 460 167S790 135 1020 168M-20 232C180 194 280 262 470 230S800 201 1020 234"/></g></svg>'''
(ROOT/'assets/textures/week-waves.svg').write_text(wave)
for name,color in [('sage','#b9c5aa'),('coral','#e0b5a6'),('blue','#b4c6ce')]:
    tile=f'''<svg xmlns="http://www.w3.org/2000/svg" width="72" height="36"><rect width="72" height="36" fill="{color}" opacity=".36"/><g fill="{color}" opacity=".34"><path d="M0 0h9v36H0zM18 0h9v36h-9zM36 0h9v36h-9zM54 0h9v36h-9z"/><path d="M0 0h72v9H0zM0 18h72v9H0z"/></g></svg>'''
    (ROOT/f'assets/textures/tape-{name}.svg').write_text(tile)
print('2 badges, 10 doodles, 5 surface/tape assets created')
