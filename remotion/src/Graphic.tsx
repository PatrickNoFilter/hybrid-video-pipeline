import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';

const C = {
  bg: '#0B1220', panel: '#111C33', white: '#F8FAFC', muted: '#94A3B8',
  vn: '#34D399', idn: '#F59E0B', amber: '#FBBF24', red: '#FB7185', blue: '#38BDF8',
};

const styles: Record<string, React.CSSProperties> = {
  root: {background: C.bg, fontFamily: 'Inter, Arial, sans-serif', color: C.white, padding: 90},
  kicker: {fontSize: 30, letterSpacing: 4, color: C.muted, textTransform: 'uppercase', fontWeight: 700},
  title: {fontSize: 74, fontWeight: 800, lineHeight: 1.1, marginTop: 18, marginBottom: 30},
  sub: {fontSize: 34, color: C.muted, lineHeight: 1.4},
  card: {background: C.panel, borderRadius: 28, padding: 42, border: '2px solid #1E293B'},
  big: {fontSize: 120, fontWeight: 800, lineHeight: 1},
  label: {fontSize: 34, color: C.muted, marginTop: 12},
  row: {display: 'flex', gap: 30, alignItems: 'stretch'},
  badge: {display: 'inline-block', background: C.amber, color: '#0B1220', fontWeight: 900, fontSize: 30, padding: '12px 28px', borderRadius: 999},
  bar: {borderRadius: 14, minWidth: 40},
  foot: {position: 'absolute', bottom: 46, left: 90, fontSize: 26, color: C.muted},
  grid: {position: 'absolute', inset: 0, backgroundImage: 'linear-gradient(#ffffff08 1px, transparent 1px), linear-gradient(90deg, #ffffff08 1px, transparent 1px)', backgroundSize: '80px 80px'},
};

const useAnim = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = spring({frame, fps, config: {damping: 18, mass: 0.8}});
  const fade = interpolate(frame, [0, 12], [0, 1], {extrapolateRight: 'clamp'});
  return {frame, enter, fade};
};

const VN = 'VIETNAM';
const IDN = 'INDONESIA';

const Content: React.FC<{section: string}> = ({section}) => {
  const {frame, enter, fade} = useAnim();
  const rise = (delay: number) => interpolate(frame, [delay, delay + 14], [40, 0], {extrapolateRight: 'clamp'}) ;
  const opa = (delay: number) => interpolate(frame, [delay, delay + 12], [0, 1], {extrapolateRight: 'clamp'});

  if (section === 's0a') {
    const results = [
      {src:'GoodStats', title:'Proyeksi PDB per Kapita ASEAN 2026 Menurut IMF Outlook Oktober', snip:'Produk domestik bruto (PDB) per kapita Vietnam diproyeksikan menyusul Indonesia pada 2026 menurut IMF.', time:'2 jam yang lalu', color:'#1a73e8', tag:'GDP'},
      {src:'Kompas.com', title:'PDB Per Kapita Vietnam Bakal Lampaui Indonesia, Ini Pendorongnya', snip:'Vietnam diproyeksikan menyalip Indonesia dalam hal PDB per kapita pada 2026.', time:'1 minggu lalu', color:'#e8412f', tag:'KOMPAS'},
      {src:'IDN Financials', title:'PDB per kapita Vietnam diproyeksi lampaui Indonesia pada 2026', snip:'Vietnam menargetkan pertumbuhan ekonomi minimal 10% pada 2026. Pada kuartal ...', time:'2 minggu lalu', color:'#f5a623', tag:'IDN'},
      {src:'kumparan', title:'Vietnam Segera Salip Indonesia, PDB per Kapita Diprediksi Naik 8,9 Persen', snip:'PDB per kapita Vietnam diperkirakan mencapai USD 5.259 tahun ini. Akan menyalip posisi Indonesia.', time:'2 minggu lalu', color:'#c62828', tag:'k'},
      {src:'CNN Indonesia', title:'IMF Prediksi Vietnam Salip Indonesia untuk PDB per Kapita', snip:'Vietnam diprediksi menyalip Indonesia dari sisi PDB per kapita pada 2026.', time:'2 minggu lalu', color:'#b31217', tag:'CNN'}
    ];
    const tabs = ['Mode AI','Semua','Gambar','Berita','Video','Shopping','Video singkat','Lainnya'];
    return <>
      <div style={{background:'#303134', borderRadius:40, height:80, display:'flex', alignItems:'center', padding:'0 34px', fontSize:30, color:'#e8eaed'}}>
        pdb perkapita vietnam <div style={{marginLeft:'auto', fontSize:38}}>×</div>
      </div>
      <div style={{display:'flex', gap:34, marginTop:20, fontSize:23, color:'#9aa0a6'}}>
        {tabs.map((tab,i)=><div key={tab} style={{color:i===3?'#8ab4f8':'#9aa0a6', borderBottom:i===3?'4px solid #8ab4f8':'none', paddingBottom:10}}>{tab}</div>)}
      </div>
      <div style={{fontSize:22, color:'#9aa0a6', margin:'16px 0 12px'}}>Mungkin maksud Anda adalah: <span style={{color:'#8ab4f8'}}>pdb per kapita vietnam</span></div>
      {results.map((r,i)=>{
        const slide=interpolate(frame,[8+i*10,22+i*10],[45,0],{extrapolateRight:'clamp'});
        const op=interpolate(frame,[8+i*10,20+i*10],[0,1],{extrapolateRight:'clamp'});
        return <div key={i} style={{display:'flex', gap:24, transform:`translateX(${slide}px)`, opacity:op, marginBottom:14}}>
          <div style={{flex:1}}>
            <div style={{fontSize:19, color:'#9aa0a6'}}>{r.src} · {r.time}</div>
            <div style={{fontSize:29, color:'#8ab4f8', lineHeight:1.18, margin:'4px 0'}}>{r.title}</div>
            <div style={{fontSize:20, color:'#bdc1c6', lineHeight:1.25}}>{r.snip}</div>
          </div>
          <div style={{width:176, height:112, borderRadius:12, background:`linear-gradient(135deg, ${r.color}, #111827)`, display:'flex', alignItems:'center', justifyContent:'center', color:'#fff', fontSize:30, fontWeight:900}}>{r.tag}</div>
        </div>;
      })}
    </>;
  }

  if (section === 's0b') return (
    <>
      <div style={styles.kicker}>DATA 2025–2026 · BPS · NSO · BANK DUNIA · IMF</div>
      <div style={{fontSize:76, fontWeight:900, lineHeight:1.08}}>Tujuh Triwulan:<br/>Tumbuhnya Vietnam<br/>Sudah Menyalip Indonesia,<br/>Ekonominya Belum?</div>
      <div style={{...styles.badge, marginTop:26, background:C.vn, color:'#0B1220'}}>VIETNAM vs INDONESIA</div>
    </>
  );

  if (section === 's1') return (
    <>
      <div style={styles.kicker}>TUJUH TRIWULAN · 2025–2026</div>
      <div style={styles.title}>Tumbuhnya sudah menyalip,<br/>ekonominya belum.</div>
      <div style={{...styles.row, marginTop: 20}}>
        <div style={{...styles.card, flex: 1, borderColor: C.vn, transform: `translateY(${rise(6)}px)`, opacity: opa(6)}}>
          <div style={{fontSize: 120}}>✓</div>
          <div style={{fontSize: 42, fontWeight: 800, color: C.vn}}>{VN}: SUDAH</div>
          <div style={styles.sub}>Pertumbuhan lebih cepat<br/>di 7 dari 7 triwulan.</div>
        </div>
        <div style={{...styles.card, flex: 1, borderColor: C.amber, transform: `translateY(${rise(14)}px)`, opacity: opa(14)}}>
          <div style={{fontSize: 120}}>?</div>
          <div style={{fontSize: 42, fontWeight: 800, color: C.amber}}>{IDN}: BELUM</div>
          <div style={styles.sub}>Level per kapita masih<br/>imgbang atau proyeksi.</div>
        </div>
      </div>
    </>
  );

  if (section === 's2' || section === 's3') {
    const q = section === 's2' ? ['Q1','Q2','Q3','Q4'] : ['Q1','Q2','Q3'];
    const vn = section === 's2' ? [7.05,8.16,8.25,8.46] : [8.15,8.81,9.95];
    const idn = section === 's2' ? [4.87,5.12,5.04,5.20] : [5.61,5.29,5.47];
    const max = 11;
    if (section === 's2') {
      const pts = (arr: number[]) => arr.map((v,i)=>`${140 + i*400},${780 - v/max*560}`).join(' ');
      return (
        <>
          <div style={styles.kicker}>DATA AKTUAL · BPS &amp; NSO</div>
          <div style={styles.title}>2025: Vietnam unggul di setiap triwulan</div>
          <svg viewBox="0 0 1560 860" style={{width: '100%', height: 650}}>
            {[0,1,2,3].map(i=><line key={i} x1={100} x2={1560} y1={200+i*190} y2={200+i*190} stroke="#ffffff12" strokeWidth={2}/>)}
            <polyline points={pts(idn)} fill="none" stroke={C.idn} strokeWidth={10} strokeLinecap="round" opacity={opa(20)}/>
            <polyline points={pts(vn)} fill="none" stroke={C.vn} strokeWidth={12} strokeLinecap="round" opacity={opa(10)}/>
            {vn.map((v,i)=><text key={i} x={140+i*400} y={760} fill={C.muted} fontSize={32} textAnchor="middle">Q{i+1}</text>)}
            {vn.map((v,i)=><text key={i} x={140+i*400} y={770-v/max*560} fill={C.vn} fontSize={38} fontWeight={800} textAnchor="middle" opacity={opa(16+i*4)}>{v.toFixed(2)}</text>)}
          </svg>
          <div style={styles.foot}>BPS Indonesia · NSO Vietnam · angka Indonesia dibulatkan (~)</div>
        </>
      );
    }
    return (
      <>
        <div style={styles.kicker}>DATA AKTUAL · 2026</div>
        <div style={styles.title}>Selisih membesar: 2,2 → 4,5 poin</div>
        <div style={{display:'flex', alignItems:'flex-end', height:620, gap:40, marginTop:20}}>
          {q.map((label,i)=>{
            const h1 = vn[i]/max*520, h2 = idn[i]/max*520;
            return <div key={i} style={{flex:1, textAlign:'center'}}>
              <div style={{display:'flex', justifyContent:'center', alignItems:'flex-end', height:540, gap:10}}>
                <div style={{...styles.bar, width:90, height:h1*enter, background:C.vn}}/> 
                <div style={{...styles.bar, width:90, height:h2*enter, background:C.idn, opacity:0.9}}/>
              </div>
              <div style={{fontSize:34, marginTop:16, fontWeight:700}}>{label}</div>
              <div style={{color:C.vn, fontSize:28}}>{vn[i].toFixed(2)}</div>
              <div style={{color:C.idn, fontSize:28}}>{idn[i].toFixed(2)}</div>
            </div>;
          })}
        </div>
        <div style={{...styles.badge, marginTop:20, background:C.vn}}>VN Q1/Q2 direvisi naik</div>
      </>
    );
  }

  if (section === 's4') return (
    <>
      <div style={styles.kicker}>BUKTI UTAMA</div>
      <div style={{fontSize:220, color:C.vn, transform:`scale(${0.8+0.2*enter})`}}>✓</div>
      <div style={styles.title}>Tumbuhnya sudah menyalip.</div>
      <div style={styles.sub}>Tujuh dari tujuh triwulan Vietnam tumbuh lebih cepat<br/>menurut data aktual BPS dan NSO.</div>
      <div style={{...styles.badge, marginTop:30, background:C.vn}}>7 / 7 QUARTERS · PROVEN</div>
    </>
  );

  if (section === 's5') return (
    <>
      <div style={styles.kicker}>CATATAN PENTING</div>
      <div style={{fontSize:180, color:C.amber}}>!</div>
      <div style={styles.title}>Pertumbuhan ≠ level.</div>
      <div style={styles.sub}>BPS dan NSO tidak menerbitkan PDB per kapita USD per triwulan.<br/>Klaim “menyalip” hanya tepat untuk pertumbuhan.</div>
      <div style={{...styles.badge, marginTop:30}}>NO QUARTERLY PER-CAPITA USD SERIES</div>
    </>
  );

  if (section === 's6') return (
    <>
      <div style={styles.kicker}>BANK DUNIA · 2025</div>
      <div style={styles.title}>Dua basis harga, dua kesimpulan</div>
      <div style={styles.row}>
        <div style={{...styles.card, flex:1, borderColor:C.vn}}>
          <div style={{fontSize:30, color:C.muted}}>CURRENT USD</div>
          <div style={{fontSize:52, fontWeight:800, marginTop:10}}>$5.066 <span style={{color:C.muted}}>vs</span> $5.060</div>
          <div style={{...styles.badge, marginTop:18, background:C.amber, color:'#0B1220'}}>DEAD HEAT · selisih $6</div>
        </div>
        <div style={{...styles.card, flex:1, borderColor:C.idn}}>
          <div style={{fontSize:30, color:C.muted}}>CONSTANT 2015 USD</div>
          <div style={{fontSize:52, fontWeight:800, marginTop:10}}>$4.308 <span style={{color:C.muted}}>vs</span> $4.555</div>
          <div style={{...styles.badge, marginTop:18, background:C.idn, color:'#0B1220'}}>INDONESIA +5,7%</div>
        </div>
      </div>
    </>
  );

  if (section === 's7') return (
    <>
      <div style={styles.kicker}>IMF · WORLD ECONOMIC OUTLOOK · OKTOBER 2026</div>
      <div style={styles.title}>Proyeksi 2026 (current USD)</div>
      <div style={styles.row}>
        <div style={{...styles.card, flex:1, borderColor:C.vn}}>
          <div style={{fontSize:30}}>{VN}</div><div style={styles.big}>$5.259</div>
        </div>
        <div style={{...styles.card, flex:1, borderColor:C.idn}}>
          <div style={{fontSize:30}}>{IDN}</div><div style={styles.big}>$5.153</div>
        </div>
      </div>
      <div style={{...styles.badge, marginTop:24, fontSize:44, padding:'18px 42px'}}>PROYEKSI · BUKAN HASIL UKUR</div>
    </>
  );

  if (section === 's8') {
    const items=[['INDUSTRI & KONSTRUksi',12.50,C.vn],['BAGIAN DARI PERTUMBUHAN',51.57,C.blue],['EKSPOR',23.27,C.idn]] as [string,number,string][];
    return <>
      <div style={styles.kicker}>MESIN PERTUMBUHAN VIETNAM · Q3 2026</div>
      <div style={styles.title}>Industri, ekspor, investasi</div>
      {items.map(([label,val,col],i)=><div key={i} style={{marginBottom:26, opacity:opa(6+i*8)}}>
        <div style={{fontSize:30, marginBottom:8}}>{label}</div>
        <div style={{height:52, width:`${Math.min(val/55*100,100)*enter}%`, background:col, borderRadius:14}}/>
        <div style={{fontSize:30, color:col, fontWeight:800}}>{val.toFixed(2)}%</div>
      </div>)}
      <div style={styles.foot}>FDI 9 bulan 2026: US$21,07 miliar (+12,1%) · sumber: NSO Vietnam</div>
    </>;
  }

  if (section === 's9') return (
    <>
      <div style={styles.kicker}>KENAPA LEVEL BELUM TERSOALIP</div>
      <div style={styles.title}>Penduduk &amp; nilai tukar</div>
      <div style={styles.row}>
        <div style={{...styles.card, flex:1}}><div style={{fontSize:30, color:C.muted}}>POPULASI 2025</div><div style={styles.big}>101,6<span style={{fontSize:44}}> jt</span></div><div style={styles.label}>{VN}</div></div>
        <div style={{...styles.card, flex:1}}><div style={{fontSize:30, color:C.muted}}>POPULASI 2025</div><div style={styles.big}>285,7<span style={{fontSize:44}}> jt</span></div><div style={styles.label}>{IDN}</div></div>
      </div>
      <div style={{...styles.card, marginTop:26}}>
        <div style={{fontSize:34, color:C.idn, fontWeight:800}}>RUPIAH −3,9%</div>
        <div style={styles.sub}>VND sekitar −2…−3% · pelemahan rupiah menurunkan PDB per kapita dolar Indonesia.</div>
      </div>
    </>
  );

  if (section === 's10') return (
    <>
      <div style={styles.kicker}>SENSITIVITAS</div>
      <div style={styles.title}>Selisihnya cuma 2,1%</div>
      <div style={{...styles.card, marginTop:10}}>
        <div style={{display:'flex', alignItems:'baseline', gap:30}}>
          <div style={{fontSize:170, fontWeight:900, color:C.amber}}>2,1%</div>
          <div style={styles.sub}>lebih kecil daripada kemungkinan<br/>kesalahan proyeksi.</div>
        </div>
        <div style={{height:30, background:'#1E293B', borderRadius:15, marginTop:20}}>
          <div style={{height:30, width:`${enter*100}%`, background:C.amber, borderRadius:15}}/>
        </div>
      </div>
      <div style={{...styles.badge, marginTop:26}}>PROYEKSI · BISA BERUBAH</div>
    </>
  );

  // s11 closing
  return (
    <>
      <div style={styles.kicker}>KESIMPULAN</div>
      <div style={styles.title}>Tumbuhnya SUDAH.<br/>Ekonominya BELUM.</div>
      <div style={styles.sub}>Tujuh triwulan data BPS &amp; NSO · proyeksi IMF WEO Oktober 2026</div>
      <div style={{...styles.card, marginTop:30}}>
        <div style={{fontSize:30, color:C.muted}}>SUMBER DATA</div>
        <div style={{fontSize:36, marginTop:10}}>BPS Indonesia · NSO Vietnam · Bank Dunia · IMF WEO Oktober 2026</div>
      </div>
      <div style={{...styles.badge, marginTop:24, background:C.vn, color:'#0B1220'}}>CEK ANGKA NYA · PERHATIKAN BASIS HARGA</div>
    </>
  );
};

export const Graphic: React.FC<{section: string; description: string}> = ({section}) => {
  const {fade} = useAnim();
  return (
    <AbsoluteFill style={{...styles.root, opacity: fade}}>
      <AbsoluteFill style={styles.grid}/>
      <div style={{position:'relative', zIndex:1, height:'100%'}}>
        <Content section={section}/>
      </div>
    </AbsoluteFill>
  );
};
