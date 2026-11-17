import asyncio, json, sys, subprocess, os
from pathlib import Path
sys.path.insert(0, '/home/desktop/Work/MoneyPrinterTurbo')
import edge_tts

PID = "vietnam-indonesia-gdp"
PD = Path('/home/desktop/Work/OpenMontage/projects') / PID
AUD = PD / "assets/audio/sections"
AUD.mkdir(parents=True, exist_ok=True)
script = json.load(open(PD / "artifacts/script.json"))
s7 = next(s for s in script["sections"] if s["id"] == "s7")

path = AUD / "s7_sample.mp3"
asyncio.run(edge_tts.Communicate(s7["text"], "id-ID-GadisNeural", rate="+0%", volume="+0%").save(str(path)))
r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)], capture_output=True, text=True)
print("sample:", path.name, "bytes", path.stat().st_size, "duration", r.stdout.strip(), "target", s7["end_seconds"]-s7["start_seconds"])
print(s7["text"])
