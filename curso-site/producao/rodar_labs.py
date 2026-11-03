#!/usr/bin/env python3
"""Executa de verdade os comandos dos laboratórios e guarda a saída (para o site mostrar a 'saída esperada')."""
import os, sys, json, subprocess, re
sys.path.insert(0, os.path.dirname(__file__)); from conteudo import AULAS, B
REPO = "/workspace/cursos/sentinel-site/repo"; ENV = {**os.environ, "KUSTO_URL": "http://localhost:8080", "KUSTO_DB": "Loja"}
sh = lambda c: subprocess.run(c, shell=True, cwd=REPO, env=ENV, capture_output=True, text=True)
sh("pkill -f '[n]ode api-loja/server'; python3 dataset/carregar_dataset.py; rm -f api-loja/logs/api.jsonl api-loja/logs/*.enviado")
out = {}
for m, a in AULAS:
    if a["id"] == "0.3" or a["id"] == "4.1":
        subprocess.Popen("node api-loja/server.js", shell=True, cwd=REPO, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); import time; time.sleep(1.5)
    if a["id"] == "4.1": sh("python3 dataset/carregar_dataset.py; rm -f api-loja/logs/api.jsonl api-loja/logs/*.enviado")
    for i, st in enumerate(a["lab"]):
        if not st.get("run"): continue
        r = sh(st.get("cmd_run", st["cmd"])); txt = (r.stdout + r.stderr).rstrip()
        txt = re.sub(r"\x1b\[[0-9;]*m", "", txt)
        out[f"{a['id']}_{i}"] = txt[-3500:]; print(a["id"], i, "ok" if r.returncode == 0 else f"rc={r.returncode}")
json.dump(out, open(f"{B}/out/labs.json", "w"), ensure_ascii=False, indent=1)
# CSVs para o site: gráfico 2.6 e prático do M0 (dataset limpo)
sh("pkill -f '[n]ode api-loja/server'; python3 dataset/carregar_dataset.py")
os.makedirs(f"{B}/out/data", exist_ok=True)
sh(f"./kql.py -f labs/m2/2.6_render.kql --csv {B}/out/data/render_26.csv --max 1")
sh(f"./kql.py 'union withsource=Tabela SigninLogs, LojaApi_CL, Syslog | summarize Linhas=count() by Tabela' --csv grader/esperado/m0_contagem.csv --max 1")
print("csv ok")
