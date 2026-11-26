/* Build inserts a small registry with inline asset URIs before this file. */
const JournalDecor=(function(){
  const library=JOURNAL_LIBRARY;
  const paletteVersion='journal-c-c-b-1';
  const allowed=note=>note.include_in_review!==false&&!note.revoked&&!note.revokedAt;
  function records(range){
    return [...(state.snippets||[]),...(state.diary||[])].filter(n=>range.includes(n.date)&&allowed(n));
  }
  function contextFor(range){
    const text=records(range).map(n=>n.text||'').concat((state.habits||[]).filter(h=>(h.logs||[]).some(l=>range.includes(l.date))).map(h=>h.name||'')).join('\n');
    const categories=[
      ['outdoors',/散步|走走|晒太阳|公园|骑车|爬山|游泳|跑步|户外|海边/],
      ['learning',/读书|阅读|小说|写作|论文|复习|学习|背单词|画画|练琴/],
      ['rest',/喝茶|咖啡|泡澡|睡觉|休息|电影|听歌|音乐|做饭|烘焙/]
    ];
    const scores=categories.map(([id,re])=>[id,(text.match(new RegExp(re.source,'g'))||[]).length]);
    scores.sort((a,b)=>b[1]-a[1]);return scores[0][1]?scores[0][0]:'neutral';
  }
  function weekNumber(monday){return Math.floor(Date.parse(monday+'T12:00:00Z')/604800000);}
  function pick(kind,category,week,previousID){
    const all=library.assets.filter(a=>a.kind===kind&&a.enabled!==false);
    let pool=all.filter(a=>a.contexts.includes(category));if(pool.length<2)pool=all;
    const start=((week%pool.length)+pool.length)%pool.length;
    let item=pool[start];if(item.id===previousID&&pool.length>1)item=pool[(start+1)%pool.length];return item;
  }
  function planFor(anchor){
    const range=weekDays(anchor),key=range[0];
    state.journalDecorWeeks ||= {};
    const old=state.journalDecorWeeks[key];
    const valid=id=>library.assets.some(a=>a.id===id&&a.enabled!==false);
    if(old&&valid(old.collage)&&valid(old.doodle))return old;
    const previous=state.journalDecorWeeks[shiftDay(key,-7)];
    const category=contextFor(range),number=weekNumber(key);
    const plan={version:paletteVersion,collage:pick('collage',category,number,previous?.collage).id,doodle:pick('doodle',category,number,previous?.doodle).id};
    state.journalDecorWeeks[key]=plan;save();return plan;
  }
  function vignette(anchor,place){
    const plan=planFor(anchor),box=document.createElement('div');box.className='journal-vignette';box.dataset.place=place;box.setAttribute('aria-hidden','true');
    for(const kind of ['collage','doodle']){const a=library.assets.find(a=>a.id===plan[kind]);const img=document.createElement('img');img.className='journal-'+kind;img.src=a.src;img.alt='';img.width=kind==='collage'?172:65;img.height=kind==='collage'?150:88;img.decoding='async';box.append(img);}
    return box;
  }
  function support(range){
    const notes=records(range).filter(n=>/散步|运动|走走|游泳|骑车|爬山|跑步|读书|阅读|小说|泡澡|追剧|电影|逛|音乐|听歌|练琴|画画|做饭|烘焙|咖啡|喝茶|晒太阳|朋友/.test(n.text||''));
    const habits=(state.habits||[]).filter(h=>(h.logs||[]).some(l=>range.includes(l.date)));
    const i=((weekNumber(range[0])%3)+3)%3;
    if(notes.length)return [
      '你把这些小片刻也留了下来，真好。生活里属于自己的这一小块，也值得被好好看见。',
      '做事之外，你也记下了自己的生活和感受。能给自己留一点位置，真好。',
      '这些看起来小小的片刻，也是这周的一部分。忙自己的事，也记得看看阳光、听听风声。'
    ][i];
    if(habits.length)return '这周，你为「'+habits[0].name+'」留下了记录。愿意给自己的小事留时间，真好。';
    const current=localDate(new Date());
    if(range[0]>current)return '这周还没开始。想不想先给自己留一件小事？听一首歌，或去喜欢的地方走走。';
    return [
      '这周留下的生活片段不多，也许只是还没来得及记。下周想给自己留十分钟，晒晒太阳吗？',
      '没有记下来，也不等于没有。下次遇到一个舒服的小片刻，可以随口告诉我。',
      '下周想给自己留一件喜欢的小事吗？听首歌、慢慢喝杯茶，或者什么也不安排地坐一会儿。'
    ][i];
  }
  function badge(type,title){return '<span class="badge" title="'+esc(title)+'"><img src="'+library.badges[type]+'" width="28" height="28" alt="'+esc(title)+'"></span>';}
  function enhance(){
    let [page,view,anchor]=(location.hash.slice(1)||'tasks').split('/');
    if(page==='review'){anchor=view;view='week';page='diary';}
    const enabled=page==='diary'||page==='insights';document.body.classList.toggle('journal-on',enabled);if(!enabled)return;
    const existing=main.querySelector('.journal-vignette');if(existing)existing.remove();
    if(page==='diary'&&view==='week'){
      const day=/^\d{4}-\d{2}-\d{2}$/.test(anchor||'')?anchor:localDate(new Date());
      const cards=main.querySelectorAll('.review-card');
      cards[0]?.querySelector('h2')?.classList.add('tape-title');
      cards[1]?.querySelector('h2')?.classList.add('tape-title','tape-coral');
      // Badges belong to each selected-week row, never to a card corner/header.
      main.querySelectorAll('.pw-head .badge').forEach(el=>el.remove());
      const life=cards[1];
      life?.querySelector('p.empty')?.remove();
      if(life&&!life.querySelector('.journal-support')){const block=document.createElement('div');block.className='journal-support';const p=document.createElement('p');p.textContent=support(weekDays(day));block.append(p);life.append(block);}
      cards[cards.length-1]?.append(vignette(day,'week'));
    }else if(page==='diary'){
      main.querySelector('.recap-card h2')?.classList.add('tape-title');
      main.querySelector('.diary-entry:not(.recap-card) h2')?.classList.add('tape-title','tape-blue');
      main.querySelector('.workspace > aside')?.append(vignette(localDate(new Date()),'today'));
    }
  }
  return {enhance,planFor,contextFor,support,pick,weekNumber,badge};
})();

// Retain the uploaded v9 functions, routes and forms. Apply bounded decoration after render.
weekBadges=function(s){
  return (s.done&&s.selfCount?JournalDecor.badge('crown','完成与生活，两头都留下了记录'):'')+
    (s.rate>80?JournalDecor.badge('rose','这一周做完了绝大部分事项'):'');
};
const journalBaseRender=render;
render=function(){journalBaseRender();JournalDecor.enhance();};
render();
// An open tab can cross a week boundary; only refresh decorative elements, not user input.
let journalLastWeek=weekDays(localDate(new Date()))[0];
function checkJournalWeek(){const key=weekDays(localDate(new Date()))[0];if(key!==journalLastWeek){journalLastWeek=key;JournalDecor.enhance();}}
setInterval(checkJournalWeek,60000);
document.addEventListener('visibilitychange',()=>{if(!document.hidden)checkJournalWeek();});
