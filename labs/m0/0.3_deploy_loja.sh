#!/usr/bin/env bash
# 0.3 — Deploy da Loja Pixel no Azure. PRECISA de 'az login' numa subscrição tua. Custa dinheiro (plano B1): apaga no fim!
set -euo pipefail
RG=rg-curso-sentinel; LOC=brazilsouth
az group create -n $RG -l $LOC -o none
az deployment group create -g $RG -f sentinel.bicep -o table
az deployment group create -g $RG -f loja.bicep -o table
# utilizadores fictícios no Entra ID (precisa de permissão de User Administrator)
DOM=$(az rest --method get --url https://graph.microsoft.com/v1.0/domains --query "value[?isDefault].id" -o tsv)
for u in ana.souza joao.pereira marina.lopes; do
  az ad user create --display-name "$u" --user-principal-name "$u@$DOM" --password "$(openssl rand -base64 18)" --force-change-password-next-sign-in true -o none
done
echo "Pronto. Para apagar tudo: az group delete -n $RG --yes"
