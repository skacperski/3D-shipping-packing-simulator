# -*- coding: utf-8 -*-
"""Buduje index.html: raport DLA odbiorcow (Sebastian vs Piotrek).
Interpretacja na pierwszym planie; dane z kerykeion jako DOWODY (drugi priorytet)."""
import json, html

with open("data.json", encoding="utf-8") as f:
    D = json.load(f)
S, P = D["sebastian"], D["piotrek"]

PL = {"Bliznieta":"Bliźnięta","Koziorozec":"Koziorożec","Slonce":"Słońce",
      "Ksiezyc":"Księżyc","Ogien":"Ogień","Stala":"Stała","poniedzialek":"poniedziałek",
      "Ubywajacy garb":"Ubywający garb","Przybywajacy garb":"Przybywający garb",
      "Plock":"Płock","Bialystok":"Białystok"}
def pl(x): return PL.get(x, x)
def e(x): return html.escape(str(x))
def pt(p):
    if not p: return "—"
    dom=f" · dom {p['dom']}" if p.get("dom") else ""
    return f"{pl(p['znak'])} {p['stopnie']}°{dom}"

EMOJI={"Słońce":"☉","Księżyc":"☽","Merkury":"☿","Wenus":"♀","Mars":"♂",
       "Jowisz":"♃","Saturn":"♄","Uran":"♅","Neptun":"♆","Pluton":"♇"}

# ====== NARRACJE (interpretacja — pierwszy priorytet) ======
# Klucz: (osoba, temat) -> HTML akapitow
NARR = {
("S","rdzen"): """<p>W środku jesteś <b>niezależnym oryginałem o miękkim sercu</b>. Twoje
Słońce w <b>Wodniku</b> sprawia, że nie znosisz sztywnych schematów — myślisz po swojemu,
ciągnie Cię to, co nowe i nietuzinkowe. Ale Twój Księżyc i Ascendent w <b>Wadze</b> dodają
zupełnie inną nutę: emocjonalnie potrzebujesz <b>harmonii, ładnych relacji i spokoju</b>,
a na zewnątrz jesteś taktowny i dyplomatyczny.</p>
<p>Co ważne — Twój Księżyc niemal styka się z Ascendentem. To znaczy, że <b>emocje masz „na
wierzchu”</b>: ludzie od razu wyczuwają Twój nastrój i odbierają Cię jako osobę ciepłą,
ugodową, wrażliwą. Przykład z życia: potrafisz mieć bardzo własne, nieszablonowe zdanie,
ale przedstawisz je tak miło, że nikt się nie poczuje urażony.</p>""",
("P","rdzen"): """<p>Jesteś <b>towarzyskim umysłem z głęboką duszą</b>. Twoje Słońce w
<b>Bliźniętach</b> to ciekawość świata, lekkość i dar rozmowy — ożywasz wśród ludzi i w wymianie
myśli (Słońce w domu 11: przyjaciele, grupy, wspólne idee). Ale uwaga, bo pod tą lekką
powierzchnią kryje się Księżyc w <b>Skorpionie</b>: emocjonalnie jesteś <b>intensywny, czujny
i głęboki</b>, czujesz mocno, choć nie każdemu to pokazujesz.</p>
<p>Twój Ascendent w <b>Raku</b> sprawia, że na zewnątrz jesteś ciepły i opiekuńczy — ludzie
czują się przy Tobie zaopiekowani. Przykład: na imprezie jesteś tym, który lekko gawędzi z
każdym, ale jednocześnie jako jedyny naprawdę zauważy, że komuś jest smutno.</p>""",

("S","umysl"): """<p>Myślisz <b>obrazami i przeczuciem</b>, nie suchą logiką — Twój Merkury jest
w <b>Rybach</b>, więc raczej „wyczuwasz”, niż wyliczasz. W miłości natomiast jesteś
<b>poważny i lojalny</b> (Wenus w <b>Koziorożcu</b>): cenisz trwałość, nie fajerwerki.</p>
<p>I tu Twój największy dar: Merkury i Wenus są ze sobą idealnie zgrane (to najdokładniejszy
aspekt w całej Twojej mapie!). W praktyce oznacza to <b>urok osobisty i dar słowa</b> —
potrafisz mówić tak, że ludzie chcą Cię słuchać, łączysz inteligencję z wdziękiem.</p>""",
("P","umysl"): """<p>Twój umysł jest <b>szybki jak błyskawica</b> — Merkury i Wenus razem w
<b>Bliźniętach</b> dają lotność, ciętą ripostę i potrzebę ciągłej wymiany słów. Schowane w
domu 12 dodają jednak refleksyjności: dużo dzieje się też „za kulisami”, w środku.</p>
<p>W uczuciach bywa jednak <b>huśtawka</b>: Twoja Wenus jest w napięciu z Uranem i Saturnem.
To klasyczne „przyciąganie–odpychanie” — z jednej strony pragniesz <b>wolności i przestrzeni</b>,
z drugiej <b>bezpieczeństwa i stałości</b>. Przykład: potrafisz zakochać się w kimś od pierwszej
rozmowy, a zaraz potem przestraszyć się zobowiązania.</p>""",

("S","dzialanie"): """<p>Działasz <b>szybko i bez owijania w bawełnę</b> — Twój Mars jest w
<b>Baranie</b>, czyli w swojej najbardziej energicznej pozycji. Gdy czegoś chcesz, ruszasz od
razu (Twoja wola i energia grają zgodnie). Masz w sobie sporo <b>zapału (Ogień) i wrażliwości
(Woda)</b> w dobrej równowadze.</p>
<p>Jeden haczyk: świetnie <b>zaczynasz</b>, łatwo się dostosowujesz, ale brakuje Ci „energii
trwania”. Przykład: rozpalasz dziesięć pomysłów naraz — wyzwaniem jest dociągnięcie ich do
końca, nie wymyślenie nowego.</p>""",
("P","dzialanie"): """<p>Ty działasz <b>finezją, nie taranem</b>. Twój Mars w <b>Rybach</b> to
cichy nurt — osiągasz swoje raczej przez wyobraźnię, wytrwałość i wyczucie niż przez napór.
Masz wyjątkowo mało „surowego ognia”, za to jesteś <b>mistrzem adaptacji</b> (aż pięć planet w
znakach zmiennych!).</p>
<p>To Twoja supermoc i Twoja pułapka naraz: <b>wszechstronność</b> (ogarniasz wiele tematów,
łatwo się przestawiasz), ale i ryzyko <b>rozproszenia</b>. Przykład: potrafisz prowadzić trzy
rozmowy i dwa projekty naraz — pod warunkiem, że nie zgubisz, który był najważniejszy.</p>""",

("S","aspekty"): """<p><b>Twój talent:</b> czar i słowo (Merkury–Wenus) — to Twoja wizytówka.
<b>Twoje wyzwanie:</b> wewnętrzny niepokój „stabilność kontra wolność” (Jowisz w napięciu z
Uranem) — część Ciebie chce spokojnie rosnąć, część chce wszystko wywrócić. <b>Twój as w
rękawie:</b> szybkie, nieszablonowe działanie (Mars zgrany z Uranem) — błyskasz oryginalnym
rozwiązaniem, gdy inni jeszcze myślą.</p>""",
("P","aspekty"): """<p><b>Twoje główne napięcie:</b> miłość rozpięta między wolnością a
bezpieczeństwem (Wenus w opozycji do Urana i Saturna) — stąd ta huśtawka w relacjach.
<b>Twój wewnętrzny paradoks:</b> w jednej osobie spotykają się „zasady” i „bunt” (Saturn zlany
z Uranem) — bywasz i odpowiedzialny, i niespokojny zarazem. <b>Twój głębszy dar:</b> wyobraźnia
połączona z przenikliwością (Neptun–Pluton) — wyczuwasz to, co ukryte pod powierzchnią.</p>""",

("S","glebia"): """<p>Twoja <b>życiowa lekcja</b> (Węzeł Północny w Baranie) to: <b>odważ się
być sobą</b> — stawiać granice, mówić „ja chcę”, nie rozpływać się w cudzych potrzebach. Twój
czuły punkt (Chiron w Bliźniętach) dotyka pytania „czy to, co mówię, jest dość mądre?” — a
jednocześnie kryje dar <b>nauczania i tłumaczenia</b>. Pluton w domu 1 daje Ci
<b>magnetyczną obecność</b>: wchodzisz do pokoju i ludzie to czują.</p>""",
("P","glebia"): """<p>Twoja <b>życiowa lekcja</b> (Węzeł Północny w Rybach, dom kariery) to:
<b>zaufaj intuicji</b> i odpuść kontrolę w drodze do celu. Twój czuły punkt (Chiron w
Bliźniętach, w domu „kulis”) dotyka wyrażania siebie — leczysz go, gdy pozwalasz sobie mówić
prawdę. Pluton w domu twórczości i miłości daje Ci <b>ogromną intensywność w tym, co tworzysz
i kogo kochasz</b> — na pół gwizdka po prostu nie umiesz.</p>""",

("S","liczba"): """<p>Twoja Liczba Życia to <b>8 — Realizator</b>. To energia <b>ambicji,
siły i materialnej realizacji</b>: chcesz osiągać realne efekty, masz smykałkę do zarządzania
i brania odpowiedzialności. Symbol ósemki (∞) to też zasada „co dasz, to wraca”.</p>
<p>Co ciekawe, ósemkę masz <b>podwójnie</b> (również jako liczbę dnia) — temat siły i osiągnięć
jest u Ciebie wyjątkowo spójny. A Twoja postawa „1” to <b>samodzielny start</b>: wolisz robić
po swojemu.</p>""",
("P","liczba"): """<p>Twoja Liczba Życia to <b>7 — Poszukiwacz</b>. To energia <b>analizy,
głębi i potrzeby zrozumienia świata</b>: nie wystarcza Ci, że coś działa — chcesz wiedzieć
<i>dlaczego</i>. Lubisz drążyć, badać, dochodzić do sedna.</p>
<p>Ale masz też lekkość: Twoja liczba dnia „3” to <b>ekspresja i komunikacja</b> — umiesz o
trudnych rzeczach opowiadać przystępnie. A postawa „8” sprawia, że na zewnątrz wyglądasz na
konkretnego i nastawionego na cel, choć w środku jesteś dociekliwym myślicielem.</p>""",
}

# ====== DOWODY (dane z kerykeion — drugi priorytet) ======
def ev_line(k, v): return f'<div class="el"><span>{k}</span><b>{v}</b></div>'

def ev_rdzen(o):
    out = ev_line("☉ Słońce", pt(o["slonce"])) + ev_line("☽ Księżyc", pt(o["ksiezyc"]))
    out += ev_line("⬆ Ascendent", pt(o["ascendent"]))
    return out

def ev_umysl(o):
    out = ev_line("☿ Merkury", pt(o["planety"]["Merkury"])) + ev_line("♀ Wenus", pt(o["planety"]["Wenus"]))
    for a in o["aspekty"]:
        if {a["p1"],a["p2"]}=={"Merkury","Wenus"}:
            out += ev_line("Aspekt ☿–♀", f"{pl(a['aspekt'])} (orb {a['orb']}°)"); break
    return out

def ev_dzialanie(o):
    out = ev_line("♂ Mars", pt(o["planety"]["Mars"]))
    z=o["zywioly"]; out += ev_line("Żywioły", f"Ogień {z['Ogien']} · Ziemia {z['Ziemia']} · Powietrze {z['Powietrze']} · Woda {z['Woda']}")
    j=o["jakosci"]; out += ev_line("Jakości", f"Kard. {j['Kardynalna']} · Stała {j['Stala']} · Zmien. {j['Zmienna']}")
    return out

def ev_aspekty(o):
    out=""
    for a in o["aspekty"][:4]:
        out += ev_line(f"{EMOJI.get(pl(a['p1']),'')}{pl(a['p1'])} – {pl(a['p2'])}",
                       f"{pl(a['aspekt'])} (orb {a['orb']}°)")
    return out

def ev_glebia(o):
    return (ev_line("Węzeł Północny", pt(o["wezel_polnocny"]))
            + ev_line("Chiron", pt(o["chiron"]))
            + ev_line("♇ Pluton", pt(o["planety"]["Pluton"])))

def ev_liczba(o):
    n=o["numerologia"]
    return (f'<div class="bignum">{n["liczba_zycia"]}</div>'
            + f'<div class="calc">cyfry daty → suma {n["liczba_zycia_suma"]} → {n["liczba_zycia"]}</div>'
            + ev_line("Liczba dnia", n["liczba_dnia"])
            + ev_line("Liczba postawy", n["liczba_postawy"]))

# ====== SEKCJE ======
TEMATY = [
 ("rdzen","🔑 Kim jesteś w środku",
   "Rdzeń osobowości: <b>Słońce</b> (kim jesteś), <b>Księżyc</b> (co czujesz) i "
   "<b>Ascendent</b> (jak Cię widzą).", ev_rdzen),
 ("umysl","💬 Jak myślisz i kochasz",
   "Twój sposób myślenia (Merkury) i to, co i jak kochasz (Wenus).", ev_umysl),
 ("dzialanie","⚡ Jak działasz",
   "Twoja energia i styl działania (Mars) oraz „temperament” — żywioły i tryby działania.", ev_dzialanie),
 ("aspekty","🔗 Talenty i wyzwania",
   "Najsilniejsze „rozmowy” planet. Harmonijne = łatwy talent; napięciowe = wyzwanie, "
   "które rozwija. Im mniejszy orb, tym mocniej.", ev_aspekty),
 ("glebia","🌑 Głębia i droga życia",
   "Najgłębsze warstwy: życiowa lekcja (Węzeł), czuły punkt (Chiron) i siła przemiany (Pluton).", ev_glebia),
 ("liczba","🔢 Twoja Liczba Życia (numerologia)",
   "To <u>numerologia</u> — liczona z samej daty urodzenia. Mówi o głównym motywie życia.", ev_liczba),
]

def cell(osoba_kod, o, ev_fn):
    return f"""<div class="cell">
      <div class="narr">{NARR[(osoba_kod, TEMAT_KEY)]}</div>
      <details class="ev"><summary>📊 Na czym to oparte (dane z kerykeion)</summary>
        <div class="evbox">{ev_fn(o)}</div>
      </details>
    </div>"""

rows=[]
for key,tytul,opis,ev_fn in TEMATY:
    TEMAT_KEY=key
    rows.append(f"""
    <div class="band"><h3>{tytul}</h3><p class="banddesc">{opis}</p></div>
    <div class="pair">{cell("S",S,ev_fn)}{cell("P",P,ev_fn)}</div>""")

# ====== PODSUMOWANIE + FINAL ======
podsum = """
<div class="summary">
  <h3>🧭 Co mówi astrologia, a co numerologia?</h3>
  <p>To dwa różne języki opowiadające o tej samej osobie — i często mówią to samo innymi słowami.
  Poniżej widać, jak <b>liczby potwierdzają obraz z gwiazd</b>:</p>
  <div class="pair">
    <div class="cell"><h4 class="cn seb">Sebastian</h4>
      <p>Astrologia mówi: <i>niezależny twórca nastawiony na cel</i> (Słońce Wodnik, mnóstwo
      inicjatywy). Numerologia dorzuca <b>8 — Realizatora</b> (ambicja, konkret) i postawę <b>1</b>
      (samodzielność). <b>Oba języki, jeden wniosek:</b> człowiek, który sam zaczyna i chce
      realnych efektów.</p></div>
    <div class="cell"><h4 class="cn pio">Piotrek</h4>
      <p>Astrologia mówi: <i>wnikliwy umysł, który drąży i czuje głęboko</i> (Bliźnięta + Księżyc
      Skorpion, pięć planet zmiennych). Numerologia dorzuca <b>7 — Poszukiwacza</b> (analiza,
      głębia). <b>Oba języki, jeden wniosek:</b> człowiek, który chce wszystko zrozumieć do
      sedna.</p></div>
  </div>
  <p class="caveat">⚖️ Uczciwie: astrologia i numerologia to systemy <b>symboliczne</b>, nie nauka.
  Pozycje planet policzone są dokładnie (kerykeion / Swiss Ephemeris), ale ich znaczenia to
  tradycja — potraktuj ten raport jako piękne lustro do autorefleksji, nie wyrocznię.</p>
</div>

<div class="finale">
  <div class="finale-icon">🎯</div>
  <h3>Na koniec — jedno zdanie o Was dwóch</h3>
  <p><b>Jesteście dwiema połówkami tej samej intensywności.</b> Sebastian <i>działa</i> —
  zaczyna, pcha do przodu, dąży do efektu z wdziękiem (8, Ogień, Ascendent Waga).
  Piotrek <i>rozumie</i> — drąży, analizuje, czuje głębiej (7, planety zmienne, Księżyc
  Skorpion). A pod spodem łączy Was to samo: <b>obaj macie Plutona w Skorpionie i Księżyc
  w domu emocji/twórczości</b> — tę samą głęboką, twórczą wrażliwość. Jeden działa, drugi
  rozumie — <b>razem bylibyście kompletni.</b></p>
</div>
"""

HTML=f"""<!DOCTYPE html><html lang="pl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Twój portret w gwiazdach — Sebastian & Piotrek</title>
<style>
:root{{--bg:#0f1024;--card:#1a1b3a;--card2:#212255;--ink:#eef0ff;--mut:#a9adde;
--seb:#5aa9d6;--pio:#e08a5a;--line:#33356b;}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
background:radial-gradient(1200px 600px at 20% -10%,#23244f,transparent),
radial-gradient(1000px 500px at 100% 0,#2a1c44,transparent),var(--bg);
color:var(--ink);line-height:1.6;padding:0 0 60px}}
.top{{text-align:center;padding:46px 16px 6px}}
.top h1{{margin:0;font-size:32px}}
.top .sub{{color:var(--mut);margin:10px auto 0;max-width:620px}}
.legend{{display:flex;gap:22px;justify-content:center;margin:18px 0 0;flex-wrap:wrap}}
.legend span{{display:flex;align-items:center;gap:8px;font-weight:600}}
.dot{{width:14px;height:14px;border-radius:50%}}
.who{{display:grid;grid-template-columns:1fr 1fr;gap:16px;max-width:1080px;margin:22px auto 0;padding:0 16px}}
.who .card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px;text-align:center}}
.who .card:first-child{{border-top:4px solid var(--seb)}}
.who .card:last-child{{border-top:4px solid var(--pio)}}
.who .emoji{{font-size:34px}}
.who h2{{margin:4px 0}}
.who .meta{{color:var(--mut);font-size:13px}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 16px}}
.band{{margin:34px 0 8px;text-align:center}}
.band h3{{margin:0;font-size:23px}}
.banddesc{{color:var(--mut);max-width:780px;margin:6px auto 0;font-size:14.5px}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:stretch}}
.cell{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px}}
.pair>.cell:first-child{{border-top:4px solid var(--seb)}}
.pair>.cell:last-child{{border-top:4px solid var(--pio)}}
.narr{{font-size:15.5px}}
.narr p{{margin:0 0 12px}}
.narr p:last-child{{margin-bottom:0}}
/* DOWODY = drugi priorytet: zwiniete, male, wyciszone */
.ev{{margin-top:14px;border-top:1px dashed var(--line);padding-top:8px}}
.ev summary{{cursor:pointer;color:var(--mut);font-size:12.5px;list-style:none}}
.ev summary::-webkit-details-marker{{display:none}}
.ev summary::before{{content:"▸ ";}}
.ev[open] summary::before{{content:"▾ ";}}
.evbox{{margin-top:8px;background:#141531;border-radius:10px;padding:6px 10px}}
.el{{display:flex;justify-content:space-between;gap:10px;font-size:12.5px;color:var(--mut);
padding:4px 0;border-bottom:1px solid #23254e}}
.el:last-child{{border-bottom:none}}
.el b{{color:#cfd2ff;text-align:right}}
.bignum{{text-align:center;font-size:46px;font-weight:800;line-height:1;color:#fff;margin:2px 0}}
.calc{{text-align:center;font-size:11px;color:var(--mut);font-family:ui-monospace,Menlo,monospace;margin-bottom:6px}}
.summary,.finale{{margin-top:36px;background:var(--card2);border:1px solid var(--line);border-radius:16px;padding:24px}}
.summary h3,.finale h3{{margin:0 0 8px;text-align:center;font-size:23px}}
.summary .pair{{margin-top:12px}}
.cn{{margin:0 0 6px;font-size:16px}}
.cn.seb{{color:var(--seb)}} .cn.pio{{color:var(--pio)}}
.caveat{{margin-top:16px;color:var(--mut);font-size:13px;text-align:center;border-top:1px solid var(--line);padding-top:12px}}
.finale{{text-align:center;background:linear-gradient(180deg,#241a44,#1a1b3a)}}
.finale-icon{{font-size:42px}}
.finale p{{max-width:840px;margin:8px auto 0;font-size:16px}}
@media(max-width:680px){{.pair,.who{{grid-template-columns:1fr}}}}
</style></head><body>
<div class="top">
  <h1>✨ Twój portret w gwiazdach ✨</h1>
  <p class="sub">Osobisty raport astrologiczno-numerologiczny. Najpierw <b>opowieść o Was</b>,
  a niżej — pod „📊” — dane z narzędzia <b>kerykeion</b>, które ją potwierdzają.</p>
  <div class="legend">
    <span><span class="dot" style="background:var(--seb)"></span>Sebastian (lewa)</span>
    <span><span class="dot" style="background:var(--pio)"></span>Piotrek (prawa)</span>
  </div>
</div>
<div class="who">
  <div class="card"><div class="emoji">🧔</div><h2>Sebastian</h2>
    <div class="meta">{e(S['data'])} · {e(S['godzina'])} · {e(pl(S['miasto']))}<br>
    {e(S['dzien_tygodnia'])} · mapa {e(S['mapa'])} · {S['faza_emoji']} {e(pl(S['faza_ksiezyca']))}</div></div>
  <div class="card"><div class="emoji">🧑</div><h2>Piotrek</h2>
    <div class="meta">{e(P['data'])} · {e(P['godzina'])} · {e(pl(P['miasto']))}<br>
    {e(P['dzien_tygodnia'])} · mapa {e(P['mapa'])} · {P['faza_emoji']} {e(pl(P['faza_ksiezyca']))}</div></div>
</div>
<div class="wrap">
{''.join(rows)}
{podsum}
</div>
</body></html>"""

with open("index.html","w",encoding="utf-8") as f:
    f.write(HTML)
print("index.html zapisany,", len(HTML), "znakow")
