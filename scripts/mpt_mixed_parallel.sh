#!/bin/bash
set -u
MPT=/home/desktop/Work/MoneyPrinterTurbo
PROJ=/home/desktop/Work/OpenMontage/projects/vietnam-indonesia-gdp
S=$PROJ/assets/audio/sections
OUT=$PROJ/assets/video/mpt
mkdir -p "$OUT"

one () {
  local sid="$1" terms text tid
  case "$sid" in
    s1) terms="Ho Chi Minh City skyline Vietnam skyscrapers, Vietnam city aerial"; text="Dalam tujuh triwulan terakhir, pertumbuhan Vietnam senantiasa lebih cepat daripada Indonesia. Namun, apakah ekonominya benar-benar telah menyalip? Marilah kita telusuri bersama.";;
    s2) terms="Vietnam electronics factory assembly line, Vietnam manufacturing workers"; text="Sepanjang tahun dua ribu dua puluh lima, Vietnam berada di kisaran tujuh hingga delapan koma empat persen. Sementara itu, Indonesia bergerak di sekitar lima persen. Marilah kita perhatikan grafiknya.";;
    s3) terms="Vietnam industrial park aerial factory, Vietnam port export containers"; text="Memasuki tahun dua ribu dua puluh enam, Vietnam terus meningkat ke delapan koma satu lima, delapan koma delapan satu, dan sembilan koma sembilan lima persen. Selisihnya turut melebar dari dua koma dua menjadi empat koma lima poin.";;
    s4) terms="Jakarta Indonesia government office building, BPS statistics office"; text="Seluruh angka tersebut bersumber dari data aktual badan statistik Vietnam serta BPS Indonesia. Dalam tujuh dari tujuh triwulan, Vietnam senantiasa unggul. Dengan demikian, pertumbuhan yang lebih cepat itu memang terbukti.";;
    s5) terms="Indonesia bank interior counter, rupiah money exchange office"; text="Namun, marilah kita perhatikan dengan saksama. BPS dan badan statistik Vietnam tidak menerbitkan PDB per kapita dalam dolar Amerika per triwulan. Oleh karena itu, istilah menyalip hanya tepat untuk pertumbuhan, bukan untuk tingkat pendapatan.";;
    s6) terms="Jakarta financial district bank building, Indonesia modern skyline"; text="Data tahun dua ribu dua puluh lima menunjukkan Vietnam lima ribu enam puluh enam dolar, Indonesia lima ribu enam puluh dolar. Keduanya praktis seimbang. Namun dengan ukuran harga konstan, Indonesia masih unggul lima koma tujuh persen.";;
    s7) terms="Vietnam skyscraper skyline Ho Chi Minh City, financial district"; text="Untuk tahun dua ribu dua puluh enam, IMF memproyeksikan Vietnam lima ribu dua ratus lima sembilan dolar dan Indonesia lima ribu seratus lima puluh tiga dolar. Perlu kami sampaikan, angka tersebut merupakan proyeksi, bukan hasil pengukuran.";;
    s8) terms="Vietnam electronics factory assembly, Vietnam manufacturing workers industrial"; text="Apa yang menyebabkan Vietnam melaju? Pada triwulan ketiga, sektor industri dan konstruksi tumbuh dua belas koma lima persen, menyumbang lebih dari setengah total pertumbuhan. Ekspor juga meningkat dua puluh tiga koma dua tujuh persen.";;
    s9) terms="Jakarta Indonesia street crowd population, urban traffic people"; text="Tingkat per kapita juga dipengaruhi jumlah penduduk dan nilai tukar. Vietnam berpenduduk sekitar seratus satu juta jiwa, Indonesia hampir dua ratus delapan puluh enam juta. Pelemahan rupiah menurunkan PDB per kapita Indonesia dalam dolar.";;
    s10) terms="Indonesia currency exchange counter, Jakarta city night lights"; text="Selisih dalam proyeksi IMF hanya dua koma satu persen, lebih kecil daripada kemungkinan kesalahan proyeksi. Pergeseran kurs beberapa persen saja dapat membalik urutannya. Oleh sebab itu, posisinya masih sangat ketat, bukan suatu kepastian.";;
    s11) terms="Jakarta skyline night Indonesia, Ho Chi Minh City lights Vietnam"; text="Demikian kesimpulannya: tujuh triwulan data BPS dan NSO menunjukkan pertumbuhan Vietnam telah mengungguli Indonesia. Adapun ekonominya, masih sebatas proyeksi IMF. Silakan simak angkanya, dan senantiasa perhatikan basis harganya.";;
  esac
  echo "start $sid $(date +%H:%M:%S) [$terms]"
  (cd "$MPT" && .venv/bin/python cli.py --video-script "$text" --custom-audio-file "$S/$sid.mp3" --video-source pexels --video-terms "$terms" --video-aspect 16:9 --video-count 1 --video-clip-duration 5 --no-subtitle-enabled --bgm-type none --video-transition-mode none --n-threads 1 > "$OUT/${sid}_mixed.log" 2>&1)
  tid=$(grep -o '"task_id": "[^"]*"' "$OUT/${sid}_mixed.log" | tail -1 | cut -d'"' -f4)
  if [ -n "$tid" ] && [ -f "$MPT/storage/tasks/$tid/final-1.mp4" ]; then
    cp "$MPT/storage/tasks/$tid/final-1.mp4" "$OUT/$sid.mp4"; echo "OK $sid $(date +%H:%M:%S)"
  else echo "FAIL $sid tid=$tid"; tail -6 "$OUT/${sid}_mixed.log"; fi
}
export -f one
export MPT PROJ S OUT
printf '%s\n' s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 | xargs -P 3 -I{} bash -c 'one "$@"' _ {}
echo "MIXED BATCH DONE $(date +%H:%M:%S)"
