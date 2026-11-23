# Matemática financeira — lista e 20 treinos

Saída: `matematica-financeira.html`, autocontida, com KaTeX e fontes incorporados. Sem serviços externos, fotos ou dados pessoais. Progresso salvo localmente no navegador.

```sh
python3 tools/matematica-financeira/build.py
node tools/matematica-financeira/validate.cjs
```

O build exige somente Python 3 e Node.js. Reutiliza os recursos KaTeX existentes em `index.html` e o CSS base do caderno de logaritmos. Acrescenta um link de navegação aos cadernos existentes, sem alterar seu conteúdo.

`data.py` contém 10 exercícios das fotos de 23/11/2026 (folha 1–6 e caderno 18, 19, 23, 24), com todos os subitens, mais 20 novos exercícios. `content.json` é gerado. `lab.js` reúne modelos puros e renderizadores SVG; a página estática e a interatividade usam esses mesmos modelos. `app.js` controla filtros, progresso, exploração, reprodução e impressão.

## Critérios matemáticos

- Sem aportes, saques intermediários, tributos ou tarifas, conforme os modelos dos enunciados.
- Taxas convertidas para decimais e prazos na unidade da taxa. Na folha 4, o laboratório usa a taxa mensal simples equivalente de 6,25%; a resposta pedida é 75% ao ano.
- Folha 5: usar os logaritmos fornecidos leva a 17,65 anos aproximadamente, mas saques anuais exigem 18 anos. O gráfico calcula potências completas e mostra a meta.
- Folha 6: taxa simples exata 24,2666…% ao mês; a alternativa C, 24,3%, é arredondada. A comparação usa a taxa sem arredondamento intermediário.
- Caderno 24(c): R$ 520.000 é o resultado aproximado solicitado, com 1,1¹⁰ ≈ 2,6. O laboratório mostra a potência completa: R$ 518.748,49.
- Treino 11: a resolução trabalha com 2,5 anos. A visualização de juros simples permite passos de meio ano e inicia no ponto de 2,5 anos; o horizonte é de 3 anos.
- Valores monetários são exibidos em centavos, sem arredondamentos intermediários. Os gráficos de juros compostos ligam pontos de fechamento de cada período; os segmentos servem como guia visual.
- Capital ilustrativo é identificado quando o enunciado fornece apenas relações ou taxas.
- Impressão com soluções restaura os dados iniciais e o prazo de referência; depois restaura a exploração anterior. Não há reprodução automática, e movimento reduzido usa avanços discretos.

Validação: todos os resultados das fotos e dos treinos, fórmulas KaTeX, percentuais encadeados, equivalência de regimes, saques inteiros, taxas zero, limites dos controles, links e navegação. Verificação no navegador cobre controles, filtros, persistência, reprodução, impressão e telas pequenas.
