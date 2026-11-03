#!/usr/bin/env python3
"""Cria o banco 'Loja' e carrega as 3 tabelas a partir dos CSV (ingestão inline, em lotes)."""
import os, csv, io
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
url = os.environ.get("KUSTO_URL", "http://localhost:8080"); db = os.environ.get("KUSTO_DB", "Loja")
kcsb = KustoConnectionStringBuilder.with_no_authentication(url) if url.startswith("http://") else KustoConnectionStringBuilder.with_az_cli_authentication(url)
c = KustoClient(kcsb)
if url.startswith("http://localhost"):   # só no emulador: criar o banco
    c.execute_mgmt("NetDefaultDB", f".create database {db} persist (@'/kustodata/dbs/{db}/md', @'/kustodata/dbs/{db}/data') ifnotexists")
SCHEMA = {
 "SigninLogs": "TimeGenerated:datetime, UserPrincipalName:string, AppDisplayName:string, IPAddress:string, Country:string, City:string, ResultType:string, ResultDescription:string, OperatingSystem:string",
 "LojaApi_CL": "TimeGenerated:datetime, Service:string, Method:string, Route:string, StatusCode:int, DurationMs:int, ClientIP:string, Properties:dynamic",
 "Syslog": "TimeGenerated:datetime, Computer:string, Facility:string, SeverityLevel:string, ProcessName:string, SyslogMessage:string"}
here = os.path.dirname(os.path.abspath(__file__))
for tbl, sch in SCHEMA.items():
    c.execute_mgmt(db, f".drop table {tbl} ifexists"); c.execute_mgmt(db, f".create table {tbl} ({sch})")
    rows = list(csv.reader(open(os.path.join(here, f"{tbl}.csv"))))[1:]
    for i in range(0, len(rows), 400):
        buf = io.StringIO(); csv.writer(buf, lineterminator="\n").writerows(rows[i:i+400])
        c.execute_mgmt(db, f".ingest inline into table {tbl} with (format='csv') <|\n" + buf.getvalue())
    n = c.execute(db, f"{tbl} | count").primary_results[0].raw_rows[0][0]
    print(f"{tbl}: {n} linhas")
