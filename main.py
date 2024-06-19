from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

import os


# setup flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("APP_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")

print(os.getenv("Test_key"))

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
    apd_preview: Mapped[str] = mapped_column(nullable=False) # enter video or image
    apd_videos: Mapped[str] = mapped_column()
    apd_images: Mapped[str] = mapped_column()

# website routes
@app.route('/')
def home():
    db_data = db.session.execute(db.select(AllProjectDemo)).scalars().all()
    
    results = db.session.execute(db.select(AllProjectDemo).where(AllProjectDemo.apd_preview == 'image')).scalars().all()
    if results != []:
        image_locs:dict[int, list] = {}
        first_loc: dict[int, str] = {}
        # ../static/assets/img/placeholder.jpg
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
        image_nums = 0
    
    print("======================================")
    print("first loc", first_loc)
    print("image locs", image_locs)
    print("image nums", image_nums)
    print("======================================")
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
    return render_template("contact.html", msg_sent=False, page="contact")


def get_from_db():
    
    return



if __name__ == "__main__":

    
    app.run(debug=True, port=5000)