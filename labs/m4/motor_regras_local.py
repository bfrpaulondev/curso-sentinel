#!/usr/bin/env python3
"""SIMULADOR LOCAL do motor de regras agendadas — NÃO é o Microsoft Sentinel.
Faz o que o Sentinel faz com uma regra Scheduled, de forma simplificada:
 1) valida o YAML (campos obrigatórios, táticas e técnicas MITRE)
 2) corre a 'query' num Kusto REAL (emulador)
 3) aplica triggerOperator/triggerThreshold
 4) cria 1 alerta por linha (AlertPerResult) com entidades e custom details
 5) agrupa alertas em incidentes segundo groupingConfiguration (por entidades selecionadas)"""
import sys, os, json, re, yaml, uuid
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
TATICAS = {"Reconnaissance","ResourceDevelopment","InitialAccess","Execution","Persistence","PrivilegeEscalation","DefenseEvasion",
           "CredentialAccess","Discovery","LateralMovement","Collection","CommandAndControl","Exfiltration","Impact","ImpairProcessControl","InhibitResponseFunction"}
OBRIG = ["id","name","severity","queryFrequency","queryPeriod","triggerOperator","triggerThreshold","tactics","relevantTechniques","query","entityMappings","kind"]
def validar(r):
    erros = [f"campo em falta: {k}" for k in OBRIG if k not in r]
    erros += [f"tática inválida: {t}" for t in r.get("tactics", []) if t not in TATICAS]
    erros += [f"técnica inválida: {t}" for t in r.get("relevantTechniques", []) if not re.fullmatch(r"T\d{4}(\.\d{3})?", t)]
    if len(r.get("entityMappings", [])) > 10: erros.append("máximo de 10 entity mappings")
    return erros
kc = KustoClient(KustoConnectionStringBuilder.with_no_authentication(os.environ.get("KUSTO_URL", "http://localhost:8080")))
incidentes = []
for f in sys.argv[1:]:
    r = yaml.safe_load(open(f)); print(f"\n▶ Regra: {r['name']}  [{r['kind']}, a cada {r['queryFrequency']}, olhando {r['queryPeriod']}]")
    e = validar(r)
    if e: print("  ✗ YAML inválido:", "; ".join(e)); continue
    print(f"  ✓ YAML válido • MITRE: {', '.join(r['tactics'])} / {', '.join(r['relevantTechniques'])}")
    t = kc.execute("Loja", r["query"]).primary_results[0]; cols = [c.column_name for c in t.columns]
    rows = [dict(zip(cols, x)) for x in t.raw_rows]
    ops = {"gt": lambda a, b: a > b, "ge": lambda a, b: a >= b, "lt": lambda a, b: a < b, "eq": lambda a, b: a == b}
    if not ops[r["triggerOperator"]](len(rows), r["triggerThreshold"]): print(f"  · {len(rows)} resultados → sem alerta"); continue
    alertas = []
    for row in rows:
        ents = [{"tipo": m["entityType"], **{fm["identifier"]: str(row.get(fm["columnName"])) for fm in m["fieldMappings"]}} for m in r["entityMappings"]]
        det = {k: str(row.get(v)) for k, v in (r.get("customDetails") or {}).items()}
        nome = (r.get("alertDetailsOverride") or {}).get("alertDisplayNameFormat", r["name"])
        nome = re.sub(r"\{\{(\w+)\}\}", lambda m: str(row.get(m.group(1))), nome)
        alertas.append({"alerta": nome, "severidade": r["severity"], "entidades": ents, "detalhes": det})
    print(f"  ⚠ {len(alertas)} alerta(s)")
    g = r.get("incidentConfiguration", {}).get("groupingConfiguration", {})
    grupos = {}
    for a in alertas:
        if g.get("enabled"):
            sel = g.get("groupByEntities") if g.get("matchingMethod") == "Selected" else None
            chave = json.dumps([x for x in a["entidades"] if not sel or x["tipo"] in sel], sort_keys=True) if g.get("matchingMethod") != "AnyAlert" else "todos"
        else: chave = str(uuid.uuid4())
        grupos.setdefault(chave, []).append(a)
    for alist in grupos.values():
        inc = {"incidente": f"INC-{uuid.uuid4().hex[:6].upper()}", "titulo": r["name"], "severidade": r["severity"],
               "taticas": r["tactics"], "tecnicas": r["relevantTechniques"], "alertas": alist}
        incidentes.append(inc); print(f"  [INCIDENTE] {inc['incidente']}: {len(alist)} alerta(s) • entidades: " + ", ".join(f"{x['tipo']}={list(x.values())[1]}" for x in alist[0]["entidades"]))
json.dump(incidentes, open("incidentes.json", "w"), ensure_ascii=False, indent=1, default=str)
print(f"\nTotal: {len(incidentes)} incidente(s) → incidentes.json")
