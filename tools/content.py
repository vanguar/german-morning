"""Indexable content for the landing: course programme and news articles.

The bot shows lessons and news inside a Telegram Mini App, which search engines
cannot read. Here the same material becomes plain HTML: the 68 lesson topics and
every news article (German text paragraph by paragraph with a translation).

News text lives in the sibling repo deutsch-meister. `sync_news()` copies what the
pages need into data/news.json, so the landing still builds without that repo.
"""
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# sibling checkout (optional); CI checks the bot repo out elsewhere and sets DEUTSCH_MEISTER_DIR
APP = Path(os.environ.get("DEUTSCH_MEISTER_DIR") or ROOT.parent / "deutsch-meister").resolve()
APP_URL = "https://vanguar.github.io/deutsch-meister/"
NEWS_JSON = ROOT / "data" / "news.json"
NEWS_LANGS = ["uk", "ru"]                       # translations that exist for news
BOOKS_JSON = ROOT / "data" / "books.json"
BOOK_LANGS = ["uk", "ru"]                       # translations that exist for books

# (German title, Russian, Ukrainian) — topics as they appear in the course
PROGRAM = {
    "A1": [
        ("Hallo! Wie heißt du?", "Приветствие и знакомство", "Привітання та знайомство"),
        ("Eins, zwei, drei!", "Числа и счёт", "Числа й лічба"),
        ("Welche Farbe ist das?", "Цвета", "Кольори"),
        ("Meine Familie", "Моя семья", "Моя родина"),
        ("Welcher Tag ist heute?", "Дни недели", "Дні тижня"),
        ("Was möchten Sie trinken?", "Напитки и заказ", "Напої та замовлення"),
        ("Wo ist die Haltestelle?", "Ориентирование в городе", "Орієнтування в місті"),
        ("Wie spät ist es?", "Который час", "Котра година"),
        ("Der Körper", "Тело", "Тіло"),
        ("Monate und Jahreszeiten", "Месяцы и времена года", "Місяці та пори року"),
        ("Tiere", "Животные", "Тварини"),
        ("Berufe", "Профессии", "Професії"),
        ("Im Supermarkt", "В супермаркете", "У супермаркеті"),
        ("Verkehrsmittel", "Транспорт", "Транспорт"),
        ("Im Café", "В кафе", "У кав’ярні"),
        ("Zahlen bis 100", "Числа до 100", "Числа до 100"),
        ("Modalverben", "Модальные глаголы", "Модальні дієслова"),
        ("Perfekt", "Прошедшее время Perfekt", "Минулий час Perfekt"),
        ("Feste und Geburtstage", "Праздники и дни рождения", "Свята та дні народження"),
        ("Wiederholung A1", "Повторение A1", "Повторення A1"),
    ],
    "A2": [
        ("Mein Tagesablauf", "Мой распорядок дня", "Мій розпорядок дня"),
        ("Hobbys und Freizeit", "Хобби и свободное время", "Хобі та дозвілля"),
        ("Beim Arzt", "У врача", "У лікаря"),
        ("Reisen", "Путешествия", "Подорожі"),
        ("Einkaufen und Kleidung", "Покупки и одежда", "Покупки та одяг"),
        ("Wohnen und Möbel", "Жильё и мебель", "Житло та меблі"),
        ("Beruf und Arbeit", "Профессия и работа", "Професія та робота"),
        ("Das Wetter", "Погода", "Погода"),
        ("Im Restaurant", "В ресторане", "У ресторані"),
        ("Feste und Traditionen", "Праздники и традиции", "Свята та традиції"),
        ("Medien und Handy", "Медиа и телефон", "Медіа та телефон"),
        ("Gefühle und Stimmungen", "Чувства и настроение", "Почуття та настрій"),
        ("Sport und Fitness", "Спорт и фитнес", "Спорт і фітнес"),
        ("Wegbeschreibung", "Как объяснить дорогу", "Як пояснити дорогу"),
        ("Freundschaft und Beziehungen", "Дружба и отношения", "Дружба та стосунки"),
        ("Natur und Ausflüge", "Природа и поездки", "Природа та мандрівки"),
        ("Präteritum: war & hatte", "Претерит: war и hatte", "Претерит: war і hatte"),
        ("Komparativ und Superlativ", "Сравнительная и превосходная степень", "Вищий і найвищий ступінь"),
        ("Zukunftspläne", "Планы на будущее", "Плани на майбутнє"),
        ("Wiederholung A2", "Повторение A2", "Повторення A2"),
    ],
    "B1": [
        ("Konjunktiv II", "Сослагательное наклонение", "Умовний спосіб"),
        ("Das Passiv", "Пассив", "Пасив"),
        ("Relativsätze", "Относительные придаточные", "Означальні підрядні речення"),
        ("Nebensätze", "Придаточные предложения", "Підрядні речення"),
        ("Infinitivkonstruktionen", "Инфинитивные конструкции", "Інфінітивні конструкції"),
        ("Beruf und Bewerbung", "Работа и отклик на вакансию", "Робота та відгук на вакансію"),
        ("Meinungen ausdrücken", "Как выражать мнение", "Як висловлювати думку"),
        ("Umwelt und Natur", "Экология и природа", "Довкілля та природа"),
        ("Adjektivdeklination", "Склонение прилагательных", "Відмінювання прикметників"),
        ("Genitiv und Präpositionen", "Генитив и предлоги", "Родовий відмінок і прийменники"),
        ("Temporale Nebensätze", "Придаточные времени", "Підрядні речення часу"),
        ("Verben mit Präpositionen", "Глаголы с предлогами", "Дієслова з прийменниками"),
        ("Medien und Nachrichten", "СМИ и новости", "ЗМІ та новини"),
        ("Wiederholung B1", "Повторение B1", "Повторення B1"),
    ],
    "B2": [
        ("Partizipialkonstruktionen", "Причастные обороты", "Дієприкметникові звороти"),
        ("Modalpartikeln", "Модальные частицы", "Модальні частки"),
        ("Konnektoren", "Связки и союзы", "Сполучні слова"),
        ("Nominalisierung", "Номинализация", "Номіналізація"),
        ("Wissenschaftlicher Stil", "Научный стиль", "Науковий стиль"),
        ("Wirtschaft und Gesellschaft", "Экономика и общество", "Економіка та суспільство"),
        ("Debatte und Argumentation", "Дебаты и аргументация", "Дебати та аргументація"),
        ("Komplexe Texte", "Сложные тексты", "Складні тексти"),
        ("Subjektive Modalverben", "Субъективные модальные глаголы", "Суб’єктивні модальні дієслова"),
        ("Nomen-Verb-Verbindungen", "Устойчивые сочетания с глаголом", "Сталі сполучення з дієсловом"),
        ("Redewendungen und Idiome", "Фразеологизмы и идиомы", "Фразеологізми та ідіоми"),
        ("Berufliche Kommunikation", "Деловое общение", "Ділове спілкування"),
        ("Politik und Medien", "Политика и СМИ", "Політика та ЗМІ"),
        ("Wiederholung B2", "Повторение B2", "Повторення B2"),
    ],
}
PROGRAM_LEVEL_NOTE = {
    "uk": {"A1": "з нуля", "A2": "базовий", "B1": "середній", "B2": "вище середнього"},
    "ru": {"A1": "с нуля", "A2": "базовый", "B1": "средний", "B2": "выше среднего"},
    "de": {"A1": "Einstieg", "A2": "Grundstufe", "B1": "Mittelstufe", "B2": "obere Mittelstufe"},
}

RUBRIC_NAMES = {
    "uk": {"astronomy": "Астрономія", "science": "Наука", "tech": "Технології",
           "economy": "Економіка", "events": "Події"},
    "ru": {"astronomy": "Астрономия", "science": "Наука", "tech": "Технологии",
           "economy": "Экономика", "events": "События"},
}


def _read(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _article(meta, chapter):
    """Only what a page needs: no glossary indices."""
    paras = []
    for p in chapter["paragraphs"]:
        if "fig" in p:
            f = p["fig"]
            paras.append({"fig": {"src": APP_URL + f["src"], "w": f["w"], "h": f["h"],
                                  "cap": f["cap"], "credit": f["credit"]}})
        else:
            paras.append({"s": [{"de": s["de"], "tr": s["ru"]} for s in p["s"]]})
    return {"title": meta["title"], "titleTr": meta["titleRu"], "blurb": meta["blurb"],
            "levelNote": meta["levelNote"], "license": meta["license"], "paragraphs": paras}


def sync_news():
    """Refresh data/news.json from ../deutsch-meister when that checkout exists."""
    index = APP / "data" / "news" / "index.json"
    if not index.is_file():
        return False
    items = []
    for it in _read(index)["items"]:
        aid = it["id"]
        meta = _read(APP / "data" / "news" / aid / "meta.json")
        item = {k: meta[k] for k in ("id", "rubric", "level", "published", "added", "source",
                                    "sourceUrl", "words", "minutes")}
        item["cover"] = APP_URL + meta["cover"]
        item["ru"] = _article(meta, _read(APP / "data" / "news" / aid / "ch-01.json"))
        uk_dir = APP / "i18n" / "uk" / "news" / aid
        if (uk_dir / "meta.json").is_file():
            item["uk"] = _article(_read(uk_dir / "meta.json"), _read(uk_dir / "ch-01.json"))
        items.append(item)
    NEWS_JSON.parent.mkdir(exist_ok=True)
    NEWS_JSON.write_text(json.dumps({"items": items}, ensure_ascii=False, indent=1) + "\n",
                         encoding="utf-8", newline="\n")
    return True


def _book(card, meta, chapters):
    """One language of a book: every chapter, German line by line with a translation."""
    return {"titleTr": meta["titleRu"], "blurb": card["blurb"], "levelNote": meta["levelNote"],
            "source": meta["source"],
            "chapters": [{"title": ch["title"], "titleTr": ch["titleRu"],
                          "paragraphs": [[{"de": s["de"], "tr": s["ru"]} for s in p["s"]]
                                         for p in ch["paragraphs"]]}
                         for ch in chapters]}


def sync_books():
    """Refresh data/books.json from ../deutsch-meister when that checkout exists."""
    index = APP / "data" / "books" / "index.json"
    if not index.is_file():
        return False
    uk_index = APP / "i18n" / "uk" / "books" / "index.json"
    uk_cards = {b["id"]: b for b in _read(uk_index)["books"]} if uk_index.is_file() else {}
    items = []
    for card in _read(index)["books"]:
        bid = card["id"]
        src = APP / "data" / "books" / bid
        meta = _read(src / "meta.json")
        n = meta["chapters"]
        item = {k: meta[k] for k in ("id", "title", "author", "level", "year", "chapters", "words",
                                    "minutes", "cover", "sourceUrl", "license")}
        item["verse"] = bool(meta.get("verse"))
        item["ru"] = _book(card, meta, [_read(src / f"ch-{i:02d}.json") for i in range(1, n + 1)])
        uk = APP / "i18n" / "uk" / "books" / bid
        if bid in uk_cards and all((uk / f).is_file() for f in
                                   ["meta.json"] + [f"ch-{i:02d}.json" for i in range(1, n + 1)]):
            item["uk"] = _book(uk_cards[bid], _read(uk / "meta.json"),
                               [_read(uk / f"ch-{i:02d}.json") for i in range(1, n + 1)])
        items.append(item)
    BOOKS_JSON.parent.mkdir(exist_ok=True)
    BOOKS_JSON.write_text(json.dumps({"items": items}, ensure_ascii=False, indent=1) + "\n",
                          encoding="utf-8", newline="\n")
    return True


def load_books():
    if not BOOKS_JSON.is_file():
        return []
    return _read(BOOKS_JSON)["items"]


def load_news():
    if not NEWS_JSON.is_file():
        return []
    items = _read(NEWS_JSON)["items"]
    return sorted(items, key=lambda it: (it["added"], it["published"]), reverse=True)
