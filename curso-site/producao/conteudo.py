import importlib.util, sys, os
B = os.path.dirname(os.path.abspath(__file__))
def load(n):
    spec = importlib.util.spec_from_file_location(n, f"{B}/content/{n}.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m.MOD
MODS = [load("m0"), load("m2"), load("m4")]
AULAS = [(m, a) for m in MODS for a in m["aulas"]]
