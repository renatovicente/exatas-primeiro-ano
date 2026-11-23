/* Pure models shared by the diagrams, controls and verification script. */
const FinanceLab = (() => {
  'use strict';
  const fmt=(x,d=2)=>x.toLocaleString('pt-BR',{maximumFractionDigits:d});
  const money=x=>x.toLocaleString('pt-BR',{style:'currency',currency:'BRL'});
  const tex=x=>Number(x.toFixed(8)).toString().replace('.', '{,}');
  const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;');
  const C={ink:'#243f35',muted:'#607369',green:'#617f4d',gold:'#9b6a13',blue:'#286b90',line:'#d9ded4'};
  const sum=(capital,rate,t,mode)=>capital*(mode==='simple'?1+rate*t:(1+rate)**t);
  function firstPeriod(capital,rate,goal,mode){
    if(goal<=capital)return 0;
    if(rate===0)return null;
    const estimate=mode==='simple'?(goal/capital-1)/rate:Math.log(goal/capital)/Math.log1p(rate);
    let n=Math.ceil(estimate-1e-10);
    // Avoid an off-by-one at an exact power due to logarithmic rounding.
    const enough=k=>sum(capital,rate,k,mode)>=goal*(1-1e-12);
    while(n>0&&enough(n-1))n--;
    while(!enough(n))n++;
    return n;
  }
  function state(q,p,n=p.periods){
    const kind=q.lab.kind;
    if(kind==='percent'){
      const factor=p.factor??1+p.rate/100, first=p.capital*factor;
      const final=first*(p.second===undefined?1:1+p.second/100);
      return {kind,p,factor,first,final,change:final-p.capital,totalFactor:final/p.capital,variation:100*(final/p.capital-1)};
    }
    if(kind==='share'){
      const group=p.total*p.portion/100, sample=group*p.sample/100;
      return {kind,p,group,sample,totalPercent:p.portion*p.sample/100};
    }
    n=Math.max(0,Math.min(p.periods,n));
    const r=p.rate/100;
    const equivalent=((1+r)**p.periods-1)/p.periods;
    const simpleRate=q.lab.equivalent?equivalent:r;
    const simple=sum(p.capital,simpleRate,n,'simple'),compound=sum(p.capital,r,n,'compound');
    const amount=q.lab.mode==='simple'?simple:compound;
    const step=q.lab.specialTime ? .5 : 1;
    const prev=sum(p.capital,q.lab.mode==='simple'?simpleRate:r,Math.max(0,n-step),q.lab.mode);
    const goalPeriod=q.lab.goal?firstPeriod(p.capital,r,q.lab.goal,q.lab.mode):null;
    return {kind,p,n,r,simpleRate,simple,compound,amount,interest:amount-p.capital,
      increment:n===0?0:amount-prev,equivalent,goalPeriod,step,unit:q.lab.unit};
  }
  function controls(q){
    const p=q.lab.base;
    const control=(key,label,min,max,step,unit='')=>({key,label,min,max,step,unit});
    if(q.lab.kind==='share')return [control('total','Total de participantes',100,6000,100),control('portion','Grupo dentro do total',5,80,5,'%'),control('sample','Parte dentro do grupo',5,100,5,'%')];
    const capital=control('capital','Valor inicial',Math.min(50,p.capital),Math.max(p.capital*2,1000),Math.min(50,p.capital),'R$');
    if(q.lab.kind==='percent')return [capital, p.factor===undefined?control('rate','Primeira variação (− = desconto)',-90,100,1,'%'):control('factor','Fator multiplicativo',.05,2,.01),...(p.second===undefined?[]:[control('second','Segunda variação (− = desconto)',-90,100,1,'%')])];
    return [capital,control('rate',`Taxa ${q.lab.unit==='anos'?'anual':'mensal'} ${q.lab.mode==='simple'?'simples':'composta'}`,0,Math.max(30,p.rate*2),p.rate===6.25?.25:.5,'%'),control('periods','Prazo total / horizonte',1,Math.max(24,p.periods+6),1,q.lab.unit)];
  }
  const text=(x,y,s,size=20,color=C.ink,anchor='middle')=>`<text x="${x}" y="${y}" font-size="${size}" text-anchor="${anchor}" fill="${color}">${esc(s)}</text>`;
  const line=(x1,y1,x2,y2,color=C.line,extra='')=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="2" ${extra}/>`;
  const svg=(body,desc,h=350)=>`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 ${h}" role="img" aria-label="${esc(desc)}" style="font-family:Arial,Helvetica,sans-serif"><title>${esc(desc)}</title>${body}</svg>`;
  const compact=x=>Intl.NumberFormat('pt-BR',{notation:'compact',maximumFractionDigits:1}).format(x);
  function chart(q,z,compare=true){
    const p=z.p;
    if(z.kind==='percent'){
      const values=[['Inicial',p.capital],...(p.second===undefined?[]:[['Após a 1ª variação',z.first]]),['Final',z.final]];
      const max=Math.max(...values.map(v=>v[1]));let body='';
      values.forEach(([name,value],i)=>{const y=55+i*88;body+=text(20,y,name,21,C.ink,'start')+`<rect x="20" y="${y+12}" width="${400*value/max}" height="24" rx="4" fill="${i===0?C.blue:C.green}"/>`+text(620,y+30,money(value),19,C.ink,'end');});
      return svg(body,`Comparação: valor inicial ${money(p.capital)}, valor final ${money(z.final)}. Variação ${fmt(z.variation)}%.`,values.length*88+35);
    }
    if(z.kind==='share'){
      const w=540, groupWidth=w*p.portion/100, sampleWidth=groupWidth*p.sample/100;
      let b=text(20,30,'O total',22,C.ink,'start')+`<rect x="20" y="48" width="${w}" height="38" rx="4" fill="#e4e9dc"/><rect x="20" y="48" width="${groupWidth}" height="38" fill="${C.blue}"/><rect x="20" y="48" width="${sampleWidth}" height="38" fill="${C.gold}"/>`;
      b+=text(20,125,`Azul + ocre: ${fmt(p.portion)}% do total`,22,C.blue,'start');
      b+=text(20,170,'Agora, amplie apenas o grupo',22,C.ink,'start')+`<rect x="20" y="190" width="${w}" height="38" fill="${C.blue}"/><rect x="20" y="190" width="${w*p.sample/100}" height="38" fill="${C.gold}"/>`;
      b+=text(20,270,`Ocre: ${fmt(p.sample)}% do grupo = ${fmt(z.totalPercent)}% do total`,21,C.gold,'start');
      return svg(b,`Total ${fmt(p.total)}. Grupo ${fmt(z.group)}. Parte do grupo ${fmt(z.sample)}, que representa ${fmt(z.totalPercent)}% do total.`,300);
    }
    const T=p.periods, steps=Math.round(T/z.step), samples=Array.from({length:steps+1},(_,i)=>state(q,p,i*z.step));
    const max=Math.max(q.lab.goal||0,...samples.map(v=>Math.max(v.amount,compare?v.simple:0,compare?v.compound:0)))*1.12;
    const x=t=>82+490*t/T,y=a=>280-a/max*245;
    let b=text(82,21,'Montante (R$)',19,C.ink,'start');
    for(let j=0;j<=4;j++){const value=max*j/4;b+=line(82,y(value),590,y(value))+text(72,y(value)+6,compact(value),17,C.muted,'end');}
    b+=line(82,30,82,280,C.ink)+line(82,280,590,280,C.ink)+text(82,308,'0',19)+text(572,308,String(T),19)+text(590,336,q.lab.unit,18,C.muted,'end');
    const paths=compare?[['simple',C.blue],['compound',C.green]]:[[q.lab.mode==='simple'?'simple':'compound',q.lab.mode==='simple'?C.blue:C.green]];
    for(const [key,color]of paths){b+=`<polyline points="${samples.map(v=>`${x(v.n)},${y(v[key])}`).join(' ')}" fill="none" stroke="${color}" stroke-width="3"/>`;
      for(const v of samples)b+=`<circle cx="${x(v.n)}" cy="${y(v[key])}" r="3" fill="${color}"/>`;
      b+=`<circle cx="${x(z.n)}" cy="${y(z[key])}" r="7" fill="${color}" stroke="white" stroke-width="2"/>`;
    }
    b+=line(x(z.n),30,x(z.n),280,C.muted,'stroke-dasharray="4 4"');
    if(q.lab.goal)b+=line(82,y(q.lab.goal),590,y(q.lab.goal),C.gold,'stroke-dasharray="8 5"')+text(590,y(q.lab.goal)-9,'Meta',19,C.gold,'end');
    return svg(b,`Montante ao longo de ${T} ${q.lab.unit}. No instante ${fmt(z.n)}, ${money(z.amount)}. ${compare?'Azul: juros simples. Verde: juros compostos.':''}`);
  }
  function metrics(q,z){
    let v;
    if(z.kind==='percent')v=[['Inicial',money(z.p.capital)],['Final',money(z.final)],['Fator total',fmt(z.totalFactor,4)],['Variação',fmt(z.variation,4)+'%']];
    else if(z.kind==='share')v=[['Total',fmt(z.p.total)],['Grupo',fmt(z.group)],['Parte do grupo',fmt(z.sample)],['Parte / total',fmt(z.totalPercent)+'%']];
    else{
      v=[['Prazo escolhido',fmt(z.n)+' '+z.unit],['Capital',money(z.p.capital)],['Montante',money(z.amount)],['Juros acumulados',money(z.interest)]];
      if(q.lab.equivalent)v.push(['Taxa simples equivalente',fmt(z.equivalent*100,6)+'% por período']);
      if(q.lab.compare)v.push(['Diferença: composto − simples',money(z.compound-z.simple)]);
      if(q.lab.goal)v.push(['Primeiro prazo inteiro da meta',z.goalPeriod===null?'Meta não atingida com taxa zero':fmt(z.goalPeriod)+' '+z.unit]);
    }
    return v.map(([k,v])=>`<div><dt>${k}</dt><dd>${v}</dd></div>`).join('');
  }
  function equation(q,z){
    const p=z.p,t=tex;let e=[];
    if(z.kind==='percent')e=[`f=${t(z.factor)}${p.second!==undefined?`\\cdot ${t(1+p.second/100)}`:''}=${t(z.totalFactor)}`,`V_f=${t(p.capital)}\\cdot ${t(z.totalFactor)}=${t(z.final)}`];
    else if(z.kind==='share')e=[`n=N\\cdot\\frac{p}{100}\\cdot\\frac{q}{100}`,`${t(z.sample)}=${t(p.total)}\\cdot${t(p.portion/100)}\\cdot${t(p.sample/100)}`];
    else{
      e=[q.lab.mode==='simple'?`M=${t(p.capital)}(1+${t(z.r)}\\cdot${t(z.n)})\\approx${t(z.amount)}`:`M=${t(p.capital)}(1+${t(z.r)})^{${t(z.n)}}\\approx${t(z.amount)}`,`J=M-C\\approx${t(z.interest)}`];
      if(q.lab.equivalent)e.push(`i_s=\\frac{(1+i_c)^t-1}{t}\\approx${t(z.equivalent*100)}\\%`);
    }
    return e.map(s=>`<div>$$${s}$$</div>`).join('');
  }
  function table(q,p){
    if(q.lab.kind!=='interest')return '';
    const step=q.lab.specialTime ? .5 : 1, rows=[];
    for(let n=0;n<=p.periods+1e-8;n+=step){const z=state(q,p,n);rows.push(`<tr data-period="${n}"><th scope="row">${fmt(n)}</th><td>${money(z.amount)}</td><td>${money(z.increment)}</td><td>${money(z.interest)}</td></tr>`);}
    return `<table><caption>Valores sem arredondamento intermediário · exibição em centavos</caption><thead><tr><th scope="col">${q.lab.unit==='anos'?'Ano':'Mês'}</th><th scope="col">Montante</th><th scope="col">Juro no intervalo</th><th scope="col">Juros acumulados</th></tr></thead><tbody>${rows.join('')}</tbody></table>`;
  }
  function voteFigure(){
    // Clockwise from twelve o'clock: 20%, 30%, 50%.
    const center=[250,165],r=120,point=a=>[center[0]+r*Math.sin(a),center[1]-r*Math.cos(a)];
    let start=0,b='';const colors=[C.gold,C.blue,'#d2dcc6'];
    [20,30,50].forEach((pct,i)=>{const end=start+2*Math.PI*pct/100,a=point(start),c=point(end);b+=`<path d="M${center} L${a} A${r} ${r} 0 0 1 ${c} Z" fill="${colors[i]}" stroke="#fffef9" stroke-width="3"/>`;const mid=(start+end)/2;b+=text(250+75*Math.sin(mid),171-75*Math.cos(mid),String(pct)+'%',23,i===2?C.ink:'#fffef9');b+=text(440,100+i*60,`${['A','B','C'][i]} · ${pct}%`,24,C.ink,'start');start=end;});
    return svg(b,'Intenções de voto: A 20%, B 30%, C 50%.',310);
  }
  return {fmt,money,tex,state,controls,chart,metrics,equation,table,voteFigure,sum,firstPeriod};
})();
