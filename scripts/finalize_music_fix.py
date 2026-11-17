import json, sys
from pathlib import Path
sys.path.insert(0,'/home/desktop/Work/OpenMontage')
from lib.checkpoint import write_checkpoint
OM='/home/desktop/Work/OpenMontage'; PID="vietnam-indonesia-gdp"; PD=Path(OM)/'projects'/PID
d=json.load(open(PD/'artifacts/decision_log.json'))
d['decisions'].append({"decision_id":"d-025","stage":"compose","category":"music_source",
 "subject":"Background music loop","options_considered":[
  {"option_id":"clean-168-loop","label":"Loop a clean 168s cut with 4s crossfade","score":0.99,
   "reason":"Source track goes silent at ~176-191s; trimming before the silent tail removes the dead zone"},
  {"option_id":"full-track-loop","label":"Loop full 191.7s track","score":0.3,"reason":"Previous attempt","rejected_because":"User reported muting at 2:50-3:10; source had a -91dB silent tail"}],
 "selected":"clean-168-loop","reason":"Fixed the muted window by looping from a clean source cut.",
 "user_visible":True,"user_approved":True,"confidence":0.99})
json.dump(d,open(PD/'artifacts/decision_log.json','w'),indent=2,ensure_ascii=False)
rr=json.load(open(PD/'artifacts/render_report.json'))
rr['verification_notes']=["ffprobe: h264 1920x1080 30fps + aac stereo",
 "duration 243.06s; music looped from clean 168s cut with 4s crossfade",
 "verified no silent window at 170-190s (final mean -26.0 dB, max -11.0 dB in that window)",
 "5 visual spot-check frames inspected","no subtitles burned in"]
json.dump(rr,open(PD/'artifacts/render_report.json','w'),indent=2,ensure_ascii=False)
m=json.load(open(PD/'artifacts/asset_manifest.json'))
for a in m['assets']:
    if a['id']=='music': a['generation_summary']='User track trimmed to clean 168s cut and looped with 4s crossfade to cover 243s with no silent gap'
json.dump(m,open(PD/'artifacts/asset_manifest.json','w'),indent=2,ensure_ascii=False)
write_checkpoint(Path(OM)/'projects',PID,"compose","completed",
 {"render_report":rr,"final_review":json.load(open(PD/'artifacts/final_review.json'))},
 pipeline_type="hybrid",style_playbook="flat-motion-graphics",checkpoint_policy="guided",
 human_approval_required=False,cost_snapshot={"total_spent_usd":0.0,"total_reserved_usd":0.0,"budget_remaining_usd":2.0},
 metadata={"note":"Music dead zone removed; final re-render verified"})
print("music fix logged")