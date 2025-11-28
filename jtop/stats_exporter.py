#!/usr/bin/env python3
import json
import os
import time
from jtop import jtop

OUT_PATH = os.environ.get("JTOP_EXPORT_PATH", "/run/jtop/jtop_stats.json")

def make_serializable(stats: dict) -> dict:
    out = {}
    for k, v in stats.items():
        if isinstance(v, (int, float, bool, str, list, dict)) or v is None:
            out[k] = v
        else:
            out[k] = str(v)
    return out

def main():
    folder = os.path.dirname(OUT_PATH)
    if folder and not os.path.isdir(folder):
        try:
            os.makedirs(folder, exist_ok=True)
        except OSError:
            pass
    with jtop() as jetson:
        while jetson.ok():
            stats = make_serializable(jetson.stats)
            tmp = OUT_PATH + ".tmp"
            with open(tmp, "w") as f:
                json.dump(stats, f)
                f.write("\n")
            os.replace(tmp, OUT_PATH)
            try:
                os.chmod(OUT_PATH, 0o644)
            except OSError:
                pass
            time.sleep(1.0)

if __name__ == "__main__":
    main()
