// API da Loja Pixel (fictícia) — Node.js puro, sem dependências.
// Cada pedido gera uma linha JSON em logs/api.jsonl, no formato da tabela LojaApi_CL.
const http = require("http"), fs = require("fs"), path = require("path");
const LOG = path.join(__dirname, "logs", "api.jsonl");
fs.mkdirSync(path.dirname(LOG), { recursive: true });
const USERS = { "carla@cliente.com": "Senha#Forte2026", "rui@cliente.com": "outraSenha!9" };
function log(req, status, t0, extra = {}) {
  const ip = req.headers["x-forwarded-for"] || req.socket.remoteAddress;
  const linha = { TimeGenerated: new Date().toISOString(), Service: "api-loja", Method: req.method, Route: req.url.split("?")[0],
    StatusCode: status, DurationMs: Date.now() - t0, ClientIP: ip,
    Properties: { userAgent: req.headers["user-agent"] || "", region: "local-lab", tags: ["web"], ...extra } };
  fs.appendFileSync(LOG, JSON.stringify(linha) + "\n");
}
http.createServer((req, res) => {
  const t0 = Date.now(); let body = "";
  req.on("data", (c) => (body += c));
  req.on("end", () => {
    if (req.method === "POST" && req.url === "/api/login") {
      let d = {}; try { d = JSON.parse(body || "{}"); } catch {}
      const ok = USERS[d.email] && USERS[d.email] === d.senha;
      log(req, ok ? 200 : 401, t0, { login: d.email || "" });
      res.writeHead(ok ? 200 : 401, { "Content-Type": "application/json" });
      return res.end(JSON.stringify(ok ? { token: "demo" } : { erro: "credenciais inválidas" }));
    }
    if (req.method === "GET" && req.url.startsWith("/api/produtos")) {
      log(req, 200, t0); res.writeHead(200, { "Content-Type": "application/json" });
      return res.end(JSON.stringify([{ id: 101, nome: "Teclado mecânico", preco: 349.9 }]));
    }
    log(req, 404, t0); res.writeHead(404); res.end();
  });
}).listen(3000, () => console.log("api-loja ouvindo em http://localhost:3000"));
