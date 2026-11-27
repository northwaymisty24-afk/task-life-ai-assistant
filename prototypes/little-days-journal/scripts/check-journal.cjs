const fs=require('fs'),vm=require('vm'),path=require('path'),assert=require('node:assert/strict');
const R=path.resolve(__dirname,'..'),lib=JSON.parse(fs.readFileSync(path.join(R,'manifest.json')));lib.sheets={};
const ctx={JOURNAL_LIBRARY:lib,document:{createElement(){return {style:{},dataset:{},classList:{add(){}},setAttribute(){},append(){}}}},main:{},state:{habits:[]}};vm.createContext(ctx);vm.runInContext(fs.readFileSync(path.join(R,'journal-assets.js'),'utf8')+';globalThis.api=JournalAssets;',ctx);
assert.equal(lib.habitBadges.length,30);for(const a of lib.habitBadges)assert.equal(ctx.api.habitBadge({name:a.label}).label,a.label);
assert.equal(ctx.api.habitBadge({name:'每天吃水果'}).label,'吃水果');
const code=fs.readFileSync(path.join(R,'journal.js'),'utf8');const plan=code.slice(code.indexOf('  function planFor('),code.indexOf('  function assetArt('));
const weekDays=d=>{const t=new Date(d+'T12:00Z');t.setUTCDate(t.getUTCDate()-(t.getUTCDay()+6)%7);return Array.from({length:7},(_,i)=>{const q=new Date(t);q.setUTCDate(q.getUTCDate()+i);return q.toISOString().slice(0,10)})};
const w={library:lib,state:{},paletteVersion:'test',save(){},contextFor(){return 'neutral'},weekDays,weekNumber:d=>Math.floor(Date.parse(d+'T12:00Z')/604800000)};vm.createContext(w);vm.runInContext(plan,w);
let last;for(let i=0;i<60;i++){const d=new Date('2026-11-23T12:00Z');d.setUTCDate(d.getUTCDate()+i*7);const k=d.toISOString().slice(0,10),a=w.planFor(k);assert.equal(a,w.planFor(weekDays(k)[6]));for(const slot of ['support','feelings'])assert(lib.assets.find(x=>x.id===a[slot]).activity);if(last)for(const slot of ['collage','doodle','support','feelings'])assert.notEqual(a[slot],last[slot]);last=a;}
const html=fs.readFileSync(path.join(R,'little-days-h5-journal.html'),'utf8');assert(!html.includes('section-pager'));assert(html.includes('.journal-feelings>.corner-tape{right:-15px}'));assert(!html.includes('right:84px'));
for(const a of lib.assets.concat(lib.habitBadges))assert(fs.existsSync(path.join(R,a.path)),a.path);
console.log('PASS: 30 habit matches, 60 weeks stable/rotating artwork, existing asset references, restored tape anchor, no swipe footer.');
