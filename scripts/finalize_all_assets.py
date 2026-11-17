import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, '/home/desktop/Work/OpenMontage')
from lib.checkpoint import write_checkpoint
import jsonschema
OM='/home/desktop/Work/OpenMontage'; PID="vietnam-indonesia-gdp"; PD=Path(OM)/'projects'/PID

script=json.load(open(PD/'artifacts/script.json'))
order={x['scene']:x['order'] for x in script['metadata']['visual_plan']}
src=PD/'assets/video/mpt'; dst=PD/'assets/video/mpt_trim'; dst.mkdir(parents=True,exist_ok=True)

def dur(p):
    r=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)],capture_output=True,text=True)
    try: return round(float(r.stdout.strip()),2)
    except: return 0.0

for s in script['sections']:
    sid=s['id']; a,b=s['start_seconds'],s['end_seconds']; mid=round((a+b)/2,2)
    fo,to=(a,mid) if order[sid]=='footage_first' else (mid,b)
    off=round(fo-a,2); d=round(to-fo,2)
    subprocess.run(['ffmpeg','-y','-v','error','-ss',str(off),'-i',str(src/f'{sid}.mp4'),'-t',str(d),
        '-an','-c:v','libx264','-preset','veryfast','-crf','20','-vf','scale=1920:1080',str(dst/f'{sid}.mp4')],check=True)

footage_map={
 "s0a":"News studio broadcast (intro headlines)","s0b":"Vietnam + Indonesia skylines (title intro)",
 "s1":"Vietnam - Ho Chi Minh City skyline (hook)","s2":"Vietnam - electronics factory (2025 growth)",
 "s3":"Vietnam - industrial park / export port (2026 growth)","s4":"Indonesia - BPS / government office (source proof)",
 "s5":"Indonesia - bank / rupiah exchange (per-capita caveat)","s6":"Indonesia - bank building / financial district (2025 levels)",
 "s7":"Vietnam - skyscraper / financial district (IMF projection)","s8":"Vietnam - electronics factory (growth engine)",
 "s9":"Indonesia - Jakarta crowd / traffic (population & FX)","s10":"Indonesia - exchange counter / Jakarta night (sensitivity)",
 "s11":"Both - Jakarta night + Vietnam city lights (conclusion)"
}
assets=[]
for s in script['sections']:
    sid=s['id']; p=PD/f'assets/audio/sections/{sid}.mp3'
    assets.append({"id":f"narr_{sid}","type":"narration","path":str(p.relative_to(PD)),"source_tool":"edge_tts",
      "scene_id":sid,"model":"id-ID-GadisNeural","duration_seconds":dur(p),"format":"mp3",
      "voice_performance":{"source_section_id":sid,"delivery_cues_applied":True,"provider_text_used":True,
        "provider_settings":{"voice":"id-ID-GadisNeural","rate":"+0%","volume":"+0%"},
        "sample_approved":True,"sample_path":"assets/audio/sections/s7_sample.mp3","review_notes":"Polite Gadis voice; intro sections included"},
      "generation_summary":"Edge TTS via MoneyPrinterTurbo environment"})
for sid,path,typ,tool,summary in [
  ("narr_full","assets/audio/narration_full.mp3","narration","ffmpeg","13 sections + 0.3s gaps + 2s final hold"),
  ("subs","assets/subtitles.srt","subtitle","custom","36 sentence-level cues"),
  ("music","assets/music/background.mp3","music","provided","User track")]:
    assets.append({"id":sid,"type":typ,"path":path,"source_tool":tool,"scene_id":"all",
      "duration_seconds":dur(PD/path) if path.endswith('.mp3') else None,"format":path.split('.')[-1],
      "generation_summary":summary})
plan=json.load(open(PD/'artifacts/scene_plan.json'))
for sc in plan['scenes']:
    section=sc['script_section_id']; sid=sc['id']
    if sid.endswith('_footage'):
        assets.append({"id":sid,"type":"video","path":f"assets/video/mpt_trim/{section}.mp4","source_tool":"moneyprinterturbo",
          "scene_id":sid,"provider":"Pexels","duration_seconds":dur(dst/f'{section}.mp4'),"resolution":"1920x1080","format":"mp4",
          "generation_summary":f"MPT + Pexels: {footage_map.get(section,'Vietnam/Indonesia footage')}; trimmed to footage half","license":"Pexels License"})
    else:
        assets.append({"id":sid,"type":"animation","path":f"assets/video/gfx/{section}.mp4","source_tool":"video_compose(remotion)",
          "scene_id":sid,"model":"Remotion 4.0.544","duration_seconds":dur(PD/f'assets/video/gfx/{section}.mp4'),
          "resolution":"1920x1080","format":"mp4","generation_summary":sc['description'],"prompt":sc['description']})
manifest={"version":"1.0","assets":assets,"total_cost_usd":0.0,"metadata":{
  "style_playbook":"flat-motion-graphics",
  "shared_support_assets":["news bulletin card","title card","subtitle treatment","stat-card system","PROYEKSI badge","source credit line"],
  "scene_asset_index":{sc['id']:[a['id'] for a in assets if a['scene_id']==sc['id']] for sc in plan['scenes']},
  "source_vs_generated_map":{"source":["MPT/Pexels mixed Vietnam+Indonesia footage","user music"],"generated":["Edge TTS narration","Remotion infographics","SRT"]},
  "scene_footage_map":footage_map,
  "voice":"id-ID-GadisNeural","render_runtime":"remotion",
  "note":"News-headline intro + title intro added; footage mixes Vietnam and Indonesia matched to narration; total "+str(script['total_duration_seconds'])+"s."}}
jsonschema.validate(manifest,json.load(open(f'{OM}/schemas/artifacts/asset_manifest.schema.json')))
json.dump(manifest,open(PD/'artifacts/asset_manifest.json','w'),indent=2,ensure_ascii=False)

d=json.load(open(PD/'artifacts/decision_log.json'))
d['decisions'].append({"decision_id":"d-021","stage":"assets","category":"capability_extension",
 "subject":"Source of real-video segments","options_considered":[
  {"option_id":"mixed-vn-id","label":"Mixed Vietnam + Indonesia footage matched to narration, plus intro","score":0.99,
   "reason":"Vietnam skyline/factory/port for growth beats; Indonesia BPS/bank/rupiah/crowd for level and FX beats; newsroom + skylines for intro"},
  {"option_id":"diverse-vn-only","label":"Diverse Vietnam-only footage","score":0.5,"reason":"Previous pass","rejected_because":"User asked to combine with Indonesian videos based on narration"}],
 "selected":"mixed-vn-id","reason":"User requested Indonesian footage mixed in, matched to narration; intro sections added too.",
 "user_visible":True,"user_approved":True,"confidence":0.99})
json.dump(d,open(PD/'artifacts/decision_log.json','w'),indent=2,ensure_ascii=False)

review={"rounds":4,"findings":[
 {"severity":"suggestion","issue":"Intro and mixed-country footage requested","resolution":"2 intro sections, 2 intro MPT clips, 2 intro Remotion cards; all 13 footage halves re-trimmed"},
 {"severity":"nitpick","issue":"Narration mix and subtitles rebuilt for 13 sections","resolution":"242.5s full mix, 36 cues"}],"critical_fixed":0}
write_checkpoint(Path(OM)/'projects',PID,"assets","awaiting_human",{"asset_manifest":manifest},
 pipeline_type="hybrid",style_playbook="flat-motion-graphics",checkpoint_policy="guided",
 human_approval_required=True,review=review,
 cost_snapshot={"total_spent_usd":0.0,"total_reserved_usd":0.0,"budget_remaining_usd":2.0},
 metadata={"note":"Assets FINAL: intro + mixed VN/ID footage; awaiting approval before edit"})
print("final assets:",len(assets),"missing:",sum(1 for a in assets if not (PD/a['path']).exists()))