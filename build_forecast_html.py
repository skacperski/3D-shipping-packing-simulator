# -*- coding: utf-8 -*-
"""Buduje forecast.html — prognoza miłosna pary (oś czasu z forecast.json)."""
import json, html
from collections import Counter, defaultdict

with open("forecast.json", encoding="utf-8") as f:
    F = json.load(f)
EV = F["wydarzenia"]
def e(x): return html.escape(str(x))

KIND_INFO={
 "romance":("❤️","Romans","var(--rom)"),
 "passion":("🔥","Namiętność","var(--pas)"),
 "tension":("⚡","Do przepracowania","var(--ten)"),
 "commit":("💍","Stabilizacja","var(--com)"),
 "luck":("🍀","Szczęście","var(--luc)"),
}
cnt=Counter(x["kind"] for x in EV)
MIES_NAZWA={"07":"Lipiec","08":"Sierpień","09":"Wrzesień","10":"Październik","11":"Listopad","12":"Grudzień"}

# grupowanie po miesiacu
bym=defaultdict(list)
for x in EV:
    bym[x["data"][5:7]].append(x)

def event_row(x):
    emo,naz,col=KIND_INFO[x["kind"]]
    kto_col="var(--seb)" if x["kto"]=="Sebastian" else "var(--jul)"
    return f"""<div class="ev" style="--k:{col}">
      <div class="evdate">{e(x['data_pl'])}</div>
      <div class="evbody">
        <div class="evhead"><span class="evemo">{emo}</span>
          <span class="evkind">{naz}</span>
          <span class="evkto" style="background:{kto_col}">{e(x['kto'])}</span></div>
        <div class="evdesc">{e(x['opis'])}</div>
        <div class="evtech">{e(x['tp'])} {e(x['aspekt'])} → {e(x['np'])} <span class="orb">orb {x['orb']}°</span></div>
      </div></div>"""

miesiace_html=[]
for mm in sorted(bym):
    rows="".join(event_row(x) for x in bym[mm])
    miesiace_html.append(f"""<div class="month"><h3>{MIES_NAZWA.get(mm,mm)} 2026</h3>{rows}</div>""")

# liczniki podsumowania
chips=[]
for k,(emo,naz,col) in KIND_INFO.items():
    if cnt.get(k):
        chips.append(f'<div class="chip" style="--c:{col}">{emo} {naz}: <b>{cnt[k]}</b></div>')

# najgoretsze daty (najmniejszy orb romance/passion)
hot=sorted([x for x in EV if x["kind"] in ("romance","passion")], key=lambda x:x["orb"])[:3]
hot_html="".join(f'<li>{x["emoji"]} <b>{e(x["data_pl"])}</b> — {e(x["kto"])} ({e(x["tp"])} {e(x["aspekt"])} {e(x["np"])})</li>' for x in hot)

HTML=f"""<!DOCTYPE html><html lang="pl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sebastian & Julka — Prognoza miłosna</title>
<style>
:root{{--bg:#0e1430;--card:#18203f;--card2:#1f2950;--ink:#eef2ff;--mut:#9fb0e0;--line:#2c3766;
--seb:#5aa9d6;--jul:#e86fa6;--rom:#e8639a;--pas:#e8553e;--ten:#e7a14e;--com:#7a9d54;--luc:#5fd08a;}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
background:radial-gradient(1200px 600px at 15% -10%,#23306a,transparent),
radial-gradient(900px 500px at 100% 0,#3a1d55,transparent),var(--bg);color:var(--ink);
line-height:1.6;padding:0 0 60px}}
.top{{text-align:center;padding:48px 16px 6px}} .top h1{{margin:0;font-size:32px}}
.top .sub{{color:var(--mut);max-width:640px;margin:10px auto 0}}
.wrap{{max-width:760px;margin:0 auto;padding:0 16px}}
.legend{{display:flex;gap:18px;justify-content:center;margin:14px 0 0;flex-wrap:wrap}}
.legend span{{display:flex;align-items:center;gap:7px;font-weight:600;font-size:14px}}
.dot{{width:13px;height:13px;border-radius:50%}}
.summary{{background:var(--card2);border:1px solid var(--line);border-radius:16px;padding:20px;margin:22px 0}}
.summary h2{{margin:0 0 10px;font-size:20px;text-align:center}}
.chips{{display:flex;gap:10px;flex-wrap:wrap;justify-content:center}}
.chip{{background:#131a38;border:1px solid var(--c);color:var(--ink);border-radius:20px;padding:6px 13px;font-size:13.5px}}
.hot{{margin:14px 0 0;background:#131a38;border-radius:12px;padding:12px 16px}}
.hot h4{{margin:0 0 6px;font-size:14px;color:var(--mut)}} .hot ul{{margin:0;padding-left:18px}}
.month{{margin:26px 0 0}}
.month h3{{font-size:20px;margin:0 0 10px;border-bottom:2px solid var(--line);padding-bottom:6px}}
.ev{{display:flex;gap:14px;background:var(--card);border:1px solid var(--line);
border-left:4px solid var(--k);border-radius:12px;padding:12px 14px;margin:0 0 10px}}
.evdate{{min-width:92px;font-weight:700;color:var(--ink)}}
.evbody{{flex:1}}
.evhead{{display:flex;align-items:center;gap:8px;flex-wrap:wrap}}
.evemo{{font-size:18px}} .evkind{{font-weight:700;color:var(--k)}}
.evkto{{margin-left:auto;color:#0e1430;font-weight:700;font-size:12px;padding:2px 9px;border-radius:12px}}
.evdesc{{font-size:14.5px;margin:3px 0}}
.evtech{{font-size:12px;color:var(--mut)}} .orb{{opacity:.7}}
.note{{color:var(--mut);font-size:13px;text-align:center;border-top:1px solid var(--line);
margin-top:30px;padding-top:16px}}
.howto{{background:var(--card2);border:1px solid var(--line);border-radius:14px;padding:16px;margin-top:24px;font-size:14px}}
.howto b{{color:var(--ink)}}
</style></head><body>
<div class="top">
  <h1>💞 Prognoza miłosna</h1>
  <p class="sub">Sebastian &amp; Julka · {e(F['od'])} – {e(F['do'])}<br>
  „Pogoda dla Waszej miłości” — tranzyty planet po Waszych mapach (z narzędzia <b>kerykeion</b>).</p>
  <div class="legend">
    <span><span class="dot" style="background:var(--seb)"></span>Sebastian</span>
    <span><span class="dot" style="background:var(--jul)"></span>Julka</span>
  </div>
</div>
<div class="wrap">
  <div class="summary">
    <h2>📊 Co Was czeka przez te 6 miesięcy</h2>
    <div class="chips">{''.join(chips)}</div>
    <div class="hot"><h4>🌟 Najmocniejsze, najgorętsze daty:</h4><ul>{hot_html}</ul></div>
  </div>

  {''.join(miesiace_html)}

  <div class="howto">
    <b>Jak to czytać?</b> ❤️ Romans = czas na bliskość i czułe gesty · 🔥 Namiętność = iskra
    i energia · ⚡ Do przepracowania = więcej cierpliwości i rozmowy (nie panikujcie — to okna
    wzrostu!) · 💍 Stabilizacja = dobry moment na poważne decyzje · 🍀 Szczęście = wspólna dobra
    passa. Im mniejszy <b>orb</b>, tym mocniej dany dzień „działa”.
  </div>
  <p class="note">⚖️ Dla zabawy i autorefleksji — tranzyty policzone dokładnie (kerykeion /
  Swiss Ephemeris), ale ich znaczenia to symbolika, nie nauka. Żadna data niczego nie gwarantuje
  ani nie przekreśla — to Wy piszecie swój związek. 💛</p>
</div>
</body></html>"""

with open("forecast.html","w",encoding="utf-8") as f:
    f.write(HTML)
print("forecast.html zapisany,", len(HTML), "znakow |", len(EV), "wydarzen")
