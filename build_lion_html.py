# -*- coding: utf-8 -*-
"""Pełny raport indywidualny dla Liona (z lion.json / kerykeion).
Format jak raport Sebastian/Piotrek: 6 działów, narracja + dowody, jedna osoba."""
import json, html
with open("lion.json",encoding="utf-8") as f: O=json.load(f)
def e(x): return html.escape(str(x))
def pt(p):
    if not p: return "—"
    return f"{p['znak']} {p['stopnie']}°" + (f" · dom {p['dom']}" if p.get('dom') else "")
EMO={"Słońce":"☉","Księżyc":"☽","Merkury":"☿","Wenus":"♀","Mars":"♂","Jowisz":"♃",
 "Saturn":"♄","Uran":"♅","Neptun":"♆","Pluton":"♇"}

NARR={
"rdzen":"""<p>W środku jesteś <b>człowiekiem głębokiego serca i spokojnej siły</b>. Twoje Słońce
w <b>Raku</b> to wrażliwość, opiekuńczość i przywiązanie do bliskich — a w domu 3 wyrażasz to
przede wszystkim <b>słowem i codziennym kontaktem</b>. Twój Księżyc w <b>Skorpionie</b> sprawia,
że emocje przeżywasz <b>intensywnie, głęboko i po cichu</b> — „wszystko albo nic”, czujesz mocno,
choć nie afiszujesz.</p>
<p>Na zewnątrz Ascendent w <b>Byku</b> daje Ci <b>spokojną, stabilną, ciepłą powierzchowność</b> —
jesteś jak solidna opoka, do której inni lgną. Przykład: rzadko wybuchasz, ale gdy Ci na kimś
naprawdę zależy, jesteś lojalny do samego końca.</p>""",
"umysl":"""<p>Myślisz <b>sercem i pamięcią</b> — Merkury w Raku łączy intelekt z intuicją i
emocją (i rzadko zapominasz, zwłaszcza krzywd). Ale Merkury <b>zlany z Marsem</b> daje Ci
<b>ostry, bystry, bezpośredni umysł</b>: potrafisz ciąć słowem jak brzytwą i błyszczysz w
dyskusji. A subtelny akord Merkury–Neptun dokłada <b>wyobraźnię i poetyckość</b>.</p>
<p>W miłości (Wenus w <b>Pannie</b>, dom 5) kochasz przez <b>konkret i troskę</b> — okazujesz
uczucie pomaganiem i dbaniem o szczegóły, nie wielkimi słowami. Cenisz oddanie i praktyczną
wierność bardziej niż fajerwerki.</p>""",
"dzialanie":"""<p>Działasz <b>z emocji i uporu, nie z brawury</b>. Masz <b>zero planet w Ogniu</b> —
więc nie napędza Cię surowa agresja ani spontaniczny poryw; do celu prziesz <b>wytrwałością i
determinacją</b> (mnóstwo energii kardynalnej i stałej, mało zmiennej). Mars w Raku włącza się
najmocniej <b>w obronie bliskich</b> — jesteś wojownikiem, gdy chodzi o rodzinę, a zwarcie Marsa
z Plutonem daje Ci <b>potężną, transformującą siłę woli</b>.</p>
<p>Uwaga na jedno: Mars w mocnym napięciu z Jowiszem potrafi pchać Cię do <b>przesady</b> —
brania na siebie za dużo i przeceniania sił. Twoja prawdziwa moc to <b>wytrwałość, nie szarża</b>.</p>""",
"aspekty":"""<p><b>Twój największy dar:</b> Słońce w niemal idealnej harmonii z Saturnem
(orb 0,03°!) — <b>wrodzona dojrzałość, dyscyplina i odpowiedzialność</b>. Jesteś typem
„self-made”, który buduje solidnie i wytrwale, i na którym można polegać jak na fundamencie.
<b>Twój bystry oręż:</b> Merkury zwarty z Marsem — umysł ostry, gotowy do debaty.
<b>Twoje wyzwanie:</b> Mars kontra Jowisz (orb 0,06°) — skłonność do przeceniania sił; ucz się
mówić „nie”. <b>Twoja subtelność:</b> Merkury–Neptun — wyobraźnia i artystyczna nuta.</p>""",
"glebia":"""<p><b>Twoja życiowa lekcja</b> (Węzeł Północny w Rybach, dom 11): odpuścić kontrolę
i nadmierną analizę, <b>zaufać intuicji i płynąć</b> — a także otworzyć się na wspólnotę,
marzenia i coś większego niż Ty sam. <b>Twój czuły punkt</b> (Chiron w Baranie, dom 12) dotyczy
prawa do <b>bycia sobą i stawiania siebie na pierwszym miejscu</b> — to rana wokół asertywności,
którą leczysz w ciszy i wewnętrznej pracy. <b>Pluton w domu twórczości</b> daje Ci głęboką,
przemieniającą moc w tym, co tworzysz i kogo kochasz.</p>""",
"liczba":"""<p>Twoja Liczba Życia to <b>1 — Lider</b> (jak przydomek „Lion”!). To energia
<b>niezależności, inicjatywy i pionierstwa</b>: masz w sobie „zrobię to sam i po swojemu”.
Ciekawy kontrast: numerologia widzi w Tobie <b>samodzielnego wodza</b>, a astrologia — czułego,
wodnego Raka. Twoja prawdziwa siła leży w połączeniu obu: <b>przewodzisz nie naporem, lecz opieką
i wytrwałością</b>. Liczba dnia 4 (solidny budowniczy) i postawa 2 (dyplomata) tylko to
potwierdzają — prowadzisz stabilnie i po ludzku.</p>""",
}
def el(k,v): return f'<div class="el"><span>{k}</span><b>{v}</b></div>'
def ev_rdzen(o): return el("☉ Słońce",pt(o["slonce"]))+el("☽ Księżyc",pt(o["ksiezyc"]))+el("⬆ Ascendent",pt(o["ascendent"]))+el("⟂ MC",pt(o["mc"]))
def ev_umysl(o):
    out=el("☿ Merkury",pt(o["planety"]["Merkury"]))+el("♀ Wenus",pt(o["planety"]["Wenus"]))
    for a in o["aspekty"]:
        if {a["p1"],a["p2"]}=={"Merkury","Mars"}: out+=el("☿ zwarty z ♂","koniunkcja (orb %s°)"%a["orb"]); break
    return out
def ev_dzialanie(o):
    z=o["zywioly"]; j=o["jakosci"]
    return (el("♂ Mars",pt(o["planety"]["Mars"]))
      +el("Żywioły",f"Ogień {z['Ogień']} · Ziemia {z['Ziemia']} · Powietrze {z['Powietrze']} · Woda {z['Woda']}")
      +el("Jakości",f"Kard. {j['Kardynalna']} · Stała {j['Stała']} · Zmien. {j['Zmienna']}"))
def ev_aspekty(o): return "".join(el(f"{EMO.get(a['p1'],'')}{a['p1']} – {a['p2']}",f"{a['aspekt']} (orb {a['orb']}°)") for a in o["aspekty"][:5])
def ev_glebia(o): return el("Węzeł Północny",pt(o["wezel_polnocny"]))+el("Chiron",pt(o["chiron"]))+el("♇ Pluton",pt(o["planety"]["Pluton"]))
def ev_liczba(o):
    n=o["numerologia"]
    return (f'<div class="bignum">{n["liczba_zycia"]}</div><div class="calc">cyfry daty → suma {n["liczba_zycia_suma"]} → {n["liczba_zycia"]}</div>'
      +el("Liczba dnia",n["liczba_dnia"])+el("Liczba postawy",n["liczba_postawy"]))

TEMATY=[("rdzen","🔑 Kim jesteś w środku","Rdzeń: <b>Słońce</b> (kim jesteś), <b>Księżyc</b> (co czujesz), <b>Ascendent</b> (jak Cię widzą).",ev_rdzen),
 ("umysl","💬 Jak myślisz i kochasz","Sposób myślenia (Merkury) oraz to, co i jak kochasz (Wenus).",ev_umysl),
 ("dzialanie","⚡ Jak działasz","Energia i styl działania (Mars) plus temperament — żywioły i tryby.",ev_dzialanie),
 ("aspekty","🔗 Talenty i wyzwania","Najsilniejsze „rozmowy” planet. Mniejszy orb = mocniejszy wpływ.",ev_aspekty),
 ("glebia","🌑 Głębia i droga życia","Życiowa lekcja (Węzeł), czuły punkt (Chiron), siła przemiany (Pluton).",ev_glebia),
 ("liczba","🔢 Twoja Liczba Życia (numerologia)","Liczona z samej daty urodzenia — główny motyw życia.",ev_liczba)]

sekcje=[]
for key,tytul,opis,ev in TEMATY:
    sekcje.append(f"""<div class="band"><h3>{tytul}</h3><p class="banddesc">{opis}</p></div>
      <div class="cell"><div class="narr">{NARR[key]}</div>
      <details class="ev"><summary>📊 Na czym to oparte (dane z kerykeion)</summary>
        <div class="evbox">{ev(O)}</div></details></div>""")

HTML=f"""<!DOCTYPE html><html lang="pl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lion — portret astrologiczny</title>
<style>
:root{{--bg:#0f1226;--card:#1a1e3c;--card2:#222753;--ink:#eef1ff;--mut:#a7afdd;--line:#323873;--acc:#e0b15a;}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
background:radial-gradient(1100px 600px at 50% -10%,#2a2c5e,transparent),
radial-gradient(800px 500px at 100% 10%,#3a2a1c,transparent),var(--bg);color:var(--ink);
line-height:1.6;padding:0 0 60px}}
.top{{text-align:center;padding:48px 16px 6px}} .top h1{{margin:0;font-size:34px}}
.top .sub{{color:var(--mut);max-width:600px;margin:10px auto 0}}
.meta{{color:var(--mut);font-size:14px;margin-top:8px}}
.wrap{{max-width:720px;margin:0 auto;padding:0 16px}}
.band{{margin:30px 0 8px;text-align:center}} .band h3{{margin:0;font-size:22px}}
.banddesc{{color:var(--mut);max-width:640px;margin:6px auto 0;font-size:14px}}
.cell{{background:var(--card);border:1px solid var(--line);border-top:4px solid var(--acc);border-radius:14px;padding:20px}}
.narr{{font-size:15.5px}} .narr p{{margin:0 0 12px}} .narr p:last-child{{margin:0}}
.ev{{margin-top:14px;border-top:1px dashed var(--line);padding-top:8px}}
.ev summary{{cursor:pointer;color:var(--mut);font-size:12.5px;list-style:none}}
.ev summary::-webkit-details-marker{{display:none}}
.ev summary::before{{content:"▸ "}} .ev[open] summary::before{{content:"▾ "}}
.evbox{{margin-top:8px;background:#141531;border-radius:10px;padding:6px 12px}}
.el{{display:flex;justify-content:space-between;gap:10px;font-size:12.5px;color:var(--mut);padding:4px 0;border-bottom:1px solid #23254e}}
.el:last-child{{border-bottom:none}} .el b{{color:#dfe3ff;text-align:right}}
.bignum{{text-align:center;font-size:46px;font-weight:800;color:#fff;line-height:1;margin:2px 0}}
.calc{{text-align:center;font-size:11px;color:var(--mut);font-family:ui-monospace,Menlo,monospace;margin-bottom:6px}}
.tldr{{background:var(--card2);border:1px solid var(--line);border-radius:16px;padding:24px;margin-top:30px;text-align:center}}
.tldr h3{{margin:0 0 8px;font-size:22px}} .tldr p{{max-width:640px;margin:8px auto 0}}
.note{{color:var(--mut);font-size:13px;text-align:center;border-top:1px solid var(--line);margin-top:18px;padding-top:12px}}
</style></head><body>
<div class="top">
  <h1>🦁 Lion — portret astrologiczny</h1>
  <p class="sub">Osobisty raport: najpierw opowieść o Tobie, niżej — pod „📊” — dane z narzędzia
  <b>kerykeion</b>, które ją potwierdzają.</p>
  <div class="meta">{e(O['data'])} · {e(O['godzina'])} · {e(O['miasto'])} · mapa {e(O['mapa'])} · {O['faza_emoji']}</div>
</div>
<div class="wrap">
{''.join(sekcje)}
  <div class="tldr">
    <h3>🦁 W jednym zdaniu</h3>
    <p>Jesteś <b>czułym, głęboko czującym Rakiem o żelaznej dyscyplinie</b> (Słońce–Saturn),
    który przewodzi nie krzykiem, lecz <b>opieką, wytrwałością i lojalnością</b> — numerologiczna
    „jedynka” w spokojnym, wodno-ziemskim wydaniu. Twoja moc to trwanie i głębia; Twoja lekcja to
    odpuścić kontrolę i zaufać przepływowi.</p>
    <p class="note">⚖️ Pozycje policzone dokładnie (kerykeion / Swiss Ephemeris), znaczenia to
    symbolika i tradycja — nie nauka. Potraktuj to jako lustro do autorefleksji. 💛</p>
  </div>
</div>
</body></html>"""
with open("index.html","w",encoding="utf-8") as f: f.write(HTML)
print("index.html (Lion) zapisany,", len(HTML), "znakow")
