"""
Some Python classes used by the server, including classes for database
and a class used to record and store website information.
"""
import json
import os
from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from functools import lru_cache, wraps
from pathlib import Path
from typing import Any, Literal, TypeAlias, cast, get_args

import requests
from flask import Response, make_response, request
from sqlalchemy import JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from werkzeug.datastructures.accept import LanguageAccept
from werkzeug.wrappers.response import Response as RedirectResponse

# ---------------------------------------------------------------------
ColorScheme: TypeAlias = Literal["light", "dark", "auto", "TBD"]
Languages: TypeAlias = Literal["English", "Traditional-Chinese"]
Desc: TypeAlias = dict[Languages, str]
Items: TypeAlias = dict[Languages, list[str]]
CookieKeys: TypeAlias = Literal["setting", "language", "endpoint", "scheme"]
BannerDesc: TypeAlias = Literal[CookieKeys, "accept", "reject"]

AllowedTitles: TypeAlias = Literal["website", "author", "tools"]
RouteRetVal: TypeAlias = tuple[str | RedirectResponse, Languages, ColorScheme]

PATH = Path("static/assets/json/github-languages.json")
ENCODING = "UTF-8"
ERRMSG = "Environment variable `{var}` don't exist, check `.env` file."
HREF_HOME = ""
HREF_WEBSITE = "/about/website"
HREF_AUTHOR = "/about/author"
HREF_TOOLS = "/about/tools"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "Content-Type": "application/json",
    "X-GitHub-Api-Version": "2022-11-28",
}
COOKIE_SETTING: CookieKeys = "setting"
COOKIE_LANG: CookieKeys = "language"
COOKIE_PATH: CookieKeys = "endpoint"
COOKIE_SCHEME: CookieKeys = "scheme"
COOKIE_NAMES: list[CookieKeys] = [COOKIE_LANG, COOKIE_PATH, COOKIE_SCHEME]
COOKIE_MAX_DAY = 14
COOKIE_MAX_SEC = COOKIE_MAX_DAY * 24 * 60 * 60
LANGUAGE_ZH: Languages = "Traditional-Chinese"
LANGUAGE_EN: Languages = "English"

ENDPOINT: str = os.getenv("ENDPOINT") or ""
assert ENDPOINT != "", ERRMSG.format(var="ENDPOINT")


class Base(DeclarativeBase):
    """base model for SQLAlchemy."""


# db tables
class Project(Base):
    """The structure of a table in the database."""
    __tablename__ = "Project"
    info_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[Desc] = mapped_column(JSON, nullable=False)
    keywords: Mapped[Items] = mapped_column(JSON, nullable=False)

    # value hint (preview_type): 'video', 'image', 'both', or none
    preview_type: Mapped[str] = mapped_column(nullable=False)
    preview_video: Mapped[str] = mapped_column(nullable=True)
    preview_image: Mapped[str] = mapped_column(nullable=True)

    # value (is_demo): True or False
    is_demo: Mapped[str] = mapped_column(nullable=False)

    # value (demo_ep): endpoint for demo, use at index.html
    demo_ep: Mapped[str] = mapped_column(nullable=True)
    gh_link: Mapped[str] = mapped_column(nullable=False)
    gh_date: Mapped[str] = mapped_column(nullable=False)


class AboutText(Base):
    """The structure of a table in the database."""
    __tablename__ = "AboutText"
    info_id: Mapped[int] = mapped_column(primary_key=True)
    info_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    title: Mapped[Desc] = mapped_column(JSON, nullable=False)
    description: Mapped[Desc] = mapped_column(JSON, nullable=False)
    paragraphs: Mapped[Items] = mapped_column(JSON, nullable=False)


class AboutImage(Base):
    """The structure of a table in the database."""
    __tablename__ = "AboutImage"
    info_id: Mapped[int] = mapped_column(primary_key=True)
    info_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    fname: Mapped[str] = mapped_column(nullable=False, unique=True)
    attribute: Mapped[str] = mapped_column(nullable=False, unique=True)


class ContactText(Base):
    """The structure of a table in the database."""
    __tablename__ = "ContactText"
    info_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[Desc] = mapped_column(JSON, nullable=False)
    description: Mapped[Desc] = mapped_column(JSON, nullable=False)
    form_name: Mapped[Desc] = mapped_column(JSON, nullable=False)
    form_mail: Mapped[Desc] = mapped_column(JSON, nullable=False)
    form_msg: Mapped[Desc] = mapped_column(JSON, nullable=False)
    form_sent: Mapped[Desc] = mapped_column(JSON, nullable=False)


# tracking class
class Current():
    """
    The current state of the website, also used to store some static
    assets and keep track of some information about the website.
    """
    path_lang_byte: Path = PATH

    navbar_about: dict[Languages, str] = {
        LANGUAGE_EN: "About",
        LANGUAGE_ZH: "關於"
    }
    navbar_about_dropdown: dict[Languages, dict[str, str]] = {
            LANGUAGE_EN: {
                "The Website": HREF_WEBSITE,
                "The Author": HREF_AUTHOR,
                "The Tools": HREF_TOOLS,
                },
            LANGUAGE_ZH: {
                "網站簡介": HREF_WEBSITE,
                "我": HREF_AUTHOR,
                "使用工具": HREF_TOOLS,
                }
        }
    navbar_contact: dict[Languages, str] = {
        LANGUAGE_EN: "Contact",
        LANGUAGE_ZH: "聯絡方式"
    }
    navbar_switch: dict[Languages, str] = {
        LANGUAGE_EN: "Switch display language to Traditional Chinese",
        LANGUAGE_ZH: "變更顯示語言為英文\nSwitch display language to English",
    }

    cookie_banner_description: dict[BannerDesc, dict[Languages, str]] = {
        COOKIE_SETTING: {
            LANGUAGE_EN: (
                "TODO: add this"
                ),
            LANGUAGE_ZH: (
                "TODO: add this"
                )
        },
        COOKIE_LANG: {
            LANGUAGE_EN: (
                "This setting allows you to switch languages."
                "\nWithout it, you will not be able to switch languages."
                ),
            LANGUAGE_ZH: (
                "同意這項設定以切換語言，拒絕此設定則無法切換語言。"
                )
        },
        COOKIE_PATH: {
            LANGUAGE_EN: (
                "This setting allows you to return to the webpage previously "
                "browsing after switching languages.\nWithout it, you will be "
                "redirected to the website homepage after switching languages."
                ),
            LANGUAGE_ZH: (
                "同意這項設定以在切換語言後返回之前瀏覽的網頁，\n"
                "拒絕此設定則會在切換語言後回到網站首頁。"
                )
        },
        COOKIE_SCHEME: {
            LANGUAGE_EN: (
                "This setting allows you to maintain the selected theme after "
                "navigating to different webpages or switching languages."
                "\nWithout it, the theme set by the browser will be used."
                ),
            LANGUAGE_ZH: (
                "同意這項設定以在瀏覽不同網頁時或切換語言後維持設定的顯示模式，\n"
                "拒絕此設定則會顯示瀏覽器設定的顯示模式。"
                )
        },
        "accept": {
            LANGUAGE_EN: (
                "TODO: add this"
                ),
            LANGUAGE_ZH: (
                "TODO: add this"
                )
        },
        "reject": {
            LANGUAGE_EN: (
                "TODO: add this"
                ),
            LANGUAGE_ZH: (
                "TODO: add this"
                )
        },
    }

    demo_title: dict[Languages, str] = {
        LANGUAGE_EN: "Check out a demo of the project",
        LANGUAGE_ZH: "在網頁上玩玩看demo吧 (不支援中文)",
    }
    gh_title: dict[Languages, str] = {
        LANGUAGE_EN: "Check out the source code on Github",
        LANGUAGE_ZH: "去GitHub上看看程式吧",
    }

    star_effect_amount: int = 2
    effect_placeholder_former = "<magic-star>"
    effect_placeholder_spliter = "<split>"
    effect_placeholder_latter = "</magic-star>"

    def __init__(self) -> None:
        self.lang_byte = self.get_lang_byte()
        self.lang_percentage = self.get_lang_percentage()
        self.lang_style = self.get_lang_style()

    def update_lang_byte(self) -> None:
        """
        Fetch the number of each language in bytes of code from this
        repository on GitHub, and store the value as Python dict to a
        JSON file.
        """
        response = requests.get(
            ENDPOINT, headers=HEADERS, timeout=10
            )
        response.raise_for_status()
        lang_byte = json.loads(response.text)
        with open(self.path_lang_byte, mode="w", encoding=ENCODING) as file:
            json.dump(lang_byte, file)

    def get_lang_byte(self) -> dict[str, int]:
        """
        Returns a previously stored number of each language in bytes of
        code from this repository on GitHub.

        Returns
        -------
        dict[str, int]
            A JSON structured Python dict, contain key-value pair with
            programming langugage as key and number of bytes of code.
            With value like ``{"HTML":31078,"Python":29948,...}``.
        """
        with open(self.path_lang_byte, encoding=ENCODING) as file:
            return json.load(file)

    def get_lang_percentage(self) -> dict[str, float]:
        """
        Convert JSON string to dictionary. The main purpose is convert
        the number bytes of code for each language (on GitHub
        repository) into their respective percentages.

        Returns
        -------
        dict[str, float]
            Languages and their bytes of code percentages. With value
            like: ``{'HTML': 36.7, 'Python': 35.2, ...}``.
        """
        lang_byte = self.lang_byte
        max_percentage = 100  # 100 or 1 (reprsent: 100% or 1/1)
        round_decimal = 1  # 1 or 3

        total_bytes = sum(lang_byte.values())
        lang_percentage = {
            lang: round((max_percentage * byte) / total_bytes, round_decimal)
            for lang, byte in lang_byte.items()
            }

        total_percentage = sum(lang_percentage.values())
        if total_percentage != max_percentage:
            max_var = max(lang_byte, key=lang_byte.get)  # type: ignore
            missing = max_percentage - total_percentage
            lang_percentage[max_var] = round(
                (lang_percentage[max_var] + missing), round_decimal
                )

        return lang_percentage

    def get_lang_style(self) -> dict[str, str]:
        """
        Format the number of language percentages to be a HTML style
        tag.

        Returns
        -------
        dict[str, str]
            Languages and their bytes of code percentages formatted as a
            HTML style tag. With value like:
            ``{'HTML': 'style="width: 36.7%;"', ...}``.
        """
        return {
            lang: f'style="width: {percent}%;"'
            for lang, percent in self.lang_percentage.items()
        }


@lru_cache
def is_lang_allowed(language: Languages) -> bool:
    """
    Check if the language is allowed (in the Languages type).

    Parameters
    ----------
    language: Languages
        The name of the language to check.

    Returns
    -------
    bool
        If the language is allowed.
    """
    return language in get_args(Languages)


def prefers_chinese(language_accept: LanguageAccept) -> bool:
    """
    If the `Accept-Language` in the request header includes Chinese.

    Parameters
    ----------
    language_accept: LanguageAccept
        Language codes from `Accept-Language` in the request header,
        takes ``request.accept_languages``.

    Returns
    -------
    bool
        If Chinese is in ``accept_languages``.

    Notes
    -----
    The check logic `> 0` is used because the ``find()`` method returns
    `1` when the finding language has the highest priority, and `-1`
    when the language is not in the list.
    """
    return language_accept.find("zh-TW") > 0 or language_accept.find("zh") > 0


def handle_lang_pref(*, switch: bool = False) -> Languages:
    """
    A helper function for Flask route function that determines the
    preferred language.

    The language set in the cookie takes precedence, followed by the
    language in `Accept-Language` from the request header. The
    determined language is also stored in ``flask.session``.

    Parameters
    ----------
    switch: bool, by default False
        Whether to switch the determined language between Traditional
        Chinese and English.

    Returns
    -------
    Languages
        The determined language.

    Notes
    -----
    If `Accept-Language` includes Chinese, then it is considered
    preferred and will be selected.
    """
    language = cast(Languages, request.cookies.get(COOKIE_LANG))
    if is_lang_allowed(language):
        pref = language
    else:
        if prefers_chinese(request.accept_languages):
            pref = LANGUAGE_ZH
        else:
            pref = LANGUAGE_EN
    if switch:
        pref = LANGUAGE_ZH if pref == LANGUAGE_EN else LANGUAGE_EN
    return pref


@lru_cache
def is_scheme_allowed(scheme: ColorScheme) -> bool:
    """
    Check if the color scheme is allowed (in the ColorScheme type).

    Parameters
    ----------
    scheme: ColorScheme
        The name of the scheme to check.

    Returns
    -------
    bool
        If the scheme is allowed.
    """
    return scheme in get_args(ColorScheme)


def get_scheme() -> ColorScheme:
    """
    A helper function for Flask route function that determines the
    color scheme set by the user, defaults to `TBD` (to be determined).
    This allows JavaScript to resolve the scheme using the
    `prefers-color-scheme` CSS media feature.

    Returns
    -------
    ColorScheme
        The validated color scheme or `TBD`.
    """
    scheme = cast(ColorScheme, request.cookies.get(COOKIE_SCHEME))
    scheme = scheme if is_scheme_allowed(scheme) else "TBD"
    return scheme


def set_cookies(func: Callable[..., RouteRetVal]) -> Callable[..., Response]:
    """
    A decorator to set user preferences in cookies for the Flask route
    function.

    Parameters
    ----------
    func: Callable[..., RouteRetVal]
        A Flask route function to be wrapped.

    Returns
    -------
    Callable[..., Response]
        A wrapped function containing the Flask route function and
        statements to set cookies.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Response:
        body, language, scheme = func(*args, **kwargs)
        expires = datetime.now(timezone.utc) + timedelta(days=COOKIE_MAX_DAY)

        response = make_response(body)

        exist_setting = request.cookies.get(COOKIE_SETTING)
        if exist_setting and exist_setting != "null":
            setting = json.loads(exist_setting)

            value = {
                COOKIE_PATH: request.path,
                COOKIE_LANG: language,
                COOKIE_SCHEME: scheme
            }
            for rule in setting:
                cookie_id = cast(CookieKeys, rule.get("id"))
                if rule.get("checked") and cookie_id in COOKIE_NAMES:
                    response.set_cookie(
                        cookie_id, value[cookie_id],
                        max_age=COOKIE_MAX_SEC, expires=expires
                    )
        else:
            # set to ``None`` to trigger cookie banner for new users
            # this becomes ``"null"``
            response.set_cookie(
                COOKIE_SETTING, json.dumps(None),
                max_age=COOKIE_MAX_SEC, expires=expires
                )
        return response
    return wrapper
