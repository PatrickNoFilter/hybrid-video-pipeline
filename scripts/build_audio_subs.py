import json, subprocess, re, shutil
from pathlib import Path

PID = "vietnam-indonesia-gdp"
PD = Path('/home/desktop/Work/OpenMontage/projects') / PID
AUD = PD / "assets/audio/sections"
script = json.load(open(PD / "artifacts/script.json"))

# 0.3s silence between sections, 2.0s final hold
sil = PD / "assets/audio/silence03.mp3"
sil2 = PD / "assets/audio/silence20.mp3"
for p, secs in [(sil, 0.3), (sil2, 2.0)]:
    subprocess.run(["ffmpeg","-y","-v","error","-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-t",str(secs),"-codec:a","libmp3lame",str(p)],check=True)

concat = PD / "assets/audio/concat.txt"
lines=[]
for i,s in enumerate(script["sections"]):
    lines.append(f"file '{AUD / (s['id']+'.mp3')}'".replace("\\","/"))
    lines.append(f"file '{sil}'".replace("\\","/"))
lines.append(f"file '{sil2}'".replace("\\","/"))
concat.write_text("\n".join(lines))
narr = PD / "assets/audio/narration_full.mp3"
subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",str(concat),"-c","copy",str(narr)],check=True)
r=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",str(narr)],capture_output=True,text=True)
print("narration_full.mp3 duration:", r.stdout.strip())

# Subtitles: split each section into sentences, distribute time by character count
def ts(t):
    h=int(t//3600); m=int((t%3600)//60); s=t%60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",", 1)
cues=[]
for s in script["sections"]:
    parts=[p.strip() for p in re.split(r'(?<=[.!?])\s+', s["text"]) if p.strip()]
    total_chars=sum(len(p) for p in parts)
    cursor=s["start_seconds"]
    for p in parts:
        d=(s["end_seconds"]-s["start_seconds"])*len(p)/total_chars
        cues.append((cursor, cursor+d, p))
        cursor+=d
srt=PD/"assets/subtitles.srt"
srt.write_text("\n".join(f"{i}\n{ts(a)} --> {ts(b)}\n{t}\n" for i,(a,b,t) in enumerate(cues,1)),encoding="utf-8")
print("subtitle cues:", len(cues))

# Music
music_src=Path("/home/desktop/Music/Background music News Investigating.mp3")
mdst=PD/"assets/music/background.mp3"
mdst.parent.mkdir(parents=True,exist_ok=True)
if music_src.exists():
    shutil.copy2(music_src,mdst)
    print("music copied:",mdst.stat().st_size,"bytes")
else:
    print("MUSIC MISSING")
