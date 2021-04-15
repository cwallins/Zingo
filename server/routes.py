from flask import Flask, redirect, url_for, render_template, request
from os import listdir, path, remove, rename
import codecs
import db_zingo

#create_game, home_page, join_game, log_out, my_profile, register_sign_in, view_all_games, view_one_game

# 2021-04-15:
#    routes: register och my_profile, eventuellt create_game och log_out  

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

    username = request.form["username"] #ska vara unikt
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    email = request.form["email"]
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]

    if password1 != password2:
        error_message = "The passwords must be the same"
    else:
        db_zingo.execute_procedure(f"sp_add_user '{email}' '{password2}' '{username}' '{surname}' '{lastname}'")

    return redirect(url_for("my_profile"))

def list_of_games():
    all_games = db_zingo.view_views("*", "vw_qp_with_nick")

    for i in all_games:
        print(", ".join(i))
    
    #sorterings algroitmer för name asc/desc, rating asc/desc, most played, asc/desc

def view_question_package(selected_qp):
    #qp: name, description, creator
    #items
    qp_name = db_zingo.read_from_db("question_package", "qp_name", f"where qp_name = '{selected_qp}'")
    print(qp_name)
    qp_description = db_zingo.read_from_db("question_package", "qp_description", f"where qp_name = '{selected_qp}'")
    print(qp_description)
    qp_creator = db_zingo.read_from_db("vw_qp_with_nick", "nickname", f"where qp_name = '{selected_qp}'")
    print(qp_creator)
    
    #listor
    qp_tags = db_zingo.read_from_db("vw_question_package_with_tag", "tag", f"where question_package = '{selected_qp}'")
    print(qp_tags)
    '''qp_rating = db_zingo.read_from_db("vw_qp_rating", "rating", f"where question_package = '{selected_qp}'")
    print(qp_rating)'''
    qp_questions = db_zingo.execute_procedure(f"sp_get_questions '{selected_qp}'") #fixa en view för enbart frågor.
    print(qp_questions)
    #1. hämta data från db
    #2. spara lista med data från db
    #3. sortera lista i python
    #4. skicka lista till html

list_of_games()
view_question_package('Blandade sportfrågor')