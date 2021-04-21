from flask import Flask, redirect, url_for, render_template, request, session
from os import listdir, path, remove, rename
import codecs
import pyodbc

#create_game, home_page, join_game, log_out, my_profile, register_sign_in, view_all_games, view_one_game
# 2021-04-15:
#    routes: register, kunna logga in och my_profile, eventuellt create_game och log_out  !!engelska? CE

app = Flask(__name__)
app.secret_key = 'zingo'

''' DATABSE '''

server_host = "localhost"
database_name = "Zingo_DB"

try:
    conn = pyodbc.connect('driver={ODBC Driver 17 for SQL Server};'
                        f'server={server_host};'  
                        f'database={database_name};'
                        'trusted_connection=yes;')

    cursor = conn.cursor()
    print("Connected")
    
except:
    print("Could't find database")

''' ROUTES '''

@app.route('/')
def home():
    return render_template("home_page.html")

@app.route('/register') #Edited by Chris and Emil
def register():
    return render_template("register.html")

@app.route('/sign_in') #Edited by Chris and Emil 
def sign_in():
    return render_template("sign_in.html")

@app.route('/profile_settings') #Edited by Chris and Emil
def profile_settings():
    return render_template("profile_settings.html")

@app.route('/my_profile')
def my_profile():
    try:
        return render_template("my_profile.html", username=session['username'])
    except(KeyError):
        return redirect(url_for('sign_in'))

    #Ska vi skicka med skapade frågepaket, userinfo, tidigare spelade frågepaket, (vänner) !!Engelska? CE

@app.route('/create_game')
def create_game():
    return render_template("create_game.html")

@app.route('/join_game')
def join_game():
    return render_template("join_game.html")

@app.route('/view_all_games')
def view_all_games():
    return render_template("view_all_games.html")

@app.route('/view_one_game')
def view_one_game():
    return render_template("view_one_game.html")

@app.route('/add_new_user', methods = ["GET", "POST"])
def add_new_user():

    username = request.form["username"] #ska vara unikt
    password_1 = request.form["password1"]
    password_2 = request.form["password2"]
    email = request.form["email"]
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]

    if password_1 != password_2:
        error_message = "The passwords must be the same"
    else:
        cursor.execute(f"exec sp_add_user '{email}', '{password_2}', '{username}', '{firstname}', '{lastname}'")
        cursor.commit()
        session['loggedin'] = True
        session['email'] = email
        session['username'] = username

    return redirect(url_for("my_profile"))

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['email']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor.execute(f"exec sp_user_login '{username}', '{password}'") 
        # Fetch one record and return result
        account = cursor.fetchone()
        print(account)
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['email'] = account[1]
            session['username'] = account[3]
            # Redirect to home page
            msg = 'Logged in'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return redirect(url_for('my_profile'))

@app.route('/logout')
def user_logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('email', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('sign_in'))
'''
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
    #qp_rating = db_zingo.read_from_db("vw_qp_rating", "rating", f"where question_package = '{selected_qp}'")
    #print(qp_rating)
    qp_questions = db_zingo.execute_procedure(f"sp_get_questions '{selected_qp}'") #fixa en view för enbart frågor.
    print(qp_questions)
'''

''' CREATE QUESTION PACKAGE '''

def control_question_package():
    # Review question packages content before saving to database.
        # banned words
    # create qp, add questions -> then control and save/inform user of banned words.

def create_question_package():
    # insert function here:
    # name qp, description of qp.
    qp_name = request.form['qp_name'] #ska vara unikt
    qp_description = request.form['qp_description']

def add_question_to_qp():
    # add question, with 4 answers which of one correct alternative.
    question = request.form['question']
    answer_1 = request.form['answer_1']
    answer_2 = request.form['answer_2']
    answer_3 = request.form['answer_3']
    answer_4 = request.form['answer_4']

    # answer_1 is the correct answer!

def edit_questions_of_qp():

def add_tags_to_qp():