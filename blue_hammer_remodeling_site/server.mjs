/**
 * Blue Hammer Remodeling: zero-dependency local / VPS website & lead collector.
 * Start: node server.mjs (Node 20+); serve behind HTTPS proxy in production.
 * POST /api/leads persists each validated lead with file permission 0600.
 * Optional email notifications via Resend: RESEND_API_KEY, LEADS_TO_EMAIL, LEADS_FROM_EMAIL.
 * This is a deployable starter, not a full hosting or CRM configuration.
 */
import http from 'node:http';
import path from 'node:path';
import fs from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import crypto from 'node:crypto';
const ROOT=path.dirname(fileURLToPath(import.meta.url));
const PORT=Number(process.env.PORT||4173);
const HOST=process.env.HOST||'127.0.0.1';
const DATA=path.join(ROOT,'data','leads.jsonl');
const TYPES={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'application/javascript; charset=utf-8','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.svg':'image/svg+xml','.webp':'image/webp','.txt':'text/plain; charset=utf-8','.xml':'application/xml; charset=utf-8','.ico':'image/x-icon'};
const rate=new Map();
function send(res,status,data){res.writeHead(status,{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'});res.end(JSON.stringify(data))}
function isStr(s,min,max){return typeof s==='string'&&s.trim().length>=min&&s.trim().length<=max}
function valid(d){return d&&typeof d==='object'&&isStr(d.firstName,2,80)&&isStr(d.lastName,1,80)&&isStr(d.email,5,180)&&/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(d.email)&&isStr(d.phone,7,25)&&/^[+0-9().\s-]+$/.test(d.phone)&&/^[0-9]{5}$/.test(d.zip||'')&&isStr(d.projectType,3,80)&&isStr(d.timeline,3,80)&&(!d.message||isStr(d.message,0,3000))&&d.consent===true;}
function clean(s,limit=1000){return String(s||'').slice(0,limit).replace(/[\x00-\x08\x0b\x0c\x0e-\x1f]/g,'').trim()}
async function notify(lead){
 const {RESEND_API_KEY:key,LEADS_TO_EMAIL:to,LEADS_FROM_EMAIL:from}=process.env;
 if(!key||!to||!from)return false;
 const lines=Object.entries(lead).map(([k,v])=>`${k}: ${String(v)}`).join('\n');
 try{
  const response=await fetch('https://api.resend.com/emails',{method:'POST',headers:{Authorization:`Bearer ${key}`,'Content-Type':'application/json'},body:JSON.stringify({from,to:[to],subject:`New Blue Hammer remodeling inquiry — ${lead.projectType}`,text:lines})});
  if(!response.ok){console.error('Email notification failed:',response.status);return false}
  return true;
 }catch(err){console.error('Email provider request failed:',err.message);return false}
}
async function leadHandler(req,res){
 const ip=req.socket.remoteAddress||'unknown';
 const now=Date.now();
 const times=(rate.get(ip)||[]).filter(t=>now-t<60*60*1000);
 if(times.length>=8){send(res,429,{message:'Too many requests. Please try again later.'});return}
 rate.set(ip,times);
 let raw='';
 try{
  if(!(req.headers['content-type']||'').includes('application/json')){send(res,415,{message:'Please submit the project form.'});return}
  for await(const chunk of req){raw+=chunk;if(raw.length>18000){send(res,413,{message:'Request too large.'});return}}
  const d=JSON.parse(raw);
  if(d.companyWebsite){send(res,200,{ok:true});return} // Spam honeypot, do not store.
  if(!valid(d)){send(res,400,{message:'Please check the required form fields and try again.'});return}
  const lead={id:crypto.randomUUID(),submittedAt:new Date().toISOString(),firstName:clean(d.firstName,80),lastName:clean(d.lastName,80),email:clean(d.email,180),phone:clean(d.phone,25),zip:clean(d.zip,5),projectType:clean(d.projectType,80),timeline:clean(d.timeline,80),message:clean(d.message,3000),source:clean(d.source,180),utm_source:clean(d.utm_source,80),utm_campaign:clean(d.utm_campaign,80),consent:true};
  await fs.mkdir(path.dirname(DATA),{recursive:true,mode:0o700});
  await fs.appendFile(DATA,JSON.stringify(lead)+'\n',{encoding:'utf8',mode:0o600,flag:'a'});
  times.push(now);rate.set(ip,times);
  const emailed=await notify(lead);
  console.log(`Saved remodeling inquiry ${lead.id}, email notification: ${emailed?'sent':'not configured/failed'}`);
  send(res,200,{ok:true,message:'Your request was received. Thank you.'});
 }catch(e){console.error('Lead handler error:',e.message);send(res,500,{message:'We could not send your request right now. Please try again.'})}
}
async function staticHandler(req,res){
 let file;
 try{
  const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
  if(pathname==='/'||pathname==='')file=path.join(ROOT,'index.html');
  else file=path.resolve(ROOT,'.'+pathname);
  if(!file.startsWith(ROOT+path.sep)&&file!==path.join(ROOT,'index.html'))throw Error('Bad path');
  const relative=path.relative(ROOT,file).replaceAll('\\','/');
  const ext=path.extname(file).toLowerCase();
  if(!TYPES[ext]||relative.startsWith('data/')||relative==='server.mjs'||relative==='assets/site-config.js.bak'||relative.startsWith('.')||relative==='sitemap.template.xml'){res.writeHead(404);res.end('Not found');return}
  const bytes=await fs.readFile(file);
  res.writeHead(200,{'Content-Type':TYPES[ext],'X-Content-Type-Options':'nosniff','Referrer-Policy':'strict-origin-when-cross-origin','X-Frame-Options':'SAMEORIGIN','Cache-Control':ext==='.html'?'no-cache':'public, max-age=86400'});
  if(req.method==='HEAD')res.end();else res.end(bytes);
 }catch(err){res.writeHead(404,{'Content-Type':'text/plain'});res.end('Not found')}
}
const server=http.createServer(async(req,res)=>{
 if(req.url?.split('?')[0]==='/api/leads'&&req.method==='POST'){await leadHandler(req,res);return}
 if(req.method==='GET'||req.method==='HEAD'){await staticHandler(req,res);return}
 res.writeHead(405);res.end('Method not allowed');
});
server.listen(PORT,HOST,()=>{
 console.log(`Blue Hammer Remodeling: http://${HOST}:${PORT}`);
 console.log('Forms save each approved inquiry to data/leads.jsonl (this path is not served).');
 if(!process.env.RESEND_API_KEY)console.log('Email notifications are not configured; set Resend environment variables before public launch.');
});
