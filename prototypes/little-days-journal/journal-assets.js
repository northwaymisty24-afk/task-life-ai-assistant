const JournalAssets=(()=>{
  const lib=JOURNAL_LIBRARY;
  function element(a,className=''){
    if(!a)return document.createElement('span');
    const box=document.createElement('span');box.className='journal-art '+className;box.dataset.assetId=a.id;box.setAttribute('aria-hidden','true');box.title=a.label||'';
    const img=document.createElement('img');img.alt='';img.draggable=false;img.decoding='async';
    if(a.sheet){
      const sheet=lib.sheets[a.sheet],[x,y,w,h]=a.crop;
      const frame=document.createElement('span');frame.className='sprite-window';
      const fit=Math.min(1,w/h),fitH=Math.min(1,h/w);
      frame.style.cssText=`width:${fit*100}%;height:${fitH*100}%;left:${(1-fit)*50}%;top:${(1-fitH)*50}%`;
      img.src=sheet.src;img.style.cssText=`position:absolute;max-width:none;width:${sheet.width/w*100}%;height:${sheet.height/h*100}%;left:${-x/w*100}%;top:${-y/h*100}%;object-fit:fill`;
      frame.append(img);box.append(frame);box.classList.add('journal-sprite');
    }else{img.src=a.src;box.append(img);}
    return box;
  }
  const matches=[
    ['用牙线',/牙线|口腔|刷牙/],['深呼吸',/呼吸/],['远眺',/远眺|看远|护眼|眼保/],['背单词',/单词|词汇|英语|外语/],
    ['早睡',/早睡|睡前|按时睡|早点睡/],['早起',/早起|起床/],['午休',/午休|午睡|小憩/],['冥想',/冥想|正念/],
    ['喝水',/喝水|饮水|补水(?!面膜)/],['骑车',/骑车|骑行|自行车/],['瑜伽',/瑜伽/],['拉伸',/拉伸|伸展|活动肩/],['游泳',/游泳|游水/],
    ['跑步',/跑步|慢跑|晨跑|夜跑/],['散步',/散步|走路|走走|步行|遛狗/],['健身',/健身|力量|哑铃|运动|锻炼/],
    ['晒太阳',/太阳|户外|阳光/],['吃早餐',/早餐|早饭/],['吃蔬菜',/蔬菜|青菜/],['吃水果',/水果|苹果/],['少糖',/少糖|控糖|奶茶|甜食/],
    ['练字',/练字|书法/],['写作',/写作|论文|写文章/],['读书',/读书|阅读|看书|读.*书/],['学新知',/学习|课程|学新|学会/],
    ['复盘',/复盘|回顾|总结|计划/],['整理房间',/整理|收拾|打扫|清洁/],['记录心情',/心情|日记|记录|感恩/],['护肤',/护肤|面膜|洗脸/],['联系朋友',/联系|朋友|家人|父母|聊天/]
  ];
  function habitBadge(h){
    const label=matches.find(([,re])=>re.test(h.name))?.[0];
    if(label)return lib.habitBadges.find(a=>a.label===label);
    const n=Array.from(h.name||h.id||'').reduce((sum,ch)=>sum+ch.codePointAt(0),0);
    return lib.habitBadges[n%lib.habitBadges.length];
  }
  const notebook='<svg aria-hidden="true" viewBox="0 0 110 100" fill="none" stroke="#64664f" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"><path d="m25 20 60 8-12 65-62-7z" fill="#f1e6cb"/><path d="m33 12 61 10-12 64-62-8z" fill="#f9efd9"/><path d="m28 7 54 8-13 63-54-8z" fill="#d5ddbf"/><path d="m27 9-11 60 53 8M32 9 21 71" stroke="#a4ac8e"/><path d="M44 34c1-8 14-9 17 0 10-3 13 11 2 12-2 8-13 7-16 1-12 2-15-11-3-13z" fill="#fcf8ee"/><path d="m88 9 4-7m4 17 8-3m-9 13 8 1"/></svg>';
  function decorate(page){
    if(page==='habits'){
      main.querySelectorAll('.habit').forEach(row=>{
        const id=row.querySelector('[data-habit-open]')?.dataset.habitOpen;
        const h=state.habits.find(h=>h.id===id);if(!h)return;
        row.querySelector('.habit-medal')?.remove();
        const art=element(habitBadge(h),'habit-medal');art.title=h.name+' · '+habitBadge(h).label+'徽章';row.prepend(art);
      });
    }
    if(page==='insights'){
      const header=main.querySelector('.pagehead');if(!header)return;
      header.classList.add('experience-header');header.querySelector('.mobile-mark')?.remove();
      const title=header.querySelector('h1');
      if(title&&!header.querySelector('.experience-book')){
        const image=document.createElement('span');image.className='experience-book';image.innerHTML=notebook;title.before(image);
      }
      const subtitle=header.querySelector('p');if(subtitle)subtitle.textContent='把值得记住的话，慢慢收起来。';
    }
  }
  return {element,habitBadge,decorate};
})();
