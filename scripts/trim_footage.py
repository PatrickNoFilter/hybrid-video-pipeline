import json, subprocess
from pathlib import Path

PID="vietnam-indonesia-gdp"
PD=Path('/home/desktop/Work/OpenMontage/projects')/PID
script=json.load(open(PD/'artifacts/script.json'))
plan=json.load(open(PD/'artifacts/scene_plan.json'))
order={x['scene']:x['order'] for x in script['metadata']['visual_plan']}
src=PD/'assets/video/mpt'; dst=PD/'assets/video/mpt_trim'; dst.mkdir(parents=True,exist_ok=True)

for s in script['sections']:
    sid=s['id']; a,b=s['start_seconds'],s['end_seconds']; mid=round((a+b)/2,2)
    fo, to = (a,mid) if order[sid]=='footage_first' else (mid,b)
    off=round(fo-a,2); dur=round(to-fo,2)
    inp=src/f'{sid}.mp4'; out=dst/f'{sid}.mp4'
    subprocess.run(['ffmpeg','-y','-v','error','-ss',str(off),'-i',str(inp),'-t',str(dur),
                    '-an','-c:v','libx264','-preset','veryfast','-crf','20','-vf','scale=1920:1080',str(out)],check=True)
    r=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(out)],capture_output=True,text=True)
    print(sid, 'order',order[sid],'offset',off,'target',dur,'actual',r.stdout.strip())
