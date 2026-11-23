(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const questions=JSON.parse(document.getElementById('exercise-data').textContent),labs=[];
  const L=FinanceLab, reduced=matchMedia('(prefers-reduced-motion: reduce)');
  const math=el=>{try{renderMathInElement(el,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],ignoredClasses:['currency','chart','readouts','period-table','parameter-grid'],throwOnError:true,strict:'ignore',trust:false,errorCallback:()=>document.getElementById('math-error').hidden=false});}catch{document.getElementById('math-error').hidden=false;}};
  for(const q of questions){
    const card=document.getElementById(q.id),el=card.querySelector('.lab'),get=s=>el.querySelector(s);
    let p={...q.lab.base},n=q.lab.specialTime??p.periods,playing=false,frame=0,start=0,startN=0;
    const interest=q.lab.kind==='interest',step=q.lab.specialTime ? .5 : 1;
    function stop(message=''){playing=false;cancelAnimationFrame(frame);if(interest){get('[data-action=play]').textContent='Reproduzir';get('[data-action=play]').setAttribute('aria-pressed','false');}if(message)get('.lab-status').textContent=message;}
    function render(withTable=false){
      const z=L.state(q,p,n),compare=interest&&get('.compare').checked;
      get('.chart').innerHTML=L.chart(q,z,compare);get('.readouts').innerHTML=L.metrics(q,z);
      get('.live-equations').innerHTML=L.equation(q,z);math(get('.live-equations'));
      const changed=Object.keys(q.lab.base).some(k=>q.lab.base[k]!==p[k]);
      get('.model-label').textContent=changed?'Exploração · valores alterados':'Valores iniciais do laboratório';
      get('.model-label').classList.toggle('modified',changed);
      if(interest){
        get('.timeline').max=p.periods;get('.timeline').value=n;
        get('.time-value').textContent=`${L.fmt(n)} de ${p.periods} ${q.lab.unit}`;
        get('.timeline').setAttribute('aria-valuetext',get('.time-value').textContent);
        if(withTable)get('.period-table').innerHTML=L.table(q,p);
        el.querySelectorAll('[data-period]').forEach(row=>row.classList.toggle('current-period',Math.abs(+row.dataset.period-n)<1e-8));
        el.dataset.period=n;el.dataset.amount=z.amount;
      }
      for(const input of el.querySelectorAll('[data-param]')){
        input.value=p[input.dataset.param];const out=document.getElementById(input.id+'-value');
        out.textContent=input.dataset.unit==='R$'?L.money(+input.value):L.fmt(+input.value,4)+(input.dataset.unit?' '+input.dataset.unit:'');
      }
    }
    for(const input of el.querySelectorAll('[data-param]'))input.addEventListener('input',()=>{stop('Dados alterados. A resolução acima mantém os valores originais.');p[input.dataset.param]=+input.value;n=p.periods;render(true);});
    get('[data-action=restore]').addEventListener('click',()=>{stop('Dados iniciais restaurados.');p={...q.lab.base};n=q.lab.specialTime??p.periods;if(interest)get('.compare').checked=Boolean(q.lab.equivalent||q.lab.compare);render(true);});
    function advance(dir){stop('Avanço por período.');n=Math.max(0,Math.min(p.periods,n+dir*step));render();}
    if(interest){
      get('.compare').addEventListener('change',()=>render());
      get('.timeline').addEventListener('input',e=>{stop('Período selecionado.');n=+e.target.value;render();});
      get('[data-action=prev]').addEventListener('click',()=>advance(-1));
      get('[data-action=next]').addEventListener('click',()=>advance(1));
      get('[data-action=start]').addEventListener('click',()=>{stop('De volta ao capital inicial.');n=0;render();});
      for(const button of el.querySelectorAll('[data-time]'))button.addEventListener('click',()=>{stop('Prazo destacado selecionado.');n=Math.min(p.periods,+button.dataset.time);render();});
      function tick(now){
        if(!playing)return;
        if(!start)start=now;
        const next=Math.min(p.periods,startN+Math.floor((now-start)/8000*(p.periods/step))*step);
        if(n!==next){n=next;render();}
        if(n>=p.periods){stop('Fim do prazo. Você pode reproduzir novamente ou explorar outros dados.');return;}
        frame=requestAnimationFrame(tick);
      }
      get('[data-action=play]').addEventListener('click',()=>{
        if(playing){stop('Pausado.');return;}
        if(reduced.matches){if(n>=p.periods)n=0;else n=Math.min(p.periods,n+step);render();get('.lab-status').textContent='Movimento reduzido: avanço de um período por toque.';return;}
        labs.forEach(l=>l.stop());if(n>=p.periods)n=0;
        startN=n;start=0;playing=true;get('[data-action=play]').textContent='Pausar';get('[data-action=play]').setAttribute('aria-pressed','true');get('.lab-status').textContent='Reprodução por períodos, em ritmo didático.';render();frame=requestAnimationFrame(tick);
      });
    }
    card.querySelector('.solution-toggle').addEventListener('toggle',e=>{if(!e.target.open)stop();});
    const lab={card,stop,save:()=>({p:{...p},n,compare:interest&&get('.compare').checked}),restore:s=>{stop();p={...s.p};n=s.n;if(interest)get('.compare').checked=s.compare;render(true);},original:()=>({p:{...q.lab.base},n:q.lab.specialTime??q.lab.base.periods,compare:Boolean(q.lab.equivalent||q.lab.compare)})};
    labs.push(lab);render(true);
  }
  reduced.addEventListener('change',()=>labs.forEach(l=>l.stop()));
  document.addEventListener('visibilitychange',()=>{if(document.hidden)labs.forEach(l=>l.stop());});
  const cards=[...document.querySelectorAll('.card')],ids=new Set(cards.map(c=>c.id));
  const storageKey='matematica-financeira-23nov-v1',topic=document.getElementById('topic'),pending=document.getElementById('pending');
  let done=new Set(),group='all';
  try{const saved=JSON.parse(localStorage.getItem(storageKey)||'[]');if(Array.isArray(saved))done=new Set(saved.filter(id=>ids.has(id)));}catch{document.getElementById('storage-note').hidden=false;}
  function update(){let count=0;for(const c of cards){c.hidden=(group!=='all'&&c.dataset.group!==group)||(topic.value!=='all'&&c.dataset.topic!==topic.value)||(pending.checked&&done.has(c.id));c.querySelector('.done-check').checked=done.has(c.id);c.classList.toggle('done',done.has(c.id));if(!c.hidden)count++;else labs.find(l=>l.card===c).stop();}
    for(const section of document.querySelectorAll('.question-group'))section.hidden=![...section.querySelectorAll('.card')].some(c=>!c.hidden);
    document.getElementById('shown').textContent=`${count} de 30 exercícios exibidos`;document.getElementById('progresslabel').textContent=`${done.size} de 30 concluídos`;document.getElementById('progress').value=done.size;document.getElementById('empty').hidden=count!==0;
    document.querySelectorAll('[data-group-filter]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.groupFilter===group));
  }
  function clear(){group='all';topic.value='all';pending.checked=false;update();}
  document.querySelectorAll('[data-group-filter]').forEach(b=>b.addEventListener('click',()=>{group=b.dataset.groupFilter;update();}));
  document.getElementById('clear-filters').addEventListener('click',clear);topic.addEventListener('change',update);pending.addEventListener('change',update);
  cards.forEach(c=>c.querySelector('.done-check').addEventListener('change',e=>{if(e.target.checked)done.add(c.id);else done.delete(c.id);try{localStorage.setItem(storageKey,JSON.stringify([...done]));}catch{document.getElementById('storage-note').hidden=false;}update();}));
  function reveal(id,solution=false){if(!ids.has(id)&&!['originais','treino'].includes(id))return;clear();if(solution&&ids.has(id))document.getElementById(id).querySelector('.solution-toggle').open=true;}
  document.querySelectorAll('[data-jump]').forEach(a=>a.addEventListener('click',()=>reveal(a.hash.slice(1),a.hasAttribute('data-solution'))));window.addEventListener('hashchange',()=>reveal(location.hash.slice(1)));
  let printState=null;
  function beforePrint(){if(printState)return;printState=labs.map(l=>({l,s:l.save(),open:l.card.querySelector('.solution-toggle').open}));labs.forEach(l=>{l.restore(l.original());l.card.querySelector('.solution-toggle').open=true;});}
  function afterPrint(){if(!printState)return;printState.forEach(v=>{v.l.restore(v.s);v.l.card.querySelector('.solution-toggle').open=v.open;});printState=null;document.body.classList.remove('printanswers');}
  window.addEventListener('beforeprint',beforePrint);window.addEventListener('afterprint',afterPrint);
  document.querySelectorAll('[data-print]').forEach(b=>b.addEventListener('click',()=>{document.body.classList.toggle('printanswers',b.dataset.print==='answers');beforePrint();try{window.print();}finally{afterPrint();}}));
  math(document.querySelector('main'));update();if(location.hash){reveal(location.hash.slice(1));document.getElementById(location.hash.slice(1))?.scrollIntoView();}
})();
