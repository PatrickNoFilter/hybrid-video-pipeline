import sys, json
from pathlib import Path
sys.path.insert(0, '/home/desktop/Work/OpenMontage')
from tools.tool_registry import registry
registry.discover()
tool = registry._tools["direct_clip_search"]
out = str(Path('/home/desktop/Work/OpenMontage/projects/vietnam-indonesia-gdp/assets/video/raw_stock'))
Path(out).mkdir(parents=True, exist_ok=True)
params = {
    "output_dir": out,
    "queries": [
        {"query": "Jakarta street traffic", "slot_id": "indonesia_street", "kind": "video"},
        {"query": "Indonesia rupiah banknotes money", "slot_id": "rupiah", "kind": "video"},
        {"query": "Jakarta city skyline", "slot_id": "indonesia_skyline", "kind": "video"},
        {"query": "Vietnam electronics factory assembly", "slot_id": "vn_factory", "kind": "video"},
        {"query": "Vietnam port containers export", "slot_id": "vn_port", "kind": "video"}
    ],
    "sources": ["wikimedia", "archive_org"],
    "clips_per_query": 2,
    "filters": {"orientation": "landscape", "min_duration": 3},
    "extract_thumbnails": True,
    "timeout_seconds": 300
}
r = tool.execute(params)
print("success", r.success)
print("error", r.error)
d = r.data or {}
print("keys", list(d.keys()) if isinstance(d, dict) else type(d))
print(json.dumps(d, indent=2, default=str)[:4500])
