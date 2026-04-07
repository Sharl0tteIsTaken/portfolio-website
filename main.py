"""
The source code of the server.
"""
import os
import smtplib
from resource.classes import (
    COOKIE_PATH, HREF_HOME, AboutImage, AboutText, AllowedTitles, Base,
    ContactText, Current, Project, RouteRetVal, handle_lang_pref, set_cookies
    )

from flask import Flask, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap5  # type: ignore[import-untyped, note]
from flask_sqlalchemy import SQLAlchemy
from waitress import serve
from werkzeug.wrappers.response import Response

from demo_morse_code_converter.converter import Converter
from demo_tic_tac_toe.showmaker_demo import ShowMaker

# ---------------------------------------------------------------------

MAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
MAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
APP_KEY = os.getenv("APP_SECRET_KEY")
SQL_DB_URI = os.getenv("SQL_DB_URI")

assert isinstance(MAIL_ADDRESS, str), f"Environment variable {MAIL_ADDRESS=}"
assert isinstance(MAIL_PASSWORD, str), f"Environment variable {MAIL_PASSWORD=}"
assert isinstance(APP_KEY, str), f"Environment variable {APP_KEY=}"
assert isinstance(SQL_DB_URI, str), f"Environment variable {SQL_DB_URI=}"

# setup flask
app = Flask(__name__)
app.config['SECRET_KEY'] = APP_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = SQL_DB_URI
db = SQLAlchemy(model_class=Base)


# website routes
@app.route('/')
@set_cookies
def home() -> RouteRetVal:
    """The home page of website."""
    project_data = db.session.execute(db.select(Project)).scalars().all()
    language = handle_lang_pref()
    body = render_template(
        "index.html",
        current=current,
        language=language,
        project_data=project_data,
        page="home"
        )
    return body, language


@app.route("/about/<title>")
@set_cookies
def about(title: AllowedTitles) -> RouteRetVal:
    """The about page of website."""
    static_data = db.session.execute(
        db.select(AboutText).where(AboutText.info_name == title)
        ).scalar()

    tags_whole = render_template("magic-star.html", current=current)
    tags_former, tags_latter = tags_whole.split(
        current.effect_placeholder_spliter
        )
    effect = {
        current.effect_placeholder_former: tags_former,
        current.effect_placeholder_latter: tags_latter,
    }

    background = db.session.execute(
        db.select(AboutImage).where(AboutImage.info_name == title)
        ).scalar()

    language = handle_lang_pref()
    body = render_template(
        "about.html",
        current=current,
        language=language,
        title=title,
        static_data=static_data,
        background=background,
        effect=effect,
        page="about"
        )
    return body, language


@app.route("/contact", methods=["GET", "POST"])
@set_cookies
def contact() -> RouteRetVal:
    """The contact page of website."""
    static_data = db.session.execute(db.select(ContactText)).scalar()
    language = handle_lang_pref()
    msg_sent = False
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["message"])
        msg_sent = True
    body = render_template(
        "contact.html",
        current=current,
        language=language,
        static_data=static_data,
        msg_sent=msg_sent,
        page="contact"
        )
    return body, language


@app.route("/switch-language")
@set_cookies
def switch_language() -> RouteRetVal:
    """
    Switch website display language between Traditional Chinese and
    English.
    """
    language = handle_lang_pref(switch=True)
    endpoint = request.cookies.get(COOKIE_PATH, default=HREF_HOME).lstrip("/")
    endpoint = "home" if endpoint == "" else endpoint
    if endpoint.startswith("about"):
        endpoint, title = endpoint.split("/", maxsplit=1)
        body = redirect(url_for(endpoint, title=title))
    else:
        body = redirect(url_for(endpoint))
    return body, language


@app.route("/gate/tic-tac-toe")
def gate_tic_tac_toe() -> Response:
    """
    The page to redirect to tic tac toe demo.
    This also resets the demo.
    """
    dk_showmaker.initiate()
    dk_showmaker.new_game()
    return redirect(url_for('demo_tic_tac_toe'))


@app.route("/demo/tic-tac-toe", methods=['GET', 'POST'])
def demo_tic_tac_toe() -> str:
    """The page with tic tac toe demo."""
    if request.method == "POST":
        enter = request.form.get('user_input') or ""
        dk_showmaker.player_input(
            user_input=enter
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
def demo_tic_tac_toe_input_receive() -> str:
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
def gate_morse_code_converter() -> Response:
    """
    The page to redirect to morse code converter demo.
    This also resets the demo.
    """
    converter.history = ""
    return redirect(url_for('demo_morse_code_converter'))


@app.route('/demo/morse-code-converter', methods=['GET', 'POST'])
def demo_morse_code_converter() -> str:
    """The page with morse code converter demo."""
    if request.method == "POST":
        enter = request.form.get('user_input') or ""
        converter.history += enter + "\n"
        converter.history += converter.convert(
            user_input=enter
            ) + "\n"
    return render_template(
        'demo-morse_code_converter.html',
        terminal_lines=converter.history,
        )


@app.route('/demo/morse-code-converter/input-recieve')
def demo_morse_code_converter_input_receive() -> str:
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


# init db & bootstrap
db.init_app(app)
Bootstrap5(app)

dk_showmaker = ShowMaker()
dk_showmaker.new_game()
converter = Converter()
current = Current()

if __name__ == "__main__":
    # local
    current.update_lang_byte()
    app.run(debug=True, port=5000)
else:
    # on Render
    assert os.path.exists(current.path_lang_byte), (
        "GitHub language percentages file not exist,"
        "do ``current.update_lang_byte()`` to create one."
    )
    serve(app, port=10000, host="0.0.0.0")
