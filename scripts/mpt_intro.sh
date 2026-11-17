#!/bin/bash
set -u
MPT=/home/desktop/Work/MoneyPrinterTurbo
PROJ=/home/desktop/Work/OpenMontage/projects/vietnam-indonesia-gdp
S=$PROJ/assets/audio/sections
OUT=$PROJ/assets/video/mpt
one(){
 local sid="$1" terms text tid
 if [ "$sid" = "s0a" ]; then
  terms="news studio broadcast anchor desk, television newsroom screens"
  text="Liputan ekonomi Asia. IMF memproyeksikan PDB per kapita Vietnam menyalip Indonesia pada tahun dua ribu dua puluh enam. Namun, data aktualnya masih sangat ketat."
 else
  terms="Ho Chi Minh City skyline Vietnam, Jakarta skyline Indonesia night"
  text="Tujuh triwulan: tumbuhnya Vietnam sudah menyalip Indonesia, ekonominya belum."
 fi
 echo "start $sid $(date +%H:%M:%S)"
 (cd "$MPT" && .venv/bin/python cli.py --video-script "$text" --custom-audio-file "$S/$sid.mp3" --video-source pexels --video-terms "$terms" --video-aspect 16:9 --video-count 1 --video-clip-duration 5 --no-subtitle-enabled --bgm-type none --video-transition-mode none --n-threads 1 > "$OUT/${sid}_intro.log" 2>&1)
 tid=$(grep -o '"task_id": "[^"]*"' "$OUT/${sid}_intro.log" | tail -1 | cut -d'"' -f4)
 if [ -n "$tid" ] && [ -f "$MPT/storage/tasks/$tid/final-1.mp4" ]; then cp "$MPT/storage/tasks/$tid/final-1.mp4" "$OUT/$sid.mp4"; echo "OK $sid"; else echo "FAIL $sid"; tail -5 "$OUT/${sid}_intro.log"; fi
}
export -f one; export MPT PROJ S OUT
printf '%s\n' s0a s0b | xargs -P 2 -I{} bash -c 'one "$@"' _ {}
echo INTRO_MPT_DONE
