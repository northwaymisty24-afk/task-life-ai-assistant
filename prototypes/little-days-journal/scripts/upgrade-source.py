"""Apply confirmed journal UI controls while leaving the v9 source itself intact."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
def upgrade(source):
    icons=json.loads(re.search(r'const icons = (.*);',source)[1])
    icons['hand']='''<g fill="none" stroke="currentColor" stroke-width="1.45" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="5.4" cy="10" rx="1.45" ry="1.85" transform="rotate(-20 5.4 10)"/><ellipse cx="9.2" cy="6.9" rx="1.5" ry="2.05"/><ellipse cx="14.1" cy="6.8" rx="1.5" ry="2.1"/><ellipse cx="18.4" cy="9.8" rx="1.4" ry="1.8" transform="rotate(21 18.4 9.8)"/><path d="M7.4 16.7c.1-1.3 1.4-2.1 2.4-3.3.7-.8 1.2-1.5 2.2-1.5 1.1 0 1.8 1.1 2.5 1.9 1 .9 2.1 1.5 2.1 2.7.1 1.7-1.2 2.5-2.8 2.4-.9 0-1.3-.4-2.1-.4-1 0-1.5.5-2.5.5-1.5.1-2.7-.8-2.8-2.3z"/></g>'''
    source=re.sub(r'const icons = .*;',lambda _: 'const icons = '+json.dumps(icons,ensure_ascii=False)+';',source,count=1)
    source=source.replace('右边的小手','右边的狗爪')
    start=source.index('function diaryTabs(active){');end=source.index('function diaryPage',start)
    source=source[:start]+'''function diaryTabs(active){
  return '<nav class="tabbar diary-tabs" aria-label="日记时间范围">'+
    '<button type="button" class="diary-tab" aria-pressed="'+(active==="today")+'" data-go="diary">'+icon("sun")+'<span>今天</span></button>'+
    '<button type="button" class="diary-tab" aria-pressed="'+(active==="week")+'" data-go="diary/week">'+icon("review")+'<span>这周</span></button>'+
    '</nav>';
}
''' +source[end:]
    return source
