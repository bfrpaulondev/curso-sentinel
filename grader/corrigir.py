#!/usr/bin/env python3
"""Corretor automático do Teste do Módulo 2.
Executa as TUAS consultas (respostas/m2/q01.kql … q10.kql) num Kusto real e compara com
os resultados esperados (grader/esperado/*.csv, gerados a partir de um Kusto real).
Compara colunas por posição e linhas sem depender da ordem; números são comparados com 2 casas."""
import os, sys, csv, subprocess, glob
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
url = os.environ.get("KUSTO_URL", "http://localhost:8080"); db = os.environ.get("KUSTO_DB", "Loja")
kc = KustoClient(KustoConnectionStringBuilder.with_no_authentication(url) if url.startswith("http://") else KustoConnectionStringBuilder.with_az_cli_authentication(url))
base = os.path.dirname(os.path.abspath(__file__)); pasta = sys.argv[1] if len(sys.argv) > 1 else os.path.join(base, "..", "respostas", "m2")
def norm(v):
    v = "" if v is None else str(v).strip()
    try: return f"{float(v):.2f}"
    except ValueError: return v.replace(".0000000Z", "Z").replace("+00:00", "Z").replace(" ", "T") if v[:4].isdigit() and "-" in v[:8] else v
nota = 0
for i in range(1, 11):
    q = f"q{i:02d}"; exp = list(csv.reader(open(os.path.join(base, "esperado", f"m2_{q}.csv"))))
    f = os.path.join(pasta, f"{q}.kql")
    if not os.path.exists(f): print(f"{q}: ✗ ficheiro em falta"); continue
    try:
        t = kc.execute(db, open(f).read()).primary_results[0]
        got = [[norm(c) for c in r] for r in t.raw_rows]
    except Exception as e:
        print(f"{q}: ✗ erro ao executar: {str(e)[:120]}"); continue
    want = [[norm(c) for c in r] for r in exp[1:]]
    if len(got) != len(want): print(f"{q}: ✗ devolveu {len(got)} linhas, esperadas {len(want)}"); continue
    if sorted(map(tuple, got)) == sorted(map(tuple, want)): print(f"{q}: ✓"); nota += 1
    else: print(f"{q}: ✗ número de linhas certo ({len(want)}), mas os valores não batem")
print(f"\nNota: {nota}/10 — {'APROVADO (mínimo 7)' if nota >= 7 else 'ainda não: mínimo 7'}")
sys.exit(0 if nota >= 7 else 1)
