"""Transcrição das quatro fotos de 23/11/2026 e vinte exercícios novos."""
QUESTIONS = []


def interest(capital, rate, periods, unit='meses', mode='compound', **extra):
    return dict(kind='interest', base=dict(capital=capital, rate=rate, periods=periods), unit=unit, mode=mode, **extra)


def percent(capital=100, **kwargs):
    return dict(kind='percent', base=dict(capital=capital, **kwargs))


def share(total, portion, sample):
    return dict(kind='share', base=dict(total=total, portion=portion, sample=sample))


def add(id, label, title, topic, prompt, steps, answer, pitfall, lab, *, parts=None, note=None, choices=None, figure=None):
    QUESTIONS.append(dict(id=id, label=label, title=title, topic=topic,
        group='treino' if id.startswith('t') else 'original', prompt=prompt,
        parts=parts or [], steps=steps, answer=answer, pitfall=pitfall,
        lab=lab, note=note, choices=choices or [], figure=figure))


add('f01','Folha · 1','Aumento é multiplicação','Porcentagens',
    r'Um aumento de $20\%$ de x é a mesma coisa que multiplicar x por qual número?',
    [r'Um aumento de $20\%$ acrescenta $20/100=0{,}20$ do valor inicial.',
     r'O novo valor é $x+0{,}20x=(1+0{,}20)x=1{,}20x$.',
     r'Portanto, o fator multiplicativo é $1{,}20$: os $100\%$ iniciais mais os $20\%$ de aumento.'],
    r'$1{,}20$.',r'$0{,}20x$ é apenas o acréscimo; o valor final ainda inclui x.',percent(rate=20))

add('f02','Folha · 2','Quanto foi retirado?','Porcentagens',
    r'Uma multiplicação por $0{,}17$ corresponde a um desconto de quantos por cento?',
    [r'O fator $0{,}17$ informa a parte que permanece: $17\%$ do valor inicial.',
     r'O desconto é a parte retirada: $100\%-17\%=83\%$.',
     r'Conferência: o fator de um desconto de $83\%$ é $1-0{,}83=0{,}17$.'],
    r'$83\%$.',r'O fator de desconto representa o que sobra, não o que foi retirado.',percent(factor=.17))

add('f03','Folha · 3','Uma porcentagem de outra porcentagem','Porcentagens',
    r'Em uma pesquisa, as intenções de voto são: A, $20\%$; B, $30\%$; C, $50\%$. Sabendo que $10\%$ dos que votam no candidato B correspondem a 90 pessoas, qual é o total de eleitores entrevistados?',
    [r'Se $10\%$ do grupo B são 90 pessoas, o grupo B tem $90/0{,}10=900$ pessoas.',
     r'Esse grupo representa $30\%$ do total N. Assim, $0{,}30N=900$.',
     r'Logo $N=900/0{,}30=3\,000$ pessoas.',
     r'Diretamente, $0{,}10\cdot0{,}30N=90$. São $3\%$ do total, não $10\%$ do total.'],
    r'$3\,000$ pessoas.',r'Os 10% são calculados sobre os eleitores de B. Primeiro identifique a base de cada porcentagem.',share(3000,30,10),figure='votes')

add('f04','Folha · 4','Dobrar com juros simples','Juros simples',
    r'A que taxa anual de juros simples um capital deve ser aplicado durante 16 meses para que o montante final seja o dobro do capital aplicado?',
    [r'Como a taxa pedida é anual, converta o prazo: $t=16/12=4/3$ de ano.',
     r'Nos juros simples, $M=C(1+it)$. Para dobrar, $2C=C(1+i\cdot4/3)$.',
     r'Divida por $C>0$: $2=1+4i/3$, portanto $i=3/4=0{,}75$.',
     r'A taxa é $75\%$ ao ano. A taxa mensal simples equivalente seria $75\%/12=6{,}25\%$ ao mês.'],
    r'$75\%$ ao ano.',r'Não use 16 como tempo em anos. Taxa e prazo precisam estar na mesma unidade.',
    interest(1000,6.25,16,mode='simple',note='Para acompanhar mês a mês, o laboratório usa a taxa simples equivalente de 6,25% ao mês. O capital ilustrativo é R$ 1.000; a taxa pedida, 75% ao ano, independe dele.'))

add('f05','Folha · 5','O primeiro saque anual possível','Juros compostos',
    r'Ao se aposentar aos 65 anos, um trabalhador recebeu R$ 50.000,00 de FGTS e aplicou esse valor a juros compostos de $4\%$ ao ano, para atingir R$ 100.000,00. O dinheiro só pode ser retirado anualmente. Quantos anos deverá esperar para atingir o objetivo e retirar o dinheiro? Use $\log104=2{,}017$ e $\log2=0{,}3$.',
    [r'O montante após t anos é $M=50\,000(1{,}04)^t$. Para alcançar a meta, precisamos de $(1{,}04)^t\ge2$.',
     r'Com as aproximações fornecidas, $\log1{,}04=\log104-\log100=2{,}017-2=0{,}017$.',
     r'Como $\log1{,}04>0$, obtemos $t\ge\dfrac{0{,}3}{0{,}017}=\dfrac{300}{17}\approx17{,}65$ anos.',
     r'Os saques só ocorrem em anos completos: o primeiro inteiro que atende à condição é $t=18$.',
     r'Conferência com as potências completas: aos 17 anos, $M\approx97\,395{,}02$ reais; aos 18, $M\approx101\,290{,}83$ reais. A meta é ultrapassada no 18º ano.'],
    r'$18$ anos de espera.',r'O prazo calculado com logaritmos não é uma data permitida de saque. Arredonde para cima, até o primeiro ano que atinge a meta.',
    interest(50000,4,18,'anos',goal=100000,note='A linha da meta está em R$ 100.000. O laboratório usa potências completas; a resolução acima respeita os logaritmos aproximados dados na folha.'))

add('f06','Folha · 6','Duas taxas, o mesmo montante','Comparação de regimes',
    r'Um capital rende $20\%$ ao mês a juros compostos durante 3 meses. Se o mesmo capital fosse aplicado por igual prazo a juros simples, qual taxa mensal produziria exatamente o mesmo montante?',
    [r'Nos juros compostos, $M_c=C(1{,}20)^3=1{,}728C$.',
     r'Nos juros simples, $M_s=C(1+3i_s)$. Iguale os montantes: $1+3i_s=1{,}728$.',
     r'Logo $i_s=0{,}728/3=0{,}242666\ldots$. Em porcentagem, $i_s=24{,}2666\ldots\%$ ao mês.',
     r'Arredondando para uma casa decimal, temos $24{,}3\%$ ao mês, alternativa C. A igualdade exata usa a taxa antes do arredondamento.'],
    r'$24{,}2666\ldots\%$ ao mês; aproximadamente $24{,}3\%$ (C).',
    r'Juros compostos de 20% por 3 meses não totalizam 60%. Os fatores se multiplicam: o rendimento acumulado é 72,8%.',
    interest(1000,20,3,equivalent=True,note='Capital ilustrativo de R$ 1.000. A taxa simples é recalculada para igualar o montante composto no prazo total. Ela não é arredondada antes do cálculo.'),
    choices=[r'$22{,}4\%$ ao mês',r'$24{,}0\%$ ao mês',r'$24{,}3\%$ ao mês',r'$25{,}0\%$ ao mês',r'$27{,}6\%$ ao mês'],
    note='Na folha, as alternativas estão arredondadas. A taxa exata é 24,2666…% ao mês; 24,3% é a aproximação da alternativa C.')

add('c18','Caderno · 18','Montante não é a mesma coisa que juros','Juros simples',
    r'Uma aplicação de R$ 100,00 rende juros simples de $2\%$ ao mês. Determine:',
    [r'Use $M=C(1+it)$ e $J=Cit$, com $C=100$ e $i=0{,}02$ ao mês.',
     r'a) Em 4 meses: $M=100(1+0{,}02\cdot4)=100\cdot1{,}08=108$ reais.',
     r'b) Converta 2 anos em $2\cdot12=24$ meses. Então $J=100\cdot0{,}02\cdot24=48$ reais.',
     r'No item b, o montante seria $100+48=148$ reais, mas a pergunta pede apenas os juros.'],
    r'a) R$ 108,00; b) R$ 48,00 de juros.',r'Confira se o item pede M ou J. Também converta anos em meses antes de usar uma taxa mensal.',interest(100,2,24,mode='simple',landmarks=[4,24]),
    parts=[r'a) O montante ao final de 4 meses.',r'b) Os juros ao final de 2 anos.'])

add('c19','Caderno · 19','Descubra a taxa simples','Juros simples',
    r'Um investidor aplicou R$ 750,00 e obteve R$ 180,00 de juros ao fim de 6 meses. No regime de juros simples, determine a taxa mensal de rendimento.',
    [r'Os R$ 180,00 são juros: $J=180$, não o montante.',
     r'Na fórmula $J=Cit$, substitua: $180=750\cdot i\cdot6$.',
     r'Isole a taxa: $i=180/4\,500=0{,}04=4\%$ ao mês.',
     r'Conferência: os juros mensais são $750\cdot0{,}04=30$ reais; em 6 meses, $6\cdot30=180$ reais.'],
    r'$4\%$ ao mês.',r'A taxa encontrada é decimal. Multiplique por 100 para expressá-la em porcentagem.',interest(750,4,6,mode='simple'))

add('c23','Caderno · 23','Encontre o fator mensal','Juros compostos',
    r'Uma aplicação a juros compostos passou de R$ 500,00 para R$ 720,00 em 2 meses. Determine:',
    [r'a) Use $720=500(1+i)^2$, portanto $(1+i)^2=1{,}44$.',
     r'O fator de crescimento é positivo: $1+i=\sqrt{1{,}44}=1{,}20$. Logo $i=0{,}20=20\%$ ao mês.',
     r'b) Contando 3 meses desde a aplicação inicial, $M_3=500(1{,}20)^3=500\cdot1{,}728=864$ reais.',
     r'Os juros totais são $J_3=M_3-C=864-500=364$ reais.'],
    r'a) $20\%$ ao mês; b) R$ 364,00 de juros.',r'O fator 1,20 inclui o capital original. A taxa é 1,20 − 1 = 0,20. No item b, subtraia o capital do montante.',interest(500,20,3,landmarks=[2,3]),
    parts=[r'a) A taxa mensal de rendimento.',r'b) Os juros obtidos em 3 meses, contados desde o início da aplicação.'])

add('c24','Caderno · 24','O crescimento se acumula','Juros compostos',
    r'Um investimento de R$ 200.000,00 se valoriza à taxa constante de $10\%$ ao ano, a juros compostos. Determine o montante ao fim de:',
    [r'A fórmula é $M=C(1+i)^t=200\,000(1{,}10)^t$, com t em anos.',
     r'a) Em 1 ano: $M_1=200\,000\cdot1{,}10=220\,000$ reais.',
     r'b) Em 2 anos: $M_2=200\,000\cdot1{,}21=242\,000$ reais.',
     r'c) Usando a aproximação pedida: $M_{10}\approx200\,000\cdot2{,}6=520\,000$ reais.',
     r'A potência completa é $(1{,}10)^{10}\approx2{,}59374246$, que produz R$ 518.748,49. A diferença vem da aproximação fornecida, não de uma troca de fórmula.'],
    r'a) R$ 220.000,00; b) R$ 242.000,00; c) aproximadamente R$ 520.000,00, usando a aproximação dada.',
    r'Em juros compostos, a taxa incide sobre o saldo atualizado. O segundo aumento é de R$ 22.000, não de R$ 20.000.',
    interest(200000,10,10,'anos',landmarks=[1,2,10],note='O laboratório calcula a potência completa: em 10 anos, R$ 518.748,49. No item c, a resposta da lista usa explicitamente 1,1¹⁰ ≈ 2,6 e resulta em aproximadamente R$ 520.000.'),
    parts=[r'a) 1 ano.',r'b) 2 anos.',r'c) 10 anos, usando $(1{,}1)^{10}\approx2{,}6$.'])

add('t01','Treino · 01','Do percentual ao fator','Porcentagens',r'Um preço aumenta $35\%$. Por qual número o preço inicial deve ser multiplicado?',
    [r'Converta: $35\%=0{,}35$.',r'O preço final é $x+0{,}35x=1{,}35x$.',r'O fator é $1+0{,}35=1{,}35$.'],r'$1{,}35$.',r'Não confunda o acréscimo de 35% com o valor final de 135%.',percent(rate=35))

add('t02','Treino · 02','O fator que sobra','Porcentagens',r'Multiplicar um preço por $0{,}72$ equivale a qual desconto percentual?',
    [r'Permanecem $72\%$ do valor inicial.',r'A parte retirada é $100\%-72\%=28\%$.',r'Conferência: $1-0{,}28=0{,}72$.'],r'$28\%$.',r'72% é a parte mantida, não o desconto.',percent(factor=.72))

add('t03','Treino · 03','Aumentou e depois diminuiu','Porcentagens',r'Um produto de R$ 200,00 recebe um aumento de $20\%$ e, em seguida, um desconto de $15\%$. Qual é o preço final e a variação percentual em relação ao preço inicial?',
    [r'Após o aumento: $200\cdot1{,}20=240$ reais.',r'O desconto incide sobre 240: $240\cdot0{,}85=204$ reais.',r'O fator total é $1{,}20\cdot0{,}85=1{,}02$. Portanto, houve aumento de $2\%$.'],r'R$ 204,00; aumento de $2\%$.',r'Não subtraia 15 de 20: as duas porcentagens incidem sobre bases diferentes.',percent(200,rate=20,second=-15))

add('t04','Treino · 04','Parte de um grupo','Porcentagens',r'Em uma pesquisa, $25\%$ dos participantes preferem a opção A. Entre eles, $20\%$, correspondentes a 80 pessoas, têm menos de 18 anos. Quantas pessoas participaram da pesquisa?',
    [r'Os 80 jovens representam $0{,}20\cdot0{,}25=0{,}05$ do total.',r'Assim, $0{,}05N=80$.',r'Logo $N=80/0{,}05=1\,600$ pessoas. O grupo A tem 400 participantes, dos quais 80 são jovens.'],r'$1\,600$ pessoas.',r'20% do grupo A não são 20% de todos os participantes.',share(1600,25,20))

add('t05','Treino · 05','Volte ao preço original','Porcentagens',r'Após um desconto de $15\%$, um produto custa R$ 340,00. Qual era seu preço antes do desconto?',
    [r'O desconto deixa $85\%$ do preço original x: $0{,}85x=340$.',r'Divida pelo fator que restou: $x=340/0{,}85=400$.',r'Conferência: $15\%$ de 400 são 60 reais; $400-60=340$.'],r'R$ 400,00.',r'Acrescentar 15% a 340 não desfaz um desconto de 15% sobre 400.',percent(400,rate=-15))

add('t06','Treino · 06','Juros constantes a cada mês','Juros simples',r'Um capital de R$ 1.200,00 rende juros simples de $1{,}5\%$ ao mês durante 8 meses. Calcule os juros e o montante.',
    [r'Use $i=0{,}015$ e $t=8$ meses.',r'Os juros são $J=1\,200\cdot0{,}015\cdot8=144$ reais.',r'O montante é $M=C+J=1\,200+144=1\,344$ reais.'],r'$J=$ R$ 144,00; $M=$ R$ 1.344,00.',r'O montante inclui o capital; juros são apenas o rendimento.',interest(1200,1.5,8,mode='simple'))

add('t07','Treino · 07','Converta o prazo','Juros simples',r'R$ 800,00 são aplicados a juros simples de $2{,}5\%$ ao mês durante 1 ano e meio. Quanto se obtém de juros?',
    [r'Um ano e meio corresponde a $1{,}5\cdot12=18$ meses.',r'A taxa decimal mensal é $i=0{,}025$.',r'Portanto $J=800\cdot0{,}025\cdot18=360$ reais.'],r'R$ 360,00 de juros.',r'Com taxa mensal, o prazo usado na fórmula deve estar em meses.',interest(800,2.5,18,mode='simple'))

add('t08','Treino · 08','Qual foi a taxa?','Juros simples',r'Uma aplicação de R$ 1.500,00 produziu R$ 270,00 de juros simples em 6 meses. Qual foi a taxa mensal?',
    [r'Parta de $J=Cit$.',r'Isole $i=J/(Ct)=270/(1\,500\cdot6)=0{,}03$.',r'Convertendo para porcentagem: $0{,}03\cdot100=3\%$ ao mês.'],r'$3\%$ ao mês.',r'Divida os juros pelo produto capital × tempo, e não apenas pelo capital.',interest(1500,3,6,mode='simple'))

add('t09','Treino · 09','Recupere o capital','Juros simples',r'Uma aplicação a juros simples de $2\%$ ao mês alcançou R$ 2.600,00 após 15 meses. Qual era o capital inicial?',
    [r'Use $2\,600=C(1+0{,}02\cdot15)$.',r'O fator de crescimento simples é $1+0{,}30=1{,}30$.',r'Logo $C=2\,600/1{,}30=2\,000$ reais.'],r'R$ 2.000,00.',r'R$ 2.600,00 é o montante, não os juros.',interest(2000,2,15,mode='simple'))

add('t10','Treino · 10','Quanto tempo é necessário?','Juros simples',r'Em quanto tempo R$ 1.500,00 se transformam em R$ 1.800,00 a juros simples de $2\%$ ao mês?',
    [r'Os juros necessários são $J=1\,800-1\,500=300$ reais.',r'Use $300=1\,500\cdot0{,}02\cdot t=30t$.',r'Portanto $t=300/30=10$ meses.'],r'$10$ meses.',r'A taxa mensal faz com que a unidade do tempo encontrado seja mês.',interest(1500,2,10,mode='simple'))

add('t11','Treino · 11','Triplique o capital','Juros simples',r'Qual taxa anual de juros simples faz um capital triplicar em 30 meses?',
    [r'Converta o prazo: $t=30/12=2{,}5$ anos.',r'Para triplicar, $3C=C(1+2{,}5i)$. Cancelando C: $2=2{,}5i$.',r'Logo $i=2/2{,}5=0{,}80=80\%$ ao ano.'],r'$80\%$ ao ano.',r'Triplicar o montante exige juros iguais a duas vezes o capital, não a três vezes.',interest(1000,80,3,'anos',mode='simple',note='Capital ilustrativo de R$ 1.000. Use o ponto de 2,5 anos para conferir a triplicação. O horizonte do gráfico é de 3 anos.',specialTime=2.5))

add('t12','Treino · 12','Juros sobre juros','Juros compostos',r'R$ 1.000,00 são aplicados a juros compostos de $10\%$ ao mês por 3 meses. Determine o montante e os juros totais.',
    [r'O fator mensal é $1+0{,}10=1{,}10$.',r'O montante é $M=1\,000(1{,}10)^3=1\,000\cdot1{,}331=1\,331$ reais.',r'Os juros são $J=M-C=1\,331-1\,000=331$ reais.'],r'$M=$ R$ 1.331,00; $J=$ R$ 331,00.',r'Nos compostos, os acréscimos mensais são 100, 110 e 121 reais; eles não são iguais.',interest(1000,10,3))

add('t13','Treino · 13','Dois fatores sucessivos','Juros compostos',r'Um capital de R$ 800,00 rende $5\%$ ao mês a juros compostos. Qual é o montante após 2 meses?',
    [r'O fator mensal é $1{,}05$.',r'$M=800(1{,}05)^2=800\cdot1{,}1025$.',r'Logo $M=882$ reais. Os juros totais são 82 reais.'],r'R$ 882,00.',r'O aumento total é 10,25%, e não 10%.',interest(800,5,2))

add('t14','Treino · 14','Da raiz à taxa','Juros compostos',r'Uma aplicação passou de R$ 1.000,00 para R$ 1.210,00 em 2 meses, a juros compostos. Qual é a taxa mensal? Quanto renderá de juros ao completar 3 meses desde o início?',
    [r'$1\,210=1\,000(1+i)^2$, então $(1+i)^2=1{,}21$.',r'O fator positivo é $1+i=\sqrt{1{,}21}=1{,}10$, logo $i=10\%$ ao mês.',r'Em 3 meses, $M_3=1\,000(1{,}10)^3=1\,331$ reais.',r'Assim, $J_3=1\,331-1\,000=331$ reais.'],r'$10\%$ ao mês; R$ 331,00 de juros em 3 meses.',r'Os 3 meses são contados desde a aplicação inicial, não depois dos 2 meses já transcorridos.',interest(1000,10,3,landmarks=[2,3]))

add('t15','Treino · 15','Desfaça o crescimento composto','Juros compostos',r'Uma aplicação a juros compostos de $10\%$ ao mês chegou a R$ 1.331,00 em 3 meses. Qual foi o capital inicial?',
    [r'$1\,331=C(1{,}10)^3$.',r'Calcule o fator acumulado: $(1{,}10)^3=1{,}331$.',r'Logo $C=1\,331/1{,}331=1\,000$ reais.'],r'R$ 1.000,00.',r'Para voltar ao capital, divida pelo fator acumulado; não desconte 30% do montante.',interest(1000,10,3))

add('t16','Treino · 16','Uma meta com saques anuais','Juros compostos',r'R$ 1.000,00 rendem $10\%$ ao ano a juros compostos. O saque só ocorre no fim de cada ano. Qual é o primeiro ano em que será possível retirar pelo menos R$ 1.500,00? Use $\log1{,}5=0{,}1761$ e $\log1{,}1=0{,}0414$.',
    [r'A condição é $1\,000(1{,}1)^t\ge1\,500$, ou $(1{,}1)^t\ge1{,}5$.',r'Pelos logaritmos dados, $t\ge0{,}1761/0{,}0414\approx4{,}25$ anos.',r'O primeiro ano completo permitido é o 5º.',r'Conferência: $M_4=1\,464{,}10$ reais e $M_5=1\,610{,}51$ reais.'],r'No fim do $5^\circ$ ano.',r'Arredondar o prazo para 4 anos deixaria o montante abaixo da meta.',interest(1000,10,5,'anos',goal=1500))

add('t17','Treino · 17','Uma sequência de montantes','Juros compostos',r'R$ 5.000,00 são aplicados a $8\%$ ao ano, a juros compostos. Calcule os montantes após 1, 2 e 3 anos.',
    [r'Use $M_t=5\,000(1{,}08)^t$.',r'$M_1=5\,000\cdot1{,}08=5\,400$ reais.',r'$M_2=5\,400\cdot1{,}08=5\,832$ reais.',r'$M_3=5\,832\cdot1{,}08=6\,298{,}56$ reais.'],r'1 ano: R$ 5.400,00; 2 anos: R$ 5.832,00; 3 anos: R$ 6.298,56.',r'O fator 1,08 deve multiplicar o saldo do ano anterior em cada etapa.',interest(5000,8,3,'anos',landmarks=[1,2,3]))

add('t18','Treino · 18','Taxa simples equivalente','Comparação de regimes',r'Qual taxa mensal de juros simples produz, em 2 meses, o mesmo montante que juros compostos de $10\%$ ao mês sobre o mesmo capital?',
    [r'O fator composto em 2 meses é $(1{,}10)^2=1{,}21$.',r'Iguale ao fator simples: $1+2i_s=1{,}21$.',r'Logo $i_s=0{,}21/2=0{,}105=10{,}5\%$ ao mês.'],r'$10{,}5\%$ ao mês.',r'A equivalência vale para o prazo escolhido. Se o prazo mudar, a taxa simples equivalente também muda.',interest(1000,10,2,equivalent=True,note='Capital ilustrativo de R$ 1.000. Os regimes coincidem no fim do prazo; os saldos intermediários podem ser diferentes.'))

add('t19','Treino · 19','Compare os dois regimes','Comparação de regimes',r'R$ 2.000,00 são aplicados por 4 meses à taxa de $5\%$ ao mês. Compare os montantes a juros simples e compostos e calcule a diferença entre eles.',
    [r'Juros simples: $M_s=2\,000(1+0{,}05\cdot4)=2\,400$ reais.',r'Juros compostos: $M_c=2\,000(1{,}05)^4=2\,431{,}0125$ reais.',r'A diferença é $M_c-M_s=31{,}0125$ reais. Arredondando apenas no final, os montantes são R$ 2.400,00 e R$ 2.431,01; a diferença é R$ 31,01.'],r'Simples: R$ 2.400,00; compostos: R$ 2.431,01; diferença: R$ 31,01.',r'Com a mesma taxa e capital, os regimes coincidem no primeiro período; a diferença surge a partir do segundo.',interest(2000,5,4,compare=True))

add('t20','Treino · 20','O desconto que desfaz um aumento','Porcentagens',r'Um produto de R$ 800,00 recebe aumento de $25\%$. Qual desconto percentual sobre o novo preço faz o produto voltar aos R$ 800,00 iniciais?',
    [r'Após o aumento, o preço é $800\cdot1{,}25=1\,000$ reais.',r'O desconto deve retirar $1\,000-800=200$ reais do novo preço.',r'Assim, $d=200/1\,000=0{,}20=20\%$.',r'Conferência pelos fatores: $1{,}25\cdot(1-0{,}20)=1{,}25\cdot0{,}80=1$.'],r'$20\%$.',r'Um aumento de 25% e um desconto de 25% não se anulam, pois usam bases diferentes.',percent(800,rate=25,second=-20))

assert len(QUESTIONS) == 30
