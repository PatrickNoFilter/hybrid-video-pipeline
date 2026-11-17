import asyncio, json, sys, subprocess
from pathlib import Path
sys.path.insert(0, '/home/desktop/Work/MoneyPrinterTurbo')
import edge_tts

PID = "vietnam-indonesia-gdp"
PD = Path('/home/desktop/Work/OpenMontage/projects') / PID
AUD = PD / "assets/audio/sections"
AUD.mkdir(parents=True, exist_ok=True)
script = json.load(open(PD / "artifacts/script.json"))

def dur(p):
    r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",str(p)],capture_output=True,text=True)
    return round(float(r.stdout.strip()),2)

async def main():
    results=[]
    for s in script["sections"]:
        p = AUD / f'{s["id"]}.mp3'
        if not p.exists():
            await edge_tts.Communicate(s["text"], "id-ID-GadisNeural", rate="+0%", volume="+0%").save(str(p))
        d = dur(p)
        planned = round(s["end_seconds"]-s["start_seconds"],2)
        results.append({"id":s["id"],"actual":d,"planned":planned,"delta":round(d-planned,2)})
    return results

res = asyncio.run(main())
print("id     actual  planned  delta")
for r in res: print(f'{r["id"]:5s} {r["actual"]:7.2f} {r["planned"]:8.2f} {r["delta"]:+.2f}')
print("TOTAL actual", round(sum(r["actual"] for r in res),2), "planned", script["total_duration_seconds"])
json.dump(res, open(PD/"artifacts/tts_timings.json","w"), indent=2)
