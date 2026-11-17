import subprocess
from pathlib import Path
PD=Path('/home/desktop/Work/OpenMontage/projects/vietnam-indonesia-gdp')
src=PD/'assets/music/background.mp3'
out=PD/'assets/music/background_loop.mp3'
L=191.692354
T=243.063833
fade=4.0
seg2=T-L+fade
fc=(f"[0:a]asplit=2[a][b];"
    f"[a]atrim=0:{L},asetpts=PTS-STARTPTS[seg1];"
    f"[b]atrim=0:{seg2:.3f},asetpts=PTS-STARTPTS[seg2];"
    f"[seg1][seg2]acrossfade=d={fade}:c1=tri:c2=tri[out]")
subprocess.run(['ffmpeg','-y','-v','error','-i',str(src),'-filter_complex',fc,'-map','[out]',
  '-c:a','libmp3lame','-q:a','2',str(out)],check=True)
r=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(out)],capture_output=True,text=True)
print("looped music duration",r.stdout.strip(),"target",T)
