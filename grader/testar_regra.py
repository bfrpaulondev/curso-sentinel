#!/usr/bin/env python3
"""Teste prático do Módulo 4: a TUA regra tem de gerar um incidente perante um ataque simulado.
Uso: python3 grader/testar_regra.py minha_regra.yaml   (com a api-loja e o Kusto a correr)"""
import sys, os, random, subprocess, json
regra = os.path.abspath(sys.argv[1]); m4 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "labs", "m4")
ip = f"203.0.113.{random.randint(100, 250)}"
print(f"1) Ataque simulado a partir de {ip}…"); subprocess.run(["bash", "ataque_forca_bruta.sh"], cwd=m4, env={**os.environ, "IP": ip}, capture_output=True, check=True)
print("2) A enviar logs para o Kusto…"); subprocess.run(["python3", "enviar_logs.py"], cwd=m4, check=True)
print("3) A correr a tua regra no simulador…"); out = subprocess.run(["python3", "motor_regras_local.py", regra], cwd=m4, capture_output=True, text=True); print(out.stdout)
inc = json.load(open(os.path.join(m4, "incidentes.json")))
ok = any(e.get("Address") == ip for i in inc for a in i["alertas"] for e in a["entidades"])
print("✓ APROVADO: a regra gerou um incidente com a entidade IP do atacante." if ok else f"✗ Ainda não: nenhum incidente com a entidade IP={ip}.")
sys.exit(0 if ok else 1)
