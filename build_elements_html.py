# -*- coding: utf-8 -*-
"""Buduje index.html — żywioły Sebastiana i Piotrka (z elements.json / kerykeion)."""
import json, html
with open("elements.json",encoding="utf-8") as f: D=json.load(f)
S,P=D["sebastian"],D["piotrek"]
def e(x): return html.escape(str(x))

EL=[("Ogień","🔥","ogn","działanie, zapał, odwaga, spontaniczność",
     "Baran, Lew, Strzelec","energia i inicjatywa — robisz pierwszy krok, zarażasz entuzjazmem",
     "porywczość, niecierpliwość","brak napędu, trudność z asertywnością i „zapaleniem się”"),
    ("Ziemia","🌍","zie","praktyczność, stabilność, konkret, cierpliwość",
     "Byk, Panna, Koziorożec","ugruntowanie — doprowadzasz rzeczy do końca, dbasz o realia i bezpieczeństwo",
     "sztywność, materializm","trudność z ugruntowaniem, rutyną, finansami, dokańczaniem"),
    ("Powietrze","🌬️","pow","umysł, komunikacja, idee, towarzyskość",
     "Bliźnięta, Waga, Wodnik","intelekt i kontakt — myślisz, gadasz, łączysz ludzi i pomysły",
     "życie „w głowie”, dystans od uczuć","trudność z nazywaniem myśli i obiektywnym dystansem"),
    ("Woda","💧","wod","emocje, intuicja, wrażliwość, empatia",
     "Rak, Skorpion, Ryby","głębia uczuć — czujesz, wyczuwasz, współodczuwasz, masz intuicję",
     "przytłoczenie emocjami, branie wszystkiego do siebie","trudność z empatią i okazywaniem uczuć")]
ELI={x[0]:x for x in EL}
KOL={"Ogień":"var(--ogn)","Ziemia":"var(--zie)","Powietrze":"var(--pow)","Woda":"var(--wod)"}

def dominant(o):
    mx=max(o["licz"].values()); return [k for k,v in o["licz"].items() if v==mx]
def weakest(o):
    mn=min(o["licz"].values()); return [k for k,v in o["licz"].items() if v==mn]

# narracje per osoba (interpretacja oparta na danych)
NARR={
"Sebastian":"""<p>Twój rozkład żywiołów jest <b>wyjątkowo zrównoważony</b> — masz po trochu
ze wszystkiego, z lekkim niedoborem <b>Ziemi</b>. To czyni Cię <b>wszechstronnym</b>: rozumiesz
i działanie, i emocje, i idee. Ale jest tu ważny smaczek — Twoja <b>„wielka trójka” (Słońce,
Księżyc, Ascendent) jest w całości w Powietrzu</b>. To znaczy, że Twój <b>rdzeń jest umysłowy
i relacyjny</b>: żyjesz ideami, rozmową i kontaktem z ludźmi, a uczucia chętnie „przepuszczasz
przez głowę”.</p>
<p><b>Co warto wiedzieć:</b> Twoją piętą achillesową jest <b>Ziemia</b> — czyli ugruntowanie,
rutyna i dociąganie spraw do końca. Świetnie zaczynasz i ogarniasz wiele wątków, ale pomaga Ci
świadome trzymanie się konkretów. I druga rzecz: skoro rdzeń masz powietrzny, czasem warto
celowo <b>zejść z głowy do ciała i emocji</b> — zwłaszcza w bliskich relacjach.</p>""",
"Piotrek":"""<p>U Ciebie jeden żywioł wyraźnie rządzi: <b>Woda</b> (najwięcej punktów), a
<b>Ognia masz jak na lekarstwo</b> (zaledwie jeden). Jesteś więc <b>osobą głęboko czującą,
intuicyjną i wrażliwą</b> — wyłapujesz nastroje, których inni nie widzą, i przeżywasz świat
mocno, choć nie zawsze to pokazujesz. Ciekawy kontrast: Twój <b>umysł jest powietrzny</b>
(Słońce, Merkury i Wenus w Bliźniętach — lekki, gadatliwy, ciekawy), ale <b>dusza jest wodna</b>
(Księżyc w Skorpionie, Ascendent w Raku). Stąd czasem „<b>mówię lekko, a czuję bardzo mocno</b>”.</p>
<p><b>Co warto wiedzieć:</b> Twój brakujący żywioł to <b>Ogień</b> — czyli spontaniczny napęd,
asertywność i „rozpalanie się” do działania. Wrażliwość to Twój największy atut, ale uważaj, by
<b>nie utonąć w emocjach</b> i czasem po prostu <b>zadziałać</b>, nie czekając aż „poczujesz, że
pora”. Świadome dokładanie sobie ognia (sport, decyzje na już, mówienie „chcę”) świetnie Cię
równoważy.</p>"""}

def bars(o):
    rows=[]
    for nazwa,emo,cls,*_ in EL:
        v=o["licz"][nazwa]; w=int(100*v/4)
        planety=", ".join(o["dist"][nazwa]) if o["dist"][nazwa] else "— (brak)"
        rows.append(f"""<div class="elrow">
          <div class="elhead"><span class="elname">{emo} {nazwa}</span><span class="elcount">{v}</span></div>
          <div class="bar"><span style="width:{w}%;background:{KOL[nazwa]}"></span></div>
          <div class="elplanety">{e(planety)}</div></div>""")
    return "".join(rows)

def badge(o):
    dom=dominant(o); wk=weakest(o)
    de=ELI[dom[0]][1]; we=ELI[wk[0]][1]
    return (f'<span class="bdg dom">Dominujący: {de} {" / ".join(dom)}</span>'
            f'<span class="bdg wk">Najsłabszy: {we} {" / ".join(wk)}</span>')

def kolumna(o):
    return f"""<div class="cell">
      <div class="who"><div class="emoji">{'🧔' if o['imie']=='Sebastian' else '🧑'}</div>
        <h2>{e(o['imie'])}</h2><div class="badges">{badge(o)}</div></div>
      <div class="bars">{bars(o)}</div>
      <div class="narr">{NARR[o['imie']]}</div>
    </div>"""

# sekcja "czym sa zywioly"
elcards="".join(f"""<div class="elcard" style="--c:{KOL[n]}">
  <div class="elcardh">{emo} {n}</div>
  <div class="elcardz">{e(znaki)}</div>
  <div class="elcardd">{e(opis)}</div>
  <div class="elcardplus"><b>Mocna strona:</b> {e(plus)}</div>
  <div class="elcardminus"><b>Za dużo:</b> {e(za)} · <b>Za mało:</b> {e(brak)}</div>
</div>""" for (n,emo,cls,opis,znaki,plus,za,brak) in EL)

HTML=f"""<!DOCTYPE html><html lang="pl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Żywioły — Sebastian i Piotrek</title>
<style>
:root{{--bg:#0f1226;--card:#1a1e3c;--card2:#222753;--ink:#eef1ff;--mut:#a7afdd;--line:#323873;
--seb:#5aa9d6;--pio:#e08a5a;--ogn:#e8553e;--zie:#7a9d54;--pow:#5aa9d6;--wod:#5566c9;}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
background:radial-gradient(1100px 600px at 18% -10%,#26285a,transparent),
radial-gradient(900px 500px at 100% 0,#2a1c44,transparent),var(--bg);color:var(--ink);
line-height:1.6;padding:0 0 60px}}
.top{{text-align:center;padding:46px 16px 6px}} .top h1{{margin:0;font-size:31px}}
.top .sub{{color:var(--mut);max-width:640px;margin:10px auto 0}}
.wrap{{max-width:1020px;margin:0 auto;padding:0 16px}}
.sectitle{{text-align:center;font-size:23px;margin:34px 0 4px}}
.sectitle .s{{display:block;color:var(--mut);font-size:14px;font-weight:400;margin-top:4px}}
.elcards{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}}
.elcard{{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--c);
border-radius:13px;padding:14px}}
.elcardh{{font-size:18px;font-weight:700}} .elcardz{{color:var(--mut);font-size:12.5px;margin:2px 0 8px}}
.elcardd{{font-size:14px;margin-bottom:8px}}
.elcardplus{{font-size:13px;color:#cfe6c8;margin-bottom:3px}}
.elcardminus{{font-size:12.5px;color:var(--mut)}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:14px;align-items:start}}
.cell{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px}}
.pair>.cell:first-child{{border-top:4px solid var(--seb)}}
.pair>.cell:last-child{{border-top:4px solid var(--pio)}}
.who{{text-align:center;margin-bottom:10px}} .who .emoji{{font-size:36px}} .who h2{{margin:4px 0}}
.badges{{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:6px}}
.bdg{{font-size:12px;font-weight:600;padding:4px 10px;border-radius:14px;border:1px solid var(--line)}}
.bdg.dom{{background:rgba(95,208,138,.14);color:#7fe0a0}}
.bdg.wk{{background:rgba(231,161,78,.14);color:#e7a14e}}
.bars{{margin:8px 0 14px}}
.elrow{{margin:9px 0}}
.elhead{{display:flex;justify-content:space-between;font-size:14px;font-weight:600}}
.elcount{{color:var(--mut)}}
.bar{{height:13px;background:#2a2f63;border-radius:8px;overflow:hidden;margin:3px 0}}
.bar span{{display:block;height:100%;border-radius:8px}}
.elplanety{{font-size:11.5px;color:var(--mut)}}
.narr{{font-size:14.5px;border-top:1px dashed var(--line);padding-top:12px}}
.narr p{{margin:0 0 11px}} .narr p:last-child{{margin:0}}
.tldr{{background:var(--card2);border:1px solid var(--line);border-radius:16px;padding:22px;margin-top:26px}}
.tldr h3{{margin:0 0 8px;text-align:center;font-size:21px}}
.tldr p{{max-width:840px;margin:6px auto 0}}
.note{{color:var(--mut);font-size:13px;text-align:center;border-top:1px solid var(--line);margin-top:18px;padding-top:12px}}
@media(max-width:680px){{.elcards,.pair{{grid-template-columns:1fr}}}}
</style></head><body>
<div class="top">
  <h1>🜂🜃🜁🜄 Wasze żywioły</h1>
  <p class="sub">Z czego „zbudowane” są mapy Sebastiana i Piotrka — i co to dla Was znaczy.
  Policzone z narzędzia <b>kerykeion</b> (10 planet + Ascendent = 11 punktów).</p>
</div>
<div class="wrap">

  <h2 class="sectitle">Cztery żywioły<span class="s">krótki słowniczek — co który oznacza</span></h2>
  <div class="elcards">{elcards}</div>

  <h2 class="sectitle">Wasze rozkłady<span class="s">ile planet w którym żywiole + co to o Was mówi</span></h2>
  <div class="pair">{kolumna(S)}{kolumna(P)}</div>

  <div class="tldr">
    <h3>🧭 W skrócie — Wy dwaj obok siebie</h3>
    <p><b>Sebastian</b> jest <b>zrównoważony z powietrznym rdzeniem</b> — wszechstronny umysłowiec
    i „relacyjniak”, któremu najmniej dostaje <b>Ziemi</b> (ugruntowania). <b>Piotrek</b> to
    <b>człowiek Wody</b> — głęboko czujący i intuicyjny, z lekkim umysłem Bliźniąt na wierzchu,
    ale niemal bez <b>Ognia</b> (spontanicznego napędu).</p>
    <p>Ciekawostka: <b>obu Wam najmniej dostaje „twardych” żywiołów działania</b> — Sebastianowi
    Ziemi, Piotrkowi Ognia. Inaczej mówiąc: obaj jesteście bardziej <b>od myślenia i czucia niż od
    napierania</b>. Świadome dokładanie sobie tego, czego brakuje (Sebastian — konkret i rutyna,
    Piotrek — odwaga i „działam teraz”), to Wasza najprostsza droga do równowagi.</p>
  </div>

  <p class="note">⚖️ Pozycje planet policzone dokładnie (kerykeion / Swiss Ephemeris), ale
  znaczenia żywiołów to symbolika i tradycja — nie nauka. Potraktujcie to jako lustro do
  autorefleksji. 💛</p>
</div>
</body></html>"""
with open("index.html","w",encoding="utf-8") as f: f.write(HTML)
print("index.html (zywioly) zapisany,", len(HTML), "znakow")
