/* Build inserts a small registry with inline asset URIs before this file. */
const JournalDecor=(function(){
  const library=JOURNAL_LIBRARY;
  const paletteVersion='journal-c-c-b-3';
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
  function tapePairFor(day){
    const first=library.tapes.pairs.findIndex(pair=>pair[0]===library.tapes.firstPair);
    const offset=weekNumber(weekDays(day)[0])-weekNumber(library.tapes.firstWeek);
    const count=library.tapes.pairs.length;
    return library.tapes.pairs[((first+offset)%count+count)%count];
  }
  function addCorner(card,position){
    if(!card||card.querySelector('.corner-tape'))return;
    const tape=document.createElement('span');
    tape.className='corner-tape corner-tape-'+position;
    tape.setAttribute('aria-hidden','true');
    tape.append(document.createElement('i'),document.createElement('i'));
    card.append(tape);
  }
  function stampTitle(title,tape,second=false){
    if(!title)return;
    title.classList.add('tape-title');
    title.classList.toggle('tape-second',second);
    title.dataset.tape=tape;
  }
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
  function decoratePlan(){
    const card=main.querySelector('[data-plan-toggle]')?.closest('.diary-entry');
    if(!card||card.querySelector('.journal-plan-actions'))return;
    card.classList.add('journal-plan');
    const actions=document.createElement('div');
    actions.className='journal-plan-actions';
    let chat=card.querySelector('[data-plan-chat]');
    if(!chat){
      chat=document.createElement('button');
      chat.type='button';
      chat.dataset.go='chat';
      chat.dataset.planChat='1';
    }
    const add=card.querySelector('[data-new=tomorrow]');
    const oldActions=add?.parentElement;
    chat.className='journal-plan-chat';
    chat.innerHTML=icon('bubble')+'<span>去聊天里说</span><span class="plan-arrow" aria-hidden="true">→</span>';
    actions.append(chat);
    if(add)actions.append(add);
    oldActions?.remove();
    card.querySelector('.section-head').after(actions);
  }
  function decorateSupport(card,day){
    if(!card)return;
    card.querySelector('.journal-support')?.remove();
    card.querySelector('p.empty')?.remove();
    const block=document.createElement('div');
    block.className='journal-support';
    const drawing=document.createElement('img');
    drawing.src=library.assets.find(a=>a.id==='resting-head').src;
    drawing.alt='';
    const paragraph=document.createElement('p'),text=document.createElement('span');
    text.className='journal-marker';
    text.textContent=support(weekDays(day));
    paragraph.append(text);
    block.append(drawing,paragraph);
    card.append(block);
  }
  function enhance(){
    let [page,view,anchor]=(location.hash.slice(1)||'tasks').split('/');
    if(page==='review'){anchor=view;view='week';page='diary';}
    document.body.classList.toggle('journal-chat-on',page==='chat');
    if(page==='chat'){
      const header=main.querySelector('.pagehead');
      header?.querySelector('.mobile-mark')?.remove();
      header?.querySelector('p')?.remove();
      main.querySelector('.composer textarea')?.setAttribute('placeholder','记待办、拆步骤，或者聊聊卡在了哪里…');
      if(header&&!header.querySelector('.journal-chat-art')){
        const art=document.createElement('div');
        art.className='journal-chat-art';
        art.setAttribute('aria-hidden','true');
        header.append(art);
      }
    }
    const enabled=page==='diary'||page==='insights';
    document.body.classList.toggle('journal-on',enabled);
    if(!enabled)return;
    main.querySelectorAll('.journal-vignette').forEach(el=>el.remove());
    main.querySelectorAll(page==='insights'?'.ins':'.diary-entry,.diary-actions,.review-card,.calendar')
      .forEach(el=>el.classList.add('journal-paper'));
    if(page==='diary'&&view==='week'){
      const day=/^\d{4}-\d{2}-\d{2}$/.test(anchor||'')?anchor:localDate(new Date());
      const cards=main.querySelectorAll('.review-card');
      const [first,second]=tapePairFor(day);
      stampTitle(cards[0]?.querySelector('h2'),first);
      stampTitle(cards[2]?.querySelector('h2'),second,true);
      cards[1]?.classList.add('journal-self-time');
      addCorner(cards[1],'top');
      main.querySelectorAll('.pw-head .badge').forEach(el=>el.remove());
      main.querySelectorAll('.bar-col').forEach(col=>{
        if(col.querySelector('strong')?.textContent==='0')col.setAttribute('data-empty','');
      });
      decorateSupport(cards[1],day);
      cards[2]?.append(vignette(day,'week'));
    }else if(page==='diary'){
      const day=localDate(new Date()),[first,second]=tapePairFor(day);
      const recap=main.querySelector('.recap-card');
      const feelings=main.querySelector('.diary-entry:not(.recap-card)');
      stampTitle(recap?.querySelector('h2'),first);
      feelings?.classList.add('journal-feelings');
      addCorner(feelings,'top');
      recap?.append(vignette(day,'today'));
      decoratePlan();
      const planChat=main.querySelector('.journal-plan-chat');
      if(planChat)planChat.dataset.tape=second;
    }
  }
  return {enhance,planFor,contextFor,support,pick,weekNumber,tapePairFor,badge};
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
