# -*- coding: utf-8 -*-
# Módulo 0 — Preparação do ambiente. Texto em pt-BR.
B="#1e66f5"; G="#2f9e44"; R="#e03131"; O="#f08c00"; P="#7048e8"; K="#343a40"
MOD = {
 "id": "m0", "num": 0, "titulo": "Módulo 0 — Preparando o laboratório",
 "resumo": "Conta Azure com freio de gastos, workspace com Microsoft Sentinel, a Loja Pixel no ar e as ferramentas que vamos usar o curso inteiro.",
 "minimo": 70,
 "aulas": [
 {
  "id": "0.1", "titulo": "Conta Azure e alertas de orçamento",
  "objetivo": "Criar a sua conta e, antes de qualquer recurso, um orçamento com alertas por e-mail — como código.",
  "termos": [["Subscrição", "A 'conta de luz' do Azure: tudo o que você cria é cobrado nela."], ["Orçamento (Budget)", "Um limite de referência mensal que dispara alertas. Ele avisa, mas NÃO desliga nada."], ["Bicep", "Linguagem da Microsoft para descrever recursos do Azure como código."]],
  "diagrama": [
   {"say": "Antes de criar qualquer coisa no Azure, vamos instalar o nosso freio de mão. Pense na subscrição como a conta de luz da casa: tudo o que você liga entra na fatura dela.",
    "els": [["box", 140, 420, 360, 160, "Subscrição Azure\n(a fatura)", B]]},
   {"say": "Dentro dela criamos um orçamento. Aqui, vinte euros por mês. Atenção a um detalhe importante: o orçamento avisa, mas não desliga recurso nenhum. Ele é o alarme, não o disjuntor.",
    "els": [["arrow", 500, 500, 760, 500, ""], ["box", 760, 420, 380, 160, "Orçamento\n20 €/mês", O]]},
   {"say": "Os alertas disparam em três pontos: cinquenta por cento do gasto real, oitenta por cento do gasto real, e cem por cento do gasto previsto. O previsto é o mais útil, porque avisa antes de você estourar.",
    "els": [["arrow", 1140, 470, 1400, 300, "50% real"], ["arrow", 1140, 500, 1400, 500, "80% real"], ["arrow", 1140, 530, 1400, 700, "100% previsto"], ["box", 1400, 240, 380, 120, "e-mail", G], ["box", 1400, 440, 380, 120, "e-mail", G], ["box", 1400, 640, 380, 120, "e-mail", R]]},
   {"say": "E um aviso honesto: os dados de custo chegam com atraso de algumas horas. Por isso, no fim de cada laboratório, a regra de ouro é apagar o grupo de recursos.",
    "els": [["text", 960, 900, "Custos chegam com horas de atraso → no fim do lab: az group delete", 40, K]]}
  ],
  "demo": [
   {"say": "Vamos ao código. Este é o arquivo orcamento ponto bicep, que está no repositório do curso.", "act": [["open", "labs/m0/orcamento.bicep"]], "shot": True},
   {"say": "Repare no targetScope igual a subscription: o orçamento vive na subscrição, não num grupo de recursos. O valor é vinte, o período é mensal, e temos três notificações, cada uma com o seu limite e o tipo Actual ou Forecasted.", "act": [["scroll", 6]]},
   {"say": "Antes de mandar para o Azure, eu valido o arquivo com o linter do Bicep. Nenhum aviso, nenhum erro.", "act": [["term", "bicep lint labs/m0/orcamento.bicep && echo 'sem avisos'"]], "shot": True},
   {"say": "Também dá para ver o JSON que o Azure vai receber. O Bicep é só uma forma mais limpa de escrever esse template.", "act": [["term", "bicep build labs/m0/orcamento.bicep --stdout | head -25"]]},
   {"say": "Agora, a parte honesta. Para aplicar de verdade, você precisa entrar na sua conta com az login. Eu não vou fazer isso aqui, porque esta máquina de gravação não tem a sua conta. Na sua máquina, o comando é este que está no comentário.", "act": [["term", "echo 'Na sua máquina: az login  &&  az deployment sub create -l brazilsouth -f labs/m0/orcamento.bicep -p email=voce@exemplo.com'"]], "shot": True},
   {"say": "Fechou: orçamento como código, validado, pronto para aplicar. Na próxima aula, criamos o workspace e ligamos o Sentinel.", "act": [["wait", 1]]}
  ],
  "lab": [
   {"txt": "Abra o arquivo do orçamento no VS Code.", "cmd": "code labs/m0/orcamento.bicep", "run": False},
   {"txt": "Valide o Bicep localmente (não precisa de conta).", "cmd": "bicep lint labs/m0/orcamento.bicep && echo 'sem avisos'", "run": True},
   {"txt": "Gere o template ARM para ver o que o Azure vai receber.", "cmd": "bicep build labs/m0/orcamento.bicep --stdout | head -12", "run": True},
   {"txt": "Na sua máquina, com a sua conta: entre e aplique. Troque o e-mail.", "cmd": "az login\naz deployment sub create -l brazilsouth -f labs/m0/orcamento.bicep -p email=voce@exemplo.com", "run": False, "nota": "Precisa de login no Azure. Confira depois em Cost Management → Budgets."}
  ],
  "desafio": "Sem guia: adicione um quarto alerta, de 120% do gasto REAL, que mande e-mail para um segundo endereço passado como parâmetro `emailExtra`. O `bicep lint` tem de continuar sem avisos.",
  "quiz": [
   {"q": "O seu orçamento de 20 €/mês chegou a 100%. O que acontece com as VMs ligadas?", "opts": ["São desligadas automaticamente", "Nada: o orçamento só dispara alertas", "A subscrição é bloqueada", "Os recursos passam para o plano gratuito"], "a": 1, "exp": "Orçamentos do Cost Management avisam (e podem acionar grupos de ação), mas não param recursos sozinhos."},
   {"q": "Qual tipo de limite avisa ANTES de você gastar o valor total?", "opts": ["Actual", "Forecasted", "Monthly", "Cost"], "a": 1, "exp": "Forecasted compara com o gasto previsto para o período, então pode disparar antes do gasto real chegar lá."},
   {"q": "Por que o arquivo usa targetScope = 'subscription'?", "opts": ["Porque Bicep exige", "Porque o orçamento é criado no escopo da subscrição", "Para ficar mais barato", "Porque o Sentinel exige"], "a": 1, "exp": "Este orçamento cobre a subscrição inteira, então o deployment é feito nesse escopo (az deployment sub create)."},
   {"q": "Qual é a regra de ouro no fim de cada laboratório pago?", "opts": ["Desligar o computador", "Apagar o grupo de recursos", "Remover o orçamento", "Trocar a senha"], "a": 1, "exp": "Apagar o grupo de recursos remove tudo o que foi criado nele e para a cobrança desses recursos."}
  ]
 },
 {
  "id": "0.2", "titulo": "Workspace do Log Analytics e Microsoft Sentinel",
  "objetivo": "Entender a relação workspace ↔ Sentinel e criá-los com Bicep, com limite diário de ingestão.",
  "termos": [["Log Analytics workspace", "O 'armazém' onde os logs ficam guardados e são consultados com KQL."], ["Microsoft Sentinel", "SIEM e SOAR que funciona por cima de um workspace."], ["Limite diário (daily cap)", "Teto de GB por dia que o workspace aceita ingerir."]],
  "diagrama": [
   {"say": "Os logs chegam de vários lugares: o Entra ID, a nossa API, as máquinas Linux.",
    "els": [["box", 80, 200, 330, 120, "Entra ID", B], ["box", 80, 470, 330, 120, "API da Loja", B], ["box", 80, 740, 330, 120, "VM Linux (Syslog)", B]]},
   {"say": "Todos eles desembocam num Log Analytics workspace. Pense num armazém com prateleiras: cada prateleira é uma tabela, como SigninLogs ou Syslog.",
    "els": [["arrow", 410, 260, 720, 500, ""], ["arrow", 410, 530, 720, 530, ""], ["arrow", 410, 800, 720, 560, ""], ["db", 720, 380, 420, 320, "Log Analytics\nworkspace\n(tabelas)", G]]},
   {"say": "O Microsoft Sentinel não é outro armazém. Ele é uma camada por cima do workspace: lê as tabelas, roda as regras de detecção e cria incidentes.",
    "els": [["box", 1300, 380, 520, 320, "Microsoft Sentinel\nregras · incidentes\nautomação", P], ["arrow", 1140, 540, 1300, 540, "lê"]]},
   {"say": "Uma novidade importante: depois de trinta e um de março de 2027, o Sentinel deixa de ser suportado no portal do Azure e passa a viver só no portal do Microsoft Defender. Neste curso, o que fazemos é código, então vale para os dois.",
    "els": [["text", 960, 960, "Após 31/03/2027: Sentinel só no portal do Microsoft Defender", 40, R]]}
  ],
  "demo": [
   {"say": "Aqui está o sentinel ponto bicep. Primeiro recurso: o workspace, com o SKU por gigabyte, retenção de noventa dias e um limite diário de um gigabyte, que é o nosso segundo freio de gastos.", "act": [["open", "labs/m0/sentinel.bicep"]], "shot": True},
   {"say": "Segundo recurso: o onboardingStates. É ele que liga o Sentinel no workspace. Repare no scope apontando para o workspace.", "act": [["scroll", 8]]},
   {"say": "Validação com o linter.", "act": [["term", "bicep lint labs/m0/sentinel.bicep && echo 'sem avisos'"]], "shot": True},
   {"say": "E vamos conferir os tipos de recurso que o template final contém.", "act": [["term", "bicep build labs/m0/sentinel.bicep --stdout | grep '\"type\"'"]], "shot": True},
   {"say": "Na sua conta, você aplica num grupo de recursos com az deployment group create. De novo: isso precisa de login, e eu não vou simular o portal aqui. Na próxima aula, colocamos a empresa fictícia no ar.", "act": [["term", "echo 'Na sua máquina: az group create -n rg-curso-sentinel -l brazilsouth && az deployment group create -g rg-curso-sentinel -f labs/m0/sentinel.bicep'"]]}
  ],
  "lab": [
   {"txt": "Valide o template do workspace + Sentinel.", "cmd": "bicep lint labs/m0/sentinel.bicep && echo 'sem avisos'", "run": True},
   {"txt": "Liste os tipos de recurso do template.", "cmd": "bicep build labs/m0/sentinel.bicep --stdout | grep '\"type\"'", "run": True},
   {"txt": "Na sua conta: crie o grupo e faça o deploy.", "cmd": "az group create -n rg-curso-sentinel -l brazilsouth\naz deployment group create -g rg-curso-sentinel -f labs/m0/sentinel.bicep", "run": False, "nota": "Precisa de login no Azure."}
  ],
  "desafio": "Sem guia: transforme a retenção em parâmetro com `@minValue(30)` e `@maxValue(730)`, e acrescente um `output` com o nome do workspace.",
  "quiz": [
   {"q": "Onde ficam guardados os logs que o Sentinel analisa?", "opts": ["No próprio Sentinel, separado", "Num Log Analytics workspace", "No GitHub", "No Entra ID"], "a": 1, "exp": "O Sentinel funciona por cima de um workspace do Log Analytics; os dados ficam nas tabelas desse workspace."},
   {"q": "Qual recurso Bicep liga o Sentinel num workspace?", "opts": ["Microsoft.SecurityInsights/onboardingStates", "Microsoft.Insights/components", "Microsoft.Web/sites", "Microsoft.Consumption/budgets"], "a": 0, "exp": "onboardingStates (com scope no workspace) é o recurso de onboarding do Microsoft Sentinel."},
   {"q": "Para que serve o dailyQuotaGb = 1 no laboratório?", "opts": ["Acelerar consultas", "Limitar a ingestão diária e o custo", "Aumentar a retenção", "Ativar o NRT"], "a": 1, "exp": "O limite diário corta a ingestão quando atinge o teto — útil num laboratório para não ter surpresas."},
   {"q": "Segundo o Microsoft Learn, o que muda após 31 de março de 2027?", "opts": ["O Sentinel deixa de existir", "O Sentinel passa a ser só no portal do Defender", "O KQL é substituído por SQL", "Os workspaces são apagados"], "a": 1, "exp": "Após essa data, o Sentinel não terá mais suporte no portal do Azure e ficará disponível apenas no portal do Microsoft Defender."}
  ]
 },
 {
  "id": "0.3", "titulo": "A empresa fictícia: Loja Pixel",
  "objetivo": "Subir a Loja Pixel (API Node.js) localmente, gerar logs reais e conhecer o script de deploy no Azure.",
  "termos": [["API", "O 'balcão' da loja: recebe pedidos (HTTP) e devolve respostas."], ["Log em JSON", "Cada linha é um objeto JSON — fácil de ingerir e de ler com parse_json."], ["X-Forwarded-For", "Cabeçalho que informa o IP original do cliente quando há um proxy no meio."]],
  "diagrama": [
   {"say": "Este é o cenário que vai nos acompanhar o curso inteiro: a Loja Pixel, uma loja online pequena.",
    "els": [["person", 160, 480, "clientes"], ["box", 520, 400, 380, 170, "API Node.js\n/api/login\n/api/produtos", B]]},
   {"say": "A API conversa com o banco de dados, os funcionários entram pelo Entra ID, e o código passa por uma pipeline no GitHub.",
    "els": [["arrow", 260, 490, 520, 490, "HTTPS"], ["db", 1060, 180, 300, 200, "Banco", G], ["arrow", 900, 450, 1060, 300, ""], ["box", 1060, 470, 360, 130, "Entra ID\n(funcionários)", B], ["box", 1060, 700, 360, 130, "GitHub\npipeline", K], ["arrow", 1060, 760, 900, 560, "deploy"]]},
   {"say": "E tudo isso gera logs. Cada login, cada erro, cada deploy vira uma linha que vai para o workspace. É desses logs que vamos caçar os atacantes.",
    "els": [["arrow", 1420, 530, 1640, 530, "logs"], ["db", 1640, 420, 240, 220, "workspace", P]]}
  ],
  "demo": [
   {"say": "No repositório, a API está em api-loja barra server ponto js. É um servidor Node puro, sem framework, para você entender cada linha.", "act": [["open", "api-loja/server.js"]], "shot": True},
   {"say": "Vou subir a API num terminal.", "act": [["term", "node api-loja/server.js &"], ["wait", 2]]},
   {"say": "Um pedido normal à lista de produtos.", "act": [["term", "curl -s localhost:3000/api/produtos"]], "shot": True},
   {"say": "Agora um login com senha errada. A API responde quatrocentos e um, não autorizado.", "act": [["term", "curl -s -X POST localhost:3000/api/login -H 'Content-Type: application/json' -d '{\"email\":\"carla@cliente.com\",\"senha\":\"errada\"}'"]]},
   {"say": "E o mais importante: o log. Cada pedido vira uma linha JSON, já no formato da tabela LojaApi underline CL que vamos usar no Sentinel.", "act": [["term", "tail -n 2 api-loja/logs/api.jsonl"]], "shot": True},
   {"say": "Para colocar a loja no Azure, existe o script zero ponto três deploy loja. Ele cria o grupo, o workspace, o App Service e três usuários fictícios no Entra ID. Ele custa dinheiro e precisa da sua conta, por isso fica para você rodar e apagar no fim.", "act": [["open", "labs/m0/0.3_deploy_loja.sh"]], "shot": True}
  ],
  "lab": [
   {"txt": "Suba a API da Loja Pixel.", "cmd": "node api-loja/server.js &", "run": False},
   {"txt": "Faça um login com senha errada.", "cmd": "curl -s -X POST localhost:3000/api/login -H 'Content-Type: application/json' -d '{\"email\":\"carla@cliente.com\",\"senha\":\"errada\"}'", "run": True},
   {"txt": "Veja o log gerado (formato LojaApi_CL).", "cmd": "tail -n 1 api-loja/logs/api.jsonl", "run": True},
   {"txt": "Opcional, na sua conta: deploy completo no Azure (custa dinheiro — apague no fim).", "cmd": "cd labs/m0 && ./0.3_deploy_loja.sh", "run": False, "nota": "Precisa de login no Azure e de permissão para criar usuários no Entra ID."}
  ],
  "desafio": "Sem guia: acrescente à API uma rota GET /api/saude que responda {\"ok\":true} e confirme que ela também aparece no api.jsonl com StatusCode 200.",
  "quiz": [
   {"q": "A API está atrás de um proxy. Qual cabeçalho ela usa para registrar o IP real do cliente?", "opts": ["User-Agent", "X-Forwarded-For", "Authorization", "Content-Type"], "a": 1, "exp": "X-Forwarded-For carrega o IP original quando há um proxy ou balanceador no caminho."},
   {"q": "Um login com senha errada gera qual StatusCode no log?", "opts": ["200", "302", "401", "500"], "a": 2, "exp": "401 (Unauthorized) é a resposta da API para credenciais inválidas."},
   {"q": "Por que o log é gravado em JSON, uma linha por evento?", "opts": ["Fica mais bonito", "É fácil de ingerir e de ler com parse_json no KQL", "É exigência do Node", "Ocupa menos que texto"], "a": 1, "exp": "JSON por linha é o formato mais simples de ingerir e de explorar com parse_json/mv-expand."}
  ]
 },
 {
  "id": "0.4", "titulo": "Ferramentas: VS Code, extensão KQL, Git e Azure CLI",
  "objetivo": "Deixar a sua máquina pronta e conhecer o Kusto local (emulador) onde as consultas do curso rodam de verdade.",
  "termos": [["Kustainer", "Emulador oficial do Kusto em Docker: roda KQL de verdade, sem conta."], ["Azure CLI (az)", "Linha de comando para gerenciar o Azure."], ["Git", "Histórico de versões do seu código — inclusive das regras de detecção."]],
  "diagrama": [
   {"say": "Quatro ferramentas, um fluxo só. No VS Code você escreve KQL, Bicep e YAML, com a extensão Kuskus colorindo o KQL.",
    "els": [["box", 120, 380, 380, 180, "VS Code\n+ Kuskus (KQL)", B]]},
   {"say": "O Git guarda o histórico. Regra de detecção também é código: tem revisão, tem versão, tem volta atrás.",
    "els": [["arrow", 500, 470, 740, 470, "commit"], ["box", 740, 380, 330, 180, "Git /\nGitHub", K]]},
   {"say": "Para executar, temos dois caminhos. Com conta, o Azure CLI publica no Azure. Sem conta, o emulador Kustainer roda o mesmo KQL na sua máquina. Todas as consultas deste curso foram executadas nele.",
    "els": [["arrow", 1070, 430, 1320, 260, "az"], ["box", 1320, 170, 480, 170, "Azure\n(precisa de login)", O], ["arrow", 1070, 520, 1320, 720, "docker"], ["box", 1320, 640, 480, 170, "Kustainer local\n(KQL real, grátis)", G]]}
  ],
  "demo": [
   {"say": "Vamos conferir as versões. Primeiro o Git.", "act": [["term", "git --version"]]},
   {"say": "O Azure CLI.", "act": [["term", "az version | head -4"]], "shot": True},
   {"say": "O histórico do repositório do curso.", "act": [["term", "git log --oneline | head -5"]]},
   {"say": "O emulador Kusto rodando em Docker.", "act": [["term", "sudo docker ps --format '{{.Names}}  {{.Image}}  {{.Status}}'"]], "shot": True},
   {"say": "E a primeira consulta KQL de verdade, com o nosso ajudante kql ponto py: quantas linhas tem cada tabela do banco Loja.", "act": [["term", "./kql.py 'union withsource=Tabela SigninLogs, LojaApi_CL, Syslog | summarize Linhas=count() by Tabela'"]], "shot": True},
   {"say": "Abrindo um arquivo ponto kql, a extensão colore operadores e funções. A partir do Módulo 2, é aqui que vamos morar.", "act": [["open", "labs/m2/2.1_where_project.kql"]], "shot": True}
  ],
  "lab": [
   {"txt": "Suba o emulador Kusto e carregue o dataset da Loja Pixel (sem conta).", "cmd": "cd labs/m0 && ./0.local_setup.sh", "run": False},
   {"txt": "Confira as ferramentas.", "cmd": "git --version && az version | head -3", "run": True},
   {"txt": "Primeira consulta real.", "cmd": "./kql.py 'union withsource=Tabela SigninLogs, LojaApi_CL, Syslog | summarize Linhas=count() by Tabela'", "run": True}
  ],
  "desafio": "Sem guia: com o kql.py, descubra o primeiro e o último TimeGenerated de cada tabela (dica: min() e max()).",
  "quiz": [
   {"q": "Você quer rodar KQL sem conta Azure. Qual opção usamos no curso?", "opts": ["Excel", "Emulador Kustainer em Docker", "SQL Server", "Não é possível"], "a": 1, "exp": "O Kustainer é o emulador oficial do Kusto em Docker e roda KQL de verdade localmente."},
   {"q": "Por que guardar regras de detecção no Git?", "opts": ["Para ocupar menos espaço", "Para ter histórico, revisão e reversão", "Porque o Sentinel só aceita Git", "Para executar mais rápido"], "a": 1, "exp": "Detecção como código ganha controle de versão, revisão por pares e deploy automatizado."},
   {"q": "Qual comando entra na sua conta no Azure CLI?", "opts": ["az start", "az login", "az connect", "az open"], "a": 1, "exp": "az login abre a autenticação na sua conta Microsoft/Entra."}
  ]
 }
 ],
 "teste": [
  {"q": "Ana criou um orçamento de 50 € e esqueceu uma VM cara ligada. O gasto chegou a 60 €. O que aconteceu?", "opts": ["A VM foi desligada em 50 €", "Ana recebeu os alertas, mas a VM continuou ligada", "O Azure bloqueou a conta", "Nada foi cobrado acima de 50 €"], "a": 1, "exp": "Orçamentos avisam; não param recursos."},
  {"q": "Você quer ser avisado assim que a projeção do mês passar do valor. Que limite usa?", "opts": ["Actual 100%", "Forecasted 100%", "Actual 50%", "Nenhum"], "a": 1, "exp": "Forecasted compara com o gasto previsto."},
  {"q": "Qual comando aplica um Bicep com targetScope = 'subscription'?", "opts": ["az deployment group create", "az deployment sub create", "az group create", "az bicep build"], "a": 1, "exp": "Escopo de subscrição usa az deployment sub create (com -l)."},
  {"q": "O Sentinel guarda os dados…", "opts": ["num banco próprio, separado", "nas tabelas do Log Analytics workspace", "no GitHub", "no Entra ID"], "a": 1, "exp": "O Sentinel opera sobre um workspace."},
  {"q": "Um colega diz: 'vou criar o Sentinel e depois um workspace para ele'. A ordem certa é…", "opts": ["Sentinel primeiro", "Workspace primeiro, depois habilitar o Sentinel nele", "Tanto faz", "Os dois vêm juntos sempre"], "a": 1, "exp": "O onboarding do Sentinel é feito num workspace existente (scope no workspace)."},
  {"q": "No laboratório, o que limita a ingestão a 1 GB por dia?", "opts": ["retentionInDays", "workspaceCapping.dailyQuotaGb", "sku PerGB2018", "onboardingStates"], "a": 1, "exp": "dailyQuotaGb é o limite diário de ingestão."},
  {"q": "Após 31/03/2027, onde o Sentinel será suportado?", "opts": ["Só no portal do Azure", "Só no portal do Microsoft Defender", "Só via CLI", "Em nenhum lugar"], "a": 1, "exp": "Segundo o Microsoft Learn, ficará apenas no portal do Defender."},
  {"q": "A API da Loja recebe um pedido via proxy. Para saber o IP do atacante, você olha…", "opts": ["o IP do proxy", "o X-Forwarded-For registrado como ClientIP", "o User-Agent", "a rota"], "a": 1, "exp": "A API usa o X-Forwarded-For para registrar o IP original."},
  {"q": "No api.jsonl aparece StatusCode 401 várias vezes seguidas do mesmo IP. Isso indica…", "opts": ["Sucesso", "Falhas de autenticação repetidas — possível força bruta", "Erro do servidor", "Cache"], "a": 1, "exp": "401 repetido do mesmo IP é o sinal clássico de tentativa de senha."},
  {"q": "Qual a vantagem do log em JSON por linha?", "opts": ["Compressão", "Ingestão simples e leitura com parse_json", "Criptografia", "Nenhuma"], "a": 1, "exp": "Formato estruturado, fácil de ingerir e consultar."},
  {"q": "Você não tem conta Azure hoje. Como pratica o Módulo 2?", "opts": ["Não pratica", "Com o Kustainer local e o dataset do curso", "Com o Excel", "Pelo portal sem login"], "a": 1, "exp": "O emulador roda o mesmo KQL localmente."},
  {"q": "O que faz a extensão Kuskus no VS Code?", "opts": ["Executa no Azure", "Destaque de sintaxe KQL", "Cria workspaces", "Faz login"], "a": 1, "exp": "Kuskus dá destaque de sintaxe ao KQL."},
  {"q": "Por que versionar regras no Git?", "opts": ["Histórico, revisão e reversão", "Obrigatório por lei", "Para rodar KQL", "Para pagar menos"], "a": 0, "exp": "Detecção como código traz as práticas de engenharia de software."},
  {"q": "Terminou o laboratório pago. Qual o comando mais importante?", "opts": ["az logout", "az group delete -n rg-curso-sentinel --yes", "git push", "docker stop kusto"], "a": 1, "exp": "Apagar o grupo de recursos encerra a cobrança dos recursos do lab."},
  {"q": "O script de deploy cria usuários no Entra ID. De que permissão você precisa?", "opts": ["Nenhuma", "Uma função como User Administrator", "Só Reader", "Só ser dono do repositório"], "a": 1, "exp": "Criar usuários exige uma função administrativa de usuários no Entra ID."}
 ],
 "pratico": {"titulo": "Desafio prático do Módulo 0", "txt": "Rode no seu computador o `labs/m0/0.local_setup.sh` e a consulta abaixo. Cole o resultado (CSV ou a tabela do kql.py) para validar.", "query_id": "m0_contagem"}
}
