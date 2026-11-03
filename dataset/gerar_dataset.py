"""Dataset fixo da Loja Pixel (fictícia) para o curso. Semente fixa: sempre os mesmos dados.
Tabelas com esquema inspirado no Sentinel: SigninLogs, LojaApi_CL, Syslog."""
import random, csv, datetime as dt
random.seed(2026)
T0 = dt.datetime(2026, 10, 20, 8, 0, tzinfo=dt.timezone.utc)
def t(minutos, seg=None): return (T0 + dt.timedelta(minutes=minutos, seconds=random.randint(0, 59) if seg is None else seg)).strftime("%Y-%m-%dT%H:%M:%SZ")
usuarios = ["ana.souza", "bruno.lima", "carla.mendes", "diego.rocha", "elisa.prado", "fabio.nunes", "gabi.torres", "henrique.alves",
            "isabela.costa", "joao.pereira", "karen.dias", "lucas.martins", "marina.lopes", "nina.reis", "otavio.ramos", "paula.freitas"]
upn = lambda u: f"{u}@lojapixel.com.br"
cidades = [("BR", "São Paulo"), ("BR", "Campinas"), ("BR", "Rio de Janeiro"), ("BR", "Belo Horizonte")]
apps = ["Microsoft Teams", "Outlook", "Azure Portal", "GitHub Enterprise"]
# ---------- SigninLogs ----------
S = []
for i in range(900):
    u = random.choice(usuarios); c = random.choice(cidades); m = random.randint(0, 1439)
    rt = "0" if random.random() > 0.04 else random.choice(["50126", "50074"])
    S.append([t(m), upn(u), random.choice(apps), f"10.20.{random.randint(1,9)}.{random.randint(2,250)}", c[0], c[1], rt,
              "Success" if rt == "0" else ("Invalid username or password" if rt == "50126" else "Strong authentication is required"), "Windows 11" if random.random() > .3 else "macOS"])
# ataque 1: password spray (1 IP, muitas contas) às 02:10–02:40
for i, u in enumerate(usuarios * 2):
    S.append([t(18*60 + 10 + i, 5), upn(u), "Azure Portal", "198.51.100.23", "NL", "Amsterdam", "50126", "Invalid username or password", "Linux"])
# ...e um sucesso na conta do joao a seguir
S.append([t(18*60 + 44, 12), upn("joao.pereira"), "Azure Portal", "198.51.100.23", "NL", "Amsterdam", "0", "Success", "Linux"])
S.sort()
with open("SigninLogs.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["TimeGenerated", "UserPrincipalName", "AppDisplayName", "IPAddress", "Country", "City", "ResultType", "ResultDescription", "OperatingSystem"]); w.writerows(S)
# ---------- LojaApi_CL (logs da API Node.js, em JSON) ----------
import json
A = []
rotas = [("GET", "/api/produtos", 200), ("GET", "/api/produtos/{id}", 200), ("POST", "/api/carrinho", 201), ("POST", "/api/checkout", 201), ("POST", "/api/login", 200)]
for i in range(2400):
    met, rota, st = random.choice(rotas); m = random.randint(0, 1439)
    if rota.endswith("{id}"): rota = rota.replace("{id}", str(random.randint(100, 180)))
    if random.random() < 0.03: st = random.choice([404, 500])
    if rota == "/api/login" and random.random() < 0.08: st = 401
    cli = f"177.{random.randint(10,200)}.{random.randint(0,255)}.{random.randint(1,254)}"
    props = {"userAgent": random.choice(["Mozilla/5.0 (Windows NT 10.0)", "Mozilla/5.0 (iPhone)", "Mozilla/5.0 (Macintosh)"]), "region": "brazilsouth",
             "tags": random.sample(["web", "mobile", "promo", "black-friday"], k=random.randint(1, 2))}
    A.append([t(m), "api-loja", met, rota, st, random.randint(8, 320) if st < 500 else random.randint(900, 3000), cli, json.dumps(props, ensure_ascii=False)])
# ataque 2: credential stuffing na API (03:00–03:06), 140 tentativas, 2 sucessos
for i in range(140):
    st = 200 if i in (97, 131) else 401
    props = {"userAgent": "python-requests/2.31", "region": "brazilsouth", "tags": ["web"], "login": f"cliente{random.randint(1000,9999)}@mail.com"}
    A.append([t(19*60 + i // 25, (i * 7) % 60), "api-loja", "POST", "/api/login", st, random.randint(40, 90), "203.0.113.77", json.dumps(props)])
A.sort()
with open("LojaApi_CL.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["TimeGenerated", "Service", "Method", "Route", "StatusCode", "DurationMs", "ClientIP", "Properties"]); w.writerows(A)
# ---------- Syslog (VM da API) ----------
Y = []
for i in range(500):
    m = random.randint(0, 1439)
    p, msg = random.choice([("sshd", f"Accepted publickey for deploy from 10.20.1.{random.randint(2,40)} port {random.randint(30000,60000)} ssh2"),
                            ("CRON", "pam_unix(cron:session): session opened for user root"), ("node", "api-loja listening on :3000"),
                            ("systemd", "Started Daily apt download activities.")])
    Y.append([t(m), "vm-api-01", "auth" if p == "sshd" else "daemon", "info", p, msg])
for i in range(35):   # força bruta SSH 04:15
    Y.append([t(20*60 + 15 + i // 12, (i * 5) % 60), "vm-api-01", "authpriv", "notice", "sshd", f"Failed password for invalid user admin from 192.0.2.150 port {50000+i} ssh2"])
Y.sort()
with open("Syslog.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["TimeGenerated", "Computer", "Facility", "SeverityLevel", "ProcessName", "SyslogMessage"]); w.writerows(Y)
print("SigninLogs", len(S), "| LojaApi_CL", len(A), "| Syslog", len(Y))
