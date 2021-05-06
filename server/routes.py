from flask import Flask, redirect, url_for, render_template, request, session
import pyodbc
from random import shuffle
import time

app = Flask(__name__)
app.secret_key = 'zingo'

''' 
database connection:
    server_host (str)
    database_name (str)
    
    cursor will be used by other functions to execute sql queries.
'''
server_host = "localhost"
database_name = "Zingo_DB"

try:
    conn = pyodbc.connect('driver={ODBC Driver 17 for SQL Server};'
                        f'server={server_host};'  
                        f'database={database_name};'
                        'trusted_connection=yes;')

    cursor = conn.cursor()   
except:
    print("Could't find database")

def execute_procedure(string): 
    # string behöver procedure namn + parametrar
    try:
        sql = f"exec [{database_name}].[dbo].{string};"
        cursor.execute(sql)
        try:
            rows = cursor.fetchall()
            if rows:
                return rows
        except:
            print("Nothing to report back!")

        conn.commit()

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        if sqlstate == '28000':
            print("LDAP Connection failed: check password")

def read_from_db(table_name, select_query, arguments):
    cursor.execute(
        f"select {select_query} from {database_name}.dbo.{table_name} {arguments}")

    row = cursor.fetchall()
    if row:
        return row

''' ROUTES '''

@app.route('/')
def home():
    return render_template("home_page.html")

@app.route('/register') 
def register():
    return render_template("register.html")

@app.route('/sign_in') 
def sign_in():
    return render_template("sign_in.html")

@app.route('/my_profile')
def my_profile():
    try:
        return render_template("my_profile.html", username=session['username'])
    except(KeyError):
        return redirect(url_for('sign_in'))

@app.route('/profile_settings')
def profile_settings():
    return render_template("profile_settings.html")

@app.route('/create_question_package')
def create_question_package():
    if 'loggedin' in session:
        cursor.execute("select tag_description from tag")
        tags = cursor.fetchall()

        list_of_tags = []

        for tag in tags:
            letter = filter(str.isalnum, tag)
            word = "".join(letter)
            list_of_tags.append(word)
        
        list_of_tags.sort()

        return render_template("create_question_package.html", tags=list_of_tags)

    else:
        return redirect(url_for('sign_in'))

@app.route('/create_question')
def create_question():

    cursor.execute(f"exec sp_get_questions '{session['qp_name']}'")
    questions = cursor.fetchall()
    print(questions)
    
    list_of_questions = []
    
    for i in questions:    
        list_of_questions.append(i[0])
    
    return render_template("create_question.html", qp_name = session['qp_name'], questions = list_of_questions)

@app.route('/invite_player')
def invite_player():
    return render_template("invite_player.html")

@app.route('/join_game')
def join_game():
    return render_template("join_game.html")

@app.route('/view_all_question_package')
def view_all_question_package():
    return render_template("view_all_question_package.html")

@app.route('/view_one_question_package')
def view_one_question_package():
    return render_template("view_one_question_package.html")

@app.route('/in_game_final_result')
def in_game_final_result():
    return render_template("in_game_final_result.html")

@app.route('/in_game_result')
def in_game_result():
    return render_template("in_game_result.html")

@app.route('/in_game_show_question')
def in_game_show_question():
    return render_template("in_game_show_question.html")

@app.route('/play_game')
def play_game():
    return render_template("play_game.html")

@app.route('/control_qp_name_desc', methods = ['GET', 'POST'])
def control_qp_name_desc():
    qp_name = request.form['qp_name']
    qp_desc = request.form['qp_description']
    qp_tags = request.form['qp_tag']
    save_qp_to_db(qp_name, qp_desc, qp_tags)
    return redirect(url_for('create_question'))

@app.route('/control_questions_answers', methods = ['GET', 'POST'])
def control_questions_answers():
    question = request.form['question']
    answer_1 = request.form['answer_1']
    answer_2 = request.form['answer_2']
    answer_3 = request.form['answer_3']
    answer_4 = request.form['answer_4']
    get_question(question, answer_1, answer_2, answer_3, answer_4)
    return redirect(url_for('create_question'))

@app.route('/add_new_user', methods = ["GET", "POST"])
def add_new_user():
    username = request.form["username"]
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
    msg = ''

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        username = request.form['email']
        password = request.form['password']
        cursor.execute(f"exec sp_user_login '{username}', '{password}'") 
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['email'] = account[1]
            session['username'] = account[3]
            msg = 'Logged in'
        else:
            msg = 'Incorrect username/password!'
    return redirect(url_for('my_profile'))

@app.route('/logout')
def user_logout():
    session.pop('loggedin', None)
    session.pop('email', None)
    session.pop('username', None)
    return redirect(url_for('sign_in'))


    print()
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
    #1. hämta data från db
    #2. spara lista med data från db
    #3. sortera lista i python
    #4. skicka lista till html

#create_game()
'''

''' CREATE QUESTION PACKAGE '''
'''
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

def add_tags_to_qp():'''




'''
chosen_qp = "Blandade sportfrågor"

def play_question_game(chosen_qp):
    question_list = execute_procedure(f"sp_get_questions '{chosen_qp}'")
    shuffle(question_list)
    
    ask_questions(question_list)

def ask_questions(question_list):
    #seperate question from answers, seperate answers from right answer
    #i[0] = question, i[1] = correct_answer
    question = []
    correct_answer = []
    all_answers = []

    #show question, put correct_answer in 1-4, put wrong_answers in 1-4 if not allready taken.

    for i in question_list:
        question.append(i[0])
        correct_answer.append(i[1])
        all_answers.append(i[1])
        all_answers.append(i[2])
        all_answers.append(i[3])
        all_answers.append(i[4])
        print(question[0])
        time.sleep(1)
        shuffle(all_answers)
        print(", ".join(all_answers)) #alt. (all_awnsers[0],all_awnsers[1],all_awnsers[2],all_awnsers[3])
        print(f"Rätt svar: {correct_answer[0]}")
        time.sleep(1)
        #ask question
        #display all answers (randomly)
        #show_result, question + correct_answer and score
        question.clear()
        correct_answer.clear()
        all_answers.clear()
    
    # visa en fråga i turordning 1-n1
    # loop med svar(?) (visa fråga, 30 sek, visa svar, 30 sek, om fråga finns, go again)
    # hämta svar och slumpmässigt ordna svar mellan 1-4. (rätt svar ska vara på "olika" platser varje fråga.)

def display_awnsers(question_list):

def show_result():
    #show question and correct answer
    for i in question_list:
        print(i[0], i[1])

    # resultat sparas "lokalt" efter varje fråga och sammanställs. resultatet förs vidare till nästa besvarde fråga och adderas, summeras och skickas vidare... ->

    
    # när inga fler frågor finns, visa slutresultat

def save_result():
    # spara slutresultat i databas
'''

def apply_tags_to_qp(tag_list):
    cursor.execute(f"select qp_id from question_package where qp_name = '{session['qp_name']}'")
    res = cursor.fetchone()
    qp_id = res[0]
    tags = []
    tags.append(tag_list)
    print(qp_id)
    print(tag_list)
    print(tags)
    for i in tags:
        print(i)
        cursor.execute(f"select tag_id from tag where tag_description = '{i}'")
        row = cursor.fetchone()
        tag_id = row[0]
        cursor.execute(f"insert into question_package_tag (qp_id, tag_id) values ({qp_id}, {tag_id})")
        cursor.commit()

def save_qp_to_db(qp_name, qp_desc, qp_tags):
    cursor.execute(f"select [user_id] from [user] where e_mail = '{session['email']}'")
    res = cursor.fetchone()
    user_id = res[0]
    #!add session id for user to relate 'created_by' in db, also add it into insert!
    qp_ndu = []
    nl = []
    qp_ndu.append(qp_name.split(" "))
    qp_ndu.append(qp_desc.split(" "))
    for i in qp_ndu:
        for x in i:
            y = filter(str.isalnum, x)
            t = "".join(y)
            nl.append(t)

    if check_words_aginst_db(nl):
        word = check_words_aginst_db(nl)

    else:
        session['qp_name'] = qp_name
        cursor.execute(f"insert into question_package (qp_description, created_by, qp_name) values ('{qp_desc}', {user_id}, '{qp_name}')")
        cursor.commit()
        apply_tags_to_qp(qp_tags)

def get_question(question, answer_1, answer_2, answer_3, answer_4):
    question_list = []
    alnum_list = []
    question_list.append(question.split(" "))
    question_list.append(answer_1.split(" "))
    question_list.append(answer_2.split(" "))
    question_list.append(answer_3.split(" "))
    question_list.append(answer_4.split(" "))
    for i in question_list:
        for x in i:
            y = filter(str.isalnum, x)
            t = "".join(y)
            alnum_list.append(t)

    if check_words_aginst_db(alnum_list):
        word = check_words_aginst_db(alnum_list)
    else:
        #-- before running: !Control that a session with qp_name is created during creation of new qp!
        qp_name = session['qp_name']

        cursor.execute(f"select qp_id from question_package where qp_name = '{qp_name}'")
        res = cursor.fetchone()
        current_qp_id = res[0]
        cursor.execute(f"insert into question (question, answer_1_correct, answer_2, answer_3, answer_4, qp_id) values ('{question}', '{answer_1}', '{answer_2}', '{answer_3}', '{answer_4}', {current_qp_id})")
        cursor.commit()

def check_words_aginst_db(all_words):
    l = []

    for word in all_words:
        profanity = read_from_db("ugly_words", "*", f"where profanity = '{word}'")
        if profanity:
            l.append(word)

    if len(l) > 0:
        return l