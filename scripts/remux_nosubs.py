import json, subprocess
from pathlib import Path
PD=Path('/home/desktop/Work/OpenMontage/projects/vietnam-indonesia-gdp')
vid=PD/'renders/video_only.mp4'; narr=PD/'assets/audio/narration_full.mp3'
music=PD/'assets/music/background.mp3'; final=PD/'renders/final.mp4'
dur=json.load(open(PD/'artifacts/script.json'))['total_duration_seconds']
fo=max(0,dur-5)
fc=(f"[1:a]volume=1.0[n];[2:a]volume=0.12,afade=t=in:st=0:d=2,afade=t=out:st={fo}:d=3[m];"
    f"[n][m]amix=inputs=2:duration=first:dropout_transition=0[a]")
subprocess.run(['ffmpeg','-y','-v','error','-i',str(vid),'-i',str(narr),'-i',str(music),
  '-filter_complex',fc,'-map','0:v','-map','[a]',
  '-c:v','copy','-c:a','aac','-b:a','192k','-shortest',str(final)],check=True)
print("final no subtitles:",final.stat().st_size)
