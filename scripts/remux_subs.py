import json, subprocess
from pathlib import Path
PD=Path('/home/desktop/Work/OpenMontage/projects/vietnam-indonesia-gdp')
vid=PD/'renders/video_only.mp4'; narr=PD/'assets/audio/narration_full.mp3'
music=PD/'assets/music/background.mp3'; sub=PD/'assets/subtitles.srt'
final=PD/'renders/final.mp4'
dur=json.load(open(PD/'artifacts/script.json'))['total_duration_seconds']
# ASS defaults to PlayResY 288 -> FontSize 30 renders ~112px at 1080p. Use 13 -> ~48px.
style="FontName=Liberation Sans,FontSize=13,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=40"
vf=f"subtitles='{sub}':force_style='{style}'"
fo=max(0,dur-5)
fc=(f"[1:a]volume=1.0[n];[2:a]volume=0.12,afade=t=in:st=0:d=2,afade=t=out:st={fo}:d=3[m];"
    f"[n][m]amix=inputs=2:duration=first:dropout_transition=0[a]")
subprocess.run(['ffmpeg','-y','-v','error','-i',str(vid),'-i',str(narr),'-i',str(music),
  '-filter_complex',fc,'-map','0:v','-map','[a]','-vf',vf,
  '-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',
  '-shortest',str(final)],check=True)
print("remuxed",final.stat().st_size)
