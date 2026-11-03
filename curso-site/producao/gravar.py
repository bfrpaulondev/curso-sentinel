#!/usr/bin/env python3
"""Grava cada aula: diagrama rough.js animado (Chrome) + demo real no code-server (Xvfb :9, ffmpeg x11grab).
Áudio: edge-tts pt-BR, posicionado nos instantes reais de cada segmento."""
import os, sys, json, time, subprocess, asyncio, re, signal
sys.path.insert(0, os.path.dirname(__file__)); from conteudo import AULAS, B
import edge_tts
from playwright.sync_api import sync_playwright
D = ":9"; ENV = {**os.environ, "DISPLAY": D}
OUT = f"{B}/out"; os.makedirs(f"{OUT}/raw", exist_ok=True); os.makedirs(f"{OUT}/tts", exist_ok=True); os.makedirs(f"{OUT}/shots", exist_ok=True)
VOZ = {"m0": "pt-BR-AntonioNeural", "m2": "pt-BR-FranciscaNeural", "m4": "pt-BR-AntonioNeural"}
EDIT = (1125, 280); TERM = (1125, 860)
def x(*a): subprocess.run(["xdotool", *map(str, a)], env=ENV)
def dur(f): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
def tts(txt, voz, f):
    if os.path.exists(f) and os.path.getsize(f) > 1000: return
    for i in range(4):
        r = subprocess.run([sys.executable, "-m", "edge_tts", "--voice", voz, "--rate=-3%", "--pitch=-1Hz", "--text", txt, "--write-media", f], capture_output=True, text=True)
        if r.returncode == 0 and os.path.getsize(f) > 1000: return
        print("tts retry", r.stderr[-200:]); time.sleep(3)
    raise SystemExit("tts falhou")
def typ(s, delay=28): subprocess.run(["xdotool", "type", "--delay", str(delay), "--", s], env=ENV)
def act(a):
    k = a[0]
    if k == "open":
        x("mousemove", *EDIT, "click", 1); time.sleep(.2); x("key", "ctrl+p"); time.sleep(.6); typ(a[1], 22); time.sleep(.8); x("key", "Return"); time.sleep(1.2)
    elif k == "scroll":
        x("mousemove", *EDIT, "click", 1); x("key", "ctrl+g"); time.sleep(.4); typ(str(a[1])); x("key", "Return"); time.sleep(.3); x("key", "ctrl+l")  # seleciona a linha (destaque)
    elif k == "term":
        x("mousemove", *TERM, "click", 1); time.sleep(.2); x("key", "ctrl+l"); time.sleep(.2); typ(a[1]); time.sleep(.3); x("key", "Return"); time.sleep(2.2)
    elif k == "wait": time.sleep(a[1])
def preparar():
    x("mousemove", *EDIT, "click", 1); x("key", "ctrl+k"); x("key", "w"); time.sleep(.5)
    x("mousemove", *TERM, "click", 1); x("key", "ctrl+l"); time.sleep(.3)
def gravar(m, a, pw):
    aid = a["id"]; voz = VOZ[m["id"]]; segs = []
    for i, s in enumerate(a["diagrama"]): segs.append(("d", s, f"{OUT}/tts/{aid}_d{i}.mp3"))
    for i, s in enumerate(a["demo"]): segs.append(("v", s, f"{OUT}/tts/{aid}_v{i}.mp3"))
    for _, s, f in segs: tts(s["say"], voz, f)
    if aid in ("0.3", "4.1"):
        subprocess.run("pkill -f '[n]ode api-loja/server'; rm -f /workspace/cursos/sentinel-site/repo/api-loja/logs/api.jsonl /workspace/cursos/sentinel-site/repo/api-loja/logs/*.enviado", shell=True)
    preparar()
    diag = subprocess.Popen(["google-chrome", "--user-data-dir=/tmp/chromediag", "--force-device-scale-factor=1", "--allow-file-access-from-files", "--remote-debugging-port=9333", "--no-first-run", "--window-position=0,0", "--window-size=1920,1080", f"--app=file://{B}/diag/diagram.html?d={aid}"], env=ENV, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(4)
    br = pw.chromium.connect_over_cdp("http://127.0.0.1:9333"); pg = [p for c in br.contexts for p in c.pages if "diagram.html" in p.url][0]
    raw = f"{OUT}/raw/aula_{aid}.mkv"
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "x11grab", "-framerate", "30", "-video_size", "1920x1080", "-draw_mouse", "1", "-i", D, "-c:v", "libx264", "-preset", "ultrafast", "-crf", "16", raw], stdin=subprocess.PIPE, env=ENV)
    t0 = time.time(); time.sleep(1.5); tl = []
    for kind, s, f in segs:
        if kind == "v" and diag:
            br.close(); diag.terminate(); diag.wait(); diag = None; time.sleep(1.0)
        ts = time.time() - t0; d = dur(f)
        if kind == "d": pg.evaluate("next()")
        else:
            for ac in s["act"]: act(ac)
        el = time.time() - t0 - ts
        if s.get("shot"):
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "x11grab", "-video_size", "1920x1080", "-i", D, "-frames:v", "1", f"{OUT}/shots/aula_{aid}_{len(tl)}.png"], env=ENV)
        time.sleep(max(0, d - el) + 0.7); tl.append({"t": round(ts, 3), "dur": d, "say": s["say"], "mp3": f, "kind": kind})
    time.sleep(1.2); ff.stdin.write(b"q"); ff.stdin.flush(); ff.wait()
    json.dump({"aula": aid, "titulo": a["titulo"], "tl": tl, "total": time.time() - t0}, open(f"{OUT}/raw/aula_{aid}.json", "w"), ensure_ascii=False, indent=1)
    print("gravada", aid, round(time.time() - t0, 1), "s", flush=True)
if __name__ == "__main__":
    only = sys.argv[1:]
    with sync_playwright() as pw:
        for m, a in AULAS:
            if only and a["id"] not in only: continue
            gravar(m, a, pw)
