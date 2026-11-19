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
  function svgCheck(){return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M20 6 9 17l-5-5"/></svg>'}
  function nav(){
    const toggle=document.querySelector('.menu-toggle');
    const menu=document.getElementById('main-navigation');
    const drops=[...document.querySelectorAll('.nav-dropdown')];
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
        const at=links.indexOf(document.activeElement);if(at<0)return;
        let next;if(ev.key==='ArrowDown')next=(at+1)%links.length;else if(ev.key==='ArrowUp')next=(at-1+links.length)%links.length;else if(ev.key==='Home')next=0;else if(ev.key==='End')next=links.length-1;
        if(next!==undefined){ev.preventDefault();links[next]?.focus()}
      });
      d.addEventListener('focusout',ev=>{if(ev.relatedTarget&&!d.contains(ev.relatedTarget))setDrop(d,false)});
    });
    document.addEventListener('click',ev=>{
      if(!ev.target.closest('.nav-dropdown'))drops.forEach(d=>setDrop(d,false));
      if(menu&&menu.classList.contains('open')&&!ev.target.closest('.site-header'))setMenu(false,false);
    });
    document.addEventListener('keydown',ev=>{
      if(ev.key!=='Escape')return;
      const openDrop=drops.find(d=>d.classList.contains('open'));
      if(openDrop){ev.preventDefault();setDrop(openDrop,false);openDrop.querySelector('button')?.focus();return}
      if(menu&&menu.classList.contains('open'))setMenu(false,true);
    });
    const desktop=window.matchMedia('(min-width: 1061px)');
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
  // Micro-interactions (2026-11-18): scroll reveal + counters for REAL numbers only (data-count). Respects reduced motion.
  function initMotion(){
    const reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if(reduce||!('IntersectionObserver' in window))return;
    // Content is visible by default; only elements that opt in with data-reveal fade in (none on the site today).
    const targets=document.querySelectorAll('[data-reveal]');
    if(!targets.length)return;
    document.documentElement.classList.add('js-reveal');
    const io=new IntersectionObserver(entries=>{entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('is-visible');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px',threshold:.08});
    targets.forEach(el=>{if(el.getBoundingClientRect().top<window.innerHeight){el.classList.add('reveal','is-visible')}else{el.classList.add('reveal');io.observe(el)}});
    document.querySelectorAll('[data-count]').forEach(el=>{
      const end=parseFloat(el.dataset.count);if(!isFinite(end))return;
      const co=new IntersectionObserver(([e])=>{if(!e.isIntersecting)return;co.disconnect();const t0=performance.now(),d=1100;
        (function step(t){const k=Math.min(1,(t-t0)/d),v=end*(1-Math.pow(1-k,3));el.textContent=Number.isInteger(end)?Math.round(v).toLocaleString('en-US'):v.toFixed(1);if(k<1)requestAnimationFrame(step)})(t0)});
      co.observe(el);
    });
  }
  // Brand motion (Remotion renders in assets/video/). Muted, looping, inline; sources attach only when the
  // video is near the viewport, motion is allowed, the element is displayed and Save-Data is off.
  // Reduced motion: the video never loads (CSS hides it; the photo/poster stays).
  function initMedia(){
    const vids=[...document.querySelectorAll('video[data-motion]')];if(!vids.length)return;
    const mq=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)');
    const connection=navigator.connection;
    const toggles=[...document.querySelectorAll('button[data-motion-toggle]')];
    const allowed=()=>!(mq&&mq.matches)&&!(connection&&connection.saveData);
    const displayed=v=>v.getClientRects().length>0&&getComputedStyle(v).visibility!=='hidden';
    const states=vids.map(v=>({v,toggle:toggles.find(b=>b.dataset.motionToggle===v.id),near:!('IntersectionObserver' in window),loaded:!!v.dataset.loaded,everReady:v.readyState>=3,manualPaused:false,playPending:false,resumeAt:0}));
    function updateControl(s){
      if(!s.toggle)return;
      const playing=!s.v.paused&&!s.v.ended;
      s.toggle.hidden=!s.everReady||!allowed()||!displayed(s.v);
      s.toggle.removeAttribute('aria-pressed');
      s.toggle.dataset.motionPlaying=String(playing);
      s.toggle.setAttribute('aria-label',playing?'Pause motion':'Play motion');
      const label=s.toggle.querySelector('[data-motion-label]');if(label)label.textContent=playing?'Pause motion':'Play motion';
    }
    const shouldPlay=s=>allowed()&&s.near&&document.visibilityState!=='hidden'&&!s.manualPaused&&displayed(s.v);
    function reconcile(s){
      const v=s.v;
      if(!allowed()){
        v.pause();
        if(s.loaded){
          s.resumeAt=Number.isFinite(v.currentTime)?v.currentTime:0;
          v.removeAttribute('src');v.querySelectorAll('source[data-src]').forEach(source=>source.removeAttribute('src'));
          s.loaded=false;delete v.dataset.loaded;v.classList.remove('is-playing');v.load();
        }
        updateControl(s);return;
      }
      if(!shouldPlay(s)){v.pause();updateControl(s);return}
      if(!s.loaded){
        s.loaded=true;v.dataset.loaded='1';v.muted=true;
        v.querySelectorAll('source[data-src]').forEach(source=>{source.src=source.dataset.src});v.load();
      }
      if(v.paused&&!s.playPending){
        s.playPending=true;
        try{
          const pending=v.play();
          if(pending&&pending.then)pending.then(()=>{s.playPending=false;if(!shouldPlay(s))v.pause();updateControl(s)},()=>{s.playPending=false;updateControl(s)});
          else{s.playPending=false;updateControl(s)}
        }catch{s.playPending=false;updateControl(s)}
      }
      updateControl(s);
    }
    states.forEach(s=>{
      if(s.toggle){s.toggle.hidden=true;s.toggle.addEventListener('click',()=>{s.manualPaused=!s.v.paused;reconcile(s)})}
      s.v.addEventListener('canplay',()=>{
        s.everReady=true;
        if(s.resumeAt>0&&Number.isFinite(s.v.duration)){s.v.currentTime=Math.min(s.resumeAt,Math.max(0,s.v.duration-.1));s.resumeAt=0}
        updateControl(s);
      });
      s.v.addEventListener('playing',()=>{if(!shouldPlay(s)){s.v.pause();return}s.v.classList.add('is-playing');updateControl(s)});
      s.v.addEventListener('pause',()=>updateControl(s));
      s.v.addEventListener('ended',()=>updateControl(s));
      s.v.addEventListener('error',()=>{s.v.classList.remove('is-playing');s.everReady=false;updateControl(s)});
    });
    if('IntersectionObserver' in window){
      const io=new IntersectionObserver(entries=>entries.forEach(entry=>{const s=states.find(state=>state.v===entry.target);if(s){s.near=entry.isIntersecting;reconcile(s)}}),{threshold:.08});
      states.forEach(s=>io.observe(s.v));
    }else states.forEach(reconcile);
    const sync=()=>states.forEach(reconcile);
    mq?.addEventListener?.('change',sync);connection?.addEventListener?.('change',sync);
    document.addEventListener('visibilitychange',sync);window.addEventListener('resize',sync,{passive:true});
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
  setContact();nav();initForms();initGallery();initTracking();initMotion();initMedia();initBadgeSafeArea();
})();
