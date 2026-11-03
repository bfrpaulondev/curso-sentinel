# -*- coding: utf-8 -*-
B="#1e66f5"; G="#2f9e44"; R="#e03131"; O="#f08c00"; P="#7048e8"; K="#343a40"
AVISO = "O motor_regras_local.py é um SIMULADOR didático: valida o YAML no formato do repositório Azure-Sentinel, roda a query no Kusto real e aplica limiar e agrupamento. Ele NÃO é o Microsoft Sentinel."
MOD = {
 "id": "m4", "num": 4, "titulo": "Módulo 4 — Regras de detecção (Analytics)",
 "resumo": "Atacamos a Loja Pixel de verdade (no laboratório local) e escrevemos, como código, as regras que transformam o ataque em incidente.",
 "minimo": 70, "aviso": AVISO,
 "aulas": [
 {"id": "4.1", "titulo": "Tipos de regra: Scheduled, NRT, Fusion e Microsoft",
  "objetivo": "Saber qual tipo de regra usar e os limites de cada um, segundo o Microsoft Learn.",
  "termos": [["Regra agendada (Scheduled)", "Uma query KQL que roda de tempos em tempos e gera alertas."], ["NRT", "Near-real-time: roda a cada minuto."], ["Fusion", "Correlação de ataques em várias etapas feita pela Microsoft."]],
  "diagrama": [
   {"say": "O Sentinel tem vários tipos de regra de análise. A mais usada é a agendada, a Scheduled. Ela roda uma query KQL num intervalo entre cinco minutos e catorze dias, olhando uma janela de tempo que tem de ser maior ou igual ao intervalo.",
    "els": [["box", 100, 200, 820, 200, "Scheduled\nintervalo: 5 min a 14 dias\njanela ≥ intervalo", B]]},
   {"say": "A NRT, de near real time, roda a cada minuto, com um atraso embutido de só dois minutos. Ela tem limites: até cinquenta regras, e até trinta alertas por execução.",
    "els": [["box", 1000, 200, 820, 200, "NRT\na cada 1 minuto · atraso 2 min\naté 50 regras · até 30 alertas", O]]},
   {"say": "A Fusion correlaciona sinais fracos num ataque de várias etapas. Mas atenção: num workspace conectado ao portal do Defender, a Fusion é desativada, porque o motor de correlação do Defender XDR assume esse papel.",
    "els": [["box", 100, 520, 820, 200, "Fusion\nataques em várias etapas\n(desativada no portal do Defender)", P]]},
   {"say": "E as regras de segurança da Microsoft transformam alertas de outros produtos, como o Defender, em incidentes. Elas também não estão disponíveis quando o Sentinel está no portal do Defender, porque lá o próprio Defender XDR cria os incidentes.",
    "els": [["box", 1000, 520, 820, 200, "Microsoft security\nalertas de outros produtos → incidentes\n(não disponível no portal do Defender)", G]]},
   {"say": "Neste módulo, vamos escrever regras agendadas como código, em YAML.",
    "els": [["text", 960, 900, "Neste módulo: Scheduled, como código (YAML)", 44, K]]}
  ],
  "demo": [
   {"say": "Esta é a nossa primeira regra, no mesmo formato YAML do repositório oficial Azure-Sentinel no GitHub.", "act": [["open", "labs/m4/regras/forca_bruta_api.yaml"]], "shot": True},
   {"say": "queryFrequency cinco minutos, queryPeriod quinze minutos. O limiar é: mais de zero resultados. E a query procura IPs com dez ou mais falhas na rota de login.", "act": [["scroll", 10]]},
   {"say": "Antes de detectar, vamos atacar. Subo a API da loja.", "act": [["term", "node api-loja/server.js >/dev/null 2>&1 &"], ["wait", 2]]},
   {"say": "E rodo o ataque de força bruta. Ele testa vinte e uma senhas contra a conta da Carla, só no localhost, e a última está certa.", "act": [["term", "bash labs/m4/ataque_forca_bruta.sh | tail -4"]], "shot": True},
   {"say": "Os logs vão para o Kusto, na tabela LojaApi underline CL.", "act": [["term", "python3 labs/m4/enviar_logs.py"]]},
   {"say": "E rodo a query da regra diretamente, para ver o que ela enxerga.", "act": [["term", "./kql.py 'LojaApi_CL | where TimeGenerated > ago(15m) and Route == \"/api/login\" | summarize Falhas=countif(StatusCode==401), Sucessos=countif(StatusCode==200) by ClientIP'"]], "shot": True},
   {"say": "Vinte falhas e um sucesso do IP 203.0.113.66. Na próxima aula, ensinamos a regra a dizer quem é quem.", "act": [["wait", 1]]}
  ],
  "lab": [
   {"txt": "Suba a API e rode o ataque (só localhost).", "cmd": "node api-loja/server.js &\nbash labs/m4/ataque_forca_bruta.sh | tail -4", "run": True, "cmd_run": "bash labs/m4/ataque_forca_bruta.sh | tail -4"},
   {"txt": "Envie os logs ao Kusto.", "cmd": "python3 labs/m4/enviar_logs.py", "run": True},
   {"txt": "Rode a query da regra.", "cmd": "./kql.py 'LojaApi_CL | where TimeGenerated > ago(15m) and Route == \"/api/login\" | summarize Falhas=countif(StatusCode==401), Sucessos=countif(StatusCode==200) by ClientIP'", "run": True}
  ],
  "desafio": "Sem guia: transforme a regra numa NRT (kind: NRT). Que campos deixam de fazer sentido e por quê? Confira no Microsoft Learn.",
  "quiz": [
   {"q": "Qual o intervalo permitido para uma regra Scheduled?", "opts": ["1 a 5 minutos", "5 minutos a 14 dias", "1 hora a 30 dias", "Qualquer um"], "a": 1, "exp": "Run query every: de 5 minutos a 14 dias; a janela deve ser ≥ ao intervalo."},
   {"q": "Com que frequência roda uma regra NRT?", "opts": ["A cada minuto", "A cada 5 minutos", "A cada hora", "Uma vez por dia"], "a": 0, "exp": "NRT é fixa em 1 minuto, com atraso embutido de 2 minutos."},
   {"q": "Workspace conectado ao portal do Defender. O que acontece com a Fusion?", "opts": ["Fica mais rápida", "É desativada; o Defender XDR faz a correlação", "Vira NRT", "Nada"], "a": 1, "exp": "Segundo o Learn, a Fusion é desativada e o motor do Defender XDR a substitui."},
   {"q": "Quantas regras NRT podem existir, segundo o Learn?", "opts": ["10", "50", "500", "Ilimitadas"], "a": 1, "exp": "No máximo 50 regras NRT."}
  ]},
 {"id": "4.2", "titulo": "Mapeamento de entidades e custom details",
  "objetivo": "Fazer o alerta dizer QUEM (IP, conta) e mostrar os números importantes sem abrir a query.",
  "termos": [["Entidade", "Um 'personagem' do alerta: IP, conta, host…"], ["Identificador", "O campo que identifica a entidade (ex.: Address do IP)."], ["Custom details", "Campos da query que aparecem direto no alerta."]],
  "diagrama": [
   {"say": "A query devolve colunas. Sozinhas, elas são só texto. O mapeamento de entidades diz ao Sentinel: esta coluna é um IP, aquela é uma conta.",
    "els": [["box", 100, 300, 520, 300, "resultado da query\nClientIP\nLogin\nFalhas", K], ["arrow", 620, 380, 900, 300, "IP.Address"], ["arrow", 620, 470, 900, 560, "Account.Name"], ["box", 900, 230, 400, 140, "Entidade IP", R], ["box", 900, 490, 400, 140, "Entidade Conta", B]]},
   {"say": "Os limites do Learn: até dez mapeamentos por regra, até três identificadores por entidade, e até quinhentas entidades por alerta, divididas entre os mapeamentos.",
    "els": [["text", 1580, 330, "≤ 10 mapeamentos\n≤ 3 identificadores\n≤ 500 entidades/alerta", 36, K]]},
   {"say": "Já os custom details colocam números da query no próprio alerta: falhas, sucessos, user agent. Até vinte por regra, e no total até dois kilobytes por alerta.",
    "els": [["box", 100, 760, 1720, 160, "customDetails:  Falhas · Sucessos · UserAgent     (≤ 20 por regra · ≤ 2 KB por alerta)", P]]}
  ],
  "demo": [
   {"say": "Na regra, o bloco entityMappings: entidade IP, identificador Address, coluna ClientIP.", "act": [["open", "labs/m4/regras/forca_bruta_api.yaml"], ["scroll", 28]], "shot": True},
   {"say": "E o customDetails, com três campos, mais o alertDetailsOverride, que coloca o IP e o número de falhas no próprio título do alerta.", "act": [["wait", 2]]},
   {"say": "Rodo a regra no simulador local. Lembrando: isto é um simulador didático, não o Sentinel. Ele valida o YAML, roda a query no Kusto de verdade e monta o alerta.", "act": [["term", "python3 labs/m4/motor_regras_local.py labs/m4/regras/forca_bruta_api.yaml"]], "shot": True},
   {"say": "Vamos ver o alerta por dentro: o título já tem o IP, a entidade IP está mapeada, e os detalhes trazem vinte falhas, um sucesso e o user agent hydra-sim.", "act": [["term", "python3 -m json.tool labs/m4/incidentes.json | head -30"]], "shot": True}
  ],
  "lab": [
   {"txt": "Rode a regra no simulador local.", "cmd": "python3 labs/m4/motor_regras_local.py labs/m4/regras/forca_bruta_api.yaml", "run": True},
   {"txt": "Inspecione entidades e detalhes.", "cmd": "python3 -m json.tool labs/m4/incidentes.json | head -30", "run": True}
  ],
  "desafio": "Sem guia: adicione uma entidade Account mapeando o primeiro login da lista Contas (dica: extend Conta = tostring(Contas[0])).",
  "quiz": [
   {"q": "Quantos mapeamentos de entidade uma regra pode ter?", "opts": ["3", "10", "20", "500"], "a": 1, "exp": "Até 10 mapeamentos de entidade por regra."},
   {"q": "Qual o limite de custom details por regra?", "opts": ["5", "10", "20", "50"], "a": 2, "exp": "Até 20 custom details, com no máximo 2 KB no total por alerta."},
   {"q": "Para que serve o alertDetailsOverride?", "opts": ["Mudar a severidade da regra inteira", "Personalizar nome/descrição do alerta com valores da query", "Criar entidades", "Agrupar incidentes"], "a": 1, "exp": "Ele permite títulos como 'Força bruta a partir de {{ClientIP}}'."}
  ]},
 {"id": "4.3", "titulo": "Mapeamento MITRE ATT&CK",
  "objetivo": "Classificar a detecção com táticas e técnicas — a língua comum dos SOCs.",
  "termos": [["Tática", "O 'porquê' do atacante (ex.: obter credenciais)."], ["Técnica", "O 'como' (ex.: T1110 Brute Force)."], ["MITRE ATT&CK", "Catálogo público de comportamentos de atacantes."]],
  "diagrama": [
   {"say": "O MITRE ATT&CK é um catálogo público de como os atacantes agem. As táticas são o porquê: entrar, obter credenciais, mover-se.",
    "els": [["box", 100, 240, 520, 150, "InitialAccess\n(entrar)", B], ["box", 700, 240, 520, 150, "CredentialAccess\n(obter credenciais)", R], ["box", 1300, 240, 520, 150, "LateralMovement\n(mover-se)", O]]},
   {"say": "As técnicas são o como. A T1110, Brute Force, fica em Credential Access. A T1078, Valid Accounts, aparece quando o atacante usa uma conta verdadeira.",
    "els": [["arrow", 960, 390, 960, 520, ""], ["box", 700, 520, 520, 140, "T1110\nBrute Force", R], ["arrow", 360, 390, 360, 520, ""], ["box", 100, 520, 520, 140, "T1078\nValid Accounts", B]]},
   {"say": "No YAML, as táticas vão em tactics, escritas sem espaços, e as técnicas em relevantTechniques. O ganho: o Sentinel mostra a sua cobertura no mapa do MITRE.",
    "els": [["text", 960, 860, "tactics: [CredentialAccess]     relevantTechniques: [T1110]", 44, K]]}
  ],
  "demo": [
   {"say": "A segunda regra: sucesso depois de várias falhas, de um país incomum. Táticas: acesso inicial e acesso a credenciais. Técnicas: T1078 e T1110.", "act": [["open", "labs/m4/regras/login_suspeito.yaml"]], "shot": True},
   {"say": "Vou gerar o evento. Como não temos um Entra ID real aqui, o script insere linhas sintéticas em SigninLogs, marcadas como tal: oito falhas e um sucesso da Rússia para a marina ponto lopes.", "act": [["term", "python3 labs/m4/login_suspeito.py"]]},
   {"say": "Rodando a regra.", "act": [["term", "python3 labs/m4/motor_regras_local.py labs/m4/regras/login_suspeito.yaml"]], "shot": True},
   {"say": "E agora o que acontece com um MITRE errado: tática traduzida para o português e técnica com um dígito a menos.", "act": [["term", "grep -A3 tactics labs/m4/exemplos/mitre_errado.yaml; python3 labs/m4/motor_regras_local.py labs/m4/exemplos/mitre_errado.yaml"]], "shot": True},
   {"say": "O validador recusa os dois. Os nomes de tática são fixos, em inglês e sem espaços, e a técnica é T seguido de quatro dígitos.", "act": [["wait", 1]]}
  ],
  "lab": [
   {"txt": "Gere o login suspeito (sintético).", "cmd": "python3 labs/m4/login_suspeito.py", "run": True},
   {"txt": "Rode a regra de login suspeito.", "cmd": "python3 labs/m4/motor_regras_local.py labs/m4/regras/login_suspeito.yaml", "run": True},
   {"txt": "Veja a validação recusar um MITRE errado.", "cmd": "python3 labs/m4/motor_regras_local.py labs/m4/exemplos/mitre_errado.yaml", "run": True}
  ],
  "desafio": "Sem guia: escreva uma regra para a força bruta no SSH (Syslog, 'Failed password') com a tática e a técnica certas.",
  "quiz": [
   {"q": "Força bruta de senha é qual técnica?", "opts": ["T1078", "T1110", "T1059", "T1566"], "a": 1, "exp": "T1110 Brute Force."},
   {"q": "O atacante entra com uma conta verdadeira. Técnica?", "opts": ["T1078 Valid Accounts", "T1110", "T1486", "T1190"], "a": 0, "exp": "T1078 Valid Accounts."},
   {"q": "Qual grafia de tática o Sentinel aceita?", "opts": ["Credential Access", "CredentialAccess", "acesso-credenciais", "TA0006 Credential"], "a": 1, "exp": "Nos templates, as táticas são escritas sem espaços: CredentialAccess."}
  ]},
 {"id": "4.4", "titulo": "Agrupando alertas em incidentes",
  "objetivo": "Evitar 50 incidentes para o mesmo ataque: configurar o agrupamento.",
  "termos": [["Alerta", "Um aviso gerado por uma execução da regra."], ["Incidente", "O 'caso' que o analista investiga; reúne alertas."], ["Agrupamento", "Regra de quando juntar alertas no mesmo incidente."]],
  "diagrama": [
   {"say": "A regra roda a cada cinco minutos. Se o ataque dura uma hora, são doze alertas. Doze incidentes para o mesmo atacante? Ninguém merece.",
    "els": [["box", 100, 200, 150, 100, "alerta", O], ["box", 280, 200, 150, 100, "alerta", O], ["box", 460, 200, 150, 100, "alerta", O], ["box", 640, 200, 150, 100, "alerta", O], ["box", 820, 200, 150, 100, "…", O]]},
   {"say": "O agrupamento junta alertas dentro de uma janela de tempo, por exemplo cinco horas, em até cento e cinquenta alertas por incidente.",
    "els": [["arrow", 540, 300, 540, 460, "janela 5h"], ["box", 200, 460, 700, 180, "1 incidente\n(até 150 alertas)", R]]},
   {"say": "São três modos: quando todas as entidades batem, que é o recomendado; tudo num incidente só; ou só as entidades e detalhes que você escolher.",
    "els": [["box", 1100, 180, 720, 120, "AllEntities (recomendado)", G], ["box", 1100, 340, 720, 120, "AnyAlert (tudo junto)", B], ["box", 1100, 500, 720, 120, "Selected (entidades escolhidas)", P]]},
   {"say": "E no portal do Defender, essas configurações valem só no momento da criação do incidente. Depois, o motor de correlação do Defender pode juntar ou separar de outro jeito.",
    "els": [["text", 960, 880, "Portal do Defender: a correlação do Defender XDR tem a palavra final", 40, R]]}
  ],
  "demo": [
   {"say": "No YAML, o bloco incidentConfiguration: criar incidente, agrupamento ligado, janela de cinco horas, modo Selected pela entidade IP.", "act": [["open", "labs/m4/regras/forca_bruta_api.yaml"], ["scroll", 38]], "shot": True},
   {"say": "Vou atacar mais duas vezes, do mesmo IP, para gerar vários alertas.", "act": [["term", "bash labs/m4/ataque_forca_bruta.sh >/dev/null; bash labs/m4/ataque_forca_bruta.sh >/dev/null; python3 labs/m4/enviar_logs.py"]]},
   {"say": "E um terceiro ataque de outro IP.", "act": [["term", "IP=203.0.113.99 bash labs/m4/ataque_forca_bruta.sh >/dev/null; python3 labs/m4/enviar_logs.py"]]},
   {"say": "Rodando as duas regras juntas.", "act": [["term", "python3 labs/m4/motor_regras_local.py labs/m4/regras/*.yaml"]], "shot": True},
   {"say": "Um incidente por IP atacante, e o da marina na regra de login suspeito. Agrupar pela entidade certa é o que separa um SOC calmo de um SOC afogado.", "act": [["wait", 1]]}
  ],
  "lab": [
   {"txt": "Ataque de um segundo IP.", "cmd": "IP=203.0.113.99 bash labs/m4/ataque_forca_bruta.sh >/dev/null; python3 labs/m4/enviar_logs.py", "run": True},
   {"txt": "Rode as duas regras.", "cmd": "python3 labs/m4/motor_regras_local.py labs/m4/regras/*.yaml", "run": True}
  ],
  "desafio": "Sem guia: troque o matchingMethod para AnyAlert e explique por que o resultado piora para o analista.",
  "quiz": [
   {"q": "Quantos alertas cabem num incidente agrupado?", "opts": ["10", "50", "150", "Ilimitados"], "a": 2, "exp": "Até 150; o excedente vai para um novo incidente."},
   {"q": "Qual modo de agrupamento o Learn recomenda?", "opts": ["Tudo num só incidente", "Quando todas as entidades batem", "Nenhum agrupamento", "Por severidade"], "a": 1, "exp": "'Group alerts into a single incident if all the entities match' é o recomendado."},
   {"q": "No portal do Defender, quem decide a correlação final?", "opts": ["O analista", "O motor de correlação do Defender XDR", "O GitHub", "A regra NRT"], "a": 1, "exp": "As configurações valem na criação; o Defender XDR pode correlacionar de outro jeito."}
  ]},
 {"id": "4.5", "titulo": "Tuning: menos ruído, mesma proteção",
  "objetivo": "Ajustar limiar e exclusões com base em dados — e testar que a detecção continua funcionando.",
  "termos": [["Falso positivo", "Alerta que dispara sem ataque de verdade."], ["Limiar", "O número a partir do qual a regra dispara."], ["Lista de exceções", "IPs ou contas conhecidos que não devem alertar."]],
  "diagrama": [
   {"say": "Regra boa é a que dispara no ataque e fica quieta no resto. O tuning é uma balança: limiar baixo demais, chove falso positivo. Alto demais, o atacante passa.",
    "els": [["box", 160, 300, 560, 180, "limiar baixo\n→ ruído", O], ["box", 1200, 300, 560, 180, "limiar alto\n→ ataque passa", R], ["arrow", 720, 390, 1200, 390, "equilíbrio"]]},
   {"say": "As ferramentas: medir antes com KQL, excluir quem é conhecido, como o monitor de disponibilidade, e, se preciso, suprimir a regra por um tempo, até vinte e quatro horas.",
    "els": [["box", 160, 620, 480, 150, "medir com KQL", B], ["box", 720, 620, 480, 150, "lista de exceções", G], ["box", 1280, 620, 480, 150, "supressão ≤ 24h", P]]},
   {"say": "E a regra mais importante: depois de ajustar, ataque de novo e prove que ainda detecta.",
    "els": [["text", 960, 930, "ajustou → ataque de novo → ainda detecta?", 44, K]]}
  ],
  "demo": [
   {"say": "Primeiro, medir. Quantas falhas por IP um usuário normal gera no nosso dataset de um dia?", "act": [["term", "./kql.py 'LojaApi_CL | where Route == \"/api/login\" and StatusCode == 401 | summarize Falhas=count() by ClientIP | summarize p99=percentile(Falhas, 99), maximo=max(Falhas)'"]], "shot": True},
   {"say": "Abro a versão ajustada da regra: uma lista de IPs permitidos e o limiar subiu para quinze.", "act": [["open", "labs/m4/exemplos/forca_bruta_ajustada.yaml"], ["scroll", 14]], "shot": True},
   {"say": "E a prova: o teste automático do módulo ataca de um IP aleatório e verifica se a regra gera um incidente com esse IP.", "act": [["term", "python3 grader/testar_regra.py labs/m4/exemplos/forca_bruta_ajustada.yaml | tail -6"]], "shot": True},
   {"say": "Aprovado. A regra continua pegando o ataque, com menos ruído. Por último, versionamos tudo no Git, porque detecção também é código.", "act": [["term", "git status --short labs/m4 | head -5"]]}
  ],
  "lab": [
   {"txt": "Meça o comportamento normal.", "cmd": "./kql.py 'LojaApi_CL | where Route == \"/api/login\" and StatusCode == 401 | summarize Falhas=count() by ClientIP | summarize p99=percentile(Falhas, 99), maximo=max(Falhas)'", "run": True},
   {"txt": "Prove que a regra ajustada ainda detecta.", "cmd": "python3 grader/testar_regra.py labs/m4/exemplos/forca_bruta_ajustada.yaml | tail -6", "run": True}
  ],
  "desafio": "Sem guia: suba o limiar para 25 e rode o testar_regra.py. Explique o resultado e qual seria um limiar seguro.",
  "quiz": [
   {"q": "Você subiu o limiar. Qual o passo obrigatório depois?", "opts": ["Nada", "Atacar de novo e confirmar que ainda detecta", "Apagar a regra", "Desligar o agrupamento"], "a": 1, "exp": "Tuning sem teste pode cegar a detecção."},
   {"q": "Por quanto tempo, no máximo, dá para suprimir uma regra agendada após um alerta?", "opts": ["1 hora", "24 horas", "7 dias", "30 dias"], "a": 1, "exp": "Stop running query for: até 24 horas."},
   {"q": "O monitor de uptime gera 401 o dia todo. Melhor ajuste?", "opts": ["Desligar a regra", "Excluir o IP do monitor numa lista de exceções", "Limiar 1000", "Apagar os logs"], "a": 1, "exp": "Exclua a fonte conhecida e mantenha a detecção para o resto."}
  ]}
 ],
 "teste": [
  {"q": "Você precisa detectar em ~1 minuto um evento crítico. Qual tipo de regra?", "opts": ["Scheduled de 1 dia", "NRT", "Fusion", "Microsoft security"], "a": 1, "exp": "NRT roda a cada minuto."},
  {"q": "Uma Scheduled roda a cada 1h. Qual janela é válida?", "opts": ["30 minutos", "1 hora ou mais", "1 minuto", "Qualquer"], "a": 1, "exp": "A janela deve ser maior ou igual ao intervalo."},
  {"q": "O cliente migrou para o portal do Defender e a Fusion 'sumiu'. Por quê?", "opts": ["Bug", "A Fusion é desativada; o Defender XDR faz a correlação", "Licença expirou", "Foi apagada pelo analista"], "a": 1, "exp": "Comportamento documentado no Learn."},
  {"q": "Quantos alertas uma NRT gera por execução, no máximo?", "opts": ["10", "30", "150", "500"], "a": 1, "exp": "Até 30 alertas (29 individuais e 1 resumo)."},
  {"q": "Seu alerta mostra só texto, sem 'IP' clicável. O que falta?", "opts": ["MITRE", "Mapeamento de entidades", "Agrupamento", "Supressão"], "a": 1, "exp": "Entity mapping transforma colunas em entidades."},
  {"q": "Você quer ver 'Falhas: 20' direto no alerta. Use…", "opts": ["customDetails", "tactics", "queryPeriod", "triggerThreshold"], "a": 0, "exp": "Custom details expõem campos da query no alerta."},
  {"q": "Quantos mapeamentos de entidade cabem numa regra?", "opts": ["3", "10", "20", "50"], "a": 1, "exp": "Até 10."},
  {"q": "Qual técnica MITRE descreve adivinhar senhas?", "opts": ["T1110", "T1078", "T1566", "T1190"], "a": 0, "exp": "T1110 Brute Force."},
  {"q": "O atacante acertou a senha e entrou. Qual técnica acrescentar?", "opts": ["T1078 Valid Accounts", "T1486", "T1059", "Nenhuma"], "a": 0, "exp": "Uso de conta válida = T1078."},
  {"q": "Ataque de 1 hora, regra a cada 5 min, sem agrupamento. Quantos incidentes, aproximadamente?", "opts": ["1", "Cerca de 12", "150", "0"], "a": 1, "exp": "Cada execução com resultado gera alerta e, sem agrupamento, incidente."},
  {"q": "Qual modo de agrupamento é o recomendado?", "opts": ["Todas as entidades batem", "Tudo junto", "Por severidade", "Nenhum"], "a": 0, "exp": "AllEntities é o recomendado pelo Learn."},
  {"q": "Quantos alertas cabem num incidente agrupado?", "opts": ["30", "100", "150", "1000"], "a": 2, "exp": "Até 150."},
  {"q": "A regra dispara 200 vezes por dia com o monitor de uptime. Melhor ação?", "opts": ["Desativar", "Excluir o IP conhecido e manter a regra", "Severidade Informational", "Apagar a tabela"], "a": 1, "exp": "Tuning cirúrgico, não cegueira."},
  {"q": "Depois do tuning, como provar que a regra funciona?", "opts": ["Confiar", "Reproduzir o ataque e checar o incidente", "Ver o YAML", "Reiniciar o Sentinel"], "a": 1, "exp": "Teste de detecção: ataque controlado → incidente."},
  {"q": "Suprimir a regra após alerta: limite máximo?", "opts": ["1h", "24h", "48h", "7 dias"], "a": 1, "exp": "Até 24 horas."},
  {"q": "Por que manter regras em YAML num repositório Git?", "opts": ["Revisão, histórico e deploy automatizado", "É obrigatório", "Roda mais rápido", "Não precisa de KQL"], "a": 0, "exp": "Detecção como código."}
 ],
 "pratico": {"titulo": "Teste prático: a sua regra tem de gerar um incidente", "txt": "Escreva a sua regra (YAML) para a força bruta na API. Rode `python3 grader/testar_regra.py minha_regra.yaml`: o script ataca a API local a partir de um IP aleatório, envia os logs para o Kusto, roda a sua regra no simulador e só aprova se surgir um incidente com a entidade IP do atacante. Cole aqui a saída para registrar a aprovação.", "regra": True}
}
