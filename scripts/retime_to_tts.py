import json, sys
from pathlib import Path
sys.path.insert(0, '/home/desktop/Work/OpenMontage')
from lib.checkpoint import write_checkpoint

PID = "vietnam-indonesia-gdp"
PD = Path('/home/desktop/Work/OpenMontage/projects') / PID
OM = '/home/desktop/Work/OpenMontage'
script = json.load(open(PD / "artifacts/script.json"))
plan = json.load(open(PD / "artifacts/scene_plan.json"))
timings = {x["id"]: x["actual"] for x in json.load(open(PD / "artifacts/tts_timings.json"))}

GAP = 0.3
FINAL_HOLD = 2.0
cursor = 0.0
new_spans = {}
for s in script["sections"]:
    start = round(cursor, 2)
    end = round(start + timings[s["id"]], 2)
    s["start_seconds"], s["end_seconds"] = start, end
    new_spans[s["id"]] = (start, end)
    cursor = end + GAP
total = round(cursor - GAP + FINAL_HOLD, 2)
script["total_duration_seconds"] = total
script["voice_performance"]["pause_policy"] = "0.3s gap between sections; final card holds 2.0s after voice ends"
json.dump(script, open(PD / "artifacts/script.json", "w"), indent=2, ensure_ascii=False)

# Retiming scene plan half-scenes
order = {x["scene"]: x["order"] for x in script["metadata"]["visual_plan"]}
for sc in plan["scenes"]:
    sid = sc["script_section_id"]
    start, end = new_spans[sid]
    mid = round((start + end) / 2, 2)
    is_footage = sc["id"].endswith("_footage")
    first = order[sid] == "footage_first"
    if (is_footage and first) or (not is_footage and not first):
        sc["start_seconds"], sc["end_seconds"] = start, mid
    else:
        sc["start_seconds"], sc["end_seconds"] = mid, end
    sc["transition_in"] = "crossfade 0.3s from previous half" if sc["start_seconds"] > 0 else "fade from black"
    sc["transition_out"] = "crossfade 0.3s to next half" if sc["end_seconds"] < total else "fade to black"

plan["metadata"]["total_duration_seconds"] = total
plan["metadata"]["note"] = f"Retimed to real Edge TTS durations: {total}s total (was 117s). 0.3s gaps, 2.0s final hold."
for v in script["metadata"]["visual_plan"]:
    s, e = new_spans[v["scene"]]
    v["crossfade_at_seconds"] = round((s + e) / 2, 2)
json.dump(script, open(PD / "artifacts/script.json", "w"), indent=2, ensure_ascii=False)
json.dump(plan, open(PD / "artifacts/scene_plan.json", "w"), indent=2, ensure_ascii=False)

# Decision log entry
d = json.load(open(PD / "artifacts/decision_log.json"))
d["decisions"].append({
 "decision_id":"d-016","stage":"assets","category":"budget_tradeoff",
 "subject":"Video duration vs narration fidelity",
 "options_considered":[
  {"option_id":"extend-220","label":"Extend video to ~220s","score":0.98,"reason":"Keeps every approved word and natural Gadis pacing"},
  {"option_id":"speed-tts","label":"Speed up voice ~30% to ~170s","score":0.5,"reason":"Shorter but rushed","rejected_because":"User chose to preserve narration fidelity"},
  {"option_id":"shorten-text","label":"Rewrite narration shorter","score":0.45,"reason":"Could approach ~150s","rejected_because":"Would lose approved polite wording and source credit"}],
 "selected":"extend-220","reason":"User approved extending the timeline after real TTS measured 214.9s of speech vs 117s planned.",
 "user_visible":True,"user_approved":True,"confidence":0.99})
json.dump(d, open(PD / "artifacts/decision_log.json", "w"), indent=2, ensure_ascii=False)

# Re-checkpoint the two retimed stages (history preserved automatically)
for stage, artifact in [("script", {"script": script}), ("scene_plan", {"scene_plan": plan})]:
    write_checkpoint(Path(OM)/"projects", PID, stage, "completed", artifact,
        pipeline_type="hybrid", style_playbook="flat-motion-graphics", checkpoint_policy="guided",
        human_approval_required=True, human_approved=True,
        cost_snapshot={"total_spent_usd":0.0,"total_reserved_usd":0.0,"budget_remaining_usd":2.0},
        metadata={"note": f"Retimed to real TTS audio ({total}s); decision d-016"})

print("retimed total:", total, "sections:", len(new_spans))
for k,(s,e) in new_spans.items(): print(f"  {k}: {s:6.2f}-{e:6.2f} ({e-s:5.2f}s)")
