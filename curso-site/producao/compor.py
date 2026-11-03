#!/usr/bin/env python3
import json, os, sys, subprocess, re, glob
B = os.path.dirname(os.path.abspath(__file__)); OUT = f"{B}/out"; os.makedirs(f"{OUT}/videos", exist_ok=True)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def ts(t): h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return f"{h:02d}:{m:02d}:{s:06.3f}"
def vtt(tl, f):
    out = ["WEBVTT", ""]; n = 1
    for seg in tl:
        frases = [x.strip() for x in re.split(r"(?<=[.!?:])\s+", seg["say"]) if x.strip()]
        tot = sum(len(x) for x in frases); t = seg["t"]
        for fr in frases:
            d = seg["dur"] * len(fr) / tot
            # quebra em blocos de até ~90 caracteres
            partes, cur = [], ""
            for w in fr.split():
                if len(cur) + len(w) > 88: partes.append(cur); cur = w
                else: cur = (cur + " " + w).strip()
            partes.append(cur); pt = t
            for p in partes:
                pd = d * len(p) / max(1, len(fr)); out += [str(n), f"{ts(pt)} --> {ts(pt + pd)}", p, ""]; n += 1; pt += pd
            t += d
    open(f, "w").write("\n".join(out))
def compor(j):
    J = json.load(open(j)); aid = J["aula"]; raw = j.replace(".json", ".mkv"); dst = f"{OUT}/videos/aula_{aid}.mp4"
    ins, filt = ["-i", raw], []
    for i, seg in enumerate(J["tl"]):
        ins += ["-i", seg["mp3"]]; ms = int(seg["t"] * 1000); filt.append(f"[{i+1}:a]adelay={ms}|{ms},aformat=channel_layouts=stereo[a{i}]")
    n = len(J["tl"])
    filt.append("".join(f"[a{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0,loudnorm=I=-16:TP=-1.5[aout]")
    filt.append(f"[0:v]drawtext=fontfile={FONT}:text='@bfrpaulondev':fontsize=30:fontcolor=white@0.55:shadowcolor=black@0.5:shadowx=2:shadowy=2:x=w-tw-36:y=h-th-60[vout]")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *ins, "-filter_complex", ";".join(filt), "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "slow", "-crf", "28", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", "-shortest", dst], check=True)
    vtt(J["tl"], dst.replace(".mp4", ".vtt"))
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", dst]))
    print(aid, f"{int(d//60)}:{int(d%60):02d}", f"{os.path.getsize(dst)/1e6:.1f} MB", flush=True)
if __name__ == "__main__":
    for j in sorted(glob.glob(f"{OUT}/raw/aula_*.json")):
        if len(sys.argv) > 1 and not any(f"aula_{a}.json" in j for a in sys.argv[1:]): continue
        compor(j)
