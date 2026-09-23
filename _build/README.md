# 5to9.me — izvor sajta (_build)

Sajt je statički, dvojezičan (ME podrazumijevano, EN pod /en/).
Tekstovi su u `content_*.py`, šabloni u `build.py`, stil u `src/base.css` + `src/extra.css`, JS u `src/site.js`.

Izmjena: uredi tekst → `python3 _build/build.py` → kopiraj sadržaj `_build/out/` u root repozitorijuma.
Slike se čitaju iz `/assets/img`. Jekyll ne objavljuje folder `_build`.

| ME | EN |
|---|---|
| / | /en/ |
| /teqball-stolovi/ | /en/teqball-tables/ |
| /interaktivne-table/ | /en/interactive-displays/ |
| /djecija-igralista/ | /en/playgrounds/ |
| /outdoor-fitness/ | /en/outdoor-fitness/ |
