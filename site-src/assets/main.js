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
  setContact();nav();initForms();initGallery();initTracking();initBadgeSafeArea();initMobileBar();
})();
