import locale
import smtplib
import sys
from datetime import datetime as dt
from datetime import timedelta as td
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from json import dump, dumps, load
from pathlib import Path
from re import sub

import pypub
import requests
import typer
from bs4 import BeautifulSoup
from crontab import CronTab
from joblib import Parallel, delayed
from rss_parser import RSSParser
from typing_extensions import Annotated

_APP_NAME = Path(__file__).parent.name
print(f"Running {_APP_NAME}")

_config_paths = [
    Path.home() / f".config/{_APP_NAME}/config.json",
    Path().absolute() / "config.json",
]

_allowed_categories = set(
    [
        "HARVARD",
        "Αθλητισμος",
        "Αμυνα",
        "Αποψεις",
        "Αστυνομικο",
        "Ατζεντα",
        "Βιβλιο",
        "Γαστρονομος",
        "Γραφηματα",
        "Διεθνης Οικονομια",
        "Δικαστικο",
        "Εκπαιδευση",
        "Ελληνικη Οικονομια",
        "Εξωτερικη Πολιτικη",
        "Επιστημη",
        "Επιχειρησεις",
        "Ιστορια",
        "Κοινωνια",
        "Κοσμος",
        "Κυβερνηση",
        "Με την «Κ»",
        "Οικονομια",
        "Περιοδικο «Κ»",
        "Πολιτικη",
        "Πολιτισμος",
        "Στηλες",
        "Ταξιδια",
        "Υγεια",
    ]
)


def _process_configs(config_paths, _config_creation=False):
    config = {}
    for cfgp in config_paths:
        try:
            config.update(load(cfgp.open()))
            print(f"Config loaded successfully from '{cfgp}'")
        except FileNotFoundError as _:
            print(f"Config not found in '{cfgp}")
    if (config == {}) and (not _config_creation):
        raise Exception(
            "ERROR: Config has not been properly defined. Please run the 'configure' command.",
        )
    return config


def _save_config(cfg, global_save=True):
    if global_save:
        _config_paths[0].parent.mkdir(parents=True, exist_ok=True)
        with _config_paths[0].open("w") as f:
            dump(cfg, f, indent=4, ensure_ascii=False)
            print(f"Config successfully written in '{_config_paths[0]}'")
    else:
        _config_paths[1].parent.mkdir(parents=True, exist_ok=True)
        with _config_paths[1].open("w") as f:
            dump(cfg, f, indent=4, ensure_ascii=False)
            print(f"Config successfully written in '{_config_paths[1]}'")


def _key_getter(x, categories):
    for idx, cat in enumerate(categories):
        if cat == x["categories"][0]:
            break
    return x["pub_date"] + td(days=idx)


def _get_chapters(sess, item):
    r = sess.get(item["links"][0])
    bs = BeautifulSoup(r.text, "html.parser")
    title = bs.find("h1", {"class": "entry-title"}).text
    article = bs.find("div", id="main-content")
    [div.decompose() for div in article.find_all("div", {"class": "is-hidden"})]
    [div.decompose() for div in article.find_all("div", {"class": "p-inarticle"})]
    [div.decompose() for div in article.find_all("div", {"class": "not-logged"})]
    [
        div.decompose()
        for div in article.find_all("div", {"class": "k-read-more-wrapper"})
    ]
    return pypub.create_chapter_from_text(article.text, title=title)


app = typer.Typer(rich_markup_mode="markdown")


@app.command()
def run():
    config = _process_configs(config_paths=_config_paths)
    values = dict(
        login=config["kathimerini_user"],
        loginType="email",
        password=config["kathimerini_pass"],
        remember=True,
    )

    dt_format = r"%a, %d %b %Y %H:%M:%S %z"
    rss_url = "https://www.kathimerini.gr/infeeds/rss/nx-rss-feed.xml"
    response = requests.get(rss_url)
    response.encoding = response.apparent_encoding

    rss = RSSParser.parse(response.text).dict_plain()["channel"]["items"]
    for it in rss:
        it["pub_date"] = dt.strptime(it["pub_date"], dt_format)

    locale.setlocale(locale.LC_ALL, "el_GR.UTF-8")
    today = dt.strftime(rss[0]["pub_date"], r"%A, %d %B")
    pt = Path(f"kathimerini_{sub(r'\W+', '_', today)}.epub")
    if len(config["news_categories"]) > 0:
        rss = sorted(rss, key=lambda x: _key_getter(x, config["news_categories"]))

    epub = pypub.Epub(f"Kathimerini {today}")
    with requests.Session() as sess:
        sess.post(
            r"https://id.kathimerini.gr/id/api/v1/identity/login/token?aid=FYeCBDdBpe&lang=el_GR",
            data=dumps(values),
            headers={"Content-type": "application/json", "Accept": "application/json"},
        )
        chapters = Parallel(n_jobs=4)(
            delayed(_get_chapters)(sess, item)
            for item in rss
            if "sketches" not in item["links"][0]
        )
        # chapters = [get_chapters(sess, item) for item in rss if 'sketches' not in item['links'][0]]
        for c in chapters:
            epub.add_chapter(c)

    epub.create(pt)

    msg = MIMEMultipart()
    msg["From"] = config["gmail_user"]
    msg["To"] = config["kindle_email"]
    msg["Subject"] = epub.title

    with pt.open("rb") as file:
        part = MIMEApplication(file.read())
    # encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment", filename=pt.name)
    msg.attach(part)
    msg.attach(MIMEText(epub.title))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
        smtp_server.login(config["gmail_user"], config["gmail_pass"])
        smtp_server.sendmail(
            config["gmail_user"], config["kindle_email"], msg.as_string()
        )
    print(
        f"Succesfullu produced '{pt.name}' and sent it to '{config["kindle_email"]}'."
    )
    pt.unlink()


@app.command()
def configure(
    kathimerini_user: str = None,
    kathimerini_pass: str = None,
    gmail_user: str = None,
    gmail_pass: str = None,
    kindle_email: str = None,
    global_save: bool = True,
):
    cfg = _process_configs(config_paths=_config_paths, _config_creation=True)
    cfg.update(
        dict(
            kathimerini_user=kathimerini_user,
            kathimerini_pass=kathimerini_pass,
            gmail_user=gmail_user,
            gmail_pass=gmail_pass,
            kindle_email=kindle_email,
            news_categories=[],
        )
    )
    _save_config(cfg, global_save=global_save)


@app.command()
def news_categories(
    categories: Annotated[list[str], typer.Argument(help="Select categories")],
    global_save: bool = True,
):
    """
    Select a smaller list of news categories. Possible values are:

    * HARVARD

    * Αθλητισμος

    * Αμυνα

    * Αποψεις

    * Αστυνομικο

    * Ατζεντα

    * Βιβλιο

    * Γαστρονομος

    * Γραφηματα

    * Διεθνης Οικονομια

    * Δικαστικο

    * Εκπαιδευση

    * Ελληνικη Οικονομια

    * Εξωτερικη Πολιτικη

    * Επιστημη

    * Επιχειρησεις

    * Ιστορια

    * Κοινωνια

    * Κοσμος

    * Κυβερνηση

    * Με την «Κ»

    * Οικονομια

    * Περιοδικο «Κ»

    * Πολιτικη

    * Πολιτισμος

    * Στηλες

    * Ταξιδια

    * Υγεια
    """

    cfg = _process_configs(config_paths=_config_paths)
    good_categories = []
    for c in categories:
        if c in _allowed_categories:
            good_categories.append(c)
        else:
            print(f"{c} is not a valid category. Ignoring it.")

    cfg.update(
        dict(
            news_categories=[c for c in good_categories],
        )
    )
    _save_config(cfg, global_save=global_save)


@app.command()
def schedule(hour: int = 8, minute: int = 0):
    assert (0 <= hour < 24) and (
        0 <= minute < 60
    ), f"Invalid time: '{hour:02d}:{minute:02d}'"
    with CronTab(user=True) as cron:
        cron.remove_all(command=sys.executable)
        job = cron.new(command=f"{sys.executable} -m kathimeripy run")
        job.hour.on(hour)
        job.minute.on(minute)
    print(f"Set to run every day at: '{hour:02d}:{minute:02d}'")


app()
