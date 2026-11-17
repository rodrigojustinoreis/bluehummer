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
    const menu=document.querySelector('.nav-links');
    if(toggle&&menu){toggle.addEventListener('click',()=>{let open=menu.classList.toggle('open');toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'Close menu':'Open menu')});}
    document.querySelectorAll('.nav-dropdown>button').forEach(btn=>{btn.addEventListener('click',()=>{const open=btn.parentElement.classList.toggle('open');btn.setAttribute('aria-expanded',String(open))})});
    document.addEventListener('keydown',ev=>{if(ev.key==='Escape'){menu?.classList.remove('open');if(toggle)toggle.setAttribute('aria-expanded','false');document.querySelectorAll('.nav-dropdown.open').forEach(el=>el.classList.remove('open'))}})
    document.querySelectorAll('a[href*="#consultation"]').forEach(link=>link.addEventListener('click',(ev)=>{
      const target=document.getElementById('consultation');if(target){ev.preventDefault();target.scrollIntoView({behavior:'smooth'});history.replaceState(null,'','#consultation')}
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
          if(!res.ok)throw new Error(result.message||'We could not submit your request. Please try again.');
          window.location.href='thank-you.html';
        }catch(err){status.className='form-status error';status.textContent=err.message||'Unable to send. Please try again.';submit.disabled=false;submit.textContent='Send Consultation Request →'}
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
  setContact();nav();initForms();initGallery();initTracking();
})();
