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
      if(!open){drops.forEach(d=>setDrop(d,false));if(returnFocus)toggle.focus()}
    }
    if(toggle&&menu){
      toggle.addEventListener('click',()=>setMenu(!menu.classList.contains('open'),false));
      menu.addEventListener('click',ev=>{if(ev.target.closest('a'))setMenu(false,false)});
    }
    drops.forEach(d=>{const b=d.querySelector('button');if(!b)return;b.addEventListener('click',()=>{const open=!d.classList.contains('open');drops.forEach(o=>{if(o!==d)setDrop(o,false)});setDrop(d,open)})});
    document.addEventListener('click',ev=>{
      if(!ev.target.closest('.nav-dropdown'))drops.forEach(d=>setDrop(d,false));
      if(menu&&menu.classList.contains('open')&&!ev.target.closest('.site-header'))setMenu(false,false);
    });
    document.addEventListener('keydown',ev=>{
      if(ev.key!=='Escape')return;
      const openDrop=drops.find(d=>d.classList.contains('open'));
      if(openDrop&&!(menu&&menu.classList.contains('open'))){setDrop(openDrop,false);openDrop.querySelector('button')?.focus();return}
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
      let step=1;
      const stepElements=[...form.querySelectorAll('.form-step')];
      const counter=form.querySelector('.form-progress');const track=form.querySelector('.form-progress-track i');
      const status=form.querySelector('.form-status');
      function showStep(n){step=n;stepElements.forEach(el=>el.classList.toggle('active',Number(el.dataset.step)===n));if(counter)counter.textContent=`Step ${n} of 2`;if(track)track.style.width=n===1?'50%':'100%';status.className='form-status';status.textContent='';let first=form.querySelector('.form-step.active input:not([type=hidden]),.form-step.active select');if(n===2)first?.focus({preventScroll:true})}
      function validatePanel(n){const controls=form.querySelectorAll(`.form-step[data-step="${n}"] input,.form-step[data-step="${n}"] select,.form-step[data-step="${n}"] textarea`);for(const el of controls){if(!el.checkValidity()){el.reportValidity();return false}}return true}
      form.querySelector('.form-next')?.addEventListener('click',()=>{if(validatePanel(1))showStep(2)});
      form.querySelector('.form-back')?.addEventListener('click',()=>showStep(1));
      form.addEventListener('submit',async(ev)=>{
        ev.preventDefault();if(step!==2){if(validatePanel(1))showStep(2);return}if(!validatePanel(2))return;
        const fd=new FormData(form), data=Object.fromEntries(fd.entries());data.source=window.location.pathname||'/';data.consent=data.consent==='on';
        const submit=form.querySelector('button[type=submit]');submit.disabled=true;submit.textContent='Sending request…';status.className='form-status';status.textContent='';
        try{
          // Local Node server (npm start) uses /api/leads; the hosted site (Netlify) uses Netlify Forms.
          const local=['localhost','127.0.0.1'].includes(location.hostname);
          let res,result={};
          if(local){
            res=await fetch('/api/leads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
            result=await res.json().catch(()=>({}));
          }else{
            const body=new URLSearchParams({'form-name':'consultation',...data,consent:data.consent?'yes':'no'});
            res=await fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:body.toString()});
          }
          if(!res.ok)throw new Error(result.message||'We couldn’t send your request just now. Please check your connection and try again in a moment. If it keeps failing, please reach out through the contact details on this site.');
          window.location.href='thank-you.html';
        }catch(err){status.className='form-status error';status.textContent=err.message||'Unable to send right now. Please try again in a moment.';submit.disabled=false;submit.textContent='Send Consultation Request'}
      });
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
  setContact();nav();initForms();initGallery();initTracking();initMotion();
})();
