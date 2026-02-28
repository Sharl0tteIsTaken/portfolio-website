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
    title: str = "Website"

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
