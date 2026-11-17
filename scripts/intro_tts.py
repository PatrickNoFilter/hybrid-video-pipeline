import asyncio, subprocess, sys
from pathlib import Path
sys.path.insert(0, '/home/desktop/Work/MoneyPrinterTurbo')
import edge_tts

PD=Path('/home/desktop/Work/OpenMontage/projects/vietnam-indonesia-gdp')
AUD=PD/'assets/audio/sections'; AUD.mkdir(parents=True,exist_ok=True)
texts={
 "s0a":"Liputan ekonomi Asia. IMF memproyeksikan PDB per kapita Vietnam menyalip Indonesia pada tahun dua ribu dua puluh enam. Namun, data aktualnya masih sangat ketat.",
 "s0b":"Tujuh triwulan: tumbuhnya Vietnam sudah menyalip Indonesia, ekonominya belum."
}
async def main():
    for k,t in texts.items():
        p=AUD/f'{k}.mp3'
        await edge_tts.Communicate(t,"id-ID-GadisNeural",rate="+0%",volume="+0%").save(str(p))
        r=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",str(p)],capture_output=True,text=True)
        print(k, r.stdout.strip(), t)
asyncio.run(main())
