import json, sys, os
sys.path.insert(0, os.path.dirname(__file__)); from conteudo import AULAS, B
from playwright.sync_api import sync_playwright
specs = {a["id"]: {"titulo": f"Aula {a['id']} · {a['titulo']}", "steps": a["diagrama"]} for m, a in AULAS}
open(f"{B}/diag/spec.js", "w").write("const SPECS=" + json.dumps(specs, ensure_ascii=False) + ";")
os.makedirs(f"{B}/out/diagramas", exist_ok=True)
only = sys.argv[1:] 
with sync_playwright() as p:
    br = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"]); pg = br.new_page(viewport={"width": 1920, "height": 1080})
    for m, a in AULAS:
        if only and a["id"] not in only: continue
        pg.goto(f"file://{B}/diag/diagram.html?d={a['id']}&all=1"); pg.wait_for_timeout(500)
        pg.screenshot(path=f"{B}/out/diagramas/aula_{a['id']}.png"); print("png", a["id"])
    br.close()
