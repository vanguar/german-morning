#!/usr/bin/env python3
"""Generate the static German Morning landing pages (uk / ru / de + root picker).

One template, three string tables: the language versions cannot drift apart.
Output is plain HTML committed to the repo; GitHub Pages serves it as-is.

    python tools/build.py
"""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://vanguar.github.io/german-morning/"
BOT = "https://t.me/GermanMorningBot"
BOT_NAME = "@GermanMorningBot"
CONTACT = "https://t.me/ObiVan1978"
CONTACT_NAME = "@ObiVan1978"
FEEDBACK = {"uk": "Зауваження та пропозиції", "ru": "Замечания и предложения", "de": "Feedback und Vorschläge"}
OG_IMAGE = BASE + "assets/img/og-image.png"
ASSET_V = "4"  # bump after changing styles.css / main.js (Pages caches for 10 min)
ORDER = ["uk", "ru", "de"]  # Ukrainian first: default language of the site
NAMES = {"uk": "Українська", "ru": "Русский", "de": "Deutsch"}
CODES = {"uk": "UK", "ru": "RU", "de": "DE"}
OG_LOCALE = {"uk": "uk_UA", "ru": "ru_RU", "de": "de_DE"}
SWITCH_LABEL = {"uk": "Українська версія", "ru": "Русская версия", "de": "Deutsche Version"}

TG_ICON = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" '
           'd="M21.5 3.6 2.9 10.8c-1.3.5-1.2 1.3-.2 1.6l4.7 1.5 1.8 5.6c.2.6.4.8.8.8s.6-.2.9-.5l2.3-2.2 '
           '4.8 3.5c.9.5 1.5.2 1.7-.8L23 4.9c.3-1.3-.5-1.9-1.5-1.3ZM8.6 13.6l9.5-6c.4-.3.9-.1.5.3l-7.8 7'
           '-.3 3.4-1.9-4.7Z"/></svg>')
THEME_ICONS = ('<svg class="sun" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="12" cy="12" '
               'r="4.5" fill="currentColor"/><g stroke="currentColor" stroke-width="2" stroke-linecap="round">'
               '<path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4'
               'M17.7 6.3l1.4-1.4"/></g></svg><svg class="moon" viewBox="0 0 24 24" aria-hidden="true" '
               'focusable="false"><path fill="currentColor" d="M20.5 14.6A8.5 8.5 0 0 1 9.4 3.5a8.5 8.5 0 1 0 '
               '11.1 11.1Z"/></svg>')
# Applied before first paint so a saved theme never flashes.
THEME_BOOT = ('<script>try{var t=localStorage.getItem("gm-theme");if(t==="dark"||t==="light")'
              'document.documentElement.setAttribute("data-theme",t)}catch(e){}</script>')

T = {
    "uk": dict(
        title="German Morning — німецька мова A1–B2 у Telegram",
        desc="German Morning — Telegram-бот та інтерактивний курс німецької мови A1–B2. 68 уроків, слова, вправи, озвучення, диктанти, ігри та книжки.",
        og_desc="Інтерактивний курс німецької від A1 до B2: короткі уроки, слова, вправи, озвучення, диктанти, ігри та книжки — просто в Telegram.",
        og_alt="German Morning — німецька A1–B2 у Telegram",
        app_desc="Telegram-бот та інтерактивний курс німецької мови від A1 до B2: 68 уроків, слова, вправи, озвучення, диктанти, ігри, книжки та новини.",
        skip="До змісту", home_label="German Morning — головна сторінка українською",
        nav_label="Мова сторінки", theme_label="Темна тема", germany="Німеччина",
        eyebrow="A1 → B2 · 68 уроків",
        h1=("German Morning — німецька ", "щодня", " в Telegram"),
        lead="Інтерактивний курс німецької від A1 до B2: короткі уроки, слова, вправи, озвучення, диктанти, ігри та книжки — просто в Telegram.",
        cta="Почати вивчати німецьку", cta2="Переглянути можливості",
        chips=["Безкоштовно", "Без встановлення", "Українська й російська"],
        bot_word="бот",
        mock=("Доброго ранку! Сьогодні — нові слова й коротка вправа.", "ранок", "сніданок",
              ["Слова", "Озвучення", "Диктант"]),
        mock_caption="Декоративна ілюстрація, не знімок екрана курсу",
        stats=[("68", "уроків"), ("A1–B2", "4 рівні"), ("2", "мови інтерфейсу")],
        features_title="Що всередині",
        features_lead="Усе для регулярних занять зібрано в одному місці — у Telegram, який і так завжди під рукою.",
        features=[
            ("🎯", "A1–B2", "Чотири рівні", "Від перших фраз до впевненого середнього рівня."),
            ("📚", "68 уроків", "Короткі заняття", "Урок легко пройти за один підхід — уранці, у дорозі чи ввечері."),
            ("✍️", "", "Слова й вправи", "Нова лексика в кожному уроці та завдання, щоб її закріпити."),
            ("🔊", "", "Озвучення", "Німецькі слова й фрази можна прослухати, щоб звикати до звучання."),
            ("🎧", "", "Диктанти", "Слухаєте й записуєте — тренування сприйняття на слух і правопису."),
            ("🎲", "", "Ігри", "Повторювати слова в ігровому форматі простіше, ніж зубрити списки."),
            ("📖", "", "Книжки", "Тексти німецькою для читання, коли хочеться більше живої мови."),
            ("📰", "", "Новини", "Короткі статті німецькою про свіже: наука, технології, економіка, події."),
        ],
        news_title="Новини німецькою",
        news_lead="Короткі статті німецькою про те, що відбувається у світі. Біля кожної вказано рівень, а читати допомагають підказки до слів, підрядник, переклад і озвучення.",
        rubrics=[("🔭", "Астрономія", "Космос, відкриття та місії"),
                 ("🔬", "Наука", "Дослідження, відкриття і премії"),
                 ("💻", "Технології", "ШІ, інтернет і ґаджети"),
                 ("💹", "Економіка", "Ринки, ціни, робота й гроші"),
                 ("🌍", "Події", "Головне в Німеччині та світі")],
        news_note="Нові статті з’являються регулярно — свіжі позначені окремо.",
        soon="Незабаром", ar_sub="Арабський інтерфейс у розробці",
        how_title="Як це працює",
        steps=[
            ("Відкрийте бота", f'Перейдіть до <a href="{BOT}" rel="noopener">{BOT_NAME}</a> і натисніть «Старт».'),
            ("Оберіть мову", "Українська або російська — нею будуть пояснення, переклади та інтерфейс."),
            ("Займайтеся регулярно", "Проходьте по уроку, повторюйте слова й повертайтеся щодня — потроху."),
        ],
        who_title="Для кого",
        who=[
            ("🌱", "Починаєте з нуля", "Рівень A1 стартує з самих основ — абетки, привітань і перших фраз."),
            ("🚀", "Уже знаєте базу", "Можна продовжити з A2, B1 або B2 і підтягнути те, що встигло забутися."),
            ("☕", "Хочете потроху щодня", "Короткі уроки зручно вбудувати в ранок або будь-яку вільну хвилину."),
        ],
        langs_title="Українська та російська",
        langs_lead="Інтерфейс, пояснення та переклади доступні двома мовами. Оберіть зручну в боті — і змініть будь-коли. Незабаром додасться арабська.",
        lang_here="Ця сторінка", lang_sub={"ru": "Страница на русском", "de": "Seite auf Deutsch"},
        faq_title="Часті запитання",
        faq=[
            ("Що таке German Morning?", "German Morning — це Telegram-бот та інтерактивний курс німецької мови від A1 до B2. Усередині 68 уроків, нові слова, вправи, озвучення, диктанти, ігри та книжки німецькою."),
            ("Чи потрібно встановлювати окремий застосунок?", "Ні. German Morning працює просто в Telegram: достатньо відкрити бота @GermanMorningBot."),
            ("Які рівні доступні?", "Курс охоплює рівні A1, A2, B1 і B2 — загалом 68 уроків. Можна почати з нуля або обрати рівень, який підходить вам зараз."),
            ("Чи є українська мова?", "Так. Інтерфейс, пояснення та переклади доступні українською та російською. Мову обирають у боті, і її можна змінити будь-коли. Арабський інтерфейс у розробці."),
            ("German Morning безкоштовний?", "Основні матеріали доступні безкоштовно. Проєкт можна підтримати добровільно просто в боті."),
            ("Куди писати зауваження та пропозиції?", "Пишіть автору проєкту в Telegram: @ObiVan1978 — https://t.me/ObiVan1978. Будемо раді відгукам та ідеям."),
            ("Де відкрити курс?", "Відкрийте бота @GermanMorningBot у Telegram за посиланням https://t.me/GermanMorningBot і натисніть «Старт»."),
        ],
        final_title="Почніть ранок із німецької",
        final_text="Один короткий урок сьогодні — і німецька стане частиною вашого дня.",
        final_cta="Відкрити German Morning у Telegram",
        sticky="Почати в Telegram",
        foot_label="Посилання в підвалі",
    ),
    "ru": dict(
        title="German Morning — немецкий язык A1–B2 в Telegram",
        desc="German Morning — Telegram-бот и интерактивный курс немецкого языка A1–B2. 68 уроков, слова, упражнения, озвучка, диктанты, игры и книги.",
        og_desc="Интерактивный курс немецкого от A1 до B2: короткие уроки, слова, упражнения, озвучка, диктанты, игры и книги — прямо в Telegram.",
        og_alt="German Morning — немецкий A1–B2 в Telegram",
        app_desc="Telegram-бот и интерактивный курс немецкого языка от A1 до B2: 68 уроков, слова, упражнения, озвучка, диктанты, игры, книги и новости.",
        skip="К содержанию", home_label="German Morning — главная страница на русском",
        nav_label="Язык страницы", theme_label="Тёмная тема", germany="Германия",
        eyebrow="A1 → B2 · 68 уроков",
        h1=("German Morning — немецкий ", "каждый день", " в Telegram"),
        lead="Интерактивный курс немецкого от A1 до B2: короткие уроки, слова, упражнения, озвучка, диктанты, игры и книги — прямо в Telegram.",
        cta="Начать учить немецкий", cta2="Посмотреть возможности",
        chips=["Бесплатно", "Без установки", "Украинский и русский"],
        bot_word="бот",
        mock=("Доброе утро! Сегодня — новые слова и короткое упражнение.", "утро", "завтрак",
              ["Слова", "Озвучка", "Диктант"]),
        mock_caption="Декоративная иллюстрация, не скриншот курса",
        stats=[("68", "уроков"), ("A1–B2", "4 уровня"), ("2", "языка интерфейса")],
        features_title="Что внутри",
        features_lead="Всё для регулярных занятий собрано в одном месте — в Telegram, который и так всегда под рукой.",
        features=[
            ("🎯", "A1–B2", "Четыре уровня", "От первых фраз до уверенного среднего уровня."),
            ("📚", "68 уроков", "Короткие занятия", "Урок легко пройти за один подход — утром, в дороге или вечером."),
            ("✍️", "", "Слова и упражнения", "Новая лексика в каждом уроке и задания, чтобы её закрепить."),
            ("🔊", "", "Озвучка", "Немецкие слова и фразы можно прослушать, чтобы привыкать к звучанию."),
            ("🎧", "", "Диктанты", "Слушаете и записываете — тренировка восприятия на слух и орфографии."),
            ("🎲", "", "Игры", "Повторять слова в игровом формате проще, чем зубрить списки."),
            ("📖", "", "Книги", "Тексты на немецком для чтения, когда захочется больше живого языка."),
            ("📰", "", "Новости", "Короткие статьи на немецком о свежем: наука, технологии, экономика, события."),
        ],
        news_title="Новости на немецком",
        news_lead="Короткие статьи на немецком о том, что происходит в мире. У каждой указан уровень, а читать помогают подсказки к словам, подстрочник, перевод и озвучка.",
        rubrics=[("🔭", "Астрономия", "Космос, открытия и миссии"),
                 ("🔬", "Наука", "Исследования, открытия и премии"),
                 ("💻", "Технологии", "ИИ, интернет и гаджеты"),
                 ("💹", "Экономика", "Рынки, цены, работа и деньги"),
                 ("🌍", "События", "Главное в Германии и мире")],
        news_note="Новые статьи появляются регулярно — свежие отмечены отдельно.",
        soon="Скоро", ar_sub="Арабский интерфейс в разработке",
        how_title="Как это работает",
        steps=[
            ("Откройте бота", f'Перейдите в <a href="{BOT}" rel="noopener">{BOT_NAME}</a> и нажмите «Старт».'),
            ("Выберите язык", 'Русский или <span lang="uk">українська</span> — на нём будут объяснения, переводы и интерфейс.'),
            ("Занимайтесь регулярно", "Проходите по уроку, повторяйте слова и возвращайтесь каждый день — понемногу."),
        ],
        who_title="Для кого",
        who=[
            ("🌱", "Начинаете с нуля", "Уровень A1 стартует с самых основ — алфавита, приветствий и первых фраз."),
            ("🚀", "Уже знаете базу", "Можно продолжить с A2, B1 или B2 и подтянуть то, что успело забыться."),
            ("☕", "Хотите понемногу каждый день", "Короткие уроки удобно встроить в утро или любую свободную минуту."),
        ],
        langs_title='Русский и <span lang="uk">українська</span>',
        langs_lead="Интерфейс, объяснения и переводы доступны на двух языках. Выберите удобный в боте — и смените в любой момент. Скоро добавится арабский.",
        lang_here="Эта страница", lang_sub={"uk": "Сторінка українською", "de": "Seite auf Deutsch"},
        faq_title="Частые вопросы",
        faq=[
            ("Что такое German Morning?", "German Morning — это Telegram-бот и интерактивный курс немецкого языка от A1 до B2. Внутри 68 уроков, новые слова, упражнения, озвучка, диктанты, игры и книги на немецком."),
            ("Нужно ли устанавливать отдельное приложение?", "Нет. German Morning работает прямо в Telegram: достаточно открыть бота @GermanMorningBot."),
            ("Какие уровни доступны?", "Курс охватывает уровни A1, A2, B1 и B2 — всего 68 уроков. Можно начать с нуля или выбрать уровень, который подходит вам сейчас."),
            ("Есть ли украинский язык?", "Да. Интерфейс, объяснения и переводы доступны на русском и на украинском языке. Язык выбирается в боте и его можно сменить в любой момент. Арабский интерфейс в разработке."),
            ("German Morning бесплатный?", "Основные материалы доступны бесплатно. Проект можно поддержать добровольно прямо в боте."),
            ("Куда писать замечания и предложения?", "Пишите автору проекта в Telegram: @ObiVan1978 — https://t.me/ObiVan1978. Будем рады отзывам и идеям."),
            ("Где открыть курс?", "Откройте бота @GermanMorningBot в Telegram по ссылке https://t.me/GermanMorningBot и нажмите «Старт»."),
        ],
        final_title="Начните утро с немецкого",
        final_text="Один короткий урок сегодня — и немецкий станет частью вашего дня.",
        final_cta="Открыть German Morning в Telegram",
        sticky="Начать в Telegram",
        foot_label="Ссылки в подвале",
    ),
    "de": dict(
        title="German Morning — Deutsch A1–B2 in Telegram",
        desc="German Morning — Telegram-Bot und interaktiver Deutschkurs A1–B2 mit ukrainischer und russischer Oberfläche: 68 Lektionen, Wörter, Übungen, Audio, Diktate, Spiele und Bücher.",
        og_desc="Interaktiver Deutschkurs von A1 bis B2: kurze Lektionen, Wörter, Übungen, Audio, Diktate, Spiele und Bücher — direkt in Telegram.",
        og_alt="German Morning — Deutsch A1–B2 in Telegram",
        app_desc="Telegram-Bot und interaktiver Deutschkurs von A1 bis B2 mit ukrainischer und russischer Oberfläche: 68 Lektionen, Wörter, Übungen, Audio, Diktate, Spiele, Bücher und Nachrichten.",
        skip="Zum Inhalt", home_label="German Morning — Startseite auf Deutsch",
        nav_label="Sprache der Seite", theme_label="Dunkles Design", germany="Deutschland",
        eyebrow="A1 → B2 · 68 Lektionen",
        h1=("German Morning — Deutsch ", "jeden Tag", " in Telegram"),
        lead="Interaktiver Deutschkurs von A1 bis B2 für Ukrainisch- und Russischsprachige: kurze Lektionen, Wörter, Übungen, Audio, Diktate, Spiele und Bücher — direkt in Telegram.",
        cta="Jetzt Deutsch lernen", cta2="Funktionen ansehen",
        chips=["Kostenlos", "Ohne Installation", "Ukrainisch & Russisch"],
        bot_word="Bot",
        mock=("Доброго ранку! Сьогодні — нові слова й коротка вправа.", "ранок", "сніданок",
              ["Wörter", "Audio", "Diktat"]),
        mock_caption="Dekorative Illustration, kein Screenshot des Kurses",
        stats=[("68", "Lektionen"), ("A1–B2", "4 Niveaus"), ("2", "Oberflächensprachen")],
        features_title="Was drin ist",
        features_lead="Alles für regelmäßiges Lernen an einem Ort — in Telegram, das ohnehin immer zur Hand ist.",
        features=[
            ("🎯", "A1–B2", "Vier Niveaus", "Von den ersten Sätzen bis zur sicheren Mittelstufe."),
            ("📚", "68 Lektionen", "Kurze Einheiten", "Eine Lektion schafft man in einem Rutsch — morgens, unterwegs oder abends."),
            ("✍️", "", "Wörter & Übungen", "Neuer Wortschatz in jeder Lektion und Aufgaben, um ihn zu festigen."),
            ("🔊", "", "Audio", "Deutsche Wörter und Sätze lassen sich anhören, um sich an den Klang zu gewöhnen."),
            ("🎧", "", "Diktate", "Hören und aufschreiben — Training für Hörverstehen und Rechtschreibung."),
            ("🎲", "", "Spiele", "Wörter spielerisch wiederholen ist leichter, als Listen zu pauken."),
            ("📖", "", "Bücher", "Deutsche Texte zum Lesen, wenn man mehr lebendige Sprache möchte."),
            ("📰", "", "Nachrichten", "Kurze deutsche Artikel über Aktuelles: Wissenschaft, Technik, Wirtschaft, Ereignisse."),
        ],
        news_title="Nachrichten auf Deutsch",
        news_lead="Kurze deutsche Artikel darüber, was in der Welt passiert. Jeder hat eine Niveauangabe, und beim Lesen helfen Worthinweise, Interlinearübersetzung, Übersetzung und Audio.",
        rubrics=[("🔭", "Astronomie", "Weltraum, Entdeckungen und Missionen"),
                 ("🔬", "Wissenschaft", "Forschung, Entdeckungen und Preise"),
                 ("💻", "Technik", "KI, Internet und Gadgets"),
                 ("💹", "Wirtschaft", "Märkte, Preise, Arbeit und Geld"),
                 ("🌍", "Ereignisse", "Das Wichtigste aus Deutschland und der Welt")],
        news_note="Neue Artikel kommen regelmäßig dazu — frische sind eigens markiert.",
        soon="Bald", ar_sub="Arabische Oberfläche in Arbeit",
        how_title="So funktioniert’s",
        steps=[
            ("Bot öffnen", f'Öffnen Sie <a href="{BOT}" rel="noopener">{BOT_NAME}</a> und tippen Sie auf „Start“.'),
            ("Sprache wählen", "Ukrainisch oder Russisch — in dieser Sprache kommen Erklärungen, Übersetzungen und Oberfläche."),
            ("Regelmäßig lernen", "Lektion für Lektion, Wörter wiederholen und jeden Tag ein bisschen dranbleiben."),
        ],
        who_title="Für wen",
        who=[
            ("🌱", "Sie fangen bei null an", "Niveau A1 beginnt mit den Grundlagen — Alphabet, Begrüßungen und ersten Sätzen."),
            ("🚀", "Sie haben schon Grundlagen", "Weiter mit A2, B1 oder B2 und auffrischen, was in Vergessenheit geraten ist."),
            ("☕", "Sie wollen täglich ein bisschen", "Kurze Lektionen passen in den Morgen oder jede freie Minute."),
        ],
        langs_title="Ukrainisch und Russisch",
        langs_lead="Oberfläche, Erklärungen und Übersetzungen gibt es auf Ukrainisch und Russisch. Die Sprache wählt man im Bot und kann sie jederzeit ändern; Arabisch kommt bald dazu. Diese Seite gibt es zusätzlich auf Deutsch — etwa zum Weiterempfehlen.",
        lang_here="Diese Seite", lang_sub={"uk": "Сторінка українською", "ru": "Страница на русском"},
        faq_title="Häufige Fragen",
        faq=[
            ("Was ist German Morning?", "German Morning ist ein Telegram-Bot und interaktiver Deutschkurs von A1 bis B2. Er enthält 68 Lektionen, neue Wörter, Übungen, Audio, Diktate, Spiele und deutsche Bücher."),
            ("Muss ich eine App installieren?", "Nein. German Morning läuft direkt in Telegram: Es genügt, den Bot @GermanMorningBot zu öffnen."),
            ("Welche Niveaus gibt es?", "Der Kurs umfasst die Niveaus A1, A2, B1 und B2 — insgesamt 68 Lektionen. Man kann bei null anfangen oder das passende Niveau wählen."),
            ("In welchen Sprachen ist die Oberfläche?", "Oberfläche, Erklärungen und Übersetzungen gibt es auf Ukrainisch und Russisch. Die Sprache wählt man im Bot und kann sie jederzeit wechseln. Eine arabische Oberfläche ist in Arbeit."),
            ("Ist German Morning kostenlos?", "Die Hauptinhalte sind kostenlos verfügbar. Das Projekt kann man freiwillig direkt im Bot unterstützen."),
            ("Wohin mit Feedback und Vorschlägen?", "Schreiben Sie dem Autor des Projekts in Telegram: @ObiVan1978 — https://t.me/ObiVan1978. Über Rückmeldungen und Ideen freuen wir uns."),
            ("Wo öffne ich den Kurs?", "Öffnen Sie den Bot @GermanMorningBot in Telegram über https://t.me/GermanMorningBot und tippen Sie auf „Start“."),
        ],
        final_title="Starten Sie den Morgen mit Deutsch",
        final_text="Eine kurze Lektion heute — und Deutsch wird Teil Ihres Tages.",
        final_cta="German Morning in Telegram öffnen",
        sticky="In Telegram starten",
        foot_label="Links in der Fußzeile",
    ),
}


def linkify(text):
    """Escape FAQ answer text and turn the bot handle / URL into links."""
    s = escape(text)
    s = s.replace("https://t.me/GermanMorningBot", f'<a href="{BOT}" rel="noopener">t.me/GermanMorningBot</a>')
    s = s.replace(CONTACT, f'<a href="{CONTACT}" rel="noopener">t.me/ObiVan1978</a>')
    s = s.replace(CONTACT_NAME + " ", f'<a href="{CONTACT}" rel="noopener">{CONTACT_NAME}</a> ', 1)
    return s.replace(BOT_NAME, f'<a href="{BOT}" rel="noopener">{BOT_NAME}</a>', 1)


def head(lang, *, title, desc, og_title, og_desc, og_alt, canonical, prefix, ld):
    alts = "".join(f'  <link rel="alternate" hreflang="{l}" href="{BASE}{l}/">\n' for l in ORDER)
    loc_alt = "".join(f'  <meta property="og:locale:alternate" content="{OG_LOCALE[l]}">\n'
                      for l in ORDER if l != lang)
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}">
  <meta name="robots" content="index, follow">
  <meta name="color-scheme" content="light dark">
  <meta name="theme-color" content="#faf7f2" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#0f1620" media="(prefers-color-scheme: dark)">
  {THEME_BOOT}
  <link rel="canonical" href="{canonical}">
{alts}  <link rel="alternate" hreflang="x-default" href="{BASE}">
  <link rel="icon" href="{prefix}assets/img/icon.svg" type="image/svg+xml">
  <link rel="icon" href="{prefix}assets/img/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="{prefix}assets/img/apple-touch-icon.png">
  <link rel="stylesheet" href="{prefix}assets/css/styles.css?v={ASSET_V}">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="German Morning">
  <meta property="og:locale" content="{OG_LOCALE[lang]}">
{loc_alt}  <meta property="og:title" content="{escape(og_title)}">
  <meta property="og:description" content="{escape(og_desc)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{escape(og_alt)}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(og_title)}">
  <meta name="twitter:description" content="{escape(og_desc)}">
  <meta name="twitter:image" content="{OG_IMAGE}">

  <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
  </script>
</head>
"""


def app_ld(desc, url):
    return {
        "@type": "SoftwareApplication",
        "@id": BASE + "#app",
        "name": "German Morning",
        "description": desc,
        "applicationCategory": "EducationalApplication",
        "operatingSystem": "Telegram, Web",
        "url": url,
        "image": OG_IMAGE,
        "inLanguage": ["uk", "ru"],
        "sameAs": [BOT],
    }


def lang_switch(lang, prefix, label):
    items = []
    for l in ORDER:
        if l == lang:
            items.append(f'<li><a href="./" hreflang="{l}" aria-current="page">{CODES[l]}</a></li>')
        else:
            items.append(f'<li><a href="{prefix}{l}/" hreflang="{l}" lang="{l}" '
                         f'aria-label="{CODES[l]} — {SWITCH_LABEL[l]}">{CODES[l]}</a></li>')
    return (f'<nav aria-label="{label}">\n          <ul class="lang-switch">\n'
            + "".join(f"            {i}\n" for i in items) + "          </ul>\n        </nav>")


def footer(lang, prefix, label, feedback=None):
    feedback = feedback or FEEDBACK[lang]
    links = []
    for l in ORDER:
        attrs = f' hreflang="{l}"' + ("" if l == lang else f' lang="{l}"')
        if l == lang:
            href, attrs = ("./" if prefix else f"{l}/"), attrs + (' aria-current="page"' if prefix else "")
        else:
            href = f"{prefix}{l}/"
        links.append(f'<li><a href="{href}"{attrs}>{NAMES[l]}</a></li>')
    links.append(f'<li><a href="{BOT}" rel="noopener">Telegram</a></li>')
    return f"""  <footer class="site-footer">
    <div class="wrap">
      <div class="foot-info">
        <p class="foot-brand"><strong>German Morning</strong> <span class="flag" aria-hidden="true"></span> · <a href="{BOT}" rel="noopener">{BOT_NAME}</a></p>
        <p class="foot-contact">{feedback}: <a href="{CONTACT}" rel="noopener">{CONTACT_NAME}</a></p>
      </div>
      <nav aria-label="{label}">
        <ul class="footer-links">
{"".join(f"          {x}{chr(10)}" for x in links)}        </ul>
      </nav>
    </div>
  </footer>
  <div class="tricolor" aria-hidden="true"></div>
"""


def page(lang):
    t = T[lang]
    p = "../"
    url = f"{BASE}{lang}/"
    ld = {"@context": "https://schema.org", "@graph": [
        app_ld(t["app_desc"], url),
        {"@type": "FAQPage", "inLanguage": lang, "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in t["faq"]]},
    ]}
    out = head(lang, title=t["title"], desc=t["desc"], og_title=t["title"], og_desc=t["og_desc"],
               og_alt=t["og_alt"], canonical=url, prefix=p, ld=ld)
    h1a, h1b, h1c = t["h1"]
    mock_tr, w1, w2, mock_chips = t["mock"]
    chips = "".join(f"<li>{escape(c)}</li>" for c in t["chips"])
    stats = "".join(f'<li><b>{escape(n)}</b><span>{escape(s)}</span></li>' for n, s in t["stats"])
    feats = "".join(
        f'          <li class="card"><span class="ico ico-{i % 8}" aria-hidden="true">{ico}</span>'
        + (f'<span class="big">{escape(big)}</span>' if big else "")
        + f"<h3>{escape(h)}</h3><p>{escape(d)}</p></li>\n"
        for i, (ico, big, h, d) in enumerate(t["features"]))
    rubrics = "".join(
        f'          <li class="rubric"><span class="rubric-ico" aria-hidden="true">{ico}</span>'
        f"<span><b>{escape(h)}</b><small>{escape(d)}</small></span></li>\n"
        for ico, h, d in t["rubrics"])
    steps = "".join(f"          <li><h3>{escape(h)}</h3><p>{d}</p></li>\n" for h, d in t["steps"])
    who = "".join(f'          <li><span class="who-ico" aria-hidden="true">{ico}</span><h3>{escape(h)}</h3>'
                  f"<p>{escape(d)}</p></li>\n" for ico, h, d in t["who"])
    lang_cards = []
    for l in ["uk", "ru"] + ([lang] if lang == "de" else []):
        if l == lang:
            lang_cards.append(f'          <a class="lang-card is-current" href="./" hreflang="{l}" aria-current="page">'
                              f'<span class="code">{CODES[l]}</span><strong>{NAMES[l]}</strong>'
                              f'<span class="sub">{t["lang_here"]}</span></a>\n')
        else:
            lang_cards.append(f'          <a class="lang-card" href="{p}{l}/" hreflang="{l}" lang="{l}">'
                              f'<span class="code">{CODES[l]}</span><strong>{NAMES[l]}</strong>'
                              f'<span class="sub">{t["lang_sub"][l]}</span></a>\n')
    lang_cards.append(f'          <div class="lang-card is-soon" aria-disabled="true"><span class="code">AR</span>'
                      f'<strong lang="ar" dir="rtl">العربية</strong>'
                      f'<span class="sub"><span class="soon-badge">{t["soon"]}</span> {t["ar_sub"]}</span></div>\n')
    faq = "".join(f"""          <details>
            <summary>{escape(q)}</summary>
            <div class="answer"><p>{linkify(a)}</p></div>
          </details>
""" for q, a in t["faq"])
    mchips = "".join(f"<span>{escape(c)}</span>" for c in mock_chips)
    mock_lang = ' lang="uk"' if lang == "de" else ""
    out += f"""<body class="has-sticky">
  <a class="skip-link" href="#main">{t["skip"]}</a>

  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="./" aria-label="{t["home_label"]}">
        <img src="{p}assets/img/icon.svg" alt="" width="36" height="36">
        <span>German Morning</span>
      </a>
      <div class="header-tools">
        {lang_switch(lang, p, t["nav_label"])}
        <button class="theme-toggle" type="button" aria-label="{t["theme_label"]}" aria-pressed="false">{THEME_ICONS}</button>
      </div>
    </div>
  </header>

  <main id="main">
    <section class="hero" aria-labelledby="hero-title">
      <div class="wrap">
        <div class="hero-copy">
          <p class="eyebrow"><span class="flag" role="img" aria-label="{t["germany"]}"></span> {escape(t["eyebrow"])}</p>
          <h1 id="hero-title">{escape(h1a)}<span class="hl">{escape(h1b)}</span>{escape(h1c)}</h1>
          <p class="lead">{escape(t["lead"])}</p>
          <div class="btn-row">
            <a class="btn btn-primary" id="hero-cta" href="{BOT}" rel="noopener">{TG_ICON}{escape(t["cta"])}</a>
            <a class="btn btn-ghost" href="#features">{escape(t["cta2"])}</a>
          </div>
          <ul class="trust">{chips}</ul>
        </div>

        <div class="mockup">
          <div class="phone" aria-hidden="true">
            <div class="phone-screen">
              <div class="phone-bar">
                <span class="dot"></span>
                <span><b>German Morning</b><small>{t["bot_word"]}</small></span>
              </div>
              <div class="chat">
                <div class="bubble"><span class="de" lang="de">Guten Morgen! ☀️</span><br><span class="tr"{mock_lang}>{escape(mock_tr)}</span></div>
                <div class="bubble"><span class="de" lang="de">der Morgen</span> — <span{mock_lang}>{w1}</span><br><span class="de" lang="de">das Frühstück</span> — <span{mock_lang}>{w2}</span>
                  <div class="chips">{mchips}</div>
                </div>
                <div class="bubble me" lang="de">Ich trinke Kaffee ☕</div>
                <div class="bubble"><span class="de" lang="de">Sehr gut!</span> 👏</div>
              </div>
            </div>
          </div>
          <span class="sticker sticker-a" aria-hidden="true">A1 → B2</span>
          <span class="sticker sticker-b" aria-hidden="true">🔊 🎧 🎲</span>
          <p class="mockup-caption">{t["mock_caption"]}</p>
        </div>
      </div>
      <div class="wrap">
        <ul class="stats">{stats}</ul>
      </div>
    </section>

    <section class="section section-alt" id="features" aria-labelledby="features-title">
      <div class="wrap">
        <div class="section-head">
          <h2 id="features-title">{t["features_title"]}</h2>
          <p>{escape(t["features_lead"])}</p>
        </div>
        <ul class="cards">
{feats}        </ul>
      </div>
    </section>

    <section class="section" id="news" aria-labelledby="news-title">
      <div class="wrap">
        <div class="section-head">
          <h2 id="news-title">{t["news_title"]}</h2>
          <p>{escape(t["news_lead"])}</p>
        </div>
        <ul class="rubrics">
{rubrics}        </ul>
        <p class="news-note">{escape(t["news_note"])}</p>
      </div>
    </section>

    <section class="section section-alt" aria-labelledby="how-title">
      <div class="wrap">
        <div class="section-head">
          <h2 id="how-title">{t["how_title"]}</h2>
        </div>
        <ol class="steps">
{steps}        </ol>
      </div>
    </section>

    <section class="section" aria-labelledby="who-title">
      <div class="wrap">
        <div class="section-head">
          <h2 id="who-title">{t["who_title"]}</h2>
        </div>
        <ul class="audience">
{who}        </ul>
      </div>
    </section>

    <section class="section section-alt" aria-labelledby="langs-title">
      <div class="wrap">
        <div class="section-head">
          <h2 id="langs-title">{t["langs_title"]}</h2>
          <p>{escape(t["langs_lead"])}</p>
        </div>
        <div class="langs">
{"".join(lang_cards)}        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="faq-title">
      <div class="wrap">
        <div class="section-head">
          <h2 id="faq-title">{t["faq_title"]}</h2>
        </div>
        <div class="faq">
{faq}        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="final-title">
      <div class="wrap">
        <div class="final">
          <h2 id="final-title">{escape(t["final_title"])}</h2>
          <p>{escape(t["final_text"])}</p>
          <div class="btn-row">
            <a class="btn btn-primary" id="final-cta" href="{BOT}" rel="noopener">{TG_ICON}{escape(t["final_cta"])}</a>
          </div>
        </div>
      </div>
    </section>
  </main>

{footer(lang, p, t["foot_label"])}
  <div class="sticky-cta" id="sticky-cta">
    <a class="btn btn-primary" href="{BOT}" rel="noopener">{TG_ICON}{escape(t["sticky"])}</a>
  </div>
  <script src="{p}assets/js/main.js?v={ASSET_V}" defer></script>
</body>
</html>
"""
    return out


def root_page():
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": BASE + "#website", "name": "German Morning", "url": BASE,
         "inLanguage": ["uk", "ru", "de"]},
        app_ld(T["uk"]["app_desc"], BASE),
    ]}
    out = head("uk",
               title="German Morning — німецька A1–B2 у Telegram · немецкий · Deutsch",
               desc="German Morning — Telegram-бот і курс німецької A1–B2: 68 уроків, слова, вправи, озвучення, диктанти, ігри та книжки. Курс немецкого в Telegram · Deutschkurs in Telegram.",
               og_title="German Morning — німецька A1–B2 у Telegram",
               og_desc="Інтерактивний курс німецької A1–B2 у Telegram · Интерактивный курс немецкого в Telegram · Interaktiver Deutschkurs in Telegram.",
               og_alt=T["uk"]["og_alt"], canonical=BASE, prefix="", ld=ld)
    choices = "".join(
        f'<a class="btn {"btn-primary is-suggested" if l == "uk" else "btn-ghost"}" href="{l}/" '
        f'hreflang="{l}" lang="{l}" data-lang="{l}"><span class="code">{CODES[l]}</span>{NAMES[l]}</a>\n          '
        for l in ORDER)
    out += f"""<body class="is-root">
  <header class="site-header site-header-plain">
    <div class="wrap">
      <span class="brand"><img src="assets/img/icon.svg" alt="" width="36" height="36"><span>German Morning</span></span>
      <div class="header-tools">
        <button class="theme-toggle" type="button" aria-label="Темна тема · Тёмная тема · Dunkles Design" aria-pressed="false">{THEME_ICONS}</button>
      </div>
    </div>
  </header>

  <main id="main" class="picker">
    <div class="wrap">
      <img class="picker-logo" src="assets/img/icon.svg" alt="German Morning" width="96" height="96">
      <h1>German Morning <span class="flag flag-lg" role="img" aria-label="Німеччина"></span></h1>
      <p class="lead">
        <span>Німецька від A1 до B2 просто в Telegram: 68 коротких уроків, слова, вправи, озвучення, диктанти, ігри, книжки та новини.</span>
        <span lang="ru">Немецкий от A1 до B2 прямо в Telegram: 68 коротких уроков, слова, упражнения, озвучка, диктанты, игры, книги и новости.</span>
        <span lang="de">Deutsch von A1 bis B2 direkt in Telegram — mit ukrainischer und russischer Oberfläche.</span>
      </p>

      <nav aria-label="Оберіть мову · Выберите язык · Sprache wählen">
        <div class="picker-choices three">
          {choices}</div>
      </nav>
      <p class="suggest" id="suggest" aria-live="polite"></p>

      <div class="btn-row picker-tg">
        <a class="btn btn-tg" href="{BOT}" rel="noopener">{TG_ICON}Відкрити {BOT_NAME}</a>
      </div>
      <p class="hero-note">Інтерфейс українською та російською · <span lang="ru">Интерфейс на украинском и русском</span></p>
    </div>
  </main>

{footer("uk", "", "Посилання · Ссылки · Links", "Зауваження та пропозиції · <span lang='ru'>Замечания и предложения</span>")}  <script src="assets/js/main.js?v={ASSET_V}" defer></script>
</body>
</html>
"""
    return out


def main():
    for lang in ORDER:
        d = ROOT / lang
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(page(lang), encoding="utf-8", newline="\n")
    (ROOT / "index.html").write_text(root_page(), encoding="utf-8", newline="\n")
    print("built:", ", ".join(["index.html"] + [f"{l}/index.html" for l in ORDER]))


if __name__ == "__main__":
    main()
