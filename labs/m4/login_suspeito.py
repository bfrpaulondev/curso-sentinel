#!/usr/bin/env python3
"""Gera um evento SINTÉTICO de login suspeito no SigninLogs (não há Entra ID neste laboratório):
8 falhas e 1 sucesso para a mesma conta, a partir de um país onde a Loja Pixel não opera."""
import os, datetime as dt
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
kc = KustoClient(KustoConnectionStringBuilder.with_no_authentication(os.environ.get("KUSTO_URL", "http://localhost:8080")))
agora = dt.datetime.now(dt.timezone.utc); rows = []
for i in range(9):
    ok = i == 8
    rows.append(f"{(agora + dt.timedelta(seconds=i*20)).strftime('%Y-%m-%dT%H:%M:%SZ')},marina.lopes@lojapixel.com.br,Azure Portal,198.51.100.99,RU,Moscow,{'0' if ok else '50126'},{'Success' if ok else 'Invalid username or password'},Linux")
kc.execute_mgmt("Loja", ".ingest inline into table SigninLogs with (format='csv') <|\n" + "\n".join(rows))
print("9 eventos sintéticos inseridos em SigninLogs (marina.lopes, IP 198.51.100.99, RU)")
