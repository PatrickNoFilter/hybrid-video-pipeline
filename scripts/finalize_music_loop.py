import json, sys
from pathlib import Path
sys.path.insert(0,'/home/desktop/Work/OpenMontage')
from lib.checkpoint import write_checkpoint
OM='/home/desktop/Work/OpenMontage'; PID="vietnam-indonesia-gdp"; PD=Path(OM)/'projects'/PID

m=json.load(open(PD/'artifacts/asset_manifest.json'))
for a in m['assets']:
    if a['id']=='music':
        a['path']='assets/music/background_loop.mp3'
        a['duration_seconds']=243.06
        a['generation_summary']='User-provided track looped with a 4s crossfade at the seam to cover the full 243s video'
m['metadata']['note']='Music looped (4s crossfade) so it plays to the end; no subtitles burned in.'
json.dump(m,open(PD/'artifacts/asset_manifest.json','w'),indent=2,ensure_ascii=False)

d=json.load(open(PD/'artifacts/decision_log.json'))
d['decisions'].append({"decision_id":"d-024","stage":"compose","category":"music_source",
 "subject":"Background music loop",
 "options_considered":[
  {"option_id":"crossfade-loop","label":"Loop track with 4s crossfade","score":0.98,"reason":"Music (191.7s) ended before the 243s video; seamless re-entry at the seam"},
  {"option_id":"let-it-stop","label":"Keep original track ending early","score":0.2,"reason":"Previous output","rejected_because":"User said music stopped before the end"}],
 "selected":"crossfade-loop","reason":"User requested the music play again with a smooth transition.",
 "user_visible":True,"user_approved":True,"confidence":0.99})
json.dump(d,open(PD/'artifacts/decision_log.json','w'),indent=2,ensure_ascii=False)

rr=json.load(open(PD/'artifacts/render_report.json'))
rr['warnings']=["Final-frame hold added to cover narration tail; midpoint transitions are hard cuts"]
rr['verification_notes']=["ffprobe: h264 1920x1080 30fps + aac stereo",
  "duration 243.06s; music looped with 4s crossfade and audible through the final 4s (tail volumedetect mean -34.8 dB)",
  "5 visual spot-check frames inspected","no subtitles burned in"]
json.dump(rr,open(PD/'artifacts/render_report.json','w'),indent=2,ensure_ascii=False)

write_checkpoint(Path(OM)/'projects',PID,"assets","completed",{"asset_manifest":m},pipeline_type="hybrid",
 style_playbook="flat-motion-graphics",checkpoint_policy="guided",human_approval_required=False,
 cost_snapshot={"total_spent_usd":0.0,"total_reserved_usd":0.0,"budget_remaining_usd":2.0},
 human_approved=True,metadata={"note":"Music asset updated to looped version"})
write_checkpoint(Path(OM)/'projects',PID,"compose","completed",
 {"render_report":rr,"final_review":json.load(open(PD/'artifacts/final_review.json'))},
 pipeline_type="hybrid",style_playbook="flat-motion-graphics",checkpoint_policy="guided",
 human_approval_required=False,cost_snapshot={"total_spent_usd":0.0,"total_reserved_usd":0.0,"budget_remaining_usd":2.0},
 metadata={"note":"Final re-render with looped music; no subtitles"})
print("updated music artifacts")