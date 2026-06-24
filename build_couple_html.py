# -*- coding: utf-8 -*-
"""Raport pary Sebastian + Julka.
Czesc 1: pelny portret kazdego (6 dzialow, narracja + dowody) - jak w raporcie Seb/Piotrek.
Czesc 2: relacja i dopasowanie (synastria + wskaznik z kerykeion).
Dane wylacznie z couple.json (kerykeion); interpretacja na pierwszym planie, dane jako dowod."""
import json, html

with open("couple.json", encoding="utf-8") as f:
    C = json.load(f)
S, J, SYN, SCORE = C["sebastian"], C["julka"], C["synastria"], C["score"]

PL={"Bliznieta":"Bliźnięta","Koziorozec":"Koziorożec","Slonce":"Słońce","Ksiezyc":"Księżyc",
    "Ogien":"Ogień","Stala":"Stała","poniedzialek":"poniedziałek","piatek":"piątek","sroda":"środa",
    "Ubywajacy garb":"Ubywający garb","Przybywajacy garb":"Przybywający garb",
    "Ubywajacy sierp":"Ubywający sierp","Przybywajacy sierp":"Przybywający sierp",
    "Plock":"Płock","Brzozow":"Brzozów"}
def pl(x): return PL.get(x, x)
def e(x): return html.escape(str(x))
def pt(p):
    if not p: return "—"
    dom=f" · dom {p['dom']}" if p.get("dom") else ""
    return f"{pl(p['znak'])} {p['stopnie']}°{dom}"
EMO={"Słońce":"☉","Księżyc":"☽","Merkury":"☿","Wenus":"♀","Mars":"♂","Jowisz":"♃",
     "Saturn":"♄","Uran":"♅","Neptun":"♆","Pluton":"♇","Ascendent":"⬆","MC":"⟂"}
ZNAK_OPIS={"Baran":"zapał, odwaga, inicjatywa","Byk":"stabilność, zmysłowość, upór",
 "Bliźnięta":"ciekawość, komunikacja, lekkość","Rak":"opiekuńczość, emocje, dom",
 "Lew":"duma, ekspresja, serce na dłoni","Panna":"porządek, analiza, troska o szczegóły",
 "Waga":"harmonia, takt, relacje, estetyka","Skorpion":"intensywność, głębia, pasja",
 "Strzelec":"optymizm, wolność, szukanie sensu","Koziorożec":"ambicja, dyscyplina, odpowiedzialność",
 "Wodnik":"oryginalność, niezależność, idee","Ryby":"wrażliwość, wyobraźnia, empatia"}

# ===================== CZESC 1: PORTRETY INDYWIDUALNE =====================
NARR = {
("S","rdzen"): """<p>W środku Sebastian jest <b>niezależnym oryginałem o miękkim sercu</b>.
Słońce w <b>Wodniku</b> (dom twórczości) to potrzeba bycia sobą i robienia rzeczy po swojemu,
a Księżyc i Ascendent w <b>Wadze</b> dokładają głód harmonii i dobrych relacji. Księżyc niemal
styka się z Ascendentem, więc <b>emocje ma „na wierzchu”</b> — od razu widać jego nastrój.</p>
<p>Przykład: potrafi mieć bardzo własne, nieszablonowe zdanie, ale przedstawi je tak miło, że
nikt nie poczuje się urażony.</p>""",
("J","rdzen"): """<p>Julka to <b>bystra, uważna perfekcjonistka z opiekuńczym sercem</b>. Słońce
i Ascendent w <b>Pannie</b> dają skromność, troskę o szczegóły i prawdziwą chęć pomagania —
zauważa rzeczy, które innym umykają. Ale jej Księżyc w <b>Raku</b> (w domu kariery!) zdradza, że
emocjonalnie najbardziej potrzebuje <b>bliskości, czułości i poczucia „domu”</b>, i że dom oraz
to, co robi w świecie, są u niej mocno splecione.</p>
<p>Przykład: jest tą osobą, która zorganizuje wszystkim wyjazd co do minuty, a przy okazji
spakuje komuś zapasowy sweter, „bo może zmarznąć”.</p>""",

("S","umysl"): """<p>Sebastian myśli <b>obrazami i przeczuciem</b> (Merkury w Rybach), a w
miłości jest <b>poważny i lojalny</b> (Wenus w Koziorożcu) — ceni trwałość. Jego znak firmowy to
idealnie zgrane Merkury–Wenus: <b>urok osobisty i dar słowa</b>, łączy inteligencję z wdziękiem.</p>""",
("J","umysl"): """<p>Julka myśli <b>sprawiedliwie i dyplomatycznie</b> — Merkury i Wenus w
<b>Wadze</b> sprawiają, że waży argumenty, dba o estetykę i nie znosi niesprawiedliwości.
W miłości szuka <b>partnerstwa i równowagi</b>: chce być w duecie, źle czuje się sama, potrzebuje
uzgadniania i bliskości. Merkury w domu 1 czyni ją <b>komunikatywną</b> — słowo to jej narzędzie.</p>""",

("S","dzialanie"): """<p>Sebastian działa <b>szybko i bez owijania</b> (Mars w Baranie); gdy
czegoś chce — rusza. Ma sporo zapału (Ogień) i wrażliwości (Woda). Haczyk: świetnie <b>zaczyna</b>
i łatwo się dostosowuje, ale gorzej z „energią trwania” — wyzwaniem jest dociąganie do końca.</p>""",
("J","dzialanie"): """<p>Julka działa <b>metodycznie i w służbie</b> — Mars w <b>Pannie</b>
(w domu przyjaciół i wspólnych celów) to pracowitość, dokładność i pomaganie innym, a nie
szarża. Ma bardzo mało „surowego ognia”, za to jest <b>elastyczna</b> (aż pięć planet zmiennych)
i ogromnie <b>„powietrzna” umysłowo</b> (sześć planet w Powietrzu) — żyje rozmową, ideami,
kontaktem. Pułapka: bywa zbyt samokrytyczna i niecierpliwa, gdy efekty przychodzą wolno.</p>""",

("S","aspekty"): """<p><b>Talent:</b> czar i słowo (Merkury–Wenus). <b>Wyzwanie:</b> wewnętrzne
„stabilność kontra wolność” (Jowisz–Uran). <b>As w rękawie:</b> szybkie, nieszablonowe działanie
(Mars–Uran) — błyska oryginalnym rozwiązaniem, gdy inni jeszcze myślą.</p>""",
("J","aspekty"): """<p><b>Mocna strona:</b> wrodzona dojrzałość i odpowiedzialność (Słońce w
harmonii z Saturnem) — na Julce można polegać. <b>Wrażliwość:</b> Słońce w zgodzie z Neptunem
dodaje wyobraźni i empatii. <b>Intensywność:</b> Jowisz naprzeciw Plutona daje silne przekonania
(„wszystko albo nic” w światopoglądzie). <b>Wyzwanie:</b> Mars w napięciu z Saturnem — bywa
hamulec i frustracja, ale też wytrwałość, gdy nauczy się cierpliwości.</p>""",

("S","glebia"): """<p><b>Życiowa lekcja</b> (Węzeł w Baranie): odważ się być sobą i stawiać
granice. <b>Czuły punkt</b> (Chiron w Bliźniętach): „czy to, co mówię, jest dość mądre?” — a
zarazem dar nauczania. <b>Pluton w domu 1:</b> magnetyczna obecność — wchodzi do pokoju i czuć
to.</p>""",
("J","glebia"): """<p><b>Życiowa lekcja</b> (Węzeł w Raku, w domu kariery): pozwolić sobie na
czułość i troskę — także na zewnątrz — zamiast chować się za chłodną analizą; budować emocjonalny
„dom”. <b>Czuły punkt</b> (Chiron w Strzelcu): wiara we własny głos i przekonania. <b>Pluton w
domu komunikacji</b> daje jej głębię i siłę w tym, co mówi i czego się uczy.</p>""",

("S","liczba"): """<p>Liczba Życia <b>8 — Realizator</b>: ambicja, siła, materialna realizacja,
„co dasz, to wraca”. Ósemkę ma <b>podwójnie</b> (też liczba dnia) — temat osiągnięć bardzo
spójny. Postawa „1” = samodzielny start.</p>""",
("J","liczba"): """<p>Liczba Życia <b>6 — Opiekun</b>: miłość, dom, harmonia i odpowiedzialność
za bliskich. To wręcz „liczba związku i rodziny” — naturalna troskliwość i potrzeba dbania o
innych. Co więcej, jej liczba dnia to <b>22 — liczba mistrzowska</b> (wielki potencjał budowania
czegoś trwałego), a postawa „4” pokazuje osobę solidną i uporządkowaną.</p>""",
}

def el(k,v): return f'<div class="el"><span>{k}</span><b>{v}</b></div>'
def ev_rdzen(o):
    return el("☉ Słońce",pt(o["slonce"]))+el("☽ Księżyc",pt(o["ksiezyc"]))+el("⬆ Ascendent",pt(o["ascendent"]))
def ev_umysl(o):
    out=el("☿ Merkury",pt(o["planety"]["Merkury"]))+el("♀ Wenus",pt(o["planety"]["Wenus"]))
    for a in o["aspekty"]:
        if {a["p1"],a["p2"]}=={"Merkury","Wenus"}:
            out+=el("Aspekt ☿–♀",f"{pl(a['aspekt'])} (orb {a['orb']}°)"); break
    return out
def ev_dzialanie(o):
    z=o["zywioly"]; j=o["jakosci"]
    return (el("♂ Mars",pt(o["planety"]["Mars"]))
        +el("Żywioły",f"Ogień {z['Ogien']} · Ziemia {z['Ziemia']} · Powietrze {z['Powietrze']} · Woda {z['Woda']}")
        +el("Jakości",f"Kard. {j['Kardynalna']} · Stała {j['Stala']} · Zmien. {j['Zmienna']}"))
def ev_aspekty(o):
    return "".join(el(f"{EMO.get(pl(a['p1']),'')}{pl(a['p1'])} – {pl(a['p2'])}",
                      f"{pl(a['aspekt'])} (orb {a['orb']}°)") for a in o["aspekty"][:4])
def ev_glebia(o):
    return (el("Węzeł Północny",pt(o["wezel_polnocny"]))+el("Chiron",pt(o["chiron"]))
            +el("♇ Pluton",pt(o["planety"]["Pluton"])))
def ev_liczba(o):
    n=o["numerologia"]
    return (f'<div class="bignum">{n["liczba_zycia"]}</div>'
        +f'<div class="calc">cyfry daty → suma {n["liczba_zycia_suma"]} → {n["liczba_zycia"]}</div>'
        +el("Liczba dnia",n["liczba_dnia"])+el("Liczba postawy",n["liczba_postawy"]))

TEMATY=[("rdzen","🔑 Kim jest w środku",
   "Rdzeń osobowości: <b>Słońce</b> (kim jest), <b>Księżyc</b> (co czuje), <b>Ascendent</b> (jak ją/go widać).",ev_rdzen),
 ("umysl","💬 Jak myśli i kocha","Sposób myślenia (Merkury) oraz to, co i jak kocha (Wenus).",ev_umysl),
 ("dzialanie","⚡ Jak działa","Energia i styl działania (Mars) plus temperament — żywioły i tryby.",ev_dzialanie),
 ("aspekty","🔗 Talenty i wyzwania","Najsilniejsze „rozmowy” planet. Mniejszy orb = mocniejszy wpływ.",ev_aspekty),
 ("glebia","🌑 Głębia i droga życia","Życiowa lekcja (Węzeł), czuły punkt (Chiron), siła przemiany (Pluton).",ev_glebia),
 ("liczba","🔢 Liczba Życia (numerologia)","Liczona z samej daty urodzenia — główny motyw życia.",ev_liczba)]

def cell(kod,o,ev_fn,key):
    return f"""<div class="cell">
      <div class="narr">{NARR[(kod,key)]}</div>
      <details class="ev"><summary>📊 Na czym to oparte (dane z kerykeion)</summary>
        <div class="evbox">{ev_fn(o)}</div></details>
    </div>"""

portrety=[]
for key,tytul,opis,ev_fn in TEMATY:
    portrety.append(f"""
    <div class="band"><h3>{tytul}</h3><p class="banddesc">{opis}</p></div>
    <div class="pair">{cell("S",S,ev_fn,key)}{cell("J",J,ev_fn,key)}</div>""")

# ===================== CZESC 2: RELACJA =====================
def syn_find(seb_pl,jul_pl):
    return [a for a in SYN if a["seb"]==seb_pl and a["jul"]==jul_pl]
def syn_el(a):
    return el(f"{EMO.get(pl(a['seb']),'')} {pl(a['seb'])} (S) – {pl(a['jul'])} (J) {EMO.get(pl(a['jul']),'')}",
              f"{pl(a['aspekt'])} · orb {a['orb']}°")
def rel_block(icon,tytul,opis,narr,pairs):
    rows=[syn_el(a) for pr in pairs for a in syn_find(*pr)]
    dowody=(f"""<details class="ev"><summary>📊 Aspekty synastryczne, na których to oparte
            (S = Sebastian, J = Julka)</summary><div class="evbox">{''.join(rows)}</div></details>"""
            if rows else "")
    return f"""<div class="relsec"><h3>{icon} {tytul}</h3><p class="reldesc">{opis}</p>
      <div class="relnarr">{narr}</div>{dowody}</div>"""

CHEMIA=rel_block("💘","Chemia i przyciąganie",
 "Czy iskrzy? Klasyczne aspekty pożądania i czułości między Waszymi mapami.",
 """<p><b>Tak, iskrzy — mocno.</b> Najsilniejszy aspekt całej synastrii to <b>Wenus Sebastiana
 naprzeciw Księżyca Julki</b> (orb 0,17°!): sposób, w jaki Sebastian okazuje uczucia, trafia
 dokładnie w to, czego emocjonalnie potrzebuje Julka. Do tego <b>Mars Seba ↔ Wenus Julki</b> —
 fizyczna chemia (ten punkt liczy się do wskaźnika relacji), a Słońce Seba w zgodzie z jej
 Wenus sprawia, że po prostu mu się podoba. Opozycje działają tu jak magnesy.</p>""",
 [("Wenus","Ksiezyc"),("Mars","Wenus"),("Slonce","Wenus")])
POROZUMIENIE=rel_block("🗣️","Porozumienie i rozmowa",
 "Czy się dogadujecie? Kontakt umysłu z emocjami i wspólny język na co dzień.",
 """<p><b>Rozmowa to Wasz atut.</b> <b>Merkury Seba w harmonii z Księżycem Julki</b> (orb 0,24°)
 znaczy, że potrafi nazwać i zrozumieć to, co ona czuje — Julka czuje się słuchana. Saturn Seba
 wnosi jej myśleniu stabilność. Jej sześć planet w Powietrzu plus jego wagowa potrzeba harmonii
 = para, która <b>dużo rozmawia i szuka porozumienia</b>.</p>""",
 [("Merkury","Ksiezyc"),("Saturn","Merkury")])
TARCIA=rel_block("⚔️","Tarcia i wyzwania",
 "Gdzie będzie zgrzytać? Uczciwie nazywamy pola pracy.",
 """<p><b>Główne wyzwanie: różne rytmy emocjonalne.</b> <b>Księżyc Seba w kwadraturze do Księżyca
 Julki</b> (0,7°): co innego daje Wam poczucie bezpieczeństwa (jemu harmonia–Waga, jej bliskość
 i „dom”–Rak). Wzmacnia to <b>Ascendent Seba w kwadraturze do jej Księżyca</b>. Drugie pole:
 <b>Słońce Seba w kwadraturze do Saturna Julki</b> — bywa, że on czuje się oceniany, a ona wnosi
 wymagania. I temperament: Julka „powietrzna” (analizuje), Sebastian „wodno-ognisty” (czuje
 gorąco) — klasyczne <b>logika kontra emocje</b>. To do pracy, nie wyroki.</p>""",
 [("Ksiezyc","Ksiezyc"),("Ascendent","Ksiezyc"),("Slonce","Saturn")])
KIERUNEK=rel_block("🏡","Wspólny kierunek i przyszłość",
 "Czy idziecie w tę samą stronę? Wsparcie celów i budowanie wspólnego życia.",
 """<p><b>Dobry fundament „idziemy razem”.</b> <b>Słońce Seba w harmonii z MC Julki</b> (1,0°)
 i jego <b>Mars wspierający jej MC</b>: Sebastian naturalnie kibicuje ambicjom Julki i dodaje
 energii. Numerologicznie też: jego <b>8 (buduje, zapewnia)</b> i jej <b>6 (miłość i dom)</b> =
 <b>on buduje, ona tworzy ciepło</b>.</p>""",
 [("Slonce","MC"),("Mars","MC")])

cn=S["numerologia"]["liczba_zycia"]+J["numerologia"]["liczba_zycia"]
while cn>9 and cn not in (11,22,33): cn=sum(int(d) for d in str(cn))
CN_NAZ={1:'Lider',2:'Dyplomata',3:'Artysta',4:'Budowniczy',5:'Podróżnik',6:'Opiekun',
        7:'Poszukiwacz',8:'Realizator',9:'Humanista',11:'Wizjoner',22:'Mistrz Budowniczy',33:'Mistrz Nauczyciel'}

val=SCORE["wartosc"]; pct=min(100,round(val/30*100)); poziom=SCORE["opis"]
POZIOM_PL={"Minimal":"Minimalna","Medium":"Średnia","Important":"Znacząca",
 "Very Important":"Bardzo znacząca","Exceptional":"Wyjątkowa","Rare Exceptional":"Rzadka wyjątkowa"}

HTML=f"""<!DOCTYPE html><html lang="pl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sebastian & Julka — portrety i relacja</title>
<style>
:root{{--bg:#160f1f;--card:#241730;--card2:#2c1d3b;--ink:#f6eefc;--mut:#c6abdd;
--seb:#5aa9d6;--jul:#e86fa6;--line:#43335a;--good:#5fd08a;--warn:#e7a14e;}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
background:radial-gradient(1200px 600px at 15% -10%,#3a2150,transparent),
radial-gradient(1000px 500px at 100% 0,#3a1d35,transparent),var(--bg);
color:var(--ink);line-height:1.6;padding:0 0 60px}}
.top{{text-align:center;padding:46px 16px 4px}}
.top h1{{margin:0;font-size:32px}} .top .sub{{color:var(--mut);max-width:660px;margin:10px auto 0}}
.legend{{display:flex;gap:22px;justify-content:center;margin:16px 0 0;flex-wrap:wrap}}
.legend span{{display:flex;align-items:center;gap:8px;font-weight:600}}
.dot{{width:14px;height:14px;border-radius:50%}}
.wrap{{max-width:1060px;margin:0 auto;padding:0 16px}}
.who{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:22px 0 0}}
.who .card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px;text-align:center}}
.who .card:first-child{{border-top:4px solid var(--seb)}}
.who .card:last-child{{border-top:4px solid var(--jul)}}
.who .emoji{{font-size:34px}} .who h2{{margin:4px 0}} .who .meta{{color:var(--mut);font-size:13px}}
.sectitle{{text-align:center;margin:36px 0 0;font-size:26px}}
.sectitle .s{{color:var(--mut);font-size:14px;font-weight:400;display:block;margin-top:4px}}
.band{{margin:28px 0 8px;text-align:center}}
.band h3{{margin:0;font-size:22px}}
.banddesc{{color:var(--mut);max-width:780px;margin:6px auto 0;font-size:14px}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:stretch}}
.cell{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px}}
.pair>.cell:first-child{{border-top:4px solid var(--seb)}}
.pair>.cell:last-child{{border-top:4px solid var(--jul)}}
.narr{{font-size:15px}} .narr p{{margin:0 0 11px}} .narr p:last-child{{margin:0}}
.ev{{margin-top:14px;border-top:1px dashed var(--line);padding-top:8px}}
.ev summary{{cursor:pointer;color:var(--mut);font-size:12.5px;list-style:none}}
.ev summary::-webkit-details-marker{{display:none}}
.ev summary::before{{content:"▸ "}} .ev[open] summary::before{{content:"▾ "}}
.evbox{{margin-top:8px;background:#1a1029;border-radius:10px;padding:6px 10px}}
.el{{display:flex;justify-content:space-between;gap:10px;font-size:12.5px;color:var(--mut);
padding:4px 0;border-bottom:1px solid #2a1c3b}}
.el:last-child{{border-bottom:none}} .el b{{color:#e7d6f5;text-align:right}}
.bignum{{text-align:center;font-size:44px;font-weight:800;color:#fff;line-height:1;margin:2px 0}}
.calc{{text-align:center;font-size:11px;color:var(--mut);font-family:ui-monospace,Menlo,monospace;margin-bottom:6px}}
.gauge{{background:var(--card2);border:1px solid var(--line);border-radius:16px;padding:22px;margin:18px 0;text-align:center}}
.gauge h3{{margin:0 0 4px;font-size:22px}} .gnum{{font-size:46px;font-weight:800;color:#fff;line-height:1.1}}
.glabel{{color:var(--mut);margin-bottom:14px}}
.gbar{{height:16px;border-radius:10px;background:#1c1228;position:relative;overflow:hidden;border:1px solid var(--line)}}
.gbar::after{{content:"";position:absolute;left:0;top:0;bottom:0;width:{pct}%;background:linear-gradient(90deg,var(--warn),var(--jul));border-radius:10px}}
.gscale{{display:flex;justify-content:space-between;color:var(--mut);font-size:11px;margin-top:6px}}
.relsec{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px;margin:16px 0;border-left:4px solid var(--jul)}}
.relsec h3{{margin:0 0 4px;font-size:22px}} .reldesc{{color:var(--mut);font-size:14px;margin:0 0 12px}}
.relnarr{{font-size:15px}} .relnarr p{{margin:0 0 12px}} .relnarr p:last-child{{margin:0}}
.num{{display:grid;grid-template-columns:1fr auto 1fr;gap:14px;align-items:center;background:var(--card2);border:1px solid var(--line);border-radius:16px;padding:20px;margin:16px 0}}
.num .p{{text-align:center}} .num .big{{font-size:40px;font-weight:800;color:#fff}} .num .eq{{font-size:24px;color:var(--mut)}}
.verdict{{background:linear-gradient(180deg,#33204a,#241730);border:1px solid var(--line);border-radius:18px;padding:26px;margin-top:22px;text-align:center}}
.verdict h3{{margin:0 0 8px;font-size:24px}} .verdict p{{max-width:840px;margin:8px auto 0;font-size:16px}}
.tags{{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin:14px 0}}
.tag{{padding:6px 12px;border-radius:20px;font-size:13px;font-weight:600}}
.tag.g{{background:rgba(95,208,138,.16);color:var(--good);border:1px solid var(--good)}}
.tag.w{{background:rgba(231,161,78,.16);color:var(--warn);border:1px solid var(--warn)}}
.caveat{{color:var(--mut);font-size:13px;border-top:1px solid var(--line);padding-top:12px;margin-top:18px}}
@media(max-width:680px){{.pair,.who,.num{{grid-template-columns:1fr}}.num .eq{{display:none}}}}
</style></head><body>
<div class="top">
  <h1>💞 Sebastian &amp; Julka</h1>
  <p class="sub">Najpierw <b>pełny portret każdego z Was</b>, potem <b>analiza relacji</b>
  (synastria) — wszystko z narzędzia <b>kerykeion</b>. Opowieść na pierwszym planie, dane pod „📊”.</p>
  <div class="legend">
    <span><span class="dot" style="background:var(--seb)"></span>Sebastian (lewa)</span>
    <span><span class="dot" style="background:var(--jul)"></span>Julka (prawa)</span>
  </div>
</div>
<div class="wrap">
  <div class="who">
    <div class="card"><div class="emoji">🧔</div><h2>Sebastian</h2>
      <div class="meta">{e(S['data'])} · {e(S['godzina'])} · {e(pl(S['miasto']))}<br>
      {e(S['dzien_tygodnia'])} · mapa {e(S['mapa'])} · {S['faza_emoji']} {e(pl(S['faza_ksiezyca']))}</div></div>
    <div class="card"><div class="emoji">👩</div><h2>Julka</h2>
      <div class="meta">{e(J['data'])} · {e(J['godzina'])} · {e(pl(J['miasto']))}<br>
      {e(J['dzien_tygodnia'])} · mapa {e(J['mapa'])} · {J['faza_emoji']} {e(pl(J['faza_ksiezyca']))}</div></div>
  </div>

  <h2 class="sectitle">👤 Portrety indywidualne<span class="s">kim jesteście — każde z osobna</span></h2>
  {''.join(portrety)}

  <h2 class="sectitle">💞 Wasza relacja<span class="s">co was łączy, a nad czym warto pracować</span></h2>
  <div class="gauge">
    <h3>🔥 Wskaźnik dopasowania</h3>
    <div class="gnum">{val} pkt</div>
    <div class="glabel">poziom: <b>{POZIOM_PL.get(poziom,poziom)}</b> ({e(poziom)})</div>
    <div class="gbar"></div>
    <div class="gscale"><span>0</span><span>Średnia</span><span>Znacząca</span><span>Wyjątkowa</span><span>30+</span></div>
    <p class="reldesc" style="margin-top:12px">Wskaźnik kerykeiona (metoda Ciro Discepolo): punkty
    zdobyły <b>Mars–Wenus</b> (pożądanie, +4) i <b>Księżyc–Ascendent</b> (więź emocjonalna, +4).
    „Średnia” to solidny, realny wynik — większość udanych par jest właśnie tu.</p>
  </div>
  {CHEMIA}{POROZUMIENIE}{TARCIA}{KIERUNEK}

  <h2 class="sectitle">🔢 Numerologia pary</h2>
  <div class="num">
    <div class="p"><div class="big">{S['numerologia']['liczba_zycia']}</div>
      <div class="reldesc">Sebastian — Realizator<br>(buduje, zapewnia)</div></div>
    <div class="eq">+&nbsp;→</div>
    <div class="p"><div class="big">{J['numerologia']['liczba_zycia']}</div>
      <div class="reldesc">Julka — Opiekun<br>(miłość, dom, harmonia)</div></div>
  </div>
  <div class="relsec" style="border-left-color:var(--good)">
    <p class="relnarr"><b>Wspólna liczba pary: {cn} — {CN_NAZ[cn]}.</b> Sumując Wasze Liczby Życia
    ({S['numerologia']['liczba_zycia']} + {J['numerologia']['liczba_zycia']} → {cn}) wychodzi
    energia <b>ruchu, wolności i przygody</b> — jako para najlepiej czujecie się, gdy się
    rozwijacie i nie popadacie w rutynę. Spina to jego potrzebę wolności (Wodnik) z jej lotnością
    (sześć planet w Powietrzu).</p>
  </div>

  <div class="verdict">
    <div style="font-size:42px">💍</div>
    <h3>Czy pasujecie do siebie?</h3>
    <div class="tags">
      <span class="tag g">💘 Silna chemia</span><span class="tag g">🗣️ Świetne porozumienie</span>
      <span class="tag g">🏡 Wsparcie celów</span><span class="tag w">🌗 Różne rytmy emocji</span>
      <span class="tag w">🧠 Logika vs uczucia</span>
    </div>
    <p><b>Tak — i to z prawdziwą iskrą.</b> Macie niemal idealne aspekty przyciągania
    (Wenus–Księżyc 0,17°) i rozumienia (Merkury–Księżyc 0,24°), a Sebastian naturalnie wspiera
    ambicje Julki. Mocna baza: <b>pożądanie + rozmowa + wspólny kierunek</b>.</p>
    <p>Praca na lata to <b>uszanowanie różnych sposobów czucia</b>: jej Księżyc w Raku chce
    bliskości i „domu”, jego w Wadze — harmonii i przestrzeni; ona myśli (Powietrze), on czuje
    (Woda/Ogień). Gdy nauczycie się tłumaczyć sobie te dwa języki, napięcie zamieni się w to, co
    Was uzupełnia. <b>Werdykt: dopasowanie solidne (Średnie, 8 pkt) z bardzo dobrym potencjałem
    na trwały, ciepły związek.</b></p>
    <p class="caveat">⚖️ Uczciwie: synastria i numerologia to systemy <b>symboliczne</b>, nie
    nauka. Liczby i aspekty policzone są dokładnie (kerykeion / Swiss Ephemeris), ale ich
    znaczenia to tradycja. O związku decydujecie Wy — potraktujcie to jako ciepłe lustro do
    rozmowy we dwoje. 💛</p>
  </div>
</div>
</body></html>"""

with open("index.html","w",encoding="utf-8") as f:
    f.write(HTML)
print("index.html (para, pelny) zapisany,", len(HTML), "znakow | couple number:", cn)
