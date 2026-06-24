"""Wyciaga dane astrologiczne (kerykeion) + numerologie dla dwoch osob -> data.json"""
import json
from kerykeion import AstrologicalSubjectFactory, NatalAspects

ZNAKI = {"Ari":"Baran","Tau":"Byk","Gem":"Bliznieta","Can":"Rak","Leo":"Lew",
         "Vir":"Panna","Lib":"Waga","Sco":"Skorpion","Sag":"Strzelec",
         "Cap":"Koziorozec","Aqu":"Wodnik","Pis":"Ryby"}
DOMY = {"First_House":1,"Second_House":2,"Third_House":3,"Fourth_House":4,
        "Fifth_House":5,"Sixth_House":6,"Seventh_House":7,"Eighth_House":8,
        "Ninth_House":9,"Tenth_House":10,"Eleventh_House":11,"Twelfth_House":12}
EL = {"Fire":"Ogien","Earth":"Ziemia","Air":"Powietrze","Water":"Woda"}
QU = {"Cardinal":"Kardynalna","Fixed":"Stala","Mutable":"Zmienna"}
ASP_PL = {"conjunction":"koniunkcja","opposition":"opozycja","trine":"trygon",
          "square":"kwadratura","sextile":"sekstyl","quintile":"kwintyl",
          "semi-sextile":"polsekstyl","quincunx":"kwinkunks"}
PLANETY = {"sun":"Slonce","moon":"Ksiezyc","mercury":"Merkury","venus":"Wenus",
           "mars":"Mars","jupiter":"Jowisz","saturn":"Saturn","uranus":"Uran",
           "neptune":"Neptun","pluto":"Pluton"}
PHASE_PL = {"New Moon":"Now","Waxing Crescent":"Przybywajacy sierp",
            "First Quarter":"Pierwsza kwadra","Waxing Gibbous":"Przybywajacy garb",
            "Full Moon":"Pelnia","Waning Gibbous":"Ubywajacy garb",
            "Last Quarter":"Ostatnia kwadra","Waning Crescent":"Ubywajacy sierp"}
DOW_PL = {"Monday":"poniedzialek","Tuesday":"wtorek","Wednesday":"sroda",
          "Thursday":"czwartek","Friday":"piatek","Saturday":"sobota","Sunday":"niedziela"}

def zn(s): return ZNAKI.get(s, s)

def point(p):
    if p is None:
        return None
    return {"znak": zn(p.sign), "stopnie": round(p.position,2),
            "dom": DOMY.get(getattr(p,"house",None))}

def reduce_num(n):
    while n>9 and n not in (11,22,33):
        n=sum(int(d) for d in str(n))
    return n

def numerologia(d,m,y):
    suma = sum(int(c) for c in f"{d:02d}{m:02d}{y}")
    return {
        "liczba_zycia": reduce_num(suma),
        "liczba_zycia_suma": suma,
        "liczba_dnia": reduce_num(d),
        "liczba_postawy": reduce_num(d+m),
    }

def osoba(name, d,m,y,h,mi, lng,lat,city):
    s = AstrologicalSubjectFactory.from_birth_data(
        name, year=y,month=m,day=d,hour=h,minute=mi,
        lng=lng,lat=lat,tz_str="Europe/Warsaw",city=city,nation="PL",online=False)
    planety = {PLANETY[k]: point(getattr(s,k)) for k in PLANETY}
    zyw={"Ogien":0,"Ziemia":0,"Powietrze":0,"Woda":0}
    jak={"Kardynalna":0,"Stala":0,"Zmienna":0}
    for k in PLANETY:
        pl=getattr(s,k); zyw[EL[pl.element]]+=1; jak[QU[pl.quality]]+=1
    # aspekty miedzy 10 planetami
    nazwy_set=set(PLANETY[k] for k in PLANETY)
    EN2PL={"Sun":"Slonce","Moon":"Ksiezyc","Mercury":"Merkury","Venus":"Wenus",
           "Mars":"Mars","Jupiter":"Jowisz","Saturn":"Saturn","Uranus":"Uran",
           "Neptune":"Neptun","Pluto":"Pluton"}
    asp=[]
    for a in NatalAspects(s).relevant_aspects:
        p1=EN2PL.get(a.p1_name); p2=EN2PL.get(a.p2_name)
        if p1 and p2:
            asp.append({"p1":p1,"aspekt":ASP_PL.get(a.aspect,a.aspect),
                        "p2":p2,"orb":round(a.orbit,2)})
    asp.sort(key=lambda x:x["orb"])
    lp=s.lunar_phase
    return {
        "imie": name,
        "data": f"{d:02d}.{m:02d}.{y}", "godzina": f"{h:02d}:{mi:02d}",
        "miasto": city,
        "slonce": point(s.sun), "ksiezyc": point(s.moon),
        "ascendent": point(s.ascendant), "mc": point(s.medium_coeli),
        "planety": planety,
        "wezel_polnocny": point(s.true_north_lunar_node),
        "chiron": point(s.chiron),
        "lilith": point(s.mean_lilith),
        "zywioly": zyw, "jakosci": jak,
        "aspekty": asp[:10],
        "faza_ksiezyca": PHASE_PL.get(lp.moon_phase_name, lp.moon_phase_name),
        "faza_emoji": lp.moon_emoji,
        "dzien_tygodnia": DOW_PL.get(s.day_of_week, s.day_of_week),
        "mapa": "dzienna" if s.is_diurnal else "nocna",
        "numerologia": numerologia(d,m,y),
    }

data = {
    "sebastian": osoba("Sebastian",17,2,1987,21,30,19.7065,52.5463,"Plock"),
    "piotrek":   osoba("Piotrek",30,5,1988,7,0,23.1688,53.1325,"Bialystok"),
}
with open("data.json","w",encoding="utf-8") as f:
    json.dump(data,f,ensure_ascii=False,indent=2)
print("OK ->", list(data.keys()))
print(json.dumps({k:{"slonce":v["slonce"],"ksiezyc":v["ksiezyc"],
    "asc":v["ascendent"],"nr_zycia":v["numerologia"]["liczba_zycia"]}
    for k,v in data.items()}, ensure_ascii=False, indent=2))
