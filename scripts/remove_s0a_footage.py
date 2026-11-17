import json, sys
from pathlib import Path
sys.path.insert(0,'/home/desktop/Work/OpenMontage')
from lib.checkpoint import write_checkpoint
import jsonschema
OM='/home/desktop/Work/OpenMontage'; PID="vietnam-indonesia-gdp"; PD=Path(OM)/'projects'/PID

script=json.load(open(PD/'artifacts/script.json'))
s0a=next(s for s in script['sections'] if s['id']=='s0a')
s0a['enhancement_cues']=[c for c in s0a['enhancement_cues'] if c['type']=='stat_card']
s0a['enhancement_cues'][0]['timestamp_seconds']=0.0
s0a['enhancement_cues'][0]['description']=s0a['enhancement_cues'][0]['description'].replace('OpenMontage Remotion infographic: ','')
s0a['label']='News headlines cold open (infographic only)'
for v in script['metadata']['visual_plan']:
    if v['scene']=='s0a':
        v['order']='infographic_only'; v['crossfade_at_seconds']=0.0
script['metadata']['required_support_assets']=[a for a in script['metadata']['required_support_assets'] if 's0a newsroom' not in a]
script['metadata']['required_support_assets']=['Remotion news headline card fills entire s0a (no footage)']+script['metadata']['required_support_assets']
jsonschema.validate(script,json.load(open(f'{OM}/schemas/artifacts/script.schema.json')))
json.dump(script,open(PD/'artifacts/script.json','w'),indent=2,ensure_ascii=False)

plan=json.load(open(PD/'artifacts/scene_plan.json'))
plan['scenes']=[s for s in plan['scenes'] if s['id']!='s0a_footage']
g=next(s for s in plan['scenes'] if s['id']=='s0a_graphic')
g['start_seconds']=0.0; g['end_seconds']=s0a['end_seconds']
g['transition_in']='fade from black'
g['description']='Animated news bulletin with 3 headlines and BREAKING tag, full intro section (no footage half)'
plan['metadata']['note']='s0a intro is infographic-only (newsroom footage removed); all other sections remain 50/50 alternating; total '+str(script['total_duration_seconds'])+'s'
jsonschema.validate(plan,json.load(open(f'{OM}/schemas/artifacts/scene_plan.schema.json')))
json.dump(plan,open(PD/'artifacts/scene_plan.json','w'),indent=2,ensure_ascii=False)

d=json.load(open(PD/'artifacts/decision_log.json'))
d['decisions'].append({"decision_id":"d-022","stage":"assets","category":"composition_mode",
 "subject":"Real-video vs infographic share within each scene",
 "options_considered":[
  {"option_id":"intro-graphic-only","label":"s0a news intro infographic-only","score":0.98,
   "reason":"User asked to delete the real video at the beginning (s0a footage); headline card fills the full intro"},
  {"option_id":"alternating","label":"Keep 50/50 footage + infographic in s0a","score":0.5,"reason":"Previous rule","rejected_because":"User asked to remove the intro footage"}],
 "selected":"intro-graphic-only","reason":"Explicit user request; exception applies to s0a only, all other sections stay alternating.",
 "user_visible":True,"user_approved":True,"confidence":0.99})
json.dump(d,open(PD/'artifacts/decision_log.json','w'),indent=2,ensure_ascii=False)

for stage,art in [("script",{"script":script}),("scene_plan",{"scene_plan":plan})]:
    write_checkpoint(Path(OM)/'projects',PID,stage,"completed",art,pipeline_type="hybrid",
      style_playbook="flat-motion-graphics",checkpoint_policy="guided",human_approval_required=True,human_approved=True,
      cost_snapshot={"total_spent_usd":0.0,"total_reserved_usd":0.0,"budget_remaining_usd":2.0},
      metadata={"note":"s0a footage removed; infographic-only intro; d-022"})
print("s0a footage removed; graphic now 0-",s0a['end_seconds'])