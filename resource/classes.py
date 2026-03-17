"""
Some Python classes used by the server, including classes for database
and a class used to record and store website information.
"""
import json
import os
from pathlib import Path
from typing import Literal

import requests
from flask import request
from sqlalchemy import JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# ---------------------------------------------------------------------
type Languages = Literal["English", "Traditional-Chinese"]
type Desc = dict[Languages, str]
type Items = dict[Languages, list[str]]

PATH = Path("static/assets/json/github-languages.json")
ENCODING = "UTF-8"
ERRMSG = "Environment variable `{var}` don't exist, check `.env` file."
HREF_WEBSITE = "/about/website"
HREF_AUTHOR = "/about/author"
HREF_TOOLS = "/about/tools"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "Content-Type": "application/json",
    "X-GitHub-Api-Version": "2022-11-28",
}

ENDPOINT: str = os.getenv("ENDPOINT") or ""
assert ENDPOINT != "", ERRMSG.format(var="ENDPOINT")


class Base(DeclarativeBase):
    """base model for SQLAlchemy."""


# db table
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


class Current():
    """
    The current state of the website, also used to store some static
    assets and keep track of every important information about the
    website.
    """
    language: Languages = "English"
    endpoint: str = "home"
    title: str = "website"
    path_lang_byte: Path = PATH

    navbar_about: dict[Languages, str] = {
        "English": "About",
        "Traditional-Chinese": "關於"
    }
    navbar_about_dropdown: dict[Languages, dict[str, str]] = {
            "English": {
                "The Website": HREF_WEBSITE,
                "The Author": HREF_AUTHOR,
                "The Tools": HREF_TOOLS,
                },
            "Traditional-Chinese": {
                "網站簡介": HREF_WEBSITE,
                "我": HREF_AUTHOR,
                "使用工具": HREF_TOOLS,
                }
        }
    navbar_contact: dict[Languages, str] = {
        "English": "Contact",
        "Traditional-Chinese": "聯絡方式"
    }

    demo_title: dict[Languages, str] = {
        "English": "Check out a demo of the project",
        "Traditional-Chinese": "在網頁上玩玩看demo吧 (不支援中文)",
    }
    gh_title: dict[Languages, str] = {
        "English": "Check out the source code on Github",
        "Traditional-Chinese": "去GitHub上看看程式吧",
    }

    star_effect_amount: int = 2
    effect_placeholder_former = "<magic-star>"
    effect_placeholder_spliter = "<split>"
    effect_placeholder_latter = "</magic-star>"

    def __init__(self) -> None:
        self.lang_byte = self.get_lang_byte()
        self.lang_percentage = self.get_lang_percentage()

    def switch_language(self) -> None:
        """
        Switch website display language between Traditional Chinese and
        English.
        """
        self.language = (
            "Traditional-Chinese"
            if self.language == "English"
            else "English"
            )

    def switch_endpoint(self) -> None:
        """
        Save the endpoint as class attribute before switching language.

        This needs to be added to each function that switches URLs, but
        this does not include demos.
        """
        if (
            request.endpoint != "switch_language"
            and isinstance(request.endpoint, str)
        ):
            self.endpoint = request.endpoint

    def record_title(self, title: str) -> None:
        """
        Save the website title as class attribute. This is only needed
        for the About page, because it has an additional parameter.

        Parameters
        ----------
        title: str
            The title of the website.
        """
        self.title = title

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
