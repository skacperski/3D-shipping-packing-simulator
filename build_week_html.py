# -*- coding: utf-8 -*-
"""Kalendarz horoskopu 6-dniowego dla 3 osob (z week.json / kerykeion) -> index.html."""
import json, html
with open("week.json",encoding="utf-8") as f: W=json.load(f)
DAYS=W["days"]; RES=W["res"]
def e(x): return html.escape(str(x))
MIES={"06":"cze","07":"lip"}
def dlabel(iso):
    y,m,d=iso.split("-"); return f"{int(d)} {MIES.get(m,m)}"

def vibe(score):
    if score>=3: return ("☀️","Świetnie","var(--good)")
    if score>=1: return ("🙂","Dobrze","var(--ok)")
    if score==0: return ("😐","Spokojnie","var(--neu)")
    if score>=-2: return ("🌥️","Mieszanie","var(--mix)")
    return ("🌧️","Trudniej","var(--bad)")

NOTES={
("Sebastian","2026-06-28"):"Wenus muska Twoją oś relacji — miły, ciepły dzień na kontakty i bliskość.",
("Sebastian","2026-06-29"):"Wenus jeszcze grzeje, ale Saturn zaczyna napierać na uczucia — lekki cień na nastroju.",
("Sebastian","2026-06-30"):"Saturn ściska Wenus i Księżyc — emocjonalnie ciężej, poczucie dystansu. Bądź dla siebie łagodny.",
("Sebastian","2026-07-01"):"Najtrudniejszy dzień: Saturn dokładnie na Wenus i naprzeciw Księżyca — przygaszenie i obowiązki. Nie podejmuj emocjonalnych decyzji.",
("Sebastian","2026-07-02"):"Wciąż pod chmurą Saturna — odpoczynek i mniej wymagań od siebie. To minie.",
("Sebastian","2026-07-03"):"Saturn powoli odpuszcza — robi się lżej, pierwszy oddech po trudniejszych dniach.",
("Lion","2026-06-28"):"Jowisz głaszcze Twoją oś relacji, Mars dodaje wigoru — świetny, energiczny start.",
("Lion","2026-06-29"):"Dalej dobra passa Jowisza; drobne tarcie Mars–Wenus (uważaj na wydatki i spięcia w miłości).",
("Lion","2026-06-30"):"Merkury zwiera się z Marsem — bystry umysł; dobry dzień na decyzje, rozmowy, załatwianie spraw.",
("Lion","2026-07-01"):"Szczyt formy: Jowisz plus ostry Merkury–Mars — produktywnie, pewnie i z fartem.",
("Lion","2026-07-02"):"Wenus ociepla emocje, Jowisz wciąż sprzyja — miły, ciepły i owocny dzień.",
("Lion","2026-07-03"):"Wciąż mocna passa — kontynuuj to, co zacząłeś. Wiatr w żagle.",
("Piotrek","2026-06-28"):"Saturn porządkuje myśli, Słońce w harmonii z Marsem — energia i skupienie.",
("Piotrek","2026-06-29"):"Księżyc naprzeciw Wenus — emocjonalnie trochę wrażliwiej w relacjach.",
("Piotrek","2026-06-30"):"Spokojnie i konkretnie — dobry dzień na uporządkowane, przemyślane działanie.",
("Piotrek","2026-07-01"):"Wenus muska Twoje Słońce — miły akcent, sympatia otoczenia.",
("Piotrek","2026-07-02"):"Wenus w napięciu z Księżycem — możliwy kapryśny nastrój w uczuciach.",
("Piotrek","2026-07-03"):"Wenus–Księżyc i Mars–Mars drażnią — dzień na cierpliwość, nie forsuj spięć.",
}
TREND={
"Sebastian":("🌧️","Tydzień schodzi w trudniejszą, saturnową fazę — emocjonalny reset (szczyt 1–2 lipca), potem ulga.","var(--seb)"),
"Lion":("☀️","Znakomity, energiczny i szczęśliwy tydzień — najlepsze dni 1–3 lipca.","var(--lion)"),
"Piotrek":("🙂","Stabilny tydzień z drobnymi wahnięciami nastroju pod koniec (2–3 lipca).","var(--pio)"),
}
ORDER=["Sebastian","Lion","Piotrek"]
EMO={"Sebastian":"🧔","Lion":"🦁","Piotrek":"🧑"}

def col(n):
    te,tt,tc=TREND[n]
    cells=[]
    for iso in DAYS:
        r=RES[n][iso]; ve,vt,vc=vibe(r["score"])
        top=r["top"][0] if r["top"] else None
        tech=f"{top[0]} {top[1]} {top[2]}" if top else "spokojnie"
        cells.append(f"""<div class="day" style="--v:{vc}">
          <div class="dh"><span class="dd">{e(dlabel(iso))}</span><span class="dv">{ve} {vt}</span></div>
          <div class="dnote">{e(NOTES.get((n,iso),''))}</div>
          <div class="dtech">{e(tech)}</div></div>""")
    return f"""<div class="pcol"><div class="phead" style="--pc:{tc}">
        <div class="pemo">{EMO[n]}</div><h2>{e(n)}</h2>
        <div class="ptrend">{te} {e(tt)}</div></div>{''.join(cells)}</div>"""

HTML=f"""<!DOCTYPE html><html lang="pl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Horoskop 6 dni — Sebastian, Lion, Piotrek</title>
<style>
:root{{--bg:#0e1330;--card:#191f42;--ink:#eef1ff;--mut:#a3acdd;--line:#2f3670;
--seb:#5aa9d6;--lion:#e0b15a;--pio:#e08a5a;
--good:#5fd08a;--ok:#8ec98a;--neu:#a3acdd;--mix:#e7a14e;--bad:#e0637a;}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
background:radial-gradient(1100px 600px at 20% -10%,#232a5e,transparent),
radial-gradient(900px 500px at 100% 0,#2a1c44,transparent),var(--bg);color:var(--ink);
line-height:1.55;padding:0 0 60px}}
.top{{text-align:center;padding:44px 16px 6px}} .top h1{{margin:0;font-size:29px}}
.top .sub{{color:var(--mut);max-width:640px;margin:9px auto 0}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 16px}}
.grid{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-top:20px}}
.pcol{{background:transparent}}
.phead{{background:var(--card);border:1px solid var(--line);border-top:4px solid var(--pc);
border-radius:14px;padding:14px;text-align:center;margin-bottom:10px}}
.pemo{{font-size:30px}} .phead h2{{margin:2px 0}}
.ptrend{{color:var(--mut);font-size:12.5px}}
.day{{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--v);
border-radius:12px;padding:11px 13px;margin-bottom:9px}}
.dh{{display:flex;justify-content:space-between;align-items:center;gap:8px}}
.dd{{font-weight:700}} .dv{{font-size:12px;color:var(--mut)}}
.dnote{{font-size:13px;margin:5px 0 4px}}
.dtech{{font-size:11px;color:var(--mut);opacity:.85}}
.note{{color:var(--mut);font-size:13px;text-align:center;border-top:1px solid var(--line);margin-top:26px;padding-top:14px}}
@media(max-width:760px){{.grid{{grid-template-columns:1fr}}}}
</style></head><body>
<div class="top">
  <h1>🔮 Horoskop na 6 dni</h1>
  <p class="sub">Sebastian · Lion · Piotrek — {e(dlabel(DAYS[0]))}–{e(dlabel(DAYS[-1]))} 2026.
  Tranzyty planet po Waszych mapach (z narzędzia <b>kerykeion</b>).</p>
</div>
<div class="wrap">
  <div class="grid">{''.join(col(n) for n in ORDER)}</div>
  <p class="note">☀️ Świetnie · 🙂 Dobrze · 😐 Spokojnie · 🌥️ Mieszanie · 🌧️ Trudniej.
  Ocena z siły dziennych tranzytów. ⚖️ Policzone dokładnie (kerykeion/Swiss Ephemeris),
  znaczenia to symbolika — nastrojowe lustro, nie wyrocznia. 💛</p>
</div>
</body></html>"""
with open("index.html","w",encoding="utf-8") as f: f.write(HTML)
print("index.html (tydzien 3 osoby) zapisany,", len(HTML), "znakow")
