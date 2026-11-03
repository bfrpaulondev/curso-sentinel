#!/usr/bin/env python3
"""Envia as linhas novas de api-loja/logs/api.jsonl para a tabela LojaApi_CL do Kusto.
No Sentinel real isto seria feito pela Logs Ingestion API (Módulo 3)."""
import os, json, csv, io
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
url = os.environ.get("KUSTO_URL", "http://localhost:8080"); db = os.environ.get("KUSTO_DB", "Loja")
kc = KustoClient(KustoConnectionStringBuilder.with_no_authentication(url))
base = os.path.dirname(os.path.abspath(__file__)); log = os.path.join(base, "..", "..", "api-loja", "logs", "api.jsonl")
pos_f = log + ".enviado"; pos = int(open(pos_f).read()) if os.path.exists(pos_f) else 0
linhas = open(log).read().splitlines()[pos:]
buf = io.StringIO(); w = csv.writer(buf, lineterminator="\n")
for l in linhas:
    d = json.loads(l); w.writerow([d["TimeGenerated"], d["Service"], d["Method"], d["Route"], d["StatusCode"], d["DurationMs"], d["ClientIP"], json.dumps(d["Properties"])])
if linhas: kc.execute_mgmt(db, ".ingest inline into table LojaApi_CL with (format='csv') <|\n" + buf.getvalue())
open(pos_f, "w").write(str(pos + len(linhas)))
print(f"{len(linhas)} eventos enviados para LojaApi_CL")
