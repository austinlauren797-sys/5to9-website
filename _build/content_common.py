# -*- coding: utf-8 -*-
"""Shared strings, page registry and category tiles for the 5TO9 site (ME + EN)."""

SITE = "https://5to9.me/"
EMAIL = "team@5to9.me"
PHONE = "+382 67 148 790"
PHONE_TEL = "+38267148790"

# page key -> URL path per language (relative to site root, '' = home)
PATHS = {
    "home":        {"me": "",                    "en": "en/"},
    "teqball":     {"me": "teqball-stolovi/",    "en": "en/teqball-tables/"},
    "panels":      {"me": "interaktivne-table/", "en": "en/interactive-displays/"},
    "playgrounds": {"me": "djecija-igralista/",  "en": "en/playgrounds/"},
    "fitness":     {"me": "outdoor-fitness/",    "en": "en/outdoor-fitness/"},
}
CAT_ORDER = ["teqball", "panels", "playgrounds", "fitness"]

HREFLANG = {"me": "sr-ME", "en": "en"}
HTML_LANG = {"me": "sr-Latn-ME", "en": "en"}
OG_LOCALE = {"me": "sr_ME", "en": "en_GB"}

COMMON = {
    "me": {
        "home": "Početna",
        "home_aria": "5TO9 početna",
        "cta": "Zatražite ponudu",
        "cta_home": "Pokrenite projekat",
        "menu_open": "Otvori meni",
        "menu_close": "Zatvori meni",
        "close": "Zatvori",
        "view": "Pogledaj proizvod →",
        "swipe": "Prevucite za još →",
        "ask": "Zatražite ponudu",
        "address": "Ibrahima Koristovića 11, Podgorica",
        "address_br": "Ibrahima Koristovića 11<br>Podgorica, Crna Gora",
        "foot": "Five to Nine — Podgorica, Crna Gora",
        "email": "Email", "phone": "Telefon", "office": "Kancelarija", "map": "Otvori u Google Maps", "review": "Ostavite recenziju na Google-u", "map_title": "5TO9 na mapi — Ibrahima Koristovića 11, Podgorica",
        "lang_label": "Jezik",
        "contact": "Kontakt",
        "go": "Saznajte više →",
    },
    "en": {
        "home": "Home",
        "home_aria": "5TO9 home",
        "cta": "Request a quote",
        "cta_home": "Start a project",
        "menu_open": "Open menu",
        "menu_close": "Close menu",
        "close": "Close",
        "view": "View product →",
        "swipe": "Swipe for more →",
        "ask": "Ask for a quote",
        "address": "Ibrahima Koristovića 11, Podgorica",
        "address_br": "Ibrahima Koristovića 11<br>Podgorica, Montenegro",
        "foot": "Five to Nine — Podgorica, Montenegro",
        "email": "Email", "phone": "Phone", "office": "Office", "map": "Open in Google Maps", "review": "Leave a Google review", "map_title": "5TO9 on the map — Ibrahima Koristovića 11, Podgorica",
        "lang_label": "Language",
        "contact": "Contact",
        "go": "Learn more →",
    },
}

# category tiles (home "offer" band + cross-links on landing pages)
CATS = {
    "teqball": {
        "img": "tile-teq.webp",
        "me": {"nav": "Teqball stolovi", "title": "Teqball stolovi",
               "text": "Četiri TEQ modela za škole, klubove, hotele i javne prostore.",
               "alt": "TEQ sto pored osvijetljenog sportskog terena"},
        "en": {"nav": "Teqball tables", "title": "Teqball tables",
               "text": "Four TEQ models for schools, clubs, hotels and public spaces.",
               "alt": "TEQ table beside a floodlit sports court"},
    },
    "panels": {
        "img": "tile-panels.webp",
        "me": {"nav": "Interaktivne table", "title": "Interaktivne table",
               "text": "4K table sa montažom, obukom i garancijom od 2 godine.",
               "alt": "Učenici rade na interaktivnoj tabli u učionici"},
        "en": {"nav": "Interactive displays", "title": "Interactive displays",
               "text": "4K panels with installation, training and a 2-year warranty.",
               "alt": "Pupils working at an interactive display in a classroom"},
    },
    "playgrounds": {
        "img": "tile-play.webp",
        "me": {"nav": "Dječija igrališta", "title": "Dječija igrališta",
               "text": "Više od 20 linija opreme, sertifikovane po EN 1176.",
               "alt": "Djeca se igraju na inkluzivnom igralištu"},
        "en": {"nav": "Playgrounds", "title": "Children's playgrounds",
               "text": "More than 20 equipment lines, certified to EN 1176.",
               "alt": "Children playing on an inclusive playground"},
    },
    "fitness": {
        "img": "tile-fitness.webp",
        "me": {"nav": "Outdoor fitness", "title": "Outdoor fitness",
               "text": "StreetBarbell sprave sa tegovima i street workout, EN 16630.",
               "alt": "Red narandžastih sprava za trening snage na otvorenom"},
        "en": {"nav": "Outdoor fitness", "title": "Outdoor fitness",
               "text": "StreetBarbell plate-loaded machines and street workout, EN 16630.",
               "alt": "A row of orange outdoor strength machines"},
    },
}
