const fs=require('fs'),vm=require('vm'),path=require('path'),assert=require('assert');
const root=path.resolve(__dirname,'../..'),qs=JSON.parse(fs.readFileSync(path.join(__dirname,'content.json'),'utf8'));
const html=fs.readFileSync(path.join(root,'matematica-financeira.html'),'utf8'),ctx={};vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(__dirname,'lab.js'),'utf8')+'\nthis.L=FinanceLab;',ctx);const L=ctx.L;
const q=id=>qs.find(q=>q.id===id),z=(id,n)=>{const v=q(id);return L.state(v,v.lab.base,n??v.lab.specialTime??v.lab.base.periods);};
const near=(a,b,label)=>assert(Math.abs(a-b)<=1e-8*Math.max(1,Math.abs(b)),`${label}: ${a} != ${b}`);
// Independent calculations from the transcribed data and authored statements.
near(z('f01').factor,1.2,'increase factor');near(z('f02').variation,-83,'discount');
near(90/(.1*.3),3000,'survey inverse');near(z('f03').sample,90,'survey forward');
near((2-1)/(16/12)*100,75,'annual simple rate');near(z('f04').amount,2000,'simple doubling');
near(Math.ceil(.3/(2.017-2)),18,'given logarithms');near(z('f05').goalPeriod,18,'annual withdrawal');
assert(50000*1.04**17<100000 && 50000*1.04**18>=100000);
near(z('f06').equivalent*100,364/15,'exact equivalent percentage');near(z('f06').simple,z('f06').compound,'same endpoint');
assert.equal((z('f06').equivalent*100).toFixed(1),'24.3');assert(Math.abs(1000*(1+.243*3)-1000*1.2**3)>0.9,'rounded option is not exact');
near(z('c18',4).amount,108,'c18a');near(z('c18',24).interest,48,'c18b');
near(180/(750*6)*100,4,'c19 inverse');near(z('c19').interest,180,'c19 forward');
near((Math.sqrt(720/500)-1)*100,20,'c23 inverse');near(z('c23',2).amount,720,'c23a');near(z('c23',3).interest,364,'c23b');
near(z('c24',1).amount,220000,'c24a');near(z('c24',2).amount,242000,'c24b');near(200000*2.6,520000,'c24 supplied approximation');near(z('c24',10).amount,518748.49202,'c24 full power');
near(z('t01').factor,1.35,'t01');near(z('t02').variation,-28,'t02');near(z('t03').final,204,'t03');near(z('t03').variation,2,'t03 percent');
near(80/(.25*.2),1600,'t04 inverse');near(z('t04').sample,80,'t04');near(340/.85,400,'t05 inverse');near(z('t05').final,340,'t05');
near(z('t06').interest,144,'t06 J');near(z('t06').amount,1344,'t06 M');near(z('t07').interest,360,'t07');
near(270/(1500*6)*100,3,'t08 inverse');near(z('t08').interest,270,'t08');near(2600/(1+.02*15),2000,'t09 inverse');near(z('t09').amount,2600,'t09');
near((1800-1500)/(1500*.02),10,'t10 inverse');near(z('t10').amount,1800,'t10');near((3-1)/(30/12)*100,80,'t11 inverse');near(z('t11').amount,3000,'t11 fractional years');
near(z('t12').amount,1331,'t12 M');near(z('t12').interest,331,'t12 J');near(z('t13').amount,882,'t13');near((Math.sqrt(1210/1000)-1)*100,10,'t14 inverse');near(z('t14',3).interest,331,'t14 J');
near(1331/1.1**3,1000,'t15 inverse');near(z('t15').amount,1331,'t15');near(Math.ceil(.1761/.0414),5,'t16 logs');near(z('t16').goalPeriod,5,'t16');
for(const [t,m]of [[1,5400],[2,5832],[3,6298.56]])near(z('t17',t).amount,m,'t17');near(z('t18').equivalent*100,10.5,'t18');near(z('t18').simple,z('t18').compound,'t18 equivalent');
near(z('t19').simple,2400,'t19 simple');near(z('t19').compound,2431.0125,'t19 compound');near(z('t19').compound-z('t19').simple,31.0125,'t19 difference');near(z('t20').final,800,'t20');near((1000-800)/1000*100,20,'t20 reverse discount');
// Consistency across parameter ranges, including zero rates and exact powers.
let cases=0,formulas=0;
const katex=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)][0][1];vm.runInContext(katex,ctx);
for(const item of qs){
  let params=[{...item.lab.base}];for(const c of L.controls(item))params=params.flatMap(p=>[c.min,item.lab.base[c.key],c.max].map(v=>({...p,[c.key]:v})));
  for(const p of params)for(const n of item.lab.kind==='interest'?[0,p.periods/2,p.periods]:[0]){
    const v=L.state(item,p,n);cases++;
    for(const [k,value]of Object.entries(v))if(typeof value==='number')assert(Number.isFinite(value),item.id+' '+k);
    if(v.kind==='interest'){
      near(v.amount-v.p.capital,v.interest,'M=C+J');
      if(item.lab.equivalent&&n===p.periods)near(v.simple,v.compound,'equivalent endpoint');
      if(p.rate===0)near(v.amount,p.capital,'zero rate');
      if(item.lab.goal&&v.goalPeriod!==null){assert(L.sum(p.capital,p.rate/100,v.goalPeriod,item.lab.mode)>=item.lab.goal*(1-1e-12));if(v.goalPeriod>0)assert(L.sum(p.capital,p.rate/100,v.goalPeriod-1,item.lab.mode)<item.lab.goal*(1-1e-12));}
    }else if(v.kind==='percent')near(v.final,p.capital*(1+v.variation/100),'percent reversal');
    else near(v.sample/p.total*100,v.totalPercent,'nested percent');
    for(const output of [L.chart(item,v,true),L.metrics(item,v),L.equation(item,v)])assert(!/NaN|Infinity|undefined/.test(output),item.id+' invalid rendering');
    for(const[,formula]of L.equation(item,v).matchAll(/\$\$([^$]+)\$\$/g)){ctx.katex.renderToString(formula,{throwOnError:true,strict:false});formulas++;}
  }
}
near(L.firstPeriod(1000,.1,1210,'compound'),2,'exact power');assert.equal(L.firstPeriod(1000,0,2000,'compound'),null);near(L.firstPeriod(2000,0,1000,'compound'),0,'already reached');
function scan(v){if(typeof v==='string'){v=v.replace(/R\$/g,'reais');assert.equal((v.match(/\$/g)||[]).length%2,0,'math delimiters');for(const[,formula]of v.matchAll(/\$([^$]+)\$/g)){ctx.katex.renderToString(formula,{throwOnError:true,strict:false});formulas++;}}else if(v&&typeof v==='object')Object.values(v).forEach(scan);}
scan(qs);
assert.equal(qs.length,30);assert.equal(qs.filter(q=>q.group==='original').length,10);assert.equal(qs.filter(q=>q.group==='treino').length,20);
assert.deepEqual(qs.filter(q=>q.group==='original').map(q=>q.id),['f01','f02','f03','f04','f05','f06','c18','c19','c23','c24']);
for(const q of qs)assert(q.steps.length>=3&&q.pitfall&&q.answer&&q.lab,q.id);
for(const[,script]of html.matchAll(/<script>([\s\S]*?)<\/script>/g))new vm.Script(script);
assert.equal((html.match(/class="card"/g)||[]).length,30);assert.equal((html.match(/class="lab"/g)||[]).length,30);
const markup=html.replace(/<script[^>]*>[\s\S]*?<\/script>/g,''),ids=[...markup.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);assert.equal(ids.length,new Set(ids).size,'duplicate IDs');
for(const[,href]of markup.matchAll(/href="([^"]+)"/g)){if(/^(https?:|data:)/.test(href))continue;const[file,anchor]=href.split('#');if(file)assert(fs.existsSync(path.join(root,file)),href);else if(anchor)assert(ids.includes(anchor),href);}
for(const file of fs.readdirSync(root).filter(f=>f.endsWith('.html'))){const nav=fs.readFileSync(path.join(root,file),'utf8').match(/<nav[^>]*aria-label="Cadernos de estudo"[^>]*>[\s\S]*?<\/nav>/);if(nav)assert.equal(nav[0].split('href="matematica-financeira.html"').length-1,1,file);}
assert(!/src="https?:/.test(html));assert(!/Lara|Buarque|Barbarato/.test(markup));
console.log(`30 exercícios (10 originais + 20 treinos), ${cases} estados de exploração e ${formulas} fórmulas conferidos. Cálculos, aproximações, arredondamentos, scripts, IDs e navegação válidos.`);
