from typing import Literal

from flask import request
from sqlalchemy import JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


type Languages = Literal["English", "Traditional-Chinese"]
type Desc = dict[Languages, str]
type Items = dict[Languages, list[str]]

HREF_WEBSITE = "/about/website"
HREF_AUTHOR = "/about/author"


class Base(DeclarativeBase):  # pylint: disable=[too-few-public-methods]
    """base model for SQLAlchemy."""


# db table
class Project(Base):  # pylint: disable=[too-few-public-methods]
    """
    Subclass db.Model to define a model class.
    The model will generate a table name by converting the CamelCase
    class name to snake_case.
    """
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
    __tablename__ = "AboutText"
    info_id: Mapped[int] = mapped_column(primary_key=True)
    info_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    title: Mapped[Desc] = mapped_column(JSON, nullable=False)
    description: Mapped[Desc] = mapped_column(JSON, nullable=False)
    paragraphs: Mapped[Items] = mapped_column(JSON, nullable=False)


class ContactText(Base):
    __tablename__ = "ContactText"
    info_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[Desc] = mapped_column(JSON, nullable=False)
    description: Mapped[Desc] = mapped_column(JSON, nullable=False)
    form_name: Mapped[Desc] = mapped_column(JSON, nullable=False)
    form_mail: Mapped[Desc] = mapped_column(JSON, nullable=False)
    form_msg: Mapped[Desc] = mapped_column(JSON, nullable=False)
    form_sent: Mapped[Desc] = mapped_column(JSON, nullable=False)


class Current():
    language: Languages = "English"
    endpoint: str = "home"
    title: str = "website"

    navbar_about: dict[Languages, str] = {
        "English": "About",
        "Traditional-Chinese": "關於"
    }
    navbar_about_dropdown: dict[Languages, dict[str, str]] = {
            "English": {
                "The website": HREF_WEBSITE,
                "Sharl0tteIsTaken": HREF_AUTHOR,
                },
            "Traditional-Chinese": {
                "網站簡介": HREF_WEBSITE,
                "我": HREF_AUTHOR,
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
        "Traditional-Chinese": "去GitHub上看看程式碼",
    }

    star_effect_amount: int = 2
    effect_placeholder_former = "<magic-star>"
    effect_placeholder_spliter = "<split>"
    effect_placeholder_latter = "</magic-star>"

    def __init__(self) -> None:
        self.lang_byte = self.get_lang_byte()
        self.lang_ratio = self.get_lang_ratio()

    def switch_language(self):
        self.language = (
            "Traditional-Chinese"
            if self.language == "English"
            else "English"
            )

    def switch_endpoint(self):
        if request.endpoint != "switch_language":
            self.endpoint = request.endpoint  # pyright: ignore

    def record_title(self, title: str):
        self.title = title

    def get_lang_byte(self) -> str:
        """
        Get the number of each language in bytes of code from this
        repository on GitHub.

        Returns
        -------
        str
            A Json string, contain key-value pair with programming
            langugage as key and number of bytes of code. With value
            like ``{"HTML":31078,"Python":29948,...}``.
        """
        import requests
        SCHEME = "https://api.github.com"
        ENDPOINT = "/repos/Sharl0tteIsTaken/portfolio-website/languages"
        URL = SCHEME + ENDPOINT

        HEADERS = {
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        response = requests.get(URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text

    def get_lang_ratio(self) -> dict[str, float]:
        """
        Convert Json string to dictionary. The main purpose is convert
        the number bytes of code for each language (on GitHub
        repository) into their respective ratios.

        Returns
        -------
        dict[str, float]
            Languages and their bytes of code ratios. With value like:
            ``{'HTML': 0.367, 'Python': 0.352, ...}``.
        """
        import json
        languages: dict[str, int] = json.loads(self.lang_byte)
        total_bytes = sum(languages.values())
        ratio = {
            lang: round(bytes/total_bytes, 3)
            for lang, bytes in languages.items()
            }

        total_amount = sum(ratio.values())
        if total_amount != 1:
            missing = round(1 - total_amount, 3)
            max_var = max(ratio, key=ratio.get)  # type: ignore
            ratio[max_var] = ratio[max_var] + missing
        return ratio
