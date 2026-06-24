"""Demo kerykeion: mapa natalna (horoskop urodzeniowy).

Uruchom:  .venv/bin/python demo.py
"""
from kerykeion import AstrologicalSubjectFactory, KerykeionChartSVG

# Dane urodzenia. Offline -> podajemy wspolrzedne i strefe czasowa.
# Plock, woj. mazowieckie: ~52.5463 N, 19.7065 E
subject = AstrologicalSubjectFactory.from_birth_data(
    "Sebastian",
    year=1987, month=2, day=17, hour=21, minute=30,
    lng=19.7065, lat=52.5463, tz_str="Europe/Warsaw",
    city="Plock", nation="PL",
    online=False,
)

ZNAKI = {
    "Ari": "Baran", "Tau": "Byk", "Gem": "Bliznieta", "Can": "Rak",
    "Leo": "Lew", "Vir": "Panna", "Lib": "Waga", "Sco": "Skorpion",
    "Sag": "Strzelec", "Cap": "Koziorozec", "Aqu": "Wodnik", "Pis": "Ryby",
}
DOMY = {
    "First_House": 1, "Second_House": 2, "Third_House": 3, "Fourth_House": 4,
    "Fifth_House": 5, "Sixth_House": 6, "Seventh_House": 7, "Eighth_House": 8,
    "Ninth_House": 9, "Tenth_House": 10, "Eleventh_House": 11, "Twelfth_House": 12,
}

def zn(s):
    return ZNAKI.get(s, s)

print("=== Najwazniejsze punkty ===")
print(f"Slonce (znak zodiaku): {zn(subject.sun.sign)}  {subject.sun.position:.2f} st.  (dom {DOMY.get(subject.sun.house)})")
print(f"Ksiezyc:               {zn(subject.moon.sign)}  {subject.moon.position:.2f} st.  (dom {DOMY.get(subject.moon.house)})")
print(f"Ascendent (znak wsch.):{zn(subject.ascendant.sign)}  {subject.ascendant.position:.2f} st.")
print(f"MC (Medium Coeli):     {zn(subject.medium_coeli.sign)}  {subject.medium_coeli.position:.2f} st.")

print("\n=== Wszystkie planety ===")
PLANETY = {
    "sun": "Slonce", "moon": "Ksiezyc", "mercury": "Merkury", "venus": "Wenus",
    "mars": "Mars", "jupiter": "Jowisz", "saturn": "Saturn",
    "uranus": "Uran", "neptune": "Neptun", "pluto": "Pluton",
}
for klucz, nazwa in PLANETY.items():
    pl = getattr(subject, klucz)
    print(f"{nazwa:10s} {zn(pl.sign):12s} {pl.position:6.2f} st.  dom {DOMY.get(pl.house)}")

# Wykres SVG mapy natalnej
chart = KerykeionChartSVG(subject, new_output_directory=".")
chart.makeSVG()
print("\nWykres SVG zapisany w biezacym katalogu (plik *.svg).")
