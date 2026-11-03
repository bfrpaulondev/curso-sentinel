# -*- coding: utf-8 -*-
B="#1e66f5"; G="#2f9e44"; R="#e03131"; O="#f08c00"; P="#7048e8"; K="#343a40"
def run(f, say, shot=True): return {"say": say, "act": [["term", f"./kql.py -f {f}"]], "shot": shot}
MOD = {
 "id": "m2", "num": 2, "titulo": "Módulo 2 — KQL na prática",
 "resumo": "Do where ao render, sempre caçando os ataques que aconteceram na Loja Pixel na madrugada de 21/10/2026.",
 "minimo": 70,
 "aulas": [
 {"id": "2.1", "titulo": "where, project, take e sort",
  "objetivo": "Filtrar linhas, escolher colunas e ordenar — a base de toda consulta.",
  "termos": [["Pipe ( | )", "A esteira da fábrica: o resultado de um passo entra no próximo."], ["where", "O WHERE do SQL: filtra linhas."], ["project", "O SELECT do SQL: escolhe e renomeia colunas."]],
  "diagrama": [
   {"say": "Se você vem do SQL, a boa notícia é que o KQL pensa parecido, só que lê de cima para baixo, como uma esteira. Começa sempre pela tabela.",
    "els": [["db", 100, 400, 300, 240, "SigninLogs\n933 linhas", G]]},
   {"say": "O where é o filtro: só passam as linhas com falha. O project escolhe as colunas, como o SELECT. O sort ordena e o take pega só algumas linhas, como o TOP.",
    "els": [["arrow", 400, 520, 520, 520, ""], ["box", 520, 450, 300, 140, "where\n(filtra linhas)", B], ["arrow", 820, 520, 920, 520, ""], ["box", 920, 450, 300, 140, "project\n(colunas)", P], ["arrow", 1220, 520, 1320, 520, ""], ["box", 1320, 450, 240, 140, "sort", O], ["arrow", 1560, 520, 1640, 520, ""], ["box", 1640, 450, 200, 140, "take 5", R]]},
   {"say": "Uma dica de quem trabalha com SQL: no KQL, comparação de texto com dois iguais diferencia maiúsculas. Se quiser ignorar, use o til igual.",
    "els": [["text", 960, 820, "==  diferencia maiúsculas     =~  ignora maiúsculas", 44, K]]}
  ],
  "demo": [
   {"say": "Abro a primeira consulta do módulo.", "act": [["open", "labs/m2/2.1_where_project.kql"]], "shot": True},
   {"say": "Tabela SigninLogs, filtro de falhas no Azure Portal: ResultType diferente de zero significa falha. Depois escolho cinco colunas, ordeno pela hora e pego as cinco primeiras.", "act": [["wait", 2]]},
   run("labs/m2/2.1_where_project.kql", "Rodando no Kusto. Cinco linhas, cada uma com o usuário, o IP, o país e o motivo da falha."),
   {"say": "Agora um teste rápido direto no terminal: quantas falhas no total? Basta trocar o fim da esteira por count.", "act": [["term", "./kql.py 'SigninLogs | where ResultType != \"0\" | count'"]], "shot": True},
   {"say": "Sessenta e oito falhas num dia. Parece pouco, mas guarde esse número: a maioria delas veio de um lugar só, e vamos descobrir de onde.", "act": [["wait", 1]]}
  ],
  "lab": [
   {"txt": "Rode a consulta da aula.", "cmd": "./kql.py -f labs/m2/2.1_where_project.kql", "run": True},
   {"txt": "Conte todas as falhas.", "cmd": "./kql.py 'SigninLogs | where ResultType != \"0\" | count'", "run": True}
  ],
  "desafio": "Sem guia: liste os 10 logins com SUCESSO mais recentes fora do Brasil, mostrando só hora, usuário e país.",
  "quiz": [
   {"q": "Qual operador KQL equivale ao SELECT do SQL?", "opts": ["where", "project", "take", "extend"], "a": 1, "exp": "project escolhe (e pode renomear) colunas."},
   {"q": "Você quer comparar o país ignorando maiúsculas. Qual operador?", "opts": ["==", "=~", "has", "!="], "a": 1, "exp": "=~ é a igualdade sem diferenciar maiúsculas."},
   {"q": "O que faz 'take 5'?", "opts": ["Pega 5 linhas quaisquer", "Pega as 5 maiores", "Ordena por 5 colunas", "Agrupa em 5"], "a": 0, "exp": "take devolve N linhas sem garantia de ordem; para 'as maiores' use top ou sort antes."},
   {"q": "Em SigninLogs, ResultType == \"0\" significa…", "opts": ["falha", "sucesso", "MFA pendente", "conta bloqueada"], "a": 1, "exp": "0 é sucesso; qualquer outro código é um tipo de falha."}
  ]},
 {"id": "2.2", "titulo": "summarize, count e bin",
  "objetivo": "Agrupar eventos no tempo para enxergar picos — o GROUP BY do KQL.",
  "termos": [["summarize", "O GROUP BY: agrega linhas."], ["bin()", "Arredonda o tempo em 'baldes' (ex.: 1 hora)."], ["dcount()", "Conta valores distintos (COUNT DISTINCT)."]],
  "diagrama": [
   {"say": "Eventos soltos não contam história. Precisamos agrupá-los. Imagine baldes de uma hora em fila.",
    "els": [["box", 160, 640, 220, 140, "00h", B], ["box", 420, 640, 220, 140, "01h", B], ["box", 680, 640, 220, 140, "02h", R], ["box", 940, 640, 220, 140, "03h", B], ["box", 1200, 640, 220, 140, "04h", B]]},
   {"say": "A função bin arredonda cada hora para o seu balde, e o summarize conta quantos eventos caíram em cada um. O balde das duas da manhã transborda: trinta e sete falhas.",
    "els": [["box", 680, 300, 220, 320, "37", R], ["box", 160, 560, 220, 60, "1", B], ["box", 420, 560, 220, 60, "2", B], ["box", 940, 560, 220, 60, "3", B], ["text", 1550, 460, "summarize count()\nby bin(TimeGenerated, 1h)", 40, K]]},
   {"say": "É exatamente o mesmo raciocínio do GROUP BY com DATEPART do SQL, só que bem mais curto.",
    "els": [["text", 960, 950, "SQL: GROUP BY DATEPART(hour, …)   ≈   KQL: by bin(TimeGenerated, 1h)", 38, K]]}
  ],
  "demo": [
   {"say": "Abro a consulta da aula dois ponto dois.", "act": [["open", "labs/m2/2.2_summarize_bin.kql"]], "shot": True},
   run("labs/m2/2.2_summarize_bin.kql", "Rodando. O primeiro lugar é dia vinte e um, às duas da manhã, com trinta e sete falhas. Ninguém trabalha nesse horário na Loja Pixel."),
   {"say": "Vamos aprofundar: nesse balde, quantos IPs e quantas contas diferentes? O dcount conta valores distintos.", "act": [["term", "./kql.py 'SigninLogs | where ResultType != \"0\" and TimeGenerated between (datetime(2026-10-21 02:00) .. 1h) | summarize Falhas=count(), Contas=dcount(UserPrincipalName) by IPAddress | top 3 by Falhas'"]], "shot": True},
   {"say": "Um IP só, 198.51.100.23, errando senha em dezesseis contas. Esse padrão tem nome: password spray. É o nosso primeiro suspeito.", "act": [["wait", 1]]}
  ],
  "lab": [
   {"txt": "Falhas por hora.", "cmd": "./kql.py -f labs/m2/2.2_summarize_bin.kql", "run": True},
   {"txt": "Quem causou o pico?", "cmd": "./kql.py 'SigninLogs | where ResultType != \"0\" and TimeGenerated between (datetime(2026-10-21 02:00) .. 1h) | summarize Falhas=count(), Contas=dcount(UserPrincipalName) by IPAddress | top 3 by Falhas'", "run": True}
  ],
  "desafio": "Sem guia: na tabela LojaApi_CL, encontre a janela de 5 minutos com mais respostas 401 na rota /api/login.",
  "quiz": [
   {"q": "Qual é o equivalente KQL do GROUP BY?", "opts": ["project", "summarize … by", "extend", "join"], "a": 1, "exp": "summarize agrega; o by define os grupos."},
   {"q": "bin(TimeGenerated, 1h) faz o quê?", "opts": ["Filtra a última hora", "Arredonda o tempo para baldes de 1 hora", "Converte para UTC", "Soma 1 hora"], "a": 1, "exp": "bin arredonda o valor para baixo, ao múltiplo do tamanho indicado."},
   {"q": "Um IP falhou em 16 contas diferentes. Que função mostrou isso?", "opts": ["count()", "dcount(UserPrincipalName)", "max()", "sum()"], "a": 1, "exp": "dcount conta valores distintos."},
   {"q": "Muitas contas, poucas tentativas por conta, um IP. Isso sugere…", "opts": ["força bruta numa conta", "password spray", "erro de MFA", "tráfego normal"], "a": 1, "exp": "Password spray tenta poucas senhas comuns em muitas contas."}
  ]},
 {"id": "2.3", "titulo": "join, union e let",
  "objetivo": "Cruzar tabelas e dar nome a pedaços da consulta — de suspeita a evidência.",
  "termos": [["let", "Dá um nome a uma expressão — como uma CTE (WITH) do SQL."], ["join", "Junta duas tabelas por uma coluna comum."], ["union", "Empilha tabelas (como UNION ALL)."]],
  "diagrama": [
   {"say": "Suspeita não é prova. Temos de um lado os IPs que erraram em muitas contas.",
    "els": [["box", 120, 300, 480, 200, "let Falhas =\nIPs com ≥5 contas", R]]},
   {"say": "Do outro, os logins que deram certo. O let dá nome a cada conjunto, como um WITH no SQL.",
    "els": [["box", 120, 600, 480, 200, "let Sucessos =\nlogins OK", G]]},
   {"say": "O join cruza os dois pelo IP. O que sobra é a pior notícia possível: o atacante acertou a senha de alguém.",
    "els": [["arrow", 600, 400, 900, 520, ""], ["arrow", 600, 700, 900, 560, ""], ["box", 900, 440, 340, 180, "join\non IPAddress", P], ["arrow", 1240, 530, 1420, 530, ""], ["box", 1420, 430, 420, 200, "joao.pereira\n198.51.100.23", R]]},
   {"say": "E o union empilha fontes diferentes numa linha do tempo só: Entra ID, API e SSH lado a lado.",
    "els": [["text", 960, 950, "union = empilhar (UNION ALL)     join = cruzar (INNER JOIN)", 40, K]]}
  ],
  "demo": [
   {"say": "Aqui está a consulta com dois let e um join.", "act": [["open", "labs/m2/2.3_join_let.kql"]], "shot": True},
   run("labs/m2/2.3_join_let.kql", "Executando. Uma linha: o IP 198.51.100.23 atacou dezesseis contas e conseguiu entrar como joao ponto pereira, às duas e quarenta e quatro."),
   {"say": "Agora o union. Três fontes, um só resultado.", "act": [["open", "labs/m2/2.3b_union.kql"]]},
   run("labs/m2/2.3b_union.kql", "Três atacantes diferentes na mesma madrugada: cento e trinta e oito falhas na API vindas de 203.0.113.77, trinta e cinco no SSH, e as trinta e duas do password spray."),
   {"say": "Esses três números vão virar regras de detecção no Módulo 4.", "act": [["wait", 1]]}
  ],
  "lab": [
   {"txt": "Cruze falhas e sucessos.", "cmd": "./kql.py -f labs/m2/2.3_join_let.kql", "run": True},
   {"txt": "Linha do tempo única com union.", "cmd": "./kql.py -f labs/m2/2.3b_union.kql", "run": True}
  ],
  "desafio": "Sem guia: troque o join para kind=leftanti e explique, com as suas palavras, o que o resultado significa.",
  "quiz": [
   {"q": "let no KQL se parece com o quê no SQL?", "opts": ["WITH (CTE)", "DELETE", "INDEX", "TRIGGER"], "a": 0, "exp": "let nomeia uma expressão para reuso, como uma CTE."},
   {"q": "Você quer empilhar falhas de 3 tabelas. Qual operador?", "opts": ["join", "union", "lookup", "evaluate"], "a": 1, "exp": "union concatena linhas de várias tabelas."},
   {"q": "Qual join devolve só as linhas da esquerda SEM par na direita?", "opts": ["inner", "leftouter", "leftanti", "fullouter"], "a": 2, "exp": "leftanti devolve o que existe só do lado esquerdo."},
   {"q": "O join do lab mostrou um sucesso após o spray. Qual a ação?", "opts": ["Ignorar", "Tratar a conta como comprometida: revogar sessões e trocar senha", "Apagar os logs", "Bloquear o país inteiro para sempre"], "a": 1, "exp": "Um sucesso vindo do IP atacante indica conta comprometida."}
  ]},
 {"id": "2.4", "titulo": "parse, extract, parse_json e mv-expand",
  "objetivo": "Tirar informação de texto livre e de JSON — o dia a dia com logs reais.",
  "termos": [["parse", "Recorta um texto usando pedaços fixos como molde."], ["extract()", "Tira um pedaço do texto com uma expressão regular."], ["mv-expand", "Transforma uma lista numa linha por item."]],
  "diagrama": [
   {"say": "Logs de Linux são texto corrido. Olhe esta mensagem do SSH.",
    "els": [["box", 100, 220, 1720, 130, "Failed password for invalid user admin from 192.0.2.150 port 52144 ssh2", K]]},
   {"say": "O parse funciona como um molde de recorte: as partes fixas ficam, e os buracos viram colunas. Usuário, IP e porta.",
    "els": [["arrow", 960, 350, 960, 440, "parse … with"], ["box", 260, 440, 400, 120, "Usuario = admin", B], ["box", 760, 440, 400, 120, "IP = 192.0.2.150", R], ["box", 1260, 440, 400, 120, "Porta = 52144", B]]},
   {"say": "Já a API grava JSON. O parse_json abre o objeto, e o mv-expand transforma a lista de tags em uma linha por tag.",
    "els": [["box", 100, 700, 760, 160, "Properties = {\"tags\":[\"web\",\"promo\"]}", P], ["arrow", 860, 780, 1080, 780, "mv-expand"], ["box", 1080, 650, 300, 100, "web", G], ["box", 1080, 800, 300, 100, "promo", G]]}
  ],
  "demo": [
   {"say": "Abrindo a consulta de parse.", "act": [["open", "labs/m2/2.4_parse.kql"]], "shot": True},
   run("labs/m2/2.4_parse.kql", "Resultado: o usuário admin, do IP 192.0.2.150, trinta e cinco tentativas. Força bruta clássica no SSH."),
   {"say": "Agora o JSON da API.", "act": [["open", "labs/m2/2.4b_json_mvexpand.kql"]]},
   run("labs/m2/2.4b_json_mvexpand.kql", "Cada pedido tem uma lista de tags. Depois do mv-expand, contamos pedidos por tag: web, mobile, promo e black-friday."),
   {"say": "Um detalhe que pega muita gente: depois do parse_json, converta o valor com tostring antes de comparar. O valor é dinâmico.", "act": [["wait", 1]]}
  ],
  "lab": [
   {"txt": "Recorte a mensagem do SSH.", "cmd": "./kql.py -f labs/m2/2.4_parse.kql", "run": True},
   {"txt": "Abra o JSON da API.", "cmd": "./kql.py -f labs/m2/2.4b_json_mvexpand.kql", "run": True}
  ],
  "desafio": "Sem guia: usando parse_json(Properties).login, descubra qual login foi usado com sucesso pelo IP 203.0.113.77.",
  "quiz": [
   {"q": "Mensagem: 'user=ana ip=10.0.0.5'. Qual operador recorta com um molde de texto fixo?", "opts": ["parse", "summarize", "union", "render"], "a": 0, "exp": "parse usa trechos fixos para extrair os pedaços variáveis."},
   {"q": "Uma coluna tem a lista [\"a\",\"b\",\"c\"]. Como gerar uma linha por item?", "opts": ["mv-expand", "project", "take", "bin"], "a": 0, "exp": "mv-expand expande arrays em várias linhas."},
   {"q": "Por que usar tostring() depois de parse_json?", "opts": ["Para ficar mais rápido", "Porque o valor é dynamic e comparações/agrupamentos funcionam melhor como string", "Porque é obrigatório sempre", "Para criptografar"], "a": 1, "exp": "Converter o dynamic para um tipo escalar evita comparações inesperadas."}
  ]},
 {"id": "2.5", "titulo": "Funções, desempenho e erros comuns",
  "objetivo": "Reutilizar lógica com funções e escrever consultas rápidas e baratas.",
  "termos": [["Função (let)", "Uma 'stored procedure' leve, definida na própria consulta."], ["invoke", "Chama uma função passando a tabela da esteira."], ["Filtro de tempo", "Limitar TimeGenerated primeiro é a otimização nº 1."]],
  "diagrama": [
   {"say": "Três hábitos que deixam a consulta rápida. Primeiro: filtre o tempo logo no começo. É como procurar só na gaveta de outubro em vez do arquivo inteiro.",
    "els": [["box", 120, 260, 520, 160, "1. TimeGenerated primeiro", G]]},
   {"say": "Segundo: reduza as colunas cedo, com project. Menos coisa na esteira, menos trabalho.",
    "els": [["box", 700, 260, 520, 160, "2. project cedo", G]]},
   {"say": "Terceiro: prefira has a contains. O has procura palavras inteiras usando o índice, o contains varre o texto letra por letra.",
    "els": [["box", 1280, 260, 520, 160, "3. has > contains", G]]},
   {"say": "E quando a lógica se repete, vira função. Definimos uma vez com let, com parâmetros, e chamamos com invoke.",
    "els": [["box", 400, 600, 1120, 220, "let FalhasPorIp = (tabela, limiar) { … };\nSigninLogs | invoke FalhasPorIp(10)", P]]}
  ],
  "demo": [
   {"say": "Esta é a função FalhasPorIp, com dois parâmetros: a tabela e o limiar.", "act": [["open", "labs/m2/2.5_funcoes.kql"]], "shot": True},
   run("labs/m2/2.5_funcoes.kql", "Com limiar dez, só o IP do password spray passa."),
   {"say": "Agora o erro mais comum de todos: nome de coluna com a maiúscula errada. No KQL, os nomes de colunas diferenciam maiúsculas.", "act": [["term", "./kql.py 'SigninLogs | where resulttype != \"0\" | count'"]], "shot": True},
   {"say": "A mensagem diz exatamente o problema: falhou ao resolver a coluna resulttype. Lendo o erro com calma, ele quase sempre aponta o culpado. Corrigindo para ResultType, com R e T maiúsculos, tudo volta a funcionar.", "act": [["term", "./kql.py 'SigninLogs | where ResultType != \"0\" | count'"]]}
  ],
  "lab": [
   {"txt": "Use a função com invoke.", "cmd": "./kql.py -f labs/m2/2.5_funcoes.kql", "run": True},
   {"txt": "Provoque o erro de nome de coluna e leia a mensagem.", "cmd": "./kql.py 'SigninLogs | where resulttype != \"0\" | count'", "run": True}
  ],
  "desafio": "Sem guia: crie uma função FalhasApi(limiar) para a LojaApi_CL (StatusCode 401 por ClientIP) e use-a com limiar 50.",
  "quiz": [
   {"q": "Qual é a otimização mais importante numa consulta KQL?", "opts": ["Usar render", "Filtrar TimeGenerated logo no início", "Usar contains", "Ordenar tudo"], "a": 1, "exp": "Limitar o tempo reduz drasticamente os dados lidos."},
   {"q": "has ou contains para procurar a palavra 'Failed'?", "opts": ["contains, é mais rápido", "has, usa o índice de termos", "tanto faz", "nenhum"], "a": 1, "exp": "has procura termos inteiros com índice; contains varre substrings."},
   {"q": "Erro SEM0100: 'Failed to resolve column named resulttype'. O motivo?", "opts": ["Tabela vazia", "Nome de coluna com maiúscula errada: o certo é ResultType", "Falta take", "O Kusto está fora"], "a": 1, "exp": "No KQL, nomes de colunas diferenciam maiúsculas."},
   {"q": "Como chamar uma função tabular sobre a tabela da esteira?", "opts": ["invoke", "call", "exec", "run"], "a": 0, "exp": "invoke passa a tabela de entrada como primeiro argumento da função."}
  ]},
 {"id": "2.6", "titulo": "render: gráficos",
  "objetivo": "Transformar o resultado em gráfico para enxergar o ataque num relance.",
  "termos": [["render", "Pede para a ferramenta desenhar o resultado como gráfico."], ["timechart", "Gráfico de linha com o tempo no eixo X."], ["série", "Cada valor de uma coluna de texto vira uma linha do gráfico."]],
  "diagrama": [
   {"say": "O render é o último passo da esteira. Ele não muda os dados, só diz como desenhar.",
    "els": [["box", 120, 420, 520, 180, "summarize count()\nby bin(30m), Status", B], ["arrow", 640, 510, 820, 510, ""], ["box", 820, 420, 380, 180, "render\ntimechart", P]]},
   {"say": "Cada status vira uma série. A linha do quatrocentos e um dá um salto às três da manhã: é o credential stuffing contra a API.",
    "els": [["arrow", 1200, 510, 1340, 510, ""], ["box", 1340, 300, 480, 420, "", K], ["text", 1580, 360, "401 ↑ 03:00", 40, R], ["text", 1580, 620, "200 ~ estável", 36, G]]},
   {"say": "Importante: quem desenha é a ferramenta cliente, como o Log Analytics ou o Kusto Explorer. No nosso terminal, o render devolve a tabela, e no site do curso o gráfico é desenhado com esses mesmos dados reais.",
    "els": [["text", 960, 900, "render = instrução de desenho para o cliente", 40, K]]}
  ],
  "demo": [
   {"say": "A consulta da aula.", "act": [["open", "labs/m2/2.6_render.kql"]], "shot": True},
   run("labs/m2/2.6_render.kql", "No terminal, recebemos a tabela que alimenta o gráfico: cento e setenta e uma linhas, uma por balde de meia hora e status."),
   {"say": "Vou filtrar só o balde das três da manhã para ver o salto do quatrocentos e um com os olhos.", "act": [["term", "./kql.py 'LojaApi_CL | summarize Pedidos=count() by bin(TimeGenerated, 30m), Status=tostring(StatusCode) | where TimeGenerated == datetime(2026-10-21 03:00) | sort by Pedidos desc'"]], "shot": True},
   {"say": "Cento e trinta e oito quatrocentos e uns em meia hora. No gráfico do site, essa é a montanha vermelha. Com isso fechamos o KQL. Hora do teste do módulo.", "act": [["wait", 1]]}
  ],
  "lab": [
   {"txt": "Gere os dados do gráfico.", "cmd": "./kql.py -f labs/m2/2.6_render.kql --max 8", "run": True},
   {"txt": "Olhe o balde das 03:00.", "cmd": "./kql.py 'LojaApi_CL | summarize Pedidos=count() by bin(TimeGenerated, 30m), Status=tostring(StatusCode) | where TimeGenerated == datetime(2026-10-21 03:00) | sort by Pedidos desc'", "run": True}
  ],
  "desafio": "Sem guia: faça um columnchart de falhas de login do SigninLogs por país.",
  "quiz": [
   {"q": "O render altera os dados do resultado?", "opts": ["Sim", "Não, só indica como desenhar", "Só em timechart", "Só no Sentinel"], "a": 1, "exp": "render é uma dica de visualização para o cliente."},
   {"q": "Qual gráfico usa o tempo no eixo X?", "opts": ["piechart", "timechart", "table", "card"], "a": 1, "exp": "timechart é o gráfico de linhas temporal."},
   {"q": "Onde deve ficar o render na consulta?", "opts": ["No início", "No fim da esteira", "Dentro do where", "Em qualquer lugar"], "a": 1, "exp": "render é sempre o último operador."}
  ]}
 ],
 "teste": [
  {"q": "Você precisa só das colunas hora, usuário e IP de SigninLogs. Qual operador?", "opts": ["project", "summarize", "extend", "union"], "a": 0, "exp": "project escolhe colunas."},
  {"q": "Quer saber quantas falhas por hora. Qual combinação?", "opts": ["take + sort", "summarize count() by bin(TimeGenerated, 1h)", "project + where", "join + union"], "a": 1, "exp": "summarize com bin agrupa no tempo."},
  {"q": "Um IP errou em 16 contas diferentes. Qual função mede isso?", "opts": ["count()", "dcount(UserPrincipalName)", "sum()", "avg()"], "a": 1, "exp": "dcount conta distintos."},
  {"q": "Você tem falhas na API, no SSH e no Entra ID e quer uma lista única. Use…", "opts": ["join", "union", "lookup", "parse"], "a": 1, "exp": "union empilha tabelas."},
  {"q": "Quer os IPs do spray que TAMBÉM tiveram login com sucesso. Use…", "opts": ["union", "join kind=inner", "join kind=leftanti", "take"], "a": 1, "exp": "inner join devolve só o que existe nos dois lados."},
  {"q": "Mensagem do SSH em texto livre: como tirar o IP com regex?", "opts": ["extract()", "bin()", "dcount()", "render"], "a": 0, "exp": "extract aplica uma expressão regular."},
  {"q": "Properties.tags é uma lista. Para contar por tag você usa…", "opts": ["mv-expand", "project-away", "top", "distinct"], "a": 0, "exp": "mv-expand gera uma linha por item."},
  {"q": "A consulta está lenta numa tabela de 1 bilhão de linhas. Primeiro passo?", "opts": ["Adicionar render", "Filtrar TimeGenerated no início", "Trocar has por contains", "Remover o where"], "a": 1, "exp": "Filtrar o tempo é a otimização número 1."},
  {"q": "Qual é mais eficiente para procurar a palavra 'Failed'?", "opts": ["contains", "has", "matches regex", "=~"], "a": 1, "exp": "has usa o índice de termos."},
  {"q": "A consulta com 'where resulttype != \"0\"' falha com SEM0100. A correção é…", "opts": ["where ResultType != \"0\"", "tolong(0)", "remover o where", "usar take"], "a": 0, "exp": "Nomes de colunas diferenciam maiúsculas."},
  {"q": "Você repete a mesma lógica em 5 consultas. Melhor prática?", "opts": ["Copiar e colar", "Criar uma função (let ou salva no workspace)", "Usar render", "Usar union"], "a": 1, "exp": "Funções reutilizam lógica com parâmetros."},
  {"q": "take 10 garante as 10 linhas mais recentes?", "opts": ["Sim", "Não; use top 10 by TimeGenerated desc", "Só com render", "Só no Sentinel"], "a": 1, "exp": "take não garante ordem."},
  {"q": "Quer gráfico de linha de pedidos ao longo do tempo. Use…", "opts": ["render piechart", "render timechart", "render table", "render card"], "a": 1, "exp": "timechart."},
  {"q": "Um valor de parse_json precisa ser comparado como texto. Faça…", "opts": ["tostring(P.campo)", "toint()", "nada", "bin()"], "a": 0, "exp": "Converter de dynamic para string."},
  {"q": "Você quer as falhas de 'Azure Portal' ignorando maiúsculas no nome do app. Use…", "opts": ["==", "=~", "!=", "has_cs"], "a": 1, "exp": "=~ ignora maiúsculas."},
  {"q": "Em SigninLogs, qual código indica sucesso?", "opts": ["50126", "0", "401", "200"], "a": 1, "exp": "ResultType 0 = sucesso."}
 ],
 "pratico": {"titulo": "Teste prático: 10 consultas corrigidas automaticamente", "txt": "Resolva as 10 tarefas no dataset fixo da Loja Pixel. Para cada uma, rode `./kql.py -f q01.kql --csv saida.csv` e cole o CSV aqui. O resultado é comparado com o CSV esperado, gerado numa execução real do Kusto. Mínimo: 7 de 10. No repositório, `python3 grader/corrigir.py` faz a mesma correção rodando as suas consultas.", "kql": True}
}
