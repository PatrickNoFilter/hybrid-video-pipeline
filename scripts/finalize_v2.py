import json, sys
from pathlib import Path
sys.path.insert(0, '/home/desktop/Work/OpenMontage')
from lib.checkpoint import write_checkpoint
OM='/home/desktop/Work/OpenMontage'; PID="vietnam-indonesia-gdp"; PD=Path(OM)/'projects'/PID

d=json.load(open(PD/'artifacts/decision_log.json'))
d['decisions'].append({
 "decision_id":"d-027","stage":"assets","category":"visual_accuracy_check",
 "subject":"Intro infographic visual style",
 "options_considered":[
  {"option_id":"google-news-results","label":"Google News search-results style with actual headlines","score":0.99,
   "reason":"User supplied a screenshot of Google News results for 'pdb perkapita vietnam' and asked the intro infographic to match it"},
  {"option_id":"breaking-bulletin","label":"BREAKING news bulletin card","score":0.4,"reason":"Previous intro","rejected_because":"User requested the Google News results look"}],
 "selected":"google-news-results",
 "reason":"Intro now reproduces a Google News results page: search bar, Berita tab, and five real headlines with sources and timestamps.",
 "user_visible":True,"user_approved":True,"confidence":0.99})
json.dump(d,open(PD/'artifacts/decision_log.json','w'),indent=2,ensure_ascii=False)

m=json.load(open(PD/'artifacts/asset_manifest.json'))
m['metadata']['note']='Intro = Google News-style results card (no footage); closing = infographic-only (no footage); music looped; no subtitles.'
for a in m['assets']:
    if a['id']=='s0a_graphic':
        a['description']=a.get('description','Google News-style results page infographic')
        a['generation_summary']='Remotion: Google News results page with search bar, Berita tab and five real headlines (GoodStats, Kompas, IDN Financials, kumparan, CNN Indonesia)'
json.dump(m,open(PD/'artifacts/asset_manifest.json','w'),indent=2,ensure_ascii=False)

rr=json.load(open(PD/'artifacts/render_report.json'))
rr['verification_notes']=["ffprobe: h264 1920x1080 30fps + aac stereo",
 "duration 243.06s; music looped from clean 168s cut with 4s crossfade",
 "intro verified as Google News-style results page; closing verified as infographic-only",
 "s11 footage removed; 24 cuts total; no subtitles burned in"]
json.dump(rr,open(PD/'artifacts/render_report.json','w'),indent=2,ensure_ascii=False)

fr=json.load(open(PD/'artifacts/final_review.json'))
fr['checks']['visual_spotcheck']['frame_paths']=["/tmp/opencode/qa_v2_5.png","/tmp/opencode/qa_v2_20.png","/tmp/opencode/qa_v2_120.png","/tmp/opencode/qa_v2_215.png","/tmp/opencode/qa_v2_235.png"]
fr['metadata']['notes']="5 frames sampled: new Google News intro, title, middle data, late scene, infographic-only closing. All clean."
json.dump(fr,open(PD/'artifacts/final_review.json','w'),indent=2,ensure_ascii=False)

write_checkpoint(Path(OM)/'projects',PID,'compose','completed',
 {"render_report":rr,"final_review":fr},pipeline_type="hybrid",style_playbook="flat-motion-graphics",
 checkpoint_policy="guided",human_approval_required=False,
 cost_snapshot={"total_spent_usd":0.0,"total_reserved_usd":0.0,"budget_remaining_usd":2.0},
 metadata={"note":"Final v2: Google News intro, infographic-only closing, looped music, no subtitles"})
print("artifacts updated")