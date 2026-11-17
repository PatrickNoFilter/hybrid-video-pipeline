"""Final assembly: normalize clips, concat, add looped music + narration, no subtitles."""
import json, subprocess, time
from pathlib import Path

OM = '/home/desktop/Work/OpenMontage'
PID = 'vietnam-indonesia-gdp'
PD = Path(OM) / 'projects' / PID
edit = json.load(open(PD / 'artifacts/edit_decisions.json'))
REND = PD / 'renders'
NORM = PD / 'assets/video/norm'
NORM.mkdir(parents=True, exist_ok=True)
t0 = time.time()

# 1) normalize every clip to identical params (fixes concat frame drops)
#    Always re-normalize: source gfx may have been re-rendered (intro/closing changes).
normalized = []
for c in edit['cuts']:
    src = PD / c['source']
    out = NORM / (c['id'] + '.mp4')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(src),
        '-vf', 'fps=30,scale=1920:1080,setsar=1,format=yuv420p',
        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-an',
        '-video_track_timescale', '30000', str(out)], check=True)
    normalized.append(out)
print("normalized", len(normalized), "clips in", round(time.time()-t0,1), "s", flush=True)

# 2) concat + hold final frame so video covers the narration tail
listf = PD / 'assets/concat_norm.txt'
listf.write_text("\n".join(f"file '{p}'" for p in normalized))
vid = REND / 'video_only.mp4'
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(listf),
    '-vf', 'tpad=stop_mode=clone:stop_duration=7',
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-r', '30',
    '-pix_fmt', 'yuv420p', str(vid)], check=True)
print("video", round(time.time()-t0,1), "s", flush=True)

# 3) final mux: narration + looped music, NO subtitles
narr = PD / 'assets/audio/narration_full.mp3'
music = PD / 'assets/music/background_loop.mp3'
final = REND / 'final.mp4'
dur = json.load(open(PD / 'artifacts/script.json'))['total_duration_seconds']
fo = max(0, dur - 5)
fc = (f"[1:a]volume=1.0[n];[2:a]volume=0.12,afade=t=in:st=0:d=2,afade=t=out:st={fo}:d=3[m];"
      f"[n][m]amix=inputs=2:duration=first:dropout_transition=0[a]")
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(vid), '-i', str(narr), '-i', str(music),
    '-filter_complex', fc, '-map', '0:v', '-map', '[a]',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '192k', '-shortest', str(final)], check=True)
print("FINAL", final.stat().st_size, round(time.time()-t0,1), "s", flush=True)
