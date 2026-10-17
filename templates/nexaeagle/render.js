// usage: node render.js video <page.html> <seconds> <out.mp4>   |   node render.js stills <page.html> t1 t2 ...   |   node render.js check <page.html> t1 t2 ...
// check: lists visible text/UI elements that leave the Instagram safe box (x 120..960, y 260..1480). Mark full-bleed decoration (backgrounds, blobs, leaves) with data-bleed.
// page must define window.seek(t) (returning nothing). 1080x1920, 30fps.
const {chromium}=require('playwright');const {spawn}=require('child_process');const path=require('path');
(async()=>{const [mode,html,...rest]=process.argv.slice(2);
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium',args:['--allow-file-access-from-files','--no-sandbox']});
 const p=await b.newPage({viewport:{width:1080,height:1920}});p.on('pageerror',e=>console.log('PAGE ERROR',e.message));
 await p.goto('file://'+path.resolve(html),{waitUntil:'domcontentloaded'});
 await p.evaluate(()=>Promise.race([document.fonts.ready,new Promise(r=>setTimeout(r,3000))]));await p.waitForTimeout(500);
 if(mode==='check'){let bad=0;for(const t of rest){await p.evaluate(t=>{seek(t)},+t);
   const v=await p.evaluate(()=>{const B={l:120,r:960,t:260,b:1480},out=[];
     const vis=el=>{let o=1;for(let e=el;e&&e.nodeType===1;e=e.parentElement){const cs=getComputedStyle(e);if(cs.display==='none'||cs.visibility==='hidden')return 0;o*=+cs.opacity;if(e.hasAttribute('data-bleed'))return 0;}return o;};
     document.querySelectorAll('body *').forEach(el=>{const leaf=[...el.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())||['IMG','svg','CANVAS'].includes(el.tagName)||el.classList.contains('ui');if(!leaf)return;
       let r;const tn=[...el.childNodes].filter(n=>n.nodeType===3&&n.textContent.trim());if(tn.length&&!el.classList.contains('ui')){const rg=document.createRange();rg.setStartBefore(tn[0]);rg.setEndAfter(tn[tn.length-1]);r=rg.getBoundingClientRect();}else r=el.getBoundingClientRect();if(r.width<2||r.height<2)return;if(r.right<0||r.left>1080||r.bottom<0||r.top>1920)return;if(vis(el)<0.05)return;
       if(r.left<B.l-1||r.right>B.r+1||r.top<B.t-1||r.bottom>B.b+1)out.push((el.id||el.className||el.tagName)+' '+(el.textContent||'').trim().slice(0,30)+' ['+Math.round(r.left)+','+Math.round(r.top)+','+Math.round(r.right)+','+Math.round(r.bottom)+']');});
     return out;});
   if(v.length){bad+=v.length;console.log('t='+t+' OUTSIDE SAFE BOX:\n  '+v.join('\n  '));}}
   console.log(bad?('FAIL: '+bad+' element(s) outside safe box'):'PASS: everything inside safe box');}
 else if(mode==='stills'){for(const t of rest){await p.evaluate(t=>{seek(t)},+t);await p.screenshot({path:`still_${t}.png`});}}
 else{const fps=30,N=Math.round(+rest[0]*fps);
  const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate',''+fps,'-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','medium','-movflags','+faststart',rest[1]],{stdio:['pipe','inherit','inherit']});
  for(let i=0;i<N;i++){await p.evaluate(t=>{seek(t)},i/fps);ff.stdin.write(await p.screenshot({type:'jpeg',quality:92}));}
  ff.stdin.end();await new Promise(r=>ff.on('close',r));}
 await b.close();})();
