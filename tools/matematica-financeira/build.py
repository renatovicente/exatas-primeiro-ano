"""Generate one offline workbook, with source-specific solutions and 20 new drills."""
from pathlib import Path
import html
import json
import re
import runpy
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
QS=runpy.run_path(str(HERE/'data.py'))['QUESTIONS']
SLUG='matematica-financeira.html'
LINK=f'<a href="{SLUG}">Matemática financeira · Lista e treino</a>'
base=(ROOT/'index.html').read_text()
nav_pattern=r'<nav[^>]*aria-label="Cadernos de estudo"[^>]*>.*?</nav>'


def prose(value):
    return 'R<span class="currency">$</span>'.join(re.sub(r'(\$[^$]+\$)',r'<span class="math-inline">\1</span>',html.escape(part)) for part in value.split('R$'))


def update_nav(nav):
    return nav if f'href="{SLUG}"' in nav else nav.replace('</nav>',LINK+'</nav>')


source=(HERE/'lab.js').read_text()+'\nconst qs='+json.dumps(QS,ensure_ascii=False)+';\n'
source+='console.log(JSON.stringify(qs.map(q=>{const p=q.lab.base,z=FinanceLab.state(q,p,q.lab.specialTime??p.periods);return {chart:FinanceLab.chart(q,z,!!(q.lab.equivalent||q.lab.compare)),metrics:FinanceLab.metrics(q,z),equation:FinanceLab.equation(q,z),table:FinanceLab.table(q,p),controls:FinanceLab.controls(q),figure:q.figure?FinanceLab.voteFigure():null};})));'
rendered=json.loads(subprocess.run(['node','-e',source],capture_output=True,text=True,check=True).stdout)


def lab(q,r):
    config=q['lab']; interest=config['kind']=='interest'; id=q['id']
    if interest:
        note=config.get('note','Mude o capital, a taxa ou o prazo e acompanhe o saldo. Os cálculos mantêm a precisão completa; os valores em reais são exibidos em centavos.')
        if config.get('equivalent'):
            guidance='Azul: simples, com taxa equivalente calculada para o prazo total. Verde: compostos, com a taxa do controle. Os montantes coincidem no fim do prazo.'
        else:
            guidance='Na comparação, os dois regimes usam o mesmo capital, a mesma taxa e o mesmo prazo. Os pontos marcam os períodos; os segmentos ajudam a acompanhar a leitura.'
        step='.5' if config.get('specialTime') else '1'
        milestones=config.get('landmarks',[])+([config['specialTime']] if config.get('specialTime') else [])
        landmarks='<div class="landmarks">'+''.join(f'<button data-time="{t}">Ver {str(t).replace(".",",")} {config["unit"]}</button>' for t in milestones)+'</div>' if milestones else ''
        player=f'''<div class="player lab-controls"><label class="time-label" for="time-{id}">Período escolhido<span class="time-value"></span></label><input id="time-{id}" class="timeline" type="range" min="0" max="{config['base']['periods']}" step="{step}" value="{config.get('specialTime',config['base']['periods'])}"><div class="player-buttons"><button data-action="play" aria-pressed="false">Reproduzir</button><button data-action="prev">Período anterior</button><button data-action="next">Próximo período</button><button data-action="start">Voltar ao início</button></div>{landmarks}</div>'''
        legend='<div class="legend"><span style="--color:#286b90">Juros simples</span><span style="--color:#617f4d">Juros compostos</span>'+('<span style="--color:#9b6a13">Meta</span>' if config.get('goal') else '')+'</div>'
        compare=f'<label class="compare-label lab-controls"><input class="compare" type="checkbox"'+(' checked' if config.get('equivalent') or config.get('compare') else '')+'>Comparar os dois regimes no gráfico</label>'
        table='<details class="table-toggle"><summary>Ver tabela por período</summary><div class="period-table">'+r['table']+'</div></details>'
        title='Acompanhe o dinheiro ao longo do tempo'
    else:
        title='Veja as proporções e mude os valores'; player=legend=compare=table=''
        note='As barras mostram os valores calculados, com escala ajustada ao maior deles. A resolução escrita acima mantém os dados originais.'
        if id in ['f01','f02','t01','t02']: note+=' Como o enunciado não fornece um valor inicial, usamos R$ 100 apenas para visualizar o fator.'
        if config['kind']=='share': note='A primeira barra mostra o total; a segunda amplia somente o grupo. O trecho ocre representa a parte escolhida dentro dele. Contagens de pessoas devem ser inteiras; os controles permitem explorar também proporções fracionárias.'
        guidance='Altere um dado de cada vez. Observe a base sobre a qual cada porcentagem é calculada.'
    controls=''.join(f'''<div class="parameter"><label for="{id}-{c['key']}">{html.escape(c['label'])}<output id="{id}-{c['key']}-value" for="{id}-{c['key']}"></output></label><input id="{id}-{c['key']}" type="range" data-param="{c['key']}" data-unit="{c['unit']}" min="{c['min']}" max="{c['max']}" step="{c['step']}" value="{config['base'][c['key']]}"></div>''' for c in r['controls'])
    return f'''<section class="lab" aria-labelledby="lab-{id}"><p class="eyebrow">Visualização interativa</p><h4 id="lab-{id}">{title}</h4><p class="model-label">Valores iniciais do laboratório</p><p class="lab-note">{prose(note)}</p><div class="chart">{r['chart']}</div>{legend}{compare}<p class="small">{guidance}</p><dl class="readouts" aria-label="Valores calculados">{r['metrics']}</dl>{player}<p class="lab-status lab-controls" role="status">Use os controles para explorar; a reprodução não é automática.</p><div class="live-equations">{r['equation']}</div>{table}<details class="explore lab-controls"><summary>Explore outros valores</summary><div class="parameter-grid">{controls}</div><button data-action="restore">Restaurar dados iniciais</button></details><p class="print-note">Impressão com os dados iniciais e o prazo de referência do exercício.</p></section>'''


def card(q,r):
    id=q['id'];note='<aside class="source-note"><strong>Sobre o arredondamento</strong><p>'+prose(q['note'])+'</p></aside>' if q['note'] else ''
    parts='<ul class="parts">'+''.join('<li>'+prose(s)+'</li>' for s in q['parts'])+'</ul>' if q['parts'] else ''
    choices='<ol class="choices" type="A" aria-label="Alternativas">'+''.join('<li>'+prose(s)+'</li>' for s in q['choices'])+'</ol>' if q['choices'] else ''
    figure='<figure class="exercise-figure">'+r['figure']+'<figcaption>Intenções de voto · proporções da folha</figcaption></figure>' if r['figure'] else ''
    return f'''<article class="card" id="{id}" data-group="{q['group']}" data-topic="{q['topic']}"><div class="card-heading"><span class="number">{q['label']}</span><h3 id="title-{id}">{q['title']}</h3><span class="topic-tag">{q['topic']}</span></div><p class="prompt">{prose(q['prompt'])}</p>{parts}{figure}{choices}
<div class="actions interactive-tools"><label><input class="done-check" type="checkbox" aria-label="Marcar {q['label']} como concluído">Entendi e refiz</label><a class="permalink" href="#{id}">Link do exercício</a></div>
<details class="solution-toggle"><summary>Ver solução e explorar · {q['label']}</summary><div class="solution" aria-labelledby="title-{id}">{note}<h4>Resolução passo a passo</h4><ol>{''.join('<li>'+prose(s)+'</li>' for s in q['steps'])}</ol><p class="answer"><strong>Resposta:</strong> {prose(q['answer'])}</p><div class="pitfall"><strong>De olho no erro comum</strong>{prose(q['pitfall'])}</div>{lab(q,r)}</div></details></article>'''


groups=[]
for group,title,description in [('original','Os exercícios das fotos','6 da folha + 4 do caderno · numeração original preservada'),('treino','20 novos exercícios para praticar','Da porcentagem ao crescimento composto')]:
    selected=[(q,r) for q,r in zip(QS,rendered) if q['group']==group]; section='originais' if group=='original' else 'treino'
    jumps='<nav class="question-jumps" aria-label="Exercícios '+title+'">'+''.join(f'<a data-jump href="#{q["id"]}">{q["label"]}</a>' for q,_ in selected)+'</nav>'
    groups.append(f'<section class="question-group" id="{section}" aria-labelledby="heading-{section}"><div class="section-heading"><h2 id="heading-{section}">{title}</h2><p>{description}</p></div>'+jumps+''.join(card(q,r) for q,r in selected)+'</section>')

nav=update_nav(re.search(nav_pattern,base,re.S).group())
nav=re.sub(r' aria-current="page"','',nav).replace(f'href="{SLUG}"',f'href="{SLUG}" aria-current="page"')
scripts=re.findall(r'<script>(.*?)</script>',base,re.S)[:2]
values=dict(KATEX_CSS=re.findall(r'<style>(.*?)</style>',base,re.S)[0],PAGE_CSS=(ROOT/'tools/revisao-logaritmos/style.css').read_text()+'\n'+(HERE/'style.css').read_text(),KATEX_JS=scripts[0],AUTORENDER_JS=scripts[1],NOTEBOOK_NAV=nav,
    TOPICS=''.join(f'<option>{t}</option>' for t in dict.fromkeys(q['topic'] for q in QS)),EXERCISES=''.join(groups),
    ANSWER_KEY=''.join(f'<li><a data-jump data-solution href="#{q["id"]}">{q["label"]} · abrir resolução</a><span>{prose(q["answer"])}</span></li>' for q in QS),
    EXERCISE_DATA=json.dumps(QS,ensure_ascii=False).replace('</','<\\/'),PAGE_APP=(HERE/'lab.js').read_text()+'\n'+(HERE/'app.js').read_text())
page=(HERE/'template.html').read_text()
for key,value in values.items():page=page.replace('{{'+key+'}}',value)
assert not re.search(r'\{\{[A-Z_]+\}\}',page)
(ROOT/SLUG).write_text(page)
(HERE/'content.json').write_text(json.dumps(QS,ensure_ascii=False,indent=2)+'\n')
count=0
for path in ROOT.glob('*.html'):
    if path.name==SLUG:continue
    old=path.read_text();new=re.sub(nav_pattern,lambda m:update_nav(m.group()),old,flags=re.S)
    if old!=new:path.write_text(new);count+=1
print(f'{SLUG}: 10 exercícios originais + 20 treinos; 30 laboratórios. Navegação atualizada em {count} páginas.')
