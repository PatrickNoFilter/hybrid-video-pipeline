import subprocess
from pathlib import Path
PD=Path('/home/desktop/Work/OpenMontage/projects/vietnam-indonesia-gdp')
src=PD/'assets/music/background.mp3'
out=PD/'assets/music/background_loop.mp3'
L=168.0          # clean source length before the silent tail
T=243.063833
fade=4.0
seg2=T-L+fade
fc=(f"[0:a]atrim=0:{L},asetpts=PTS-STARTPTS,volume=1,alimiter=limit=0.95[src];"
    f"[src]asplit=2[a][b];"
    f"[a]atrim=0:{L},asetpts=PTS-STARTPTS[seg1];"
    f"[b]atrim=0:{seg2:.3f},asetpts=PTS-STARTPTS[seg2];"
    f"[seg1][seg2]acrossfade=d={fade}:c1=tri:c2=tri[out]")
subprocess.run(['ffmpeg','-y','-v','error','-i',str(src),'-filter_complex',fc,'-map','[out]',
  '-c:a','libmp3lame','-q:a','2',str(out)],check=True)
r=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(out)],capture_output=True,text=True)
print("loop duration",r.stdout.strip(),"target",T)
for a,b in [(160,170),(170,180),(180,190),(190,200),(235,242)]:
    rr=subprocess.run(["ffmpeg","-v","info","-ss",str(a),"-t",str(b-a),"-i",str(out),"-af","volumedetect","-f","null","-"],capture_output=True,text=True)
    m=[l for l in rr.stderr.splitlines() if "mean_volume" in l]
    print(f" {a}-{b}: {m[0].split(':')[-1].strip() if m else '?'}")
