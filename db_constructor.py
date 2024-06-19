from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, Column, ForeignKey

import os, glob


# set constructor variable
db_name = "code-preview.db" # create db with name if the name isn't in instance folder
db_add_table = True # set to true to add table to db
db_add_value = True # set to true to add value to table in db


# =================================================================
# if db didn't exist, create one
os.chdir(os.path.dirname(os.path.realpath(__file__)) + "/instance")
db_list:list[str] = [file for file in glob.glob("*.db")]
print("all dbs:", *db_list)

# initializate db
class Base(DeclarativeBase):
    """base model, customize : https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/models/"""
    pass
db = SQLAlchemy(model_class=Base)
app = Flask(__name__)

db_fp = f"sqlite:///{os.path.dirname(os.path.realpath(__file__))}/instance/{db_name}"
app.config["SQLALCHEMY_DATABASE_URI"] = db_fp
db.init_app(app)
print(f"db with name: {db_name} initializated.")
if db_name not in db_list:
    with app.app_context():
        db.create_all()
        print(f"db with name: {db_name} created.")
else:
    print(f"db with name: {db_name} already exist.")
# =================================================================
# create table in db
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
    apd_images: Mapped[str] = mapped_column(String(500))

if db_add_table:
    with app.app_context():
        db.create_all()
    print(f"db with name: {db_name} created with table.")
else:
    print("no table added.")
# =================================================================
# add value to table in db
if db_add_value:
    with app.app_context():
        db_len = len(db.session.execute(db.select(AllProjectDemo).order_by(AllProjectDemo.apd_id)).scalars().all())
        data = AllProjectDemo(
            apd_id = db_len,
            apd_title = "Tic Tac Toe",
            apd_desc = 'Build a text-based version of the Tic Tac Toe game in the command line. It should be a 2-player game, where one person is "X" and the other plays "O".',
            apd_preview = "video",
            apd_videos = "Tic-Tac-Toe-Demo.mov",
            apd_images = "",) # type: ignore
        db.session.add(data)
        db.session.commit()
        print(f"db with name: {db_name} added value.")
else:
    print("no value added.")
# =================================================================