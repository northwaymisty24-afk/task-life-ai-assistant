/* Section navigation shares existing routes. Forms and card-specific gestures keep priority. */
const SectionPages=(()=>{
  const routes=navItems.map(x=>x[0]),labels=Object.fromEntries(navItems.map(x=>[x[0],x[1]]));
  const drafts=new Map();let shown='',gesture=null,moving=false,animation=null;
  const reduce=()=>matchMedia('(prefers-reduced-motion:reduce)').matches;
  function current(){let page=(location.hash.slice(1)||'tasks').split('/')[0];if(page==='review')page='diary';return routes.includes(page)?page:'tasks';}
  function capture(){
    if(!shown)return;
    const fields=Array.from(main.querySelectorAll('input,textarea,select')).filter(el=>!['checkbox','radio','button','submit','hidden'].includes(el.type));
    drafts.set(shown,fields.map(el=>({id:el.id,name:el.name,form:el.form?.id||'',value:el.value})));
  }
  const base=render;
  render=function(){
    const previous=shown;capture();const next=current();base();shown=next;
    for(const field of (next!==previous?drafts.get(next):[])||[]){
      let el=field.id?document.getElementById(field.id):null;
      if(!el&&field.form&&field.name)el=document.getElementById(field.form)?.elements.namedItem(field.name);
      if(el&&main.contains(el)&&el.value!==field.value)el.value=field.value;
    }

  };
  function clear(){main.style.transition='';main.style.transform='';main.style.opacity='';main.style.willChange='';}
  function go(delta){
    if(moving||document.querySelector('dialog[open]'))return;
    const index=routes.indexOf(current()),next=routes[index+delta];if(!next){clear();return;}
    capture();moving=true;const dir=delta>0?-1:1;
    const enter=()=>{
      location.hash=next;
      requestAnimationFrame(()=>requestAnimationFrame(()=>{
        clear();
        if(!reduce()&&main.animate){animation=main.animate([{transform:`translateX(${-dir*45}px)`,opacity:.45},{transform:'translateX(0)',opacity:1}],{duration:210,easing:'cubic-bezier(.2,.7,.2,1)'});animation.finished.catch(()=>{}).finally(()=>{moving=false;animation=null;});}else moving=false;
      }));
    };
    if(reduce()||!main.animate){clear();enter();return;}
    const from=main.style.transform||'translateX(0)';clear();
    animation=main.animate([{transform:from,opacity:1},{transform:`translateX(${dir*65}px)`,opacity:.35}],{duration:140,easing:'ease-in',fill:'forwards'});
    animation.finished.then(()=>{animation.cancel();animation=null;enter();}).catch(()=>{moving=false;clear();});
  }
  main.addEventListener('pointerdown',e=>{
    if(!e.isPrimary||e.pointerType==='mouse'||moving||document.querySelector('dialog[open]'))return;
    if(e.target.closest('input,textarea,select,button,a,summary,.ins,.drag-handle,.sortable-list,.wk-grid,.cal-grid,[contenteditable]'))return;
    // Leave the screen edges for browser back/forward gestures.
    if(e.clientX<22||e.clientX>innerWidth-22)return;
    gesture={id:e.pointerId,x:e.clientX,y:e.clientY,locked:false,dx:0};
  });
  main.addEventListener('pointermove',e=>{
    if(!gesture||e.pointerId!==gesture.id)return;
    const dx=e.clientX-gesture.x,dy=e.clientY-gesture.y;
    if(!gesture.locked){if(Math.abs(dy)>14&&Math.abs(dy)>Math.abs(dx)){gesture=null;return;}if(Math.abs(dx)<18||Math.abs(dx)<Math.abs(dy)*1.6)return;gesture.locked=true;main.setPointerCapture(e.pointerId);main.style.willChange='transform';}
    gesture.dx=dx;const index=routes.indexOf(current()),allowed=dx<0?index<routes.length-1:index>0;
    main.style.transform=`translateX(${Math.max(-innerWidth*.4,Math.min(innerWidth*.4,dx))*(allowed?.65:.15)}px)`;
  });
  function finish(e){
    if(!gesture||e.pointerId!==gesture.id)return;
    const {dx,locked}=gesture;gesture=null;
    if(main.hasPointerCapture(e.pointerId))main.releasePointerCapture(e.pointerId);
    if(e.type==='pointerup'&&locked&&Math.abs(dx)>Math.max(65,Math.min(110,innerWidth*.18))){go(dx<0?1:-1);}
    else{main.style.transition=reduce()?'':'transform .18s ease';main.style.transform='';setTimeout(clear,190);}
  }
  main.addEventListener('pointerup',finish);main.addEventListener('pointercancel',finish);
  addEventListener('hashchange',()=>{if(!moving)clear();});
  render();return {go,capture};
})();
