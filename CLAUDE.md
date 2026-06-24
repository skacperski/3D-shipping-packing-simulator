# Wytyczne projektu

## Astrologia — zasada nadrzędna

Przy każdym pytaniu astrologicznym (mapy natalne, znaki, planety, domy, aspekty,
żywioły, kompatybilność itp.):

- **Dane wyciągaj WYŁĄCZNIE z narzędzia `kerykeion`** (biblioteka Python w `.venv`).
  Uruchamiaj kod, który liczy konkretne wartości, i opieraj się na jego wyniku.
- **Nigdy nie zmyślaj** pozycji planet, znaków, domów ani aspektów. Jeśli czegoś
  nie ma w wyniku narzędzia — nie podawaj tego.
- **Zawsze faktycznie korzystaj z narzędzia** (nie z pamięci modelu), zanim
  przedstawisz jakiekolwiek liczby lub fakty astrologiczne.
- Interpretacje symboliczne można opisywać słownie, ale muszą być oparte na
  danych zwróconych przez `kerykeion` (znak, dom, aspekt z konkretnym orbem).

Uruchamianie narzędzia: `.venv/bin/python demo.py` (lub własny skrypt korzystający
z `kerykeion`).
