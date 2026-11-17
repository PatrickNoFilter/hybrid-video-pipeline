#!/bin/bash
set -u
R=/home/desktop/Work/OpenMontage/remotion-composer
OUT=/home/desktop/Work/OpenMontage/projects/vietnam-indonesia-gdp/assets/video/gfx
mkdir -p "$OUT"
cd "$R" || exit 1
for s in s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11; do
  echo "=== rendering gfx-$s $(date +%H:%M:%S)"
  npx remotion render src/index.tsx "gfx-$s" "$OUT/$s.mp4" --codec h264 --crf 20 --log=error > "$OUT/$s.log" 2>&1
  if [ -f "$OUT/$s.mp4" ]; then echo "=== gfx-$s OK $(date +%H:%M:%S)"; else echo "=== gfx-$s FAILED"; tail -10 "$OUT/$s.log"; fi
done
echo "ALL GFX DONE $(date +%H:%M:%S)"
