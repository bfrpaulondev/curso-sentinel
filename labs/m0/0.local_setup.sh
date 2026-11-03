#!/usr/bin/env bash
# Alternativa GRATUITA e sem conta: Kusto real (emulador Kustainer) + dataset da Loja Pixel + API local
set -euo pipefail
docker run -d --name kusto -p 8080:8080 -e ACCEPT_EULA=Y mcr.microsoft.com/azuredataexplorer/kustainer-linux:latest
echo "A aguardar o Kusto arrancar…"; until curl -s -X POST localhost:8080/v1/rest/mgmt -H 'Content-Type: application/json' -d '{"csl":".show version"}' >/dev/null; do sleep 3; done
pip install azure-kusto-data pyyaml
python3 ../../dataset/carregar_dataset.py
node ../../api-loja/server.js &
echo "Laboratório pronto: Kusto em http://localhost:8080 (banco Loja), API em http://localhost:3000"
