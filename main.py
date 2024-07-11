from flask import Flask, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

import os, smtplib

from demos.showmaker_demo import ShowMaker
# TODO: [last] check import orders
# TODO: [last] delete unused image in static/assects



# setup from environmental variables
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

# setup flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("APP_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")

# setup db
class Base(DeclarativeBase):
  pass
db = SQLAlchemy(model_class=Base)

# init db & bootstrap
db.init_app(app)
Bootstrap5(app)

# db table
class AllProjectDemo(db.Model):
    '''
    Subclass db.Model to define a model class.
    The model will generate a table name by converting the CamelCase class name to snake_case.
    '''
    apd_id: Mapped[int] = mapped_column(primary_key=True)
    apd_title: Mapped[str] = mapped_column(nullable=False, unique=True)
    apd_desc: Mapped[str] = mapped_column(nullable=False)
    apd_preview: Mapped[str] = mapped_column(nullable=False) # enter video, image or both
    apd_videos: Mapped[str] = mapped_column()
    apd_images: Mapped[str] = mapped_column()
    apd_is_demo: Mapped[str] = mapped_column(nullable=False) # enter true or false
    apd_demo_ep: Mapped[str] = mapped_column() # enter endpoint for demo, use at index.html
    apd_github_link: Mapped[str] = mapped_column(nullable=False)

# website routes
@app.route('/')
def home():
    db_data = db.session.execute(db.select(AllProjectDemo)).scalars().all()
    results = db.session.execute(db.select(AllProjectDemo).where(AllProjectDemo.apd_preview == 'image')).scalars().all()
    if results != []:
        image_locs:dict[int, list] = {}
        first_loc: dict[int, str] = {}
        for project in results:
            locations = project.apd_images.split(", ")
            image_loc = []
            for loc in locations:
                image_loc.append(loc)
            first_loc[project.apd_id] = image_loc[0] # type: ignore
            del image_loc[0]
            image_locs[project.apd_id] = image_loc
        image_nums = range(len(image_locs))
    else:
        first_loc = {}
        image_locs = {}
        image_nums = 0
    return render_template(
        "index.html",
        db_data=db_data,
        first_loc=first_loc,
        image_locs=image_locs,
        image_nums=image_nums,
        page="home"
        )

@app.route("/about")
def about():
    return render_template("about.html", page="about")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False, page="contact")

@app.route("/gate/tic-tac-toe")
def gate_tic_tac_toe():
    dk_showmaker.__init__()
    dk_showmaker.new_game()
    return redirect(url_for('demo_tic_tac_toe'))

@app.route("/demo/tic-tac-toe", methods=['GET','POST'])
def demo_tic_tac_toe():
    if request.method == "POST":
        enter = request.form.get('user_input')
        dk_showmaker.player_input(user_input=enter) # type: ignore
    result = dk_showmaker.output
    pwd = dk_showmaker.pwd
    history = dk_showmaker.history
    is_winner = str(dk_showmaker._iswinner)
    player = int(dk_showmaker._current_player) + 1
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
    result = dk_showmaker.output
    pwd = dk_showmaker.pwd
    history = dk_showmaker.history
    is_winner = str(dk_showmaker._iswinner)
    player = int(dk_showmaker._current_player) + 1
    return render_template(
        'demo-cz_terminal.html',
        terminal_lines=result,
        pwd=pwd, history=history,
        is_winner=is_winner,
        player=player
        ) # cz stands for customized

# other functions
def send_email(name, email, message):
    email_message = f"Subject:Message from site.\n\n{message}\n\nby {name}.\nEmail: {email}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=EMAIL_ADDRESS, password=EMAIL_PASSWORD) # type: ignore
        connection.sendmail(from_addr=EMAIL_ADDRESS, to_addrs=EMAIL_ADDRESS, msg=email_message) # type: ignore


if __name__ == "__main__":
    dk_showmaker = ShowMaker()
    dk_showmaker.new_game()
    app.run(debug=True, port=5000)