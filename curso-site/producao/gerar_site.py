#!/usr/bin/env python3
"""Gera o site Astro/Starlight a partir do conteúdo, das saídas reais dos labs e das gravações."""
import os, sys, json, shutil, glob, csv, io, subprocess, re
sys.path.insert(0, os.path.dirname(__file__)); from conteudo import MODS, AULAS, B
SITE = "/workspace/cursos/sentinel-site/site"; REPO = "/workspace/cursos/sentinel-site/repo"; OUT = f"{B}/out"
BASE = "/curso-sentinel/"; GH = "https://github.com/bfrpaulondev/curso-sentinel"
DOCS = f"{SITE}/src/content/docs"; PUB = f"{SITE}/public"
shutil.rmtree(DOCS, ignore_errors=True); os.makedirs(DOCS)
for d in ("diagramas", "shots", "videos", "data"): os.makedirs(f"{PUB}/{d}", exist_ok=True)
labs = json.load(open(f"{OUT}/labs.json")) if os.path.exists(f"{OUT}/labs.json") else {}
slug = lambda aid: aid.replace(".", "-")
def dur(f):
    try: d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f])); return f"{int(d//60)}:{int(d%60):02d}"
    except Exception: return None
def esc(s): return s.replace("{", "&#123;").replace("}", "&#125;").replace("<", "&lt;")
def fm(title, desc, order=None, extra=""):
    o = f"sidebar:\n  order: {order}\n" if order is not None else ""
    return f"---\ntitle: {json.dumps(title, ensure_ascii=False)}\ndescription: {json.dumps(desc, ensure_ascii=False)}\n{o}{extra}---\n\n"
# ---------- arquivos estáticos ----------
for f in glob.glob(f"{OUT}/diagramas/*.png"): shutil.copy(f, f"{PUB}/diagramas/")
for f in glob.glob(f"{OUT}/shots/*.png"):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f, "-vf", "scale=1280:-1", "-q:v", "4", f"{PUB}/shots/" + os.path.basename(f).replace(".png", ".jpg")])
for f in glob.glob(f"{OUT}/videos/*"): shutil.copy(f, f"{PUB}/videos/")
shutil.copy(f"{SITE}/node_modules/chart.js/dist/chart.umd.js", f"{PUB}/js/chart.umd.js")
if os.path.exists(f"{OUT}/data/render_26.csv"): shutil.copy(f"{OUT}/data/render_26.csv", f"{PUB}/data/")
# ---------- dados para o JS ----------
def csvtxt(p): return open(p).read()
TAREFAS = [
 "Quantos logins com falha (ResultType diferente de \"0\") existem em SigninLogs? Coluna: `Count`.",
 "Liste os logins com SUCESSO feitos de fora do Brasil: TimeGenerated, UserPrincipalName, IPAddress, Country.",
 "Quantos logins (sucesso ou falha) por AppDisplayName? Colunas: AppDisplayName, Logins — do maior para o menor.",
 "Na LojaApi_CL, para StatusCode >= 500: Erros = count() e DuracaoMedia = round(avg(DurationMs), 0) por Route.",
 "Na rota /api/login, janelas de 5 minutos com 20 ou mais respostas 401: TimeGenerated, Falhas.",
 "Quais logins (campo `login` do Properties) o IP 203.0.113.77 conseguiu usar com StatusCode 200? TimeGenerated, Login.",
 "No Syslog, tentativas de 'Failed password' por Computer e IP (extraído com regex), com Tentativas, Inicio e Fim.",
 "Contas com login de SUCESSO vindas de um IP que fez spray (ResultType 50126 em 10+ contas): TimeGenerated, UserPrincipalName, IPAddress, Contas.",
 "Pedidos com a tag black-friday por Method (use mv-expand): Method, Pedidos.",
 "Juntando Entra ID, API (401) e SSH (Failed password): origens com 30+ falhas. Colunas: Origem, Falhas.",
]
praticos = {
 "m0": {"minimo": 1, "itens": [{"id": "m0_contagem", "enunciado": "Rode: `./kql.py 'union withsource=Tabela SigninLogs, LojaApi_CL, Syslog | summarize Linhas=count() by Tabela' --csv saida.csv` (dataset recém-carregado) e cole o CSV.", "esperado": csvtxt(f"{REPO}/grader/esperado/m0_contagem.csv") if os.path.exists(f"{REPO}/grader/esperado/m0_contagem.csv") else ""}]},
 "m2": {"minimo": 7, "itens": [{"id": f"q{i:02d}", "enunciado": f"**Q{i:02d}.** " + TAREFAS[i-1], "esperado": csvtxt(f"{REPO}/grader/esperado/m2_q{i:02d}.csv")} for i in range(1, 11)]},
 "m4": {"minimo": 1, "itens": [{"id": "regra", "tipo": "saida", "enunciado": "Cole a saída completa de `python3 grader/testar_regra.py minha_regra.yaml`.", "esperado": ""}]},
}
glossario = sorted({t: (t, d, {"id": a["id"], "url": f"{m['id']}/{slug(a['id'])}/"}) for m, a in AULAS for t, d in a["termos"]}.values(), key=lambda x: x[0].lower())
data = {"modulos": [{"id": m["id"], "titulo": m["titulo"], "minimo": m["minimo"], "aulas": [a["id"] for a in m["aulas"]], "teste": m["teste"]} for m in MODS],
        "aulas": {a["id"]: {"quiz": a["quiz"]} for m, a in AULAS}, "praticos": praticos, "glossario": glossario}
json.dump(data, open(f"{PUB}/data/curso.json", "w"), ensure_ascii=False)
# ---------- páginas ----------
videos = {}
open(f"{DOCS}/index.mdx", "w").write(fm("Microsoft Sentinel na prática", "Curso prático de SIEM e SOAR com o Microsoft Sentinel, KQL e detecção como código.", extra="template: splash\nhero:\n  tagline: \"Um cenário só, do começo ao fim: a Loja Pixel é atacada, você detecta e responde. Tudo como código, alinhado ao SC-200.\"\n  actions:\n    - text: Começar pelo Módulo 0\n      link: " + BASE + "m0/\n      icon: right-arrow\n    - text: Repositório do curso\n      link: " + GH + "\n      variant: minimal\n") + f"""import {{ Card, CardGrid }} from '@astrojs/starlight/components';

<CardGrid>
  <Card title="Ataque → detecção → resposta" icon="warning">Na madrugada de 21/10/2026 a Loja Pixel sofre um password spray, um credential stuffing na API e força bruta no SSH. Você vai achar cada um com KQL.</Card>
  <Card title="KQL rodando de verdade" icon="seti:db">Todas as consultas foram executadas num Kusto real (emulador oficial Kustainer). Você roda o mesmo na sua máquina, sem conta.</Card>
  <Card title="Detecção como código" icon="github">Regras em YAML no formato do repositório Azure-Sentinel, versionadas no Git e testadas com um ataque controlado.</Card>
  <Card title="Progresso no seu navegador" icon="approve-check">Quizzes com explicação, testes por módulo e liberação do próximo módulo com nota mínima. Nada sai do seu navegador.</Card>
</CardGrid>

## Seu progresso

<div data-progresso></div>

## Como o curso funciona

Cada aula tem: **vídeo** (diagrama animado + demo real no VS Code), **diagrama de referência**, **laboratório guiado** com a saída esperada, **desafio sem guia** e **mini-quiz**. Cada módulo termina com um **teste** (múltipla escolha com cenários + desafio prático corrigido automaticamente). O próximo módulo libera com **70%**.

Esta é a **primeira versão**: Módulos 0, 2 e 4.
""")
for m in MODS:
    d = f"{DOCS}/{m['id']}"; os.makedirs(d)
    aviso = f"\n:::caution[Importante]\n{m['aviso']}\n:::\n" if m.get("aviso") else ""
    lista = "\n".join(f"- [Aula {a['id']} · {a['titulo']}]({BASE}{m['id']}/{slug(a['id'])}/)" for a in m["aulas"])
    open(f"{d}/index.mdx", "w").write(fm(m["titulo"], m["resumo"], extra="sidebar:\n  label: Visão geral\n  order: 0\n") + f"<div data-modulo=\"{m['id']}\"></div>\n\n{m['resumo']}\n{aviso}\n## Aulas\n\n{lista}\n- [Teste do módulo]({BASE}{m['id']}/teste/)\n")
    for k, a in enumerate(m["aulas"], 1):
        aid = a["id"]; v = f"{OUT}/videos/aula_{aid}.mp4"; vd = dur(v) if os.path.exists(v) else None; videos[aid] = vd
        p = [fm(f"Aula {aid} · {a['titulo']}", a["objetivo"], k), f"<div data-modulo=\"{m['id']}\"></div>\n\n**Objetivo:** {esc(a['objetivo'])}\n\n## Vídeo\n\n"]
        if vd:
            p.append(f'<video controls preload="metadata" playsinline poster="{BASE}diagramas/aula_{aid}.png" style="width:100%;border-radius:8px"><source src="{BASE}videos/aula_{aid}.mp4" type="video/mp4" /><track kind="subtitles" srclang="pt-BR" label="Português" src="{BASE}videos/aula_{aid}.vtt" default /></video>\n\n<small>Duração: {vd} · narração em voz sintética pt-BR · demo gravada de verdade no code-server.</small>\n\n')
        else: p.append(":::note\nVídeo em produção.\n:::\n\n")
        p.append(f"## Diagrama de referência\n\n![Diagrama da aula {aid}]({BASE}diagramas/aula_{aid}.png)\n\n## Termos desta aula\n\n")
        p.append("\n".join(f"- **{esc(t)}** — {esc(dd)}" for t, dd in a["termos"]) + "\n\n")
        if m.get("aviso") : p.append(f":::caution\n{m['aviso']}\n:::\n\n")
        p.append("## Laboratório guiado\n\nTodos os comandos rodam a partir da pasta raiz do [repositório do curso](" + GH + ").\n\n")
        for i, st in enumerate(a["lab"], 1):
            p.append(f"### Passo {i}\n\n{esc(st['txt'])}\n\n```bash\n{st['cmd']}\n```\n\n")
            o = labs.get(f"{aid}_{i-1}")
            if st.get("run") and o is not None: p.append(f"**Saída esperada** (execução real):\n\n```text\n{o}\n```\n\n")
            if st.get("nota"): p.append(f":::note[Precisa da sua conta]\n{esc(st['nota'])}\n:::\n\n")
        shots = sorted(glob.glob(f"{OUT}/shots/aula_{aid}_*.png"), key=lambda s: int(s.rsplit('_', 1)[1].split('.')[0]))
        if shots:
            p.append("### Capturas da demo\n\n" + "\n".join(f"![Captura {j} da aula {aid}]({BASE}shots/{os.path.basename(s).replace('.png', '.jpg')})" for j, s in enumerate(shots, 1)) + "\n\n")
        p.append(f"## Desafio (sem guia)\n\n{esc(a['desafio'])}\n\n## Mini-quiz\n\n<div data-quiz=\"{aid}\"></div>\n\n<button class=\"cs-btn\" data-concluir=\"{aid}\">Marcar aula como concluída</button>\n")
        open(f"{d}/{slug(aid)}.mdx", "w").write("".join(p))
    pr = m["pratico"]; extra = ""
    if m["id"] == "m2": extra = "\nNo repositório: copie as suas consultas para `respostas/m2/q01.kql … q10.kql` e rode `python3 grader/corrigir.py` — ele executa no Kusto e dá a nota.\n\n:::caution\nO Módulo 4 insere eventos novos nas tabelas. Antes deste teste, recarregue o dataset fixo: `python3 dataset/carregar_dataset.py`.\n:::\n"
    open(f"{d}/teste.mdx", "w").write(fm(f"Teste — {m['titulo'].split(' — ')[0]}", "Teste do módulo: múltipla escolha com cenários e desafio prático.", 99, extra="") + f"<div data-modulo=\"{m['id']}\"></div>\n\n## Situação\n\n<div data-estado=\"{m['id']}\"></div>\n\n## Parte 1 — {len(m['teste'])} questões de cenário\n\nMínimo: **{m['minimo']}%**. Cada resposta vem com explicação.\n\n<div data-teste=\"{m['id']}\"></div>\n\n## Parte 2 — {esc(pr['titulo'])}\n\n{pr['txt']}\n{extra}\n<div data-pratico=\"{m['id']}\"></div>\n")
# glossário, playground, sobre
open(f"{DOCS}/glossario.mdx", "w").write(fm("Glossário", "Todos os termos do curso, com busca.", 100) + "Busque qualquer termo; o link leva à aula onde ele aparece.\n\n<div data-glossario></div>\n")
open(f"{DOCS}/playground.mdx", "w").write(fm("Playground KQL grátis", "Dataset da Loja Pixel para praticar KQL sem pagar nada.", 101) + f"""O dataset fixo da Loja Pixel (933 logins, 2540 pedidos de API, 535 linhas de Syslog — 24 horas com três ataques escondidos) está no repositório, em `dataset/`.

## Opção 1 — Kusto local (sem conta nenhuma)

```bash
docker run -d --name kusto -p 8080:8080 -e ACCEPT_EULA=Y mcr.microsoft.com/azuredataexplorer/kustainer-linux:latest
pip install azure-kusto-data pyyaml
python3 dataset/carregar_dataset.py
./kql.py "SigninLogs | take 5"
```

Foi assim que todas as consultas do curso foram executadas.

## Opção 2 — Cluster gratuito do Azure Data Explorer

A Microsoft oferece um [cluster gratuito do Azure Data Explorer](https://learn.microsoft.com/azure/data-explorer/start-for-free) que precisa só de uma conta Microsoft (sem subscrição e sem cartão). Crie o cluster e um banco `Loja`, e depois:

```bash
az login
export KUSTO_URL=https://SEU-CLUSTER.REGIAO.kusto.windows.net KUSTO_DB=Loja
python3 dataset/carregar_dataset.py
```

:::note
A opção 2 não foi testada nesta versão porque exige login numa conta Microsoft.
:::

## Gráfico com os dados reais (aula 2.6)

<canvas data-grafico height="120"></canvas>
""")
open(f"{DOCS}/sobre.mdx", "w").write(fm("O que é real neste curso", "Transparência: o que foi executado de verdade e o que é só código.", 102) + f"""## Executado de verdade
- **Todas as consultas KQL** (labs, gabaritos do teste do Módulo 2, saídas esperadas): emulador oficial do Kusto (Kustainer) em Docker.
- **API da Loja Pixel** (Node.js), **ataque de força bruta** (apenas contra `localhost`), envio dos logs para o Kusto.
- **Demos dos vídeos**: gravação real da tela (ffmpeg) do code-server (VS Code no navegador) com a extensão Kuskus, terminal, Git e Azure CLI.
- **Bicep**: validado com `bicep lint` e `bicep build`.
- **Corretores**: `grader/corrigir.py` (Módulo 2) e `grader/testar_regra.py` (Módulo 4).

## Só código (precisa da sua conta Azure)
- Orçamento, workspace + Sentinel e deploy da Loja Pixel no Azure (`labs/m0/`). Nada foi aplicado numa subscrição.
- Nenhuma tela do portal do Azure ou do Defender aparece no curso: nós não simulamos o portal.

## Simulado, e avisado
- **Logins do Entra ID**: o dataset e o script `login_suspeito.py` geram linhas **sintéticas** de SigninLogs (não há um tenant real).
- **`motor_regras_local.py`** é um **simulador didático** do motor de regras. Valida o YAML e roda a query no Kusto real, mas **não é o Microsoft Sentinel**.

## Fontes
Os limites e comportamentos citados (NRT, entidades, custom details, agrupamento, Fusion, portal do Defender) foram conferidos no Microsoft Learn em 03/11/2026.

Vídeos com marca d'água @bfrpaulondev. Narração com vozes neurais pt-BR.
""")
cfg = f"""// @ts-check
import {{ defineConfig }} from 'astro/config';
import starlight from '@astrojs/starlight';
export default defineConfig({{
  site: 'https://bfrpaulondev.github.io', base: '{BASE.rstrip('/')}', trailingSlash: 'always',
  integrations: [starlight({{
    title: 'Sentinel na prática', defaultLocale: 'root', locales: {{ root: {{ label: 'Português do Brasil', lang: 'pt-BR' }} }},
    social: [{{ icon: 'github', label: 'GitHub', href: '{GH}' }}],
    customCss: ['./src/styles/curso.css'],
    head: [{{ tag: 'script', content: "window.CS_BASE='{BASE}'" }}, {{ tag: 'script', attrs: {{ src: '{BASE}js/chart.umd.js', defer: true }} }}, {{ tag: 'script', attrs: {{ src: '{BASE}js/curso.js', defer: true }} }}],
    sidebar: [
      {{ label: 'Módulo 0 — Laboratório', autogenerate: {{ directory: 'm0' }} }},
      {{ label: 'Módulo 2 — KQL', autogenerate: {{ directory: 'm2' }} }},
      {{ label: 'Módulo 4 — Detecção', autogenerate: {{ directory: 'm4' }} }},
      {{ label: 'Extras', items: [{{ label: 'Glossário', link: '/glossario/' }}, {{ label: 'Playground KQL', link: '/playground/' }}, {{ label: 'O que é real', link: '/sobre/' }}] }},
    ],
  }})],
}});
"""
open(f"{SITE}/astro.config.mjs", "w").write(cfg)
os.makedirs(f"{SITE}/src", exist_ok=True)
open(f"{SITE}/src/content.config.ts", "w").write("import { defineCollection } from 'astro:content';\nimport { docsLoader } from '@astrojs/starlight/loaders';\nimport { docsSchema } from '@astrojs/starlight/schema';\nexport const collections = { docs: defineCollection({ loader: docsLoader(), schema: docsSchema() }) };\n")
json.dump(videos, open(f"{OUT}/videos.json", "w"), indent=1)
print("site gerado", videos)
