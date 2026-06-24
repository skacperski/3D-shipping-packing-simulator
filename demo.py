"""Demo kerykeion: obliczenie mapy natalnej (horoskopu urodzeniowego).

Uruchom:  .venv/bin/python demo.py
"""
from kerykeion import AstrologicalSubjectFactory

# Dane urodzenia (przyklad). Offline -> podajemy wspolrzedne i strefe czasowa.
subject = AstrologicalSubjectFactory.from_birth_data(
    "Przyklad",
    year=1990, month=6, day=15, hour=14, minute=30,
    lng=21.0122, lat=52.2297, tz_str="Europe/Warsaw",  # Warszawa
    city="Warszawa", nation="PL",
    online=False,
)

print("=== Dane podstawowe ===")
print(f"Slonce:    {subject.sun.sign}  {subject.sun.position:.2f}stopni  (dom {subject.sun.house})")
print(f"Ksiezyc:   {subject.moon.sign}  {subject.moon.position:.2f}stopni  (dom {subject.moon.house})")
print(f"Ascendent: {subject.ascendant.sign}  {subject.ascendant.position:.2f}stopni")

print("\n=== Wszystkie planety ===")
planety = ["sun", "moon", "mercury", "venus", "mars",
           "jupiter", "saturn", "uranus", "neptune", "pluto"]
for p in planety:
    pl = getattr(subject, p)
    print(f"{pl.name:12s} {pl.sign:12s} {pl.position:6.2f}stopni  dom {pl.house}")
