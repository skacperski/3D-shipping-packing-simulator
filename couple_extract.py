# -*- coding: utf-8 -*-
"""Dane pary: Sebastian + Julka. Natal obojga + synastria + wskaznik relacji (kerykeion)."""
import json
from kerykeion import (AstrologicalSubjectFactory, NatalAspects,
                       SynastryAspects, RelationshipScoreFactory,
                       HouseComparisonFactory, CompositeSubjectFactory,
                       KerykeionChartSVG)

ACTIVE=['Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto',
        'True_North_Lunar_Node','True_South_Lunar_Node','Juno','Chiron','Mean_Lilith',
        'Ascendant','Medium_Coeli','Descendant','Imum_Coeli']

ZNAKI={"Ari":"Baran","Tau":"Byk","Gem":"Bliznieta","Can":"Rak","Leo":"Lew","Vir":"Panna",
       "Lib":"Waga","Sco":"Skorpion","Sag":"Strzelec","Cap":"Koziorozec","Aqu":"Wodnik","Pis":"Ryby"}
DOMY={"First_House":1,"Second_House":2,"Third_House":3,"Fourth_House":4,"Fifth_House":5,
      "Sixth_House":6,"Seventh_House":7,"Eighth_House":8,"Ninth_House":9,"Tenth_House":10,
      "Eleventh_House":11,"Twelfth_House":12}
EL={"Fire":"Ogien","Earth":"Ziemia","Air":"Powietrze","Water":"Woda"}
QU={"Cardinal":"Kardynalna","Fixed":"Stala","Mutable":"Zmienna"}
ASP_PL={"conjunction":"koniunkcja","opposition":"opozycja","trine":"trygon","square":"kwadratura",
        "sextile":"sekstyl","quintile":"kwintyl","semi-sextile":"polsekstyl","quincunx":"kwinkunks"}
PLANETY={"sun":"Slonce","moon":"Ksiezyc","mercury":"Merkury","venus":"Wenus","mars":"Mars",
         "jupiter":"Jowisz","saturn":"Saturn","uranus":"Uran","neptune":"Neptun","pluto":"Pluton"}
EN2PL={"Sun":"Slonce","Moon":"Ksiezyc","Mercury":"Merkury","Venus":"Wenus","Mars":"Mars",
       "Jupiter":"Jowisz","Saturn":"Saturn","Uranus":"Uran","Neptune":"Neptun","Pluto":"Pluton",
       "Ascendant":"Ascendent","Medium_Coeli":"MC","Descendant":"Descendent",
       "Juno":"Junona","True_North_Lunar_Node":"Wezel Polnocny","True_South_Lunar_Node":"Wezel Poludniowy",
       "Chiron":"Chiron"}
PHASE_PL={"New Moon":"Now","Waxing Crescent":"Przybywajacy sierp","First Quarter":"Pierwsza kwadra",
          "Waxing Gibbous":"Przybywajacy garb","Full Moon":"Pelnia","Waning Gibbous":"Ubywajacy garb",
          "Last Quarter":"Ostatnia kwadra","Waning Crescent":"Ubywajacy sierp"}
DOW_PL={"Monday":"poniedzialek","Tuesday":"wtorek","Wednesday":"sroda","Thursday":"czwartek",
        "Friday":"piatek","Saturday":"sobota","Sunday":"niedziela"}
def zn(s): return ZNAKI.get(s,s)
def point(p):
    if p is None: return None
    return {"znak":zn(p.sign),"stopnie":round(p.position,2),"dom":DOMY.get(getattr(p,"house",None))}
def reduce_num(n):
    while n>9 and n not in (11,22,33): n=sum(int(d) for d in str(n))
    return n
def numerologia(d,m,y):
    s=sum(int(c) for c in f"{d:02d}{m:02d}{y}")
    return {"liczba_zycia":reduce_num(s),"liczba_zycia_suma":s,
            "liczba_dnia":reduce_num(d),"liczba_postawy":reduce_num(d+m)}

def osoba(name,d,m,y,h,mi,lng,lat,city):
    s=AstrologicalSubjectFactory.from_birth_data(name,year=y,month=m,day=d,hour=h,minute=mi,
        lng=lng,lat=lat,tz_str="Europe/Warsaw",city=city,nation="PL",online=False,
        active_points=ACTIVE)
    planety={PLANETY[k]:point(getattr(s,k)) for k in PLANETY}
    zyw={"Ogien":0,"Ziemia":0,"Powietrze":0,"Woda":0}; jak={"Kardynalna":0,"Stala":0,"Zmienna":0}
    for k in PLANETY:
        pl=getattr(s,k); zyw[EL[pl.element]]+=1; jak[QU[pl.quality]]+=1
    asp=[]
    for a in NatalAspects(s).relevant_aspects:
        p1=EN2PL.get(a.p1_name); p2=EN2PL.get(a.p2_name)
        if p1 in PLANETY.values() and p2 in PLANETY.values():
            asp.append({"p1":p1,"aspekt":ASP_PL.get(a.aspect,a.aspect),"p2":p2,"orb":round(a.orbit,2)})
    asp.sort(key=lambda x:x["orb"])
    lp=s.lunar_phase
    data={"imie":name,"data":f"{d:02d}.{m:02d}.{y}","godzina":f"{h:02d}:{mi:02d}","miasto":city,
        "slonce":point(s.sun),"ksiezyc":point(s.moon),"ascendent":point(s.ascendant),
        "mc":point(s.medium_coeli),"planety":planety,"wezel_polnocny":point(s.true_north_lunar_node),
        "chiron":point(s.chiron),"lilith":point(s.mean_lilith),"zywioly":zyw,"jakosci":jak,
        "aspekty":asp[:10],"faza_ksiezyca":PHASE_PL.get(lp.moon_phase_name,lp.moon_phase_name),
        "faza_emoji":lp.moon_emoji,"dzien_tygodnia":DOW_PL.get(s.day_of_week,s.day_of_week),
        "mapa":"dzienna" if s.is_diurnal else "nocna","numerologia":numerologia(d,m,y)}
    return s, data

seb_subj, seb = osoba("Sebastian",17,2,1987,21,30,19.7065,52.5463,"Plock")
jul_subj, jul = osoba("Julka",22,9,2000,6,25,22.0190,49.6953,"Brzozow")

# --- synastria (planeta Sebastiana <-> planeta Julki) ---
WAZNE={"Slonce","Ksiezyc","Wenus","Mars","Merkury","Jowisz","Saturn","Ascendent","MC"}
syn=[]
for a in SynastryAspects(seb_subj,jul_subj).relevant_aspects:
    p1=EN2PL.get(a.p1_name); p2=EN2PL.get(a.p2_name)
    if not p1 or not p2: continue
    # p1_owner / p2_owner: czyje
    o1=a.p1_owner; o2=a.p2_owner
    if o1=="Sebastian":
        seb_pl, jul_pl = p1, p2
    else:
        seb_pl, jul_pl = p2, p1
    if seb_pl in WAZNE and jul_pl in WAZNE:
        syn.append({"seb":seb_pl,"aspekt":ASP_PL.get(a.aspect,a.aspect),"jul":jul_pl,
                    "orb":round(a.orbit,2)})
syn.sort(key=lambda x:x["orb"])

# --- wskaznik relacji ---
rs=RelationshipScoreFactory(seb_subj,jul_subj).get_relationship_score()
score={"wartosc":rs.score_value,"opis":rs.score_description,"przeznaczenie":rs.is_destiny_sign,
       "rozbicie":[{"regula":b.rule,"opis":b.description,"punkty":b.points,"detale":b.details}
                   for b in rs.score_breakdown]}

# --- nakladki domow (czyje planety w czyich domach) ---
def overlays(hc_list):
    out=[]
    for o in hc_list:
        nm=EN2PL.get(o.point_name)
        if nm: out.append({"punkt":nm,"dom":o.projected_house_number})
    return out
hc=HouseComparisonFactory(seb_subj,jul_subj).get_house_comparison()
overlay={"seb_w_domach_julki":overlays(hc.first_points_in_second_houses),
         "jul_w_domach_seba":overlays(hc.second_points_in_first_houses)}

# --- mapa zlozona (composite, punkty srodkowe) ---
comp=CompositeSubjectFactory(seb_subj,jul_subj).get_midpoint_composite_subject_model()
def cpoint(p):
    return None if p is None else {"znak":zn(p.sign),"stopnie":round(p.position,2),
                                   "dom":DOMY.get(getattr(p,"house",None))}
composite={"slonce":cpoint(comp.sun),"ksiezyc":cpoint(comp.moon),
           "ascendent":cpoint(getattr(comp,"ascendant",None)),
           "wenus":cpoint(comp.venus),"mars":cpoint(comp.mars)}

# --- Junona + Wezly (przeznaczenie) ---
juno={"seb":point(seb_subj.juno),"jul":point(jul_subj.juno)}
przeznaczenie=[]
for a in SynastryAspects(seb_subj,jul_subj,active_points=ACTIVE).relevant_aspects:
    p1=EN2PL.get(a.p1_name); p2=EN2PL.get(a.p2_name)
    if not p1 or not p2: continue
    if ("Wezel" in p1 or "Wezel" in p2 or "Junona" in (p1,p2)):
        seb_pl,jul_pl=(p1,p2) if a.p1_owner=="Sebastian" else (p2,p1)
        przeznaczenie.append({"seb":seb_pl,"aspekt":ASP_PL.get(a.aspect,a.aspect),
                              "jul":jul_pl,"orb":round(a.orbit,2)})
przeznaczenie.sort(key=lambda x:x["orb"])

# --- wykres synastryczny SVG ---
chart=KerykeionChartSVG(seb_subj,"Synastry",jul_subj,new_output_directory=".")
chart.makeSVG()

out={"sebastian":seb,"julka":jul,"synastria":syn[:14],"score":score,
     "overlay":overlay,"composite":composite,"juno":juno,
     "przeznaczenie":przeznaczenie[:8]}
with open("couple.json","w",encoding="utf-8") as f:
    json.dump(out,f,ensure_ascii=False,indent=2)
print("OK. score=",score["wartosc"],score["opis"],"| synastr aspektow:",len(syn))
print("TOP synastria:")
for a in syn[:8]: print("  ",a["seb"],a["aspekt"],a["jul"],"orb",a["orb"])
