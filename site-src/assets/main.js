// SOURCE of blue_hammer_remodeling_site/assets/main.js. Edit this file, then run `python3 scripts/build.py`
// (esbuild minifies it; the published copy is generated and never edited). Classic script, loaded with defer.
(function(){
  'use strict';
  const c=window.BLUE_HAMMER_CONFIG||{};
  const phoneDigits=(c.phone||'').replace(/\D/g,'');
  function setContact(){
    document.querySelectorAll('.phone-slot').forEach(el=>{
      if(!phoneDigits){el.textContent='';const panel=el.closest('.contact-method');if(panel)panel.hidden=true;return}
      const a=document.createElement('a');a.href='tel:+'+(phoneDigits.length===10?'1':'')+phoneDigits;
      a.textContent=c.phone;a.setAttribute('aria-label','Call Blue Hammer Remodeling: '+c.phone);el.replaceChildren(a)
    });
    document.querySelectorAll('.phone-link').forEach(el=>{
      if(!phoneDigits){el.hidden=true;return}
      el.href='tel:+'+(phoneDigits.length===10?'1':'')+phoneDigits;el.hidden=false;
      if(el.dataset.textPhone)el.textContent=c.phone
    });
    document.querySelectorAll('.email-slot').forEach(el=>{
      if(!c.email){el.textContent='';const panel=el.closest('.contact-method');if(panel)panel.hidden=true;return}
      const a=document.createElement('a');a.href='mailto:'+c.email;a.textContent=c.email;el.replaceChildren(a)
    });
    document.querySelectorAll('.license-slot').forEach(el=>{el.textContent=c.mhicLicense?'MHIC License #'+c.mhicLicense:''});
  }
  function nav(){
    const toggle=document.querySelector('.menu-toggle');
    const menu=document.getElementById('main-navigation');
    const drops=[...document.querySelectorAll('.nav-dropdown')];
    const desktop=window.matchMedia('(min-width: 1061px)');
    function setDrop(d,open){d.classList.toggle('open',open);const b=d.querySelector('button');if(b)b.setAttribute('aria-expanded',String(open))}
    function setMenu(open,returnFocus){
      if(!toggle||!menu)return;
      menu.classList.toggle('open',open);toggle.setAttribute('aria-expanded',String(open));
      const label=toggle.querySelector('.menu-label');if(label)label.textContent=open?'Close':'Menu';
      if(!open){drops.forEach(d=>setDrop(d,false));if(returnFocus)toggle.focus()}
    }
    if(toggle&&menu){
      toggle.addEventListener('click',()=>setMenu(!menu.classList.contains('open'),false));
      menu.addEventListener('click',ev=>{if(ev.target.closest('a'))setMenu(false,false)});
    }
    drops.forEach(d=>{
      const b=d.querySelector('button');if(!b)return;
      const links=[...d.querySelectorAll('.dropdown-panel a')];
      const openDrop=()=>{drops.forEach(o=>{if(o!==d)setDrop(o,false)});setDrop(d,true)};
      b.addEventListener('click',()=>{const open=!d.classList.contains('open');if(open)openDrop();else setDrop(d,false)});
      b.addEventListener('keydown',ev=>{
        if(!['ArrowDown','ArrowUp'].includes(ev.key))return;ev.preventDefault();openDrop();
        (ev.key==='ArrowUp'?links[links.length-1]:links[0])?.focus();
      });
      d.addEventListener('keydown',ev=>{
        // The button's own handler above has just moved focus to the first or last link; do not step again.
        if(ev.target===b)return;
        const at=links.indexOf(document.activeElement);if(at<0)return;
        let next;if(ev.key==='ArrowDown')next=(at+1)%links.length;else if(ev.key==='ArrowUp')next=(at-1+links.length)%links.length;else if(ev.key==='Home')next=0;else if(ev.key==='End')next=links.length-1;
        if(next!==undefined){ev.preventDefault();links[next]?.focus()}
      });
      // Desktop only: the panel floats, so closing it when focus leaves moves nothing. In the mobile menu the
      // panel is in the page flow: collapsing it on focus-out (which fires on pointer down) shifted the rows
      // under the finger before the tap finished, so the tap on the next item landed elsewhere and the
      // document click handler closed everything. There the panel closes on its own button, when another
      // dropdown opens, on Escape, or with the menu.
      d.addEventListener('focusout',ev=>{if(desktop.matches&&ev.relatedTarget&&!d.contains(ev.relatedTarget))setDrop(d,false)});
    });
    document.addEventListener('click',ev=>{
      // Inside the open mobile menu a tap on a plain row leaves the open dropdown alone (a link tap closes the menu anyway).
      if(!ev.target.closest('.nav-dropdown')&&!(!desktop.matches&&menu&&menu.contains(ev.target)))drops.forEach(d=>setDrop(d,false));
      if(menu&&menu.classList.contains('open')&&!ev.target.closest('.site-header'))setMenu(false,false);
    });
    document.addEventListener('keydown',ev=>{
      if(ev.key!=='Escape')return;
      const openDrop=drops.find(d=>d.classList.contains('open'));
      if(openDrop){ev.preventDefault();setDrop(openDrop,false);openDrop.querySelector('button')?.focus();return}
      if(menu&&menu.classList.contains('open'))setMenu(false,true);
    });
    desktop.addEventListener?.('change',e=>{if(e.matches)setMenu(false,false)});
    document.querySelectorAll('a[href*="#consultation"]').forEach(link=>link.addEventListener('click',(ev)=>{
      const target=document.getElementById('consultation');if(target){ev.preventDefault();target.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});history.replaceState(null,'','#consultation')}
    }));
  }
  function initForms(){
    document.querySelectorAll('form.lead-form').forEach(form=>{
      let step=1,submitting=false;
      const stepElements=[...form.querySelectorAll('.form-step')];
      const counter=form.querySelector('.form-progress');const track=form.querySelector('.form-progress-track i');
      const status=form.querySelector('.form-status');
      const submit=form.querySelector('button[type=submit]');
      const submitLabel=submit?.textContent||'Send consultation request';
      function setStatus(message,error){if(status){status.className=error?'form-status error':'form-status';status.textContent=message}}
      function showStep(n,focus=true){
        step=n;stepElements.forEach(el=>{const active=Number(el.dataset.step)===n;el.classList.toggle('active',active);el.setAttribute('aria-hidden',String(!active))});
        if(counter)counter.textContent=`Step ${n} of 2`;if(track)track.style.width=n===1?'50%':'100%';setStatus('',false);
        if(focus)form.querySelector('.form-step.active input:not([type=hidden]),.form-step.active select')?.focus({preventScroll:true});
      }
      function validatePanel(n){
        const controls=form.querySelectorAll(`.form-step[data-step="${n}"] input,.form-step[data-step="${n}"] select,.form-step[data-step="${n}"] textarea`);
        for(const el of controls){
          el.setCustomValidity('');
          if(['firstName','lastName'].includes(el.name)&&el.value.trim().length<Math.max(1,el.minLength))el.setCustomValidity('Please enter your name.');
          if(el.name==='phone'&&el.value){const digits=el.value.replace(/\D/g,'');if(!/^\+?[\d\s().-]+$/.test(el.value.trim())||digits.length<10||digits.length>15)el.setCustomValidity('Please enter a phone number with 10 to 15 digits.')}
          if(!el.checkValidity()){if(step!==n)showStep(n,false);el.focus({preventScroll:false});el.reportValidity();return false}
        }
        return true;
      }
      form.addEventListener('input',ev=>{if(typeof ev.target.setCustomValidity==='function')ev.target.setCustomValidity('')});
      form.querySelector('.form-next')?.addEventListener('click',()=>{if(validatePanel(1))showStep(2)});
      form.querySelector('.form-back')?.addEventListener('click',()=>{if(!submitting)showStep(1)});
      form.addEventListener('submit',async(ev)=>{
        ev.preventDefault();if(submitting)return;
        if(form.querySelector('[name="companyWebsite"]')?.value.trim()){setStatus('We could not send this request. Please refresh the page and try again.',true);return}
        if(step!==2){if(validatePanel(1))showStep(2);return}
        // Recheck both panels: hidden fields may have changed after going back or autofill.
        if(!validatePanel(1)||!validatePanel(2))return;
        const fd=new FormData(form), data=Object.fromEntries(fd.entries());data.source=window.location.pathname||'/';data.consent=data.consent==='on';
        const formName=String(fd.get('form-name')||form.getAttribute('name')||'consultation');
        const buttons=[...form.querySelectorAll('button')];const disabledStates=buttons.map(b=>b.disabled);
        submitting=true;form.setAttribute('aria-busy','true');buttons.forEach(b=>b.disabled=true);if(submit)submit.textContent='Sending request…';setStatus('Sending your request…',false);
        const controller=new AbortController();const timeout=setTimeout(()=>controller.abort(),20000);
        try{
          // Local Node server (npm start) uses /api/leads; the hosted site (Netlify) uses Netlify Forms.
          const local=['localhost','127.0.0.1'].includes(location.hostname);
          let res,result={};
          if(local){
            res=await fetch('/api/leads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data),signal:controller.signal});
            result=await res.json().catch(()=>({}));
          }else{
            const body=new URLSearchParams({...data,'form-name':formName,consent:data.consent?'yes':'no'});
            res=await fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:body.toString(),signal:controller.signal});
          }
          if(!res.ok)throw new Error(result.message||'We couldn’t send your request just now. Your details are still here. Please check your connection and try again in a moment.');
          window.location.href=form.getAttribute('action')||'/thank-you.html';
        }catch(err){
          setStatus(err.name==='AbortError'?'The connection took too long. Your details are still here; please try again.':err.message||'Unable to send right now. Please try again in a moment.',true);
          submitting=false;form.removeAttribute('aria-busy');buttons.forEach((b,i)=>b.disabled=disabledStates[i]);if(submit)submit.textContent=submitLabel;
        }finally{clearTimeout(timeout)}
      });
      showStep(1,false);
    });
  }
  function initGallery(){
    const buttons=document.querySelectorAll('[data-filter]');
    if(!buttons.length)return;
    buttons.forEach(btn=>btn.addEventListener('click',()=>{
      const filter=btn.dataset.filter;
      buttons.forEach(b=>{b.classList.toggle('active',b===btn);b.setAttribute('aria-pressed',String(b===btn))});
      document.querySelectorAll('.gallery-card[data-category]').forEach(card=>card.classList.toggle('hidden',filter!=='all'&&card.dataset.category!==filter));
    }));
  }
  function initTracking(){
    const q=new URLSearchParams(location.search),u=q.get('utm_source')||'',campaign=q.get('utm_campaign')||'';
    document.querySelectorAll('form.lead-form').forEach(f=>{
      const source=f.querySelector('[name=utm_source]');if(source)source.value=u;
      const cmp=f.querySelector('[name=utm_campaign]');if(cmp)cmp.value=campaign;
      const svc=q.get('service');if(svc){const el=f.querySelector('[name=projectType]');if(el&&[...el.options].some(o=>o.value===svc))el.value=svc}
    });
  }
  // Netlify's "Powered by Netlify" badge is injected by Netlify's edge (a dashboard setting, not our code).
  // When it is present, give the mobile sticky CTA room so the two never overlap.
  function initBadgeSafeArea(){
    const root=document.documentElement;
    const check=()=>{const f=document.getElementById('nl-badge-frame');if(!f)return false;const r=f.getBoundingClientRect();
      if(r.height>0&&r.top>window.innerHeight/2){root.style.setProperty('--nl-badge-h',Math.ceil(window.innerHeight-r.top+6)+'px');root.classList.add('has-nl-badge')}else{root.classList.remove('has-nl-badge')}return true};
    if(check())return;
    const mo=new MutationObserver(()=>{if(check())mo.disconnect()});mo.observe(document.body,{childList:true});
    setTimeout(()=>mo.disconnect(),15000);window.addEventListener('resize',check);
  }
  // Fixed mobile bar: it repeats the page's own "Schedule a Consultation" button, so it steps aside while one
  // of those buttons, or the form itself, is already on screen. Without IntersectionObserver it simply stays.
  function initMobileBar(){
    const bar=document.querySelector('.mobile-cta');
    if(!bar||!('IntersectionObserver' in window))return;
    const targets=[...document.querySelectorAll('main a.btn--primary, main form.lead-form')];
    if(!targets.length)return;
    const seen=new Set();
    const io=new IntersectionObserver(entries=>{
      entries.forEach(e=>{if(e.isIntersecting)seen.add(e.target);else seen.delete(e.target)});
      bar.classList.toggle('is-idle',seen.size>0);
    },{rootMargin:'-68px 0px 0px 0px'});
    targets.forEach(t=>io.observe(t));
  }
  // Home hero carousel (2026-11-20). The <img> poster is slide 1 and is the no-JS / reduced-motion / Save-Data / <768px view.
  // With motion allowed, a pre-rendered Remotion video (all slides, 0.6 s crossfades, seamless loop) is attached
  // after load, only near the viewport. Controls seek the video to the start of a slide (index * slide duration),
  // a frame that is never inside a crossfade; the counter follows timeupdate. Without the video the controls swap
  // the still (srcset loaded on demand). The live region speaks only on manual changes, never on autoplay.
  function initHeroCarousel(){
    const root=document.querySelector('[data-carousel]');
    if(!root)return;
    let slides=[];try{slides=JSON.parse(root.dataset.slides||'[]')}catch(e){return}
    const n=slides.length;if(n<2)return;
    const dur=parseFloat(root.dataset.slideDuration)||5.5,fade=parseFloat(root.dataset.fade)||0.6;
    const img=root.querySelector('.home-hero-still'),video=root.querySelector('video');
    const controls=root.querySelector('.home-hero-controls'),count=root.querySelector('[data-count]');
    const caption=root.querySelector('[data-caption]'),status=root.querySelector('[data-status]');
    const prev=root.querySelector('[data-prev]'),next=root.querySelector('[data-next]'),toggle=root.querySelector('[data-toggle]');
    const phone=window.matchMedia('(max-width: 700px)');
    const reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const saveData=!!(navigator.connection&&navigator.connection.saveData);
    // 2026-11-22: the video is for >=768px only. Below that the carousel is manual (poster + WebP stills loaded
    // on demand by showStill), no autoplay, no Pause button and no video request.
    const wide=window.matchMedia('(min-width: 768px)').matches;
    const motion=wide&&!!video&&!reduce&&!saveData&&typeof video.canPlayType==='function'&&(video.canPlayType('video/webm')||video.canPlayType('video/mp4'));
    // stillMode: the video is paused and hidden and the WebP still of the current slide is shown. Entered when a
    // seek is not possible (server without HTTP Range, video.seekable empty) or does not take effect; left on Play.
    let index=0,userPaused=false,ready=false,attached=false,stillMode=false,quietUntil=0;const holds=new Set();
    controls.hidden=false;
    if(!motion&&toggle)toggle.hidden=true;
    const pos=i=>phone.matches?slides[i].posPhone:slides[i].pos;
    function paint(i,announce){
      index=(i%n+n)%n;const s=slides[index];
      count.textContent=(index+1)+' / '+n;caption.textContent=s.caption;img.alt=s.alt;
      if(announce)status.textContent='Photo '+(index+1)+' of '+n+': '+s.caption;
    }
    function showStill(){const s=slides[index];if(img.getAttribute('src')!==s.src){img.srcset=s.srcset;img.src=s.src}img.style.objectPosition=pos(index)}
    const target=i=>i*dur+0.05;
    function canSeek(t){const r=video.seekable;for(let k=0;k<r.length;k++){if(r.start(k)<=t&&t<=r.end(k))return true}return false}
    function setPaused(on){userPaused=on;if(toggle){toggle.toggleAttribute('data-paused',on);toggle.setAttribute('aria-label',on?'Play slideshow':'Pause slideshow')}}
    function enterStill(){stillMode=true;setPaused(true);video.pause();root.classList.remove('is-video');showStill()}
    function seek(){
      const t=target(index);
      if(!canSeek(t))return false;
      try{video.currentTime=t}catch(e){return false}
      // Verify the seek landed; some servers report seekable but still cannot serve the range.
      const want=index,check=()=>{if(!stillMode&&index===want&&Math.abs(video.currentTime-t)>0.3)enterStill()};
      video.addEventListener('seeked',check,{once:true});setTimeout(check,800);
      return true;
    }
    function sync(){if(!ready||stillMode){if(ready)video.pause();return}if(userPaused||holds.size)video.pause();else{const p=video.play();if(p&&p.catch)p.catch(()=>{})}}
    function go(i){
      paint(i,true);quietUntil=Date.now()+900;
      if(!ready||stillMode){showStill();return}
      if(!seek())enterStill();
    }
    prev.addEventListener('click',()=>go(index-1));
    next.addEventListener('click',()=>go(index+1));
    if(toggle)toggle.addEventListener('click',()=>{
      setPaused(!userPaused);
      status.textContent=userPaused?'Slideshow paused':'Slideshow playing';
      if(!userPaused){
        // An explicit Play wins over the hover / focus holds of the control it was pressed on.
        holds.delete('hover');holds.delete('focus');
        if(stillMode&&ready){stillMode=false;quietUntil=Date.now()+900;if(!seek())quietUntil=0;root.classList.add('is-video')}  // not seekable: the video resumes where it was and the counter follows it
      }
      sync();
    });
    if(!motion)return;
    // Pause while the pointer or keyboard focus is on the controls, while off-screen and while the tab is hidden.
    const hold=(k,on)=>{if(on)holds.add(k);else holds.delete(k);sync()};
    controls.addEventListener('pointerenter',()=>hold('hover',true));
    controls.addEventListener('pointerleave',()=>hold('hover',false));
    controls.addEventListener('focusin',e=>{if(e.target.matches(':focus-visible'))hold('focus',true)});  // keyboard focus only; a mouse click is covered by hover
    controls.addEventListener('focusout',e=>{if(!controls.contains(e.relatedTarget))hold('focus',false)});
    document.addEventListener('visibilitychange',()=>hold('hidden',document.hidden));
    video.addEventListener('timeupdate',()=>{
      if(video.seeking||stillMode||Date.now()<quietUntil)return;
      const i=Math.floor((video.currentTime+fade/2)/dur)%n;
      if(i!==index)paint(i,false);
    });
    function sources(){
      const webm=phone.matches?video.dataset.webmPhone:video.dataset.webm,mp4=phone.matches?video.dataset.mp4Phone:video.dataset.mp4;
      video.replaceChildren();
      [[webm,'video/webm'],[mp4,'video/mp4']].forEach(([src,type])=>{const el=document.createElement('source');el.src=src;el.type=type;video.appendChild(el)});
      video.lastElementChild.addEventListener('error',fail);
      video.preload='auto';video.load();
    }
    video.addEventListener('loadeddata',()=>{
      ready=true;
      if(stillMode)return;
      if(index!==0&&!seek()){enterStill();return}
      const show=()=>{if(!stillMode){root.classList.add('is-video');sync()}};
      if(video.readyState>=2)show();else video.addEventListener('canplay',show,{once:true});
    });
    // Only the last source failing means no playable video: fall back to the stills.
    const fail=()=>{ready=false;root.classList.remove('is-video');showStill()};
    function attach(){if(attached)return;attached=true;sources()}
    phone.addEventListener?.('change',()=>{if(attached){ready=false;root.classList.remove('is-video');showStill();sources()}else showStill()});
    const idle=window.requestIdleCallback||(cb=>setTimeout(cb,300));
    const start=()=>idle(()=>{
      if(!('IntersectionObserver' in window)){attach();return}
      const io=new IntersectionObserver(entries=>{
        entries.forEach(e=>{
          if(e.isIntersecting)attach();
          hold('offscreen',!e.isIntersecting);
        });
      },{rootMargin:'200px 0px',threshold:0});
      io.observe(root);
    });
    if(document.readyState==='complete')start();else window.addEventListener('load',start,{once:true});
  }
  // Entry motion on the home sections: a short fade-up the first time each block enters the viewport. Content is
  // visible without JS and with reduced motion (the class that hides it is only added here). Blocks already on
  // screen when the script runs are shown at once.
  function initReveal(){
    const items=[...document.querySelectorAll('[data-reveal]')];
    if(!items.length||!('IntersectionObserver' in window)||window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
    const vh=window.innerHeight;
    items.forEach(el=>{if(el.getBoundingClientRect().top<vh*0.92)el.classList.add('is-in')});
    document.documentElement.classList.add('reveal-on');
    const io=new IntersectionObserver(entries=>{
      entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('is-in');io.unobserve(e.target)}});
    },{rootMargin:'0px 0px -8% 0px',threshold:0.08});
    items.forEach(el=>{if(!el.classList.contains('is-in'))io.observe(el)});
  }
  // Homepage area picker: the select lists only existing town pages; "View area" opens the chosen page.
  // Without JS the form falls back to a GET on /service-areas, which lists every area.
  function initAreaPicker(){
    document.querySelectorAll('[data-area-picker]').forEach(form=>{
      form.addEventListener('submit',e=>{
        const v=form.querySelector('select').value;
        if(/^\/[a-z-]+$/.test(v)){e.preventDefault();window.location.href=v}
      });
    });
  }
  setContact();nav();initForms();initGallery();initTracking();initBadgeSafeArea();initMobileBar();initHeroCarousel();initReveal();initAreaPicker();
})();
