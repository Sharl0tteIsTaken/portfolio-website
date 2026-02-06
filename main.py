"""
The source code of the server.
"""

import os
import smtplib
from typing import Literal

from flask import Flask, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap5  # type: ignore[import-untyped, note]
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from demo_morse_code_converter.converter import Converter
from demo_tic_tac_toe.showmaker_demo import ShowMaker

# ---------------------------------------------------------------------

type LanguageCode = Literal["Eng", "ZhTw"]

LANGUAGES: list[LanguageCode] = ["Eng", "ZhTw"]
MAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
MAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
APP_KEY = os.getenv("APP_SECRET_KEY")
SQL_DB_URI = os.getenv("SQL_DB_URI")

assert isinstance(MAIL_ADDRESS, str), f"Environment variable {MAIL_ADDRESS=}"
assert isinstance(MAIL_PASSWORD, str), f"Environment variable {MAIL_PASSWORD=}"
assert isinstance(APP_KEY, str), f"Environment variable {APP_KEY=}"
assert isinstance(SQL_DB_URI, str), f"Environment variable {SQL_DB_URI=}"


class Base(DeclarativeBase):
    """Base model for SQLAlchemy."""


# setup flask
app = Flask(__name__)
app.config['SECRET_KEY'] = APP_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = SQL_DB_URI
db = SQLAlchemy(model_class=Base)


# db table
class Project(Base):  # type: ignore[name-defined]
    """
    Subclass db.Model to define a model class.
    The model will generate a table name by converting the CamelCase
    class name to snake_case.
    """
    __tablename__ = "Project"
    info_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    desc_eng: Mapped[str] = mapped_column(nullable=False)
    desc_zhtw: Mapped[str] = mapped_column(nullable=False)
    keyword_eng: Mapped[list] = mapped_column(JSON, nullable=False)
    keyword_zhtw: Mapped[list] = mapped_column(JSON, nullable=False)

    # value hint (preview_type): video, image, both, or none
    preview_type: Mapped[str] = mapped_column(nullable=True)
    preview_video: Mapped[str] = mapped_column(nullable=True)
    preview_image: Mapped[str] = mapped_column(nullable=True)

    # value (is_demo): True or False
    is_demo: Mapped[str] = mapped_column(nullable=False)

    # value (demo_ep): endpoint for demo, use at index.html
    demo_ep: Mapped[str] = mapped_column(nullable=True)
    gh_link: Mapped[str] = mapped_column(nullable=False)
    gh_date: Mapped[str] = mapped_column(nullable=False)


class Current():
    language: LanguageCode = "Eng"
    endpoint: str = "home"

    def switch_language(self):
        self.language = "Eng" if self.language == "ZhTw" else "ZhTw"

    def switch_endpoint(self):
        if request.endpoint != "switch_language":
            self.endpoint = request.endpoint  # pyright: ignore


# website routes
@app.route('/')
def home() -> str:
    """The home page of website."""
    db_data = db.session.execute(db.select(Project)).scalars().all()
    results = db.session.execute(
        db.select(Project).where(Project.preview_type == 'image')
        ).scalars().all()
    if results != []:
        image_locs: dict[int, list] = {}
        first_loc: dict[int, str] = {}
        for project in results:
            locations = project.preview_image.split(", ")
            image_loc = []
            for loc in locations:
                image_loc.append(loc)
            first_loc[project.info_id] = image_loc[0]
            del image_loc[0]
            image_locs[project.info_id] = image_loc
        image_nums = range(len(image_locs))
    else:
        first_loc = {}
        image_locs = {}
        image_nums = range(0)
    return render_template(
        "index.html",
        # pylint: disable-next=possibly-used-before-assignment
        language=current.language,
        db_data=db_data,
        first_loc=first_loc,
        image_locs=image_locs,
        image_nums=image_nums,
        page="home"
        )


@app.route("/about")
def about():
    """The about page of website."""
    current.switch_endpoint()
    return render_template(
        "about.html",
        language=current.language,
        page="about")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """The contact page of website."""
    current.switch_endpoint()
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template(
        "contact.html",
        language=current.language,
        msg_sent=False,
        page="contact"
        )


@app.route("/switch-language")
def switch_language():
    current.switch_endpoint()
    current.switch_language()
    return redirect(url_for(
        current.endpoint  # pyright: ignore[reportArgumentType]
        ))


@app.route("/gate/tic-tac-toe")
def gate_tic_tac_toe():
    """
    The page to redirect to tic tac toe demo.
    This also resets the demo.
    """
    # pylint: disable-next=possibly-used-before-assignment
    dk_showmaker.initiate()
    dk_showmaker.new_game()
    return redirect(url_for('demo_tic_tac_toe'))


@app.route("/demo/tic-tac-toe", methods=['GET', 'POST'])
def demo_tic_tac_toe():
    """The page with tic tac toe demo."""
    if request.method == "POST":
        enter = request.form.get('user_input')
        dk_showmaker.player_input(
            user_input=enter  # type: ignore[reportArgumentType]
            )
    result = dk_showmaker.output
    pwd = dk_showmaker.pwd
    history = dk_showmaker.history
    is_winner = str(dk_showmaker.iswinner)
    player = int(dk_showmaker.current_player) + 1
    return render_template(
        'demo-tic_tac_toe.html',
        terminal_lines=result,
        pwd=pwd,
        history=history,
        is_winner=is_winner,
        player=player
        )


@app.route('/demo/tic-tac-toe/input-receive')
def demo_tic_tac_toe_input_receive():
    """The page to receive user input on tic tac toe demo."""
    result = dk_showmaker.output
    pwd = dk_showmaker.pwd
    history = dk_showmaker.history
    is_winner = str(dk_showmaker.iswinner)
    player = int(dk_showmaker.current_player) + 1
    return render_template(
        'demo-cz_terminal-tic_tac_toe.html',
        terminal_lines=result,
        pwd=pwd, history=history,
        is_winner=is_winner,
        player=player
        )  # cz stands for customized


@app.route("/gate/morse-code-converter")
def gate_morse_code_converter():
    """
    The page to redirect to morse code converter demo.
    This also resets the demo.
    """
    converter.history = ""  # pylint: disable=possibly-used-before-assignment
    return redirect(url_for('demo_morse_code_converter'))


@app.route('/demo/morse-code-converter', methods=['GET', 'POST'])
def demo_morse_code_converter():
    """The page with morse code converter demo."""
    if request.method == "POST":
        enter = request.form.get('user_input')
        converter.history += enter + "\n"  # type: ignore[reportArgumentType]
        converter.history += converter.convert(
            user_input=enter  # type: ignore[reportArgumentType]
            ) + "\n"
    return render_template(
        'demo-morse_code_converter.html',
        terminal_lines=converter.history,
        )


@app.route('/demo/morse-code-converter/input-recieve')
def demo_morse_code_converter_input_receive():
    """The page to receive user input on morse code converter demo."""
    return render_template(
        'demo-cz_terminal-morse_code_converter.html',
        terminal_lines=converter.history,
        )  # cz stands for customized


# other functions
def send_email(name: str, email: str, message: str) -> None:
    """
    Use my email address to send emails to myself, so there is no need
    to valid user input on this.

    Parameters
    ----------
    name: str
        The name of the user who sent the email.
    email: str
        The email address of the user who sent the email.
    message: str
        The message as the email body.
    """
    email_message = (
        f"Subject:Message from site.\n\n{message}"
        f"\n\nby {name}.\nEmail: {email}"
    )
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(
            user=MAIL_ADDRESS, password=MAIL_PASSWORD  # type: ignore
            )
        connection.sendmail(
            from_addr=MAIL_ADDRESS, to_addrs=MAIL_ADDRESS,  # type: ignore
            msg=email_message
            )


if __name__ == "__main__":
    # init db & bootstrap
    db.init_app(app)
    Bootstrap5(app)

    dk_showmaker = ShowMaker()
    dk_showmaker.new_game()
    converter = Converter()
    current = Current()
    app.run(debug=True, port=5000)
