# -*- coding: utf-8 -*-
"""Raport pary Sebastian + Julka: relacja i dopasowanie (synastria z kerykeion).
Interpretacja na pierwszym planie; dane (natal + synastria + wskaznik) jako DOWODY."""
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
def syn_find(seb_pl, jul_pl):
    """Znajdz aspekt synastryczny seb_pl(Sebastian) - jul_pl(Julka)."""
    out=[]
    for a in SYN:
        if a["seb"]==seb_pl and a["jul"]==jul_pl:
            out.append(a)
    return out
def ev(rows): return "".join(rows)
def el(k,v): return f'<div class="el"><span>{k}</span><b>{v}</b></div>'
def syn_el(a):
    return el(f"{EMO.get(pl(a['seb']),'')} {pl(a['seb'])} (S) – {pl(a['jul'])} (J) {EMO.get(pl(a['jul']),'')}",
              f"{pl(a['aspekt'])} · orb {a['orb']}°")

# ---------- KIM JESTESCIE (krotko, na potrzeby relacji) ----------
NARR_S = """<p>Sebastian to <b>niezależny twórca o miękkim, relacyjnym sercu</b>. W rdzeniu
oryginał (Słońce w Wodniku), który jednak emocjonalnie żyje <b>harmonią i relacjami</b>
(Księżyc i Ascendent w Wadze). W związku: ceni partnerstwo, nie znosi konfliktu, ale
potrzebuje też wolności i przestrzeni na bycie sobą.</p>"""
NARR_J = """<p>Julka to <b>bystra, towarzyska perfekcjonistka z opiekuńczym sercem</b>. Słońce
i Ascendent w Pannie dają uważność, troskę o szczegóły i chęć realnej pomocy, a Księżyc w Raku
sprawia, że emocjonalnie najbardziej potrzebuje <b>bliskości, czułości i poczucia „domu”</b>.
Sześć planet w żywiole Powietrza czyni z niej osobę <b>rozmowną, lotną umysłowo</b>, ceniącą
kontakt — a Wenus i Merkury w Wadze dorzucają wdzięk i pragnienie partnerstwa.</p>"""

# ---------- SEKCJE RELACJI (pelna szerokosc) ----------
def rel_block(icon, tytul, opis, narracja, aspekty_list):
    rows = [syn_el(a) for pair in aspekty_list for a in syn_find(*pair)]
    dowody = (f"""<details class="ev"><summary>📊 Aspekty synastryczne, na których to oparte
              (S = Sebastian, J = Julka)</summary><div class="evbox">{ev(rows)}</div></details>"""
              if rows else "")
    return f"""<div class="relsec">
      <h3>{icon} {tytul}</h3>
      <p class="reldesc">{opis}</p>
      <div class="relnarr">{narracja}</div>
      {dowody}
    </div>"""

CHEMIA = rel_block("💘","Chemia i przyciąganie",
  "Czy iskrzy? Tu patrzymy na klasyczne aspekty pożądania i czułości między Waszymi mapami.",
  """<p><b>Tak, iskrzy — i to mocno.</b> Najsilniejszy aspekt w całej Waszej synastrii to
  <b>Wenus Sebastiana naprzeciw Księżyca Julki</b> (orb zaledwie 0,17° — niemal idealny!).
  W praktyce: sposób, w jaki Sebastian okazuje uczucia, trafia <i>dokładnie</i> w to, czego
  emocjonalnie potrzebuje Julka — ona czuje się kochana tak, jak chce być kochana.</p>
  <p>Do tego dochodzi <b>Mars Sebastiana naprzeciw Wenus Julki</b> — to klasyczny aspekt
  <b>fizycznej chemii i pożądania</b> (właśnie ten punkt kerykeion liczy do wskaźnika relacji).
  A Słońce Sebastiana w harmonii z Wenus Julki sprawia, że po prostu <b>mu się podoba</b>.
  Opozycje działają tu jak magnesy: przyciągacie się.</p>""",
  [("Wenus","Ksiezyc"),("Mars","Wenus"),("Slonce","Wenus")])

POROZUMIENIE = rel_block("🗣️","Porozumienie i rozmowa",
  "Czy się dogadujecie? Tu liczy się kontakt umysłu z emocjami i wspólny język na co dzień.",
  """<p><b>Rozmowa to Wasz atut.</b> <b>Merkury Sebastiana w harmonii z Księżycem Julki</b>
  (orb 0,24°!) oznacza, że Sebastian potrafi nazwać i zrozumieć to, co Julka czuje — ona czuje
  się <b>słuchana i rozumiana</b>. Przykład: gdy ma gorszy dzień, on trafia w sedno słowami,
  zamiast gubić się w domysłach.</p>
  <p>Saturn Sebastiana wspiera myślenie Julki stabilnością i powagą, a oboje macie dużo planet
  „zmiennych” — jesteście elastyczni i lubicie gadać. Jej sześć planet w Powietrzu plus jego
  wagowa potrzeba harmonii = para, która <b>dużo rozmawia i szuka porozumienia</b>.</p>""",
  [("Merkury","Ksiezyc"),("Saturn","Merkury")])

TARCIA = rel_block("⚔️","Tarcia i wyzwania",
  "Gdzie będzie zgrzytać? Każda para ma swoje pola pracy — uczciwie je nazywamy.",
  """<p><b>Wasze główne wyzwanie to różne rytmy emocjonalne.</b> <b>Księżyc Sebastiana w
  kwadraturze do Księżyca Julki</b> (orb 0,7°) znaczy, że instynktownie reagujecie inaczej:
  co innego daje Wam poczucie bezpieczeństwa (jemu — harmonia i relacje w stylu Wagi; jej —
  bliskość i „dom” w stylu Raka). Stąd czasem „nie czujemy tego tak samo”. Wzmacnia to
  <b>Ascendent Sebastiana w kwadraturze do jej Księżyca</b> (też liczony do wskaźnika).</p>
  <p>Drugie pole: <b>Słońce Sebastiana w kwadraturze do Saturna Julki</b> — bywa, że on czuje
  się oceniany lub hamowany, a ona wnosi wymagania i powagę. I różnica temperamentów: Julka jest
  bardzo „powietrzna” (analizuje, dystansuje), Sebastian bardziej „wodno-ognisty” (czuje i
  reaguje gorąco) — czyli klasyczne <b>„logika kontra emocje”</b>. To punkty do świadomej
  pracy, nie wyroki.</p>""",
  [("Ksiezyc","Ksiezyc"),("Ascendent","Ksiezyc"),("Slonce","Saturn")])

KIERUNEK = rel_block("🏡","Wspólny kierunek i przyszłość",
  "Czy idziecie w tę samą stronę? Tu patrzymy na wsparcie celów i budowanie wspólnego życia.",
  """<p><b>Macie dobry fundament „idziemy razem”.</b> <b>Słońce Sebastiana w harmonii z punktem
  kariery (MC) Julki</b> (orb 1,0°) oraz <b>jego Mars wspierający jej MC</b> oznaczają, że
  Sebastian naturalnie <b>kibicuje ambicjom Julki</b> i dodaje jej energii do działania —
  nie rywalizuje, lecz wspiera.</p>
  <p>Numerologicznie też się uzupełniacie: jego <b>8 (Realizator — buduje, zapewnia)</b> i jej
  <b>6 (Opiekun — to wręcz „liczba miłości i domu”)</b> tworzą naturalny duet:
  <b>on buduje, ona tworzy ciepło</b>. Razem moglibyście zbudować dom z prawdziwego zdarzenia.</p>""",
  [("Slonce","MC"),("Mars","MC")])

# couple number
cn = S["numerologia"]["liczba_zycia"] + J["numerologia"]["liczba_zycia"]
while cn>9 and cn not in (11,22,33): cn=sum(int(d) for d in str(cn))

# ---------- gauge ----------
val=SCORE["wartosc"]; pct=min(100, round(val/30*100))
poziom=SCORE["opis"]
POZIOM_PL={"Minimal":"Minimalna","Medium":"Średnia","Important":"Znacząca",
           "Very Important":"Bardzo znacząca","Exceptional":"Wyjątkowa","Rare Exceptional":"Rzadka wyjątkowa"}

HTML=f"""<!DOCTYPE html><html lang="pl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sebastian & Julka — czy pasujecie? Raport relacji</title>
<style>
:root{{--bg:#160f1f;--card:#241730;--card2:#2c1d3b;--ink:#f6eefc;--mut:#c6abdd;
--seb:#5aa9d6;--jul:#e86fa6;--line:#43335a;--good:#5fd08a;--warn:#e7a14e;}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
background:radial-gradient(1200px 600px at 15% -10%,#3a2150,transparent),
radial-gradient(1000px 500px at 100% 0,#3a1d35,transparent),var(--bg);
color:var(--ink);line-height:1.6;padding:0 0 60px}}
.top{{text-align:center;padding:46px 16px 4px}}
.top h1{{margin:0;font-size:32px}}
.top .sub{{color:var(--mut);max-width:640px;margin:10px auto 0}}
.wrap{{max-width:1060px;margin:0 auto;padding:0 16px}}
.who{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:22px 0 0}}
.who .card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px}}
.who .card:first-child{{border-top:4px solid var(--seb)}}
.who .card:last-child{{border-top:4px solid var(--jul)}}
.who h2{{margin:2px 0 2px}}
.who .meta{{color:var(--mut);font-size:13px;margin-bottom:8px}}
.narr p{{margin:0 0 10px}} .narr p:last-child{{margin:0}}
.gauge{{background:var(--card2);border:1px solid var(--line);border-radius:16px;
padding:22px;margin:24px 0 6px;text-align:center}}
.gauge h3{{margin:0 0 4px;font-size:22px}}
.gnum{{font-size:48px;font-weight:800;color:#fff;line-height:1.1}}
.glabel{{color:var(--mut);margin-bottom:14px}}
.gbar{{height:16px;border-radius:10px;background:#1c1228;position:relative;overflow:hidden;
border:1px solid var(--line)}}
.gbar::after{{content:"";position:absolute;left:0;top:0;bottom:0;width:{pct}%;
background:linear-gradient(90deg,var(--warn),var(--jul));border-radius:10px}}
.gscale{{display:flex;justify-content:space-between;color:var(--mut);font-size:11px;margin-top:6px}}
.relsec{{background:var(--card);border:1px solid var(--line);border-radius:16px;
padding:22px;margin:18px 0;border-left:4px solid var(--jul)}}
.relsec h3{{margin:0 0 4px;font-size:22px}}
.reldesc{{color:var(--mut);font-size:14px;margin:0 0 12px}}
.relnarr{{font-size:15.5px}}
.relnarr p{{margin:0 0 12px}} .relnarr p:last-child{{margin:0}}
.ev{{margin-top:14px;border-top:1px dashed var(--line);padding-top:8px}}
.ev summary{{cursor:pointer;color:var(--mut);font-size:12.5px;list-style:none}}
.ev summary::-webkit-details-marker{{display:none}}
.ev summary::before{{content:"▸ "}} .ev[open] summary::before{{content:"▾ "}}
.evbox{{margin-top:8px;background:#1a1029;border-radius:10px;padding:6px 10px}}
.el{{display:flex;justify-content:space-between;gap:10px;font-size:12.5px;color:var(--mut);
padding:4px 0;border-bottom:1px solid #2a1c3b}}
.el:last-child{{border-bottom:none}} .el b{{color:#e7d6f5;text-align:right}}
.num{{display:grid;grid-template-columns:1fr auto 1fr;gap:14px;align-items:center;
background:var(--card2);border:1px solid var(--line);border-radius:16px;padding:20px;margin:18px 0}}
.num .p{{text-align:center}} .num .big{{font-size:40px;font-weight:800;color:#fff}}
.num .eq{{font-size:26px;color:var(--mut)}}
.verdict{{background:linear-gradient(180deg,#33204a,#241730);border:1px solid var(--line);
border-radius:18px;padding:26px;margin-top:24px;text-align:center}}
.verdict h3{{margin:0 0 8px;font-size:24px}}
.verdict p{{max-width:840px;margin:8px auto 0;font-size:16px}}
.tags{{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin:14px 0}}
.tag{{padding:6px 12px;border-radius:20px;font-size:13px;font-weight:600}}
.tag.g{{background:rgba(95,208,138,.16);color:var(--good);border:1px solid var(--good)}}
.tag.w{{background:rgba(231,161,78,.16);color:var(--warn);border:1px solid var(--warn)}}
.caveat{{color:var(--mut);font-size:13px;border-top:1px solid var(--line);padding-top:12px;margin-top:18px}}
.bandtitle{{text-align:center;margin:30px 0 2px;font-size:23px}}
@media(max-width:680px){{.who,.num{{grid-template-columns:1fr}}.num .eq{{display:none}}}}
</style></head><body>
<div class="top">
  <h1>💞 Sebastian &amp; Julka</h1>
  <p class="sub">Raport relacji oparty na <b>synastrii</b> (porównaniu Waszych map) z narzędzia
  <b>kerykeion</b>. Najpierw opowieść, niżej — pod „📊” — dane, które ją potwierdzają.</p>
</div>
<div class="wrap">

  <h2 class="bandtitle">👥 Kim jesteście</h2>
  <div class="who">
    <div class="card"><h2>🧔 Sebastian</h2>
      <div class="meta">{e(S['data'])} · {e(S['godzina'])} · {e(pl(S['miasto']))} ·
        {S['faza_emoji']} {e(pl(S['faza_ksiezyca']))}</div>
      <div class="narr">{NARR_S}</div>
      <details class="ev"><summary>📊 Dane (kerykeion)</summary><div class="evbox">
        {el("☉ Słońce",pt(S['slonce']))}{el("☽ Księżyc",pt(S['ksiezyc']))}
        {el("⬆ Ascendent",pt(S['ascendent']))}{el("♀ Wenus",pt(S['planety']['Wenus']))}
        {el("♂ Mars",pt(S['planety']['Mars']))}
        {el("Żywioły","Ogień "+str(S['zywioly']['Ogien'])+" · Ziemia "+str(S['zywioly']['Ziemia'])+" · Powietrze "+str(S['zywioly']['Powietrze'])+" · Woda "+str(S['zywioly']['Woda']))}
      </div></details>
    </div>
    <div class="card"><h2>👩 Julka</h2>
      <div class="meta">{e(J['data'])} · {e(J['godzina'])} · {e(pl(J['miasto']))} ·
        {J['faza_emoji']} {e(pl(J['faza_ksiezyca']))}</div>
      <div class="narr">{NARR_J}</div>
      <details class="ev"><summary>📊 Dane (kerykeion)</summary><div class="evbox">
        {el("☉ Słońce",pt(J['slonce']))}{el("☽ Księżyc",pt(J['ksiezyc']))}
        {el("⬆ Ascendent",pt(J['ascendent']))}{el("♀ Wenus",pt(J['planety']['Wenus']))}
        {el("♂ Mars",pt(J['planety']['Mars']))}
        {el("Żywioły","Ogień "+str(J['zywioly']['Ogien'])+" · Ziemia "+str(J['zywioly']['Ziemia'])+" · Powietrze "+str(J['zywioly']['Powietrze'])+" · Woda "+str(J['zywioly']['Woda']))}
      </div></details>
    </div>
  </div>

  <div class="gauge">
    <h3>🔥 Wskaźnik dopasowania</h3>
    <div class="gnum">{val} pkt</div>
    <div class="glabel">poziom: <b>{POZIOM_PL.get(poziom,poziom)}</b> ({e(poziom)})</div>
    <div class="gbar"></div>
    <div class="gscale"><span>0</span><span>Średnia</span><span>Znacząca</span>
      <span>Wyjątkowa</span><span>30+</span></div>
    <p class="reldesc" style="margin-top:12px">Wskaźnik kerykeiona (metoda Ciro Discepolo) liczy
    najmocniejsze aspekty więzi. Punkty zdobyły: <b>Mars–Wenus</b> (pożądanie, +4) i
    <b>Księżyc–Ascendent</b> (więź emocjonalna, +4). „Średnia” to solidny, realny wynik —
    większość udanych par mieści się właśnie tu.</p>
  </div>

  <h2 class="bandtitle">💞 Wasza relacja — analiza</h2>
  {CHEMIA}
  {POROZUMIENIE}
  {TARCIA}
  {KIERUNEK}

  <h2 class="bandtitle">🔢 Numerologia pary</h2>
  <div class="num">
    <div class="p"><div class="big">{S['numerologia']['liczba_zycia']}</div>
      <div class="reldesc">Sebastian — Realizator<br>(buduje, zapewnia)</div></div>
    <div class="eq">+&nbsp;→</div>
    <div class="p"><div class="big">{J['numerologia']['liczba_zycia']}</div>
      <div class="reldesc">Julka — Opiekun<br>(miłość, dom, harmonia)</div></div>
  </div>
  <div class="relsec" style="border-left-color:var(--good)">
    <p class="relnarr"><b>Wspólna liczba pary: {cn}.</b> Sumując Wasze Liczby Życia
    ({S['numerologia']['liczba_zycia']} + {J['numerologia']['liczba_zycia']} =
    {S['numerologia']['liczba_zycia']+J['numerologia']['liczba_zycia']} → {cn}) wychodzi
    „<b>{ {1:'Lider',2:'Dyplomata',3:'Artysta',4:'Budowniczy',5:'Podróżnik',6:'Opiekun',7:'Poszukiwacz',8:'Realizator',9:'Humanista',11:'Wizjoner',22:'Mistrz Budowniczy',33:'Mistrz Nauczyciel'}[cn] }</b>”.
    To energia <b>ruchu, wolności i przygody</b> — jako para najlepiej czujecie się, gdy się
    rozwijacie, podróżujecie i nie popadacie w rutynę. Ładnie spina to jego potrzebę wolności
    (Wodnik) z jej lotnością (6 planet w Powietrzu).</p>
  </div>

  <div class="verdict">
    <div style="font-size:42px">💍</div>
    <h3>Czy pasujecie do siebie?</h3>
    <div class="tags">
      <span class="tag g">💘 Silna chemia</span>
      <span class="tag g">🗣️ Świetne porozumienie</span>
      <span class="tag g">🏡 Wsparcie celów</span>
      <span class="tag w">🌗 Różne rytmy emocji</span>
      <span class="tag w">🧠 Logika vs uczucia</span>
    </div>
    <p><b>Tak — i to z prawdziwą iskrą.</b> Macie rzadko spotykane, niemal idealne aspekty
    przyciągania (Wenus–Księżyc 0,17°) i rozumienia (Merkury–Księżyc 0,24°), a do tego Sebastian
    naturalnie wspiera ambicje Julki. To mocna baza: <b>pożądanie + rozmowa + wspólny kierunek</b>.</p>
    <p>Wasza praca na lata to <b>uszanowanie różnych sposobów czucia</b>: jej Księżyc w Raku chce
    bliskości i „domu”, jego w Wadze — harmonii i przestrzeni; ona myśli (Powietrze), on czuje
    (Woda/Ogień). Gdy nauczycie się tłumaczyć sobie nawzajem te dwa języki, napięcie zamieni się
    w to, co Was uzupełnia. <b>Werdykt: dopasowanie solidne (Średnie, 8 pkt) z bardzo dobrym
    potencjałem na trwały, ciepły związek.</b></p>
    <p class="caveat">⚖️ Uczciwie: synastria i numerologia to systemy <b>symboliczne</b>, nie
    nauka. Liczby i aspekty policzone są dokładnie (kerykeion / Swiss Ephemeris), ale ich
    znaczenia to tradycja. Żadna mapa nie decyduje o związku — decydujecie Wy. Potraktujcie to
    jako ciepłe lustro do rozmowy we dwoje. 💛</p>
  </div>
</div>
</body></html>"""

with open("index.html","w",encoding="utf-8") as f:
    f.write(HTML)
print("index.html (para) zapisany,", len(HTML), "znakow | couple number:", cn)
