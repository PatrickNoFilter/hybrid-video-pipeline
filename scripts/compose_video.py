import json, subprocess, time, os
from pathlib import Path
OM='/home/desktop/Work/OpenMontage'; PID="vietnam-indonesia-gdp"; PD=Path(OM)/'projects'/PID
edit=json.load(open(PD/'artifacts/edit_decisions.json'))
REND=PD/'renders'; REND.mkdir(parents=True,exist_ok=True)
listf=PD/'assets/concat_edit.txt'
lines=[]
for c in edit['cuts']:
    p=PD/c['source']
    assert p.exists(), p
    lines.append(f"file '{p}'")
listf.write_text("\n".join(lines))
vid=REND/'video_only.mp4'
t0=time.time()
print("concatenating",len(edit['cuts']),"clips")
subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(listf),
  '-an','-c:v','libx264','-preset','veryfast','-crf','20','-r','30','-vf','scale=1920:1080,setsar=1',str(vid)],check=True)
print("video assembled",round(time.time()-t0,1),"s")

narr=PD/'assets/audio/narration_full.mp3'
music=PD/'assets/music/background.mp3'
sub=PD/'assets/subtitles.srt'
final=REND/'final.mp4'
dur=json.load(open(PD/'artifacts/script.json'))['total_duration_seconds']
fade_out_start=max(0,dur-5)
style="FontName=Liberation Sans,FontSize=30,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=3,Alignment=2,MarginV=45"
vf=f"subtitles='{sub}':force_style='{style}'"
fc=(f"[1:a]volume=1.0[n];[2:a]volume=0.12,afade=t=in:st=0:d=2,afade=t=out:st={fade_out_start}:d=3[m];"
    f"[n][m]amix=inputs=2:duration=first:dropout_transition=0[a]")
print("muxing audio + subtitles")
subprocess.run(['ffmpeg','-y','-v','error','-i',str(vid),'-i',str(narr),'-i',str(music),
  '-filter_complex',fc,'-map','0:v','-map','[a]','-vf',vf,
  '-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',
  '-shortest',str(final)],check=True)
print("FINAL",final,final.stat().st_size,"bytes",round(time.time()-t0,1),"s total")
