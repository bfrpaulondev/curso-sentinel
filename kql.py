#!/usr/bin/env python3
"""Executa KQL num cluster Kusto REAL (emulador Kustainer local ou cluster gratuito do Azure Data Explorer).
Uso:  ./kql.py "SigninLogs | take 3"      |  ./kql.py -f consulta.kql  |  ./kql.py -f q.kql --csv saida.csv
Cluster: variável KUSTO_URL (padrão http://localhost:8080) e KUSTO_DB (padrão Loja).
Para o cluster gratuito do ADX: KUSTO_URL=https://<seu-cluster>.kusto.windows.net (login com 'az login')."""
import os, sys, csv, argparse
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
p = argparse.ArgumentParser(); p.add_argument("query", nargs="?"); p.add_argument("-f"); p.add_argument("--csv"); p.add_argument("--max", type=int, default=20)
a = p.parse_args()
url = os.environ.get("KUSTO_URL", "http://localhost:8080"); db = os.environ.get("KUSTO_DB", "Loja")
kcsb = KustoConnectionStringBuilder.with_no_authentication(url) if url.startswith("http://") else KustoConnectionStringBuilder.with_az_cli_authentication(url)
q = open(a.f).read() if a.f else a.query
client = KustoClient(kcsb)
try:
    res = client.execute_mgmt(db, q) if q.lstrip().startswith(".") else client.execute(db, q)
except Exception as e:
    msg = str(e); i = msg.find("Semantic error"); i = i if i >= 0 else msg.find("Syntax error")
    print("ERRO do Kusto:", (msg[i:] if i >= 0 else msg)[:300]); sys.exit(1)
t = res.primary_results[0]
cols = [c.column_name for c in t.columns]
rows = [[("" if v is None else str(v)) for v in r] for r in t.raw_rows]
if a.csv:
    with open(a.csv, "w", newline="") as f: w = csv.writer(f); w.writerow(cols); w.writerows(rows)
W = [min(48, max([len(c)] + [len(r[i]) for r in rows[:a.max]])) for i, c in enumerate(cols)]
line = lambda vals: " | ".join(v[:W[i]].ljust(W[i]) for i, v in enumerate(vals))
print(line(cols)); print("-+-".join("-" * w for w in W))
for r in rows[:a.max]: print(line(r))
print(f"\n({len(rows)} linha{'s' if len(rows)!=1 else ''})" + (f" — mostrando {a.max}" if len(rows) > a.max else ""))
