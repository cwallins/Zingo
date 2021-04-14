from flask import Flask, redirect, url_for, render_template, request
from os import listdir, path, remove, rename
import codecs
import db_zingo
'''
#create_game, home_page, join_game, log_out, my_profile, register_sign_in, view_all_games, view_one_game

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home_page.html")

@app.route('/register')
def register():
    return render_template("register_sign_in.html")

@app.route('/my_profile')
def my_profile():
    return render_template("my_profile.html")
    #Ska vi skicka med skapade frågepaket, userinfo, tidigare spelade frågepaket, (vänner)

@app.route('/create_game')
def create_game():
    return render_template("create_game.html")

@app.route('/log_out')
def log_out():
    return render_template("log_out.html")

@app.route('/join_game')
def join_game():
    return render_template("join_game.html")

@app.route('/view_all_games')
def view_all_games():
    return render_template("view_all_games.html")

@app.route('/view_one_game')
def view_one_game():
    return render_template("view_one_game.html")

#funktion för att hämta alla frågepaket från db

#route för formulär, get/post vid registrering, logga in
@app.route('/add_new_user', methods=["GET", "POST"])
def add_new_user():

    username = request.form["Username"] #ska vara unikt
    password1 = request.form["Password1"]
    password2 = request.form["Password2"]
    email = request.form["Email"]
    surname = request.form["Surname"]
    lastname = request.form["Lastname"]

    if password1 != password2:
        error_message = "The passwords must be the same"
    else:
        db_zingo.execute_procedure(f"sp_add_user '{email}' '{password2}' '{username}' '{surname}' '{lastname}'")

    return redirect(url_for("my_profile"))
'''
def list_of_games():
    all_games = db_zingo.view_views("*", "vw_qp_with_nick")

    for i in all_games:
        print(", ".join(i))

def view_question_package(selected_qp):
    #qp: name, description, creator
    qp_name = selected_qp
    qp_description = db_zingo.read_from_db("question_package", "qp_description", f"where qp_name = {qp_name}")
    qp_creator = db_zingo.read_from_db("nickname", "vw_qp_with_nick", f"where qp_name = {qp_name}")
    qp_tags = db_zingo.read_from_db("tag", "vw_question_package_with_tag", f"where question_package = {qp_name}")
    qp_rating = db_zingo.read_from_db("rating", "vw_qp_rating", f"where question_package = {qp_name}")
    qp_questions = db_zingo.execute_procedure(f"sp_get_questions '{qp_name}'")

    print(qp_name, qp_description, qp_creator, qp_tags, qp_rating, qp_questions)

view_question_package("Blandade sportfrågor")