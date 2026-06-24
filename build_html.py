# -*- coding: utf-8 -*-
"""Buduje index.html (porownanie 1:1) z data.json (dane z kerykeion + numerologia)."""
import json, html

with open("data.json", encoding="utf-8") as f:
    D = json.load(f)
S, P = D["sebastian"], D["piotrek"]

# --- poprawa polskich znakow (dane wewn. sa ASCII) ---
PL = {
    "Bliznieta":"Bliźnięta","Koziorozec":"Koziorożec","Slonce":"Słońce",
    "Ksiezyc":"Księżyc","Ogien":"Ogień","Stala":"Stała","poniedzialek":"poniedziałek",
    "Ubywajacy garb":"Ubywający garb","Przybywajacy garb":"Przybywający garb",
    "Plock":"Płock","Bialystok":"Białystok",
}
def pl(x):
    return PL.get(x, x)

# --- znaczenia symboliczne (interpretacja, opisy moje; liczby z narzedzia) ---
ZNAK_OPIS = {
    "Baran":"zapał, odwaga, inicjatywa (pierwszy rusza do akcji)",
    "Byk":"stabilność, zmysłowość, upór, cierpliwość",
    "Bliźnięta":"ciekawość, komunikacja, lekkość, wielowątkowość",
    "Rak":"opiekuńczość, emocje, przywiązanie do domu i bliskich",
    "Lew":"duma, ekspresja, serce na dłoni, chęć błyszczenia",
    "Panna":"porządek, analiza, troska o szczegóły i jakość",
    "Waga":"harmonia, takt, relacje, poczucie estetyki",
    "Skorpion":"intensywność, głębia, pasja, dociekliwość",
    "Strzelec":"optymizm, wolność, podróże, szukanie sensu",
    "Koziorożec":"ambicja, dyscyplina, odpowiedzialność, długi dystans",
    "Wodnik":"oryginalność, niezależność, idee, myślenie inaczej",
    "Ryby":"wrażliwość, wyobraźnia, empatia, intuicja",
}
PLANETA_OPIS = {
    "Słońce":"rdzeń osobowości, do czego dążysz",
    "Księżyc":"emocje i potrzeby, wewnętrzne „ja”",
    "Merkury":"myślenie i komunikacja",
    "Wenus":"miłość, gust, to co lubisz",
    "Mars":"działanie, energia, złość",
    "Jowisz":"rozwój, szczęście, optymizm",
    "Saturn":"obowiązek, dyscyplina, struktura",
    "Uran":"bunt, zmiana, oryginalność",
    "Neptun":"marzenia, duchowość, wyobraźnia",
    "Pluton":"transformacja, władza, głębia",
}
ASP_OPIS = {
    "koniunkcja":"planety zlane w jedno — działają razem, wzmacniają się",
    "opozycja":"napięcie/przeciąganie liny — trzeba szukać równowagi",
    "trygon":"harmonia, talent przychodzi naturalnie",
    "kwadratura":"tarcie, wyzwanie, które motywuje do pracy",
    "sekstyl":"szansa, łatwa współpraca dwóch energii",
    "kwintyl":"twórcza, nietypowa nuta talentu",
    "kwinkunks":"lekka niezgrana nuta, potrzeba dostrojenia",
    "półsekstyl":"delikatne połączenie sąsiednich energii",
}
LICZBA_OPIS = {
    1:("Lider","samodzielność, inicjatywa, „zrobię to po swojemu”"),
    2:("Dyplomata","współpraca, wrażliwość, równowaga, partnerstwo"),
    3:("Artysta","ekspresja, radość, komunikacja, kreatywność"),
    4:("Budowniczy","porządek, praca, stabilność, solidne fundamenty"),
    5:("Podróżnik","wolność, zmiana, przygoda, wszechstronność"),
    6:("Opiekun","rodzina, troska, odpowiedzialność, harmonia"),
    7:("Poszukiwacz","analiza, duchowość, mądrość, potrzeba zrozumienia świata"),
    8:("Realizator","ambicja, władza, pieniądze, materialny sukces, „co dasz, to wraca”"),
    9:("Humanista","współczucie, ideały, służba innym, szeroka perspektywa"),
    11:("Wizjoner (liczba mistrzowska)","intuicja, inspiracja, duchowe przewodzenie"),
    22:("Mistrz Budowniczy (liczba mistrzowska)","wielkie wizje wcielane w realne dzieła"),
    33:("Mistrz Nauczyciel (liczba mistrzowska)","bezwarunkowa miłość, uzdrawianie, nauczanie"),
}
EMOJI = {"Słońce":"☉","Księżyc":"☽","Merkury":"☿","Wenus":"♀","Mars":"♂",
         "Jowisz":"♃","Saturn":"♄","Uran":"♅","Neptun":"♆","Pluton":"♇"}

def e(x): return html.escape(str(x))

def pt(p):  # "Wodnik 28.64° (dom 5)"
    if not p: return "—"
    dom = f" · dom {p['dom']}" if p.get("dom") else ""
    return f"{pl(p['znak'])} {p['stopnie']}°{dom}"

# ---------- budowanie sekcji ----------
def osoba_naglowek(o):
    return f"""<div class="who">
        <div class="emoji">{'🧔' if o['imie']=='Sebastian' else '🧑'}</div>
        <h2>{e(o['imie'])}</h2>
        <div class="meta">{e(o['data'])} · {e(o['godzina'])}<br>{e(pl(o['miasto']))}
        · {e(o['dzien_tygodnia'])}<br>mapa {e(o['mapa'])} {o['faza_emoji']} {e(pl(o['faza_ksiezyca']))}</div>
    </div>"""

def trojca(o):
    rows = []
    for klucz, nazwa, ikona in [("slonce","Słońce","☉"),("ksiezyc","Księżyc","☽"),
                                 ("ascendent","Ascendent","⬆"),("mc","MC (cel/kariera)","⟂")]:
        p = o[klucz]
        rows.append(f"""<div class="line"><span class="k">{ikona} {nazwa}</span>
            <span class="v"><b>{pl(p['znak'])}</b> {p['stopnie']}°{(' · dom '+str(p['dom'])) if p.get('dom') else ''}</span></div>
            <div class="note">{ZNAK_OPIS.get(pl(p['znak']),'')}</div>""")
    return "".join(rows)

def planety(o):
    rows = ["<table><tr><th>Planeta</th><th>Znak</th><th>Dom</th></tr>"]
    for nazwa, p in o["planety"].items():
        n = pl(nazwa)
        rows.append(f"<tr><td>{EMOJI.get(n,'')} {n}</td><td>{pl(p['znak'])}</td>"
                    f"<td>{p['dom'] if p.get('dom') else '—'}</td></tr>")
    rows.append("</table>")
    return "".join(rows)

def punkty(o):
    out=[]
    for klucz,nazwa,opis in [("wezel_polnocny","Węzeł Północny","kierunek rozwoju, „lekcja życia”"),
                             ("chiron","Chiron","zraniony uzdrowiciel — czuły punkt i dar pomagania"),
                             ("lilith","Lilith","dzika, nieujarzmiona część natury")]:
        p=o[klucz]
        out.append(f"""<div class="line"><span class="k">{nazwa}</span>
            <span class="v">{pt(p)}</span></div><div class="note">{opis}</div>""")
    return "".join(out)

def bilans(o):
    z=o["zywioly"]; j=o["jakosci"]
    def bar(d, kolory):
        mx=max(d.values()) or 1
        b=""
        for k,v in d.items():
            kk=pl(k)
            w=int(100*v/4)
            b+=f"""<div class="bar"><span class="bl">{kk}</span>
            <span class="bt" style="--w:{w}%;--c:{kolory.get(kk,'#888')}"></span>
            <span class="bn">{v}</span></div>"""
        return b
    kolz={"Ogień":"#e8553e","Ziemia":"#7a9d54","Powietrze":"#5aa9d6","Woda":"#5566c9"}
    kolj={"Kardynalna":"#c77dab","Stała":"#b08a4a","Zmienna":"#5fae9b"}
    return f"""<div class="sub">Żywioły</div>{bar(z,kolz)}
               <div class="sub">Jakości</div>{bar(j,kolj)}"""

def aspekty(o):
    rows=["<ul class='asp'>"]
    for a in o["aspekty"][:6]:
        p1=pl(a["p1"]); p2=pl(a["p2"]); name=a["aspekt"]
        rows.append(f"""<li><b>{EMOJI.get(p1,'')}{p1} – {name} – {EMOJI.get(p2,'')}{p2}</b>
            <span class="orb">orb {a['orb']}°</span>
            <div class="note">{ASP_OPIS.get(name,'')}</div></li>""")
    rows.append("</ul>")
    return "".join(rows)

def numer(o):
    n=o["numerologia"]
    lz=n["liczba_zycia"]; tytul,opis=LICZBA_OPIS.get(lz,("",""))
    ld=n["liczba_dnia"]; lp_=n["liczba_postawy"]
    return f"""
    <div class="bignum">{lz}</div>
    <div class="bigtitle">{tytul}</div>
    <div class="note center">{opis}</div>
    <div class="calc">obliczenie: cyfry daty → suma {n['liczba_zycia_suma']} → {lz}</div>
    <div class="line"><span class="k">Liczba dnia</span><span class="v"><b>{ld}</b> — {LICZBA_OPIS[ld][0]}</span></div>
    <div class="line"><span class="k">Liczba postawy</span><span class="v"><b>{lp_}</b> — {LICZBA_OPIS[lp_][0]}</span></div>
    """

# ---------- sekcje (tytul, opis, funkcja) ----------
SEKCJE = [
    ("👤 Kim są", "Podstawowe dane urodzeniowe i „pogoda nieba” w dniu narodzin.", osoba_naglowek),
    ("🔑 Trójca podstawowa", "Najważniejsze trzy punkty. <b>Słońce</b> = kim jesteś w rdzeniu, "
        "<b>Księżyc</b> = co czujesz w środku, <b>Ascendent</b> = jak Cię widzą inni. "
        "Przykład: ktoś ze Słońcem w Wodniku „myśli inaczej”, a z Ascendentem w Wadze "
        "robi to z taktem i uśmiechem.", trojca),
    ("🪐 Wszystkie planety", "Każda planeta to inna „funkcja” osobowości (np. Wenus = miłość i gust, "
        "Mars = działanie). Znak mówi JAK działa, dom — GDZIE w życiu.", planety),
    ("✨ Punkty specjalne", "Mniej znane, ale ciekawe punkty mapy.", punkty),
    ("⚖️ Charakter w pigułce", "Rozkład żywiołów i „trybów działania”. Dużo Ognia = zapał; "
        "dużo Wody = emocje; przewaga jakości Zmiennej = elastyczność i łatwość adaptacji.", bilans),
    ("🔗 Najsilniejsze aspekty", "Jak planety „rozmawiają” ze sobą. Im mniejszy <i>orb</i> "
        "(odchylenie w stopniach), tym mocniejszy wpływ. Harmonijne (trygon, sekstyl) = łatwo; "
        "napięciowe (kwadratura, opozycja) = wyzwanie, które rozwija.", aspekty),
    ("🔢 Numerologia — Liczba Życia", "To <u>numerologia</u>, nie astrologia — liczona z samej daty "
        "urodzenia (sumujemy cyfry aż do jednej). Mówi o głównym motywie życia.", numer),
]

# ---------- render ----------
def kolumna(o):
    cells=[]
    for tytul,_,fn in SEKCJE:
        cells.append(f'<div class="cell">{fn(o)}</div>')
    return cells

cells_s = kolumna(S)
cells_p = kolumna(P)

rows_html=[]
for i,(tytul,opis,_) in enumerate(SEKCJE):
    rows_html.append(f"""
    <div class="band">
        <h3>{tytul}</h3>
        <p class="banddesc">{opis}</p>
    </div>
    <div class="pair">
        {cells_s[i]}
        {cells_p[i]}
    </div>""")

# --- podsumowanie astrologia vs numerologia (tekst staly, oparty na danych) ---
def syn(o):
    lz=o["numerologia"]["liczba_zycia"]
    return f"{o['imie']}: Słońce {pl(o['slonce']['znak'])}, Księżyc {pl(o['ksiezyc']['znak'])}, " \
           f"Ascendent {pl(o['ascendent']['znak'])} — Liczba Życia {lz} ({LICZBA_OPIS[lz][0]})"

podsumowanie = f"""
<div class="summary">
  <h3>🧭 Jak astrologia ma się do numerologii?</h3>
  <p>To dwa różne języki opisujące tę samą osobę. <b>Astrologia</b> patrzy na niebo w chwili
  narodzin (gdzie były planety), <b>numerologia</b> — tylko na liczby z daty. Co ciekawe,
  często mówią podobne rzeczy innymi słowami:</p>
  <div class="pair">
    <div class="cell">
      <p><b>{e(syn(S))}</b></p>
      <p>Numerologiczna <b>8</b> (ambicja, struktura, realizacja) brzmi jak astrologiczny
      <b>Saturn</b> i przewaga jakości <b>kardynalnej</b> w mapie Sebastiana — czyli „inicjator,
      który chce realnych efektów”. Liczba postawy <b>1</b> pasuje do Słońca w niezależnym
      <b>Wodniku</b>. Dwa języki, jeden wniosek: <i>samodzielny twórca nastawiony na cel.</i></p>
    </div>
    <div class="cell">
      <p><b>{e(syn(P))}</b></p>
      <p>Numerologiczna <b>7</b> (poszukiwacz, analiza, głębia) współgra z <b>Księżycem
      w Skorpionie</b> (intensywność, dociekliwość) i Słońcem w ciekawych świata
      <b>Bliźniętach</b>. Aż <b>5 planet zmiennych</b> = elastyczność, tak jak „7” lubi badać
      wiele tematów. Jeden wniosek: <i>wnikliwy umysł, który drąży i rozumie.</i></p>
    </div>
  </div>
  <p class="caveat">⚠️ Uczciwie: astrologia i numerologia to systemy <b>symboliczne</b>, nie nauka.
  Pozycje planet policzone są dokładnie (Swiss Ephemeris / kerykeion), ale znaczenia to
  tradycja kulturowa — traktuj to jako zabawę i lustro do autorefleksji.</p>
</div>

<div class="finale">
  <div class="finale-icon">🎯</div>
  <h3>Jedno ciekawe podsumowanie</h3>
  <p>Sebastian i Piotrek to <b>dwa uzupełniające się typy</b>: Sebastian (Liczba <b>8</b>, dużo
  Ognia, Ascendent Waga) to <b>„człowiek czynu z wdziękiem”</b> — zaczyna, działa, dąży do efektu.
  Piotrek (Liczba <b>7</b>, dużo planet zmiennych, Księżyc w Skorpionie) to
  <b>„człowiek wglądu”</b> — analizuje, drąży, rozumie głębiej.
  I tu mrugnięcie losu: obaj mają <b>Plutona w Skorpionie</b> (pokolenie transformacji)
  oraz <b>Księżyc w domu emocji i twórczości</b> — czyli pod spodem łączy ich ta sama,
  intensywna, twórcza wrażliwość. <b>Jeden działa, drugi rozumie — razem byliby kompletni.</b></p>
</div>
"""

HTML = f"""<!DOCTYPE html>
<html lang="pl"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sebastian vs Piotrek — astrologia i numerologia</title>
<style>
:root{{--bg:#0f1024;--card:#1a1b3a;--card2:#212255;--ink:#eef0ff;--mut:#a9adde;
--seb:#5aa9d6;--pio:#e08a5a;--line:#33356b;}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
background:radial-gradient(1200px 600px at 20% -10%,#23244f,transparent),
radial-gradient(1000px 500px at 100% 0,#2a1c44,transparent),var(--bg);
color:var(--ink);line-height:1.5;padding:0 0 60px}}
.top{{text-align:center;padding:40px 16px 10px}}
.top h1{{margin:0;font-size:30px;letter-spacing:.5px}}
.top p{{color:var(--mut);margin:8px 0 0}}
.legend{{display:flex;gap:22px;justify-content:center;margin:18px 0 6px;flex-wrap:wrap}}
.legend span{{display:flex;align-items:center;gap:8px;font-weight:600}}
.dot{{width:14px;height:14px;border-radius:50%}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 16px}}
.band{{margin:30px 0 6px;text-align:center}}
.band h3{{margin:0;font-size:22px}}
.banddesc{{color:var(--mut);max-width:760px;margin:6px auto 0;font-size:14.5px}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:stretch}}
.cell{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px}}
.pair>.cell:first-child{{border-top:4px solid var(--seb)}}
.pair>.cell:last-child{{border-top:4px solid var(--pio)}}
.who{{text-align:center}}
.who .emoji{{font-size:40px}}
.who h2{{margin:4px 0}}
.who .meta{{color:var(--mut);font-size:13.5px}}
.line{{display:flex;justify-content:space-between;gap:10px;padding:7px 0;border-bottom:1px dashed var(--line)}}
.line .k{{color:var(--mut)}}
.line .v{{text-align:right}}
.note{{color:var(--mut);font-size:12.5px;margin:2px 0 8px}}
.note.center{{text-align:center}}
.sub{{font-weight:700;margin:12px 0 6px;color:#cfd2ff}}
table{{width:100%;border-collapse:collapse;font-size:14px}}
th,td{{text-align:left;padding:6px 4px;border-bottom:1px solid var(--line)}}
th{{color:var(--mut);font-weight:600}}
.bar{{display:grid;grid-template-columns:90px 1fr 24px;align-items:center;gap:8px;margin:5px 0}}
.bl{{font-size:13px;color:var(--mut)}}
.bt{{height:12px;border-radius:7px;background:#2a2c63;position:relative}}
.bt::after{{content:"";position:absolute;left:0;top:0;bottom:0;width:var(--w);
background:var(--c);border-radius:7px}}
.bn{{text-align:right;font-weight:700}}
.asp{{list-style:none;padding:0;margin:0}}
.asp li{{padding:8px 0;border-bottom:1px dashed var(--line)}}
.orb{{float:right;color:var(--mut);font-size:12px}}
.bignum{{text-align:center;font-size:64px;font-weight:800;line-height:1;
background:linear-gradient(180deg,#fff,#9aa0ff);-webkit-background-clip:text;
background-clip:text;color:transparent}}
.bigtitle{{text-align:center;font-size:18px;font-weight:700;margin:2px 0}}
.calc{{text-align:center;font-size:12px;color:var(--mut);margin:6px 0 12px;
font-family:ui-monospace,Menlo,monospace}}
.summary,.finale{{margin-top:34px;background:var(--card2);border:1px solid var(--line);
border-radius:16px;padding:22px}}
.summary h3,.finale h3{{margin:0 0 8px;text-align:center;font-size:22px}}
.summary .pair{{margin-top:12px}}
.caveat{{margin-top:16px;color:var(--mut);font-size:13px;text-align:center;
border-top:1px solid var(--line);padding-top:12px}}
.finale{{text-align:center;background:linear-gradient(180deg,#241a44,#1a1b3a)}}
.finale-icon{{font-size:40px}}
.finale p{{max-width:820px;margin:8px auto 0}}
@media(max-width:680px){{.pair{{grid-template-columns:1fr}}}}
</style></head>
<body>
<div class="top">
  <h1>✨ Sebastian &nbsp;vs&nbsp; Piotrek ✨</h1>
  <p>Porównanie 1:1 — astrologia (z narzędzia <b>kerykeion</b>) + numerologia</p>
  <div class="legend">
    <span><span class="dot" style="background:var(--seb)"></span>Sebastian (lewa)</span>
    <span><span class="dot" style="background:var(--pio)"></span>Piotrek (prawa)</span>
  </div>
</div>
<div class="wrap">
{''.join(rows_html)}
{podsumowanie}
</div>
</body></html>"""

with open("index.html","w",encoding="utf-8") as f:
    f.write(HTML)
print("index.html zapisany,", len(HTML), "znakow")
