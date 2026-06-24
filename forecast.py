# -*- coding: utf-8 -*-
"""Prognoza miłosna pary (tranzyty z kerykeion) -> forecast.json.
Liczy tranzyty Wenus/Marsa/Jowisza/Saturna po mapach Sebastiana i Julki,
klasyfikuje na romantyczne / namietne / do przepracowania / stabilizujace."""
import json
from datetime import datetime
from kerykeion import (AstrologicalSubjectFactory, EphemerisDataFactory,
                       TransitsTimeRangeFactory)

START=datetime(2026,7,1); END=datetime(2026,12,31)
T_PLANETS=["Venus","Mars","Jupiter","Saturn"]
N_POINTS={"Sun","Moon","Venus","Mars","Ascendant","Descendant","Medium_Coeli"}
PLPL={"Venus":"Wenus","Mars":"Mars","Jupiter":"Jowisz","Saturn":"Saturn","Sun":"Słońce",
      "Moon":"Księżyc","Ascendant":"Ascendent","Descendant":"Descendent","Medium_Coeli":"MC"}
ASP={"conjunction":"złączenie","opposition":"naprzeciw","trine":"harmonia",
     "sextile":"szansa","square":"napięcie","quintile":"iskra"}
HARM={"trine","sextile","conjunction","quintile"}
HARD={"square","opposition"}
MIES=["","stycznia","lutego","marca","kwietnia","maja","czerwca","lipca","sierpnia",
      "września","października","listopada","grudnia"]

def klasyfikuj(tp, asp, npt):
    if tp in ("Venus","Jupiter") and asp in HARM and npt in ("Venus","Moon","Sun","Ascendant","Descendant"):
        return ("romance","❤️","Romantyczne, czułe okno — dobry czas na bliskość i miłe gesty")
    if tp=="Mars" and asp in HARM and npt in ("Venus","Mars","Sun"):
        return ("passion","🔥","Przypływ namiętności i energii — iskrzy między Wami")
    if tp in ("Mars","Saturn") and asp in HARD and npt in ("Venus","Moon","Sun","Mars"):
        return ("tension","⚡","Okno do przepracowania — więcej cierpliwości i rozmowy")
    if tp=="Saturn" and asp in HARM and npt in ("Venus","Sun","Moon","Descendant"):
        return ("commit","💍","Stabilizacja i powaga uczuć — dobry czas na zobowiązania")
    if tp=="Jupiter" and asp in HARM and npt in ("Sun","Mars","Medium_Coeli"):
        return ("luck","🍀","Wspólny rozwój, optymizm, szczęśliwa passa")
    return None

def transity(name,d,m,y,h,mi,lng,lat):
    s=AstrologicalSubjectFactory.from_birth_data(name,year=y,month=m,day=d,hour=h,minute=mi,
        lng=lng,lat=lat,tz_str="Europe/Warsaw",city="x",nation="PL",online=False)
    eph=EphemerisDataFactory(START,END,step_type="days",step=2,lat=lat,lng=lng,
        tz_str="Europe/Warsaw").get_ephemeris_data_as_astrological_subjects()
    moments=TransitsTimeRangeFactory(s,eph,active_points=T_PLANETS).get_transit_moments()
    peaks={}  # (tp,asp,npt) -> (orb,date)
    for mom in moments.transits:
        dt=mom.date[:10]
        for a in mom.aspects:
            tp=a.p1_name; npt=a.p2_name; asp=a.aspect
            if tp not in T_PLANETS or npt not in N_POINTS: continue
            k=(tp,asp,npt)
            if k not in peaks or a.orbit<peaks[k][0]:
                peaks[k]=(a.orbit,dt)
    ev=[]
    for (tp,asp,npt),(orb,dt) in peaks.items():
        kl=klasyfikuj(tp,asp,npt)
        if not kl or orb>3.0: continue
        kind,emo,opis=kl
        y_,m_,d_=dt.split("-")
        ev.append({"data":dt,"data_pl":f"{int(d_)} {MIES[int(m_)]}","kto":name,
                   "tp":PLPL[tp],"aspekt":ASP.get(asp,asp),"np":PLPL[npt],
                   "orb":round(orb,2),"kind":kind,"emoji":emo,"opis":opis})
    ev.sort(key=lambda x:x["data"])
    return ev

seb=transity("Sebastian",17,2,1987,21,30,19.7065,52.5463)
jul=transity("Julka",22,9,2000,6,25,22.0190,49.6953)
allev=sorted(seb+jul,key=lambda x:x["data"])

out={"od":START.strftime("%d.%m.%Y"),"do":END.strftime("%d.%m.%Y"),
     "wydarzenia":allev,"seb":seb,"jul":jul}
with open("forecast.json","w",encoding="utf-8") as f:
    json.dump(out,f,ensure_ascii=False,indent=2)
print("Wydarzen razem:",len(allev),"| Sebastian:",len(seb),"| Julka:",len(jul))
from collections import Counter
print("Typy:",Counter(e["kind"] for e in allev))
print("Przyklady:")
for e in allev[:10]:
    print(" ",e["data_pl"],e["emoji"],e["kto"],"-",e["tp"],e["aspekt"],e["np"],"orb",e["orb"])
