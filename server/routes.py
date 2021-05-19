import pdb
import pyodbc
import time
import re
from flask import Flask, redirect, url_for, render_template, request, session
from random import shuffle
from uuid import uuid4

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
    # string needs procedure name + parameters
    try:
        sql = f"exec [{database_name}].[dbo].{string};"
        cursor.execute(sql)
        try:
            rows = cursor.fetchall()
            if rows:
                return rows
        except:            print("Nothing to report back!")

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
    session['message'] = ""
    return render_template("home_page.html", session = session)

@app.route('/register') 
def register():
    return render_template("register.html")

@app.route('/sign_in') 
def sign_in():
    return render_template("sign_in.html")

@app.route('/my_profile')
def my_profile():
    session['message'] = ""
    if 'loggedin' in session:
        qp_list = list_of_games()
        cursor.execute(f"select q.qp_name, q.qp_description, u.nickname from question_package q left join [user] u on q.created_by = u.[user_id] where u.nickname = '{session['username']}'")
        res = cursor.fetchall()
        return render_template("my_profile.html", username=session['username'], games = res)
    else:
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
    list_of_questions = []
    qna = []
    for i in questions:    
        list_of_questions.append(i[0])
    
    return render_template("create_question.html", qp_name = session['qp_name'], questions = list_of_questions, qna = qna, msg = session['message'])

@app.route('/edit_qp/<qp_name>')
def edit_qp(qp_name):
    session['qp_name'] = qp_name
    cursor.execute(f"exec sp_get_questions '{qp_name}'")
    questions = cursor.fetchall()
    
    qna = []

    list_of_questions = []
    
    for i in questions:    
        list_of_questions.append(i[0])

    return render_template("create_question.html", qp_name = qp_name, questions = list_of_questions, qna = qna, msg = session['message'])

@app.route('/edit_qp/<qp_name>/<question>')
def edit_q(qp_name, question):
    cursor.execute(f"exec sp_get_questions '{qp_name}'")
    questions = cursor.fetchall()
    
    list_of_questions = []
    
    for i in questions:    
        list_of_questions.append(i[0])

    question_and_answers = []
    for i in questions:
        if question in i:
            for x in i:
                question_and_answers.append(x)

    session['question'] = question_and_answers[0]

    return render_template("create_question.html", qp_name = qp_name, questions = list_of_questions, qna = question_and_answers)

@app.route('/receive_temporal_user', methods = ['GET', 'POST'])
def receive_temporal_user():
    string = request.args.get("url")
    temp_user = request.form['temporary_username']
    session['temp_login'] = True
    session['username'] = temp_user
    return redirect(string)

@app.route('/view_all_question_package')
def view_all_question_package():
    cursor.execute(f"select q.qp_name, q.qp_description, u.nickname from question_package q left join [user] u on q.created_by = u.[user_id]")
    res = cursor.fetchall()

    return render_template("view_all_question_package.html", qp_list = res)

@app.route('/view_one_question_package/<qp_name>')
def view_one_question_package(qp_name):
    cursor.execute(f"select qp_description, created_by from question_package where qp_name = '{qp_name}'")
    qp_info = cursor.fetchone()
    qp_desc = qp_info[0]
    qp_creator = qp_info[1]
    cursor.execute(f"select nickname from [user] where user_id = '{qp_creator}'")
    qp_nick = cursor.fetchone()
   
    return render_template("view_one_question_package.html", qp_name = qp_name, qp_desc = qp_desc, username = session['username'])

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
    
    cursor.execute(f"exec sp_get_questions '{session['qp_name']}'")
    questions = cursor.fetchall()

    for i in questions:
        if question == i[0] and answer_1 == i[1] and answer_2 == i[2] and answer_3 == i[3] and answer_4 == i[4]:
            msg = 'The question does already exist in the question package.'
            session['message'] = msg
            return redirect(url_for('create_question'))

    if get_question(question, answer_1, answer_2, answer_3, answer_4) == True:
        msg = 'Question added!'
    else:
        msg = 'The question contained a word which we do not allow.'
    
    session['message'] = msg
    
    
    return redirect(url_for('create_question'))

@app.route('/edit_questions_and_answers', methods = ['GET', 'POST'],)
def edit_question():
    question = request.form['question']
    answer_1 = request.form['answer_1']
    answer_2 = request.form['answer_2']
    answer_3 = request.form['answer_3']
    answer_4 = request.form['answer_4']

    cursor.execute(f"select q_id from question where question = '{session['question']}'")
    res = cursor.fetchone()
    question_id = res[0]

    '''
    cursor.execute(f"exec sp_get_questions '{session['qp_name']}'")
    questions = cursor.fetchall()

    for i in questions:
        if question == i[0] and answer_1 == i[1] and answer_2 == i[2] and answer_3 == i[3] and answer_4 == i[4]:
            msg = 'The question does already exist in the question package.'
            session['message'] = msg
            return redirect(url_for('edit_qp', qp_name=session['qp_name']))
    '''
    if get_question(question, answer_1, answer_2, answer_3, answer_4) == True:
        cursor.execute(f"delete from question where q_id = {question_id}")
        cursor.commit()
        msg = 'Changes confirmed!'
    else:
        msg = 'The question contained a word which we do not allow.'
    
    session['message'] = msg

    return redirect(url_for('edit_qp', qp_name=session['qp_name']))

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

@app.route('/terms_conditions')
def terms_conditions():
    return render_template("terms_conditions.html")

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

def list_of_games():
    cursor.execute(f"select qp_name from vw_qp_with_nick where nickname = '{session['username']}'")
    res = cursor.fetchall()
    qp_list = []
    for i in res:
        qp_list.append(i[0])
           
    return qp_list

def apply_tags_to_qp(tag_list):
    cursor.execute(f"select qp_id from question_package where qp_name = '{session['qp_name']}'")
    res = cursor.fetchone()
    qp_id = res[0]
    tags = []
    tags.append(tag_list)
    for i in tags:
        cursor.execute(f"select tag_id from tag where tag_description = '{i}'")
        row = cursor.fetchone()
        tag_id = row[0]
        cursor.execute(f"insert into question_package_tag (qp_id, tag_id) values ({qp_id}, {tag_id})")
        cursor.commit()

def save_qp_to_db(qp_name, qp_desc, qp_tags):
    cursor.execute(f"select [user_id] from [user] where e_mail = '{session['email']}'")
    res = cursor.fetchone()
    user_id = res[0]
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
        return False
    else:
        #-- before running: !Control that a session with qp_name is created during creation of new qp!
        qp_name = session['qp_name']

        cursor.execute(f"select qp_id from question_package where qp_name = '{qp_name}'")
        res = cursor.fetchone()
        current_qp_id = res[0]
        cursor.execute(f"insert into question (question, answer_1_correct, answer_2, answer_3, answer_4, qp_id) values ('{question}', '{answer_1}', '{answer_2}', '{answer_3}', '{answer_4}', {current_qp_id})")
        cursor.commit()
        return True

def check_words_aginst_db(all_words):
    l = []

    for word in all_words:
        profanity = read_from_db("ugly_words", "*", f"where profanity = '{word}'")
        if profanity:
            l.append(word)

    if len(l) > 0:
        return l

@app.route('/search', methods = ['GET', 'POST'])
def search_form():
    search_input = request.form['search_input']
    cursor.execute(f"select q.qp_name, q.qp_description, u.nickname from question_package q full outer join [user] u on q.created_by = u.[user_id]  where q.qp_name like '%{search_input}%'")         
    res = cursor.fetchall()

    list_of_qp = []

    for x in res:
        for qp in x:
            list_of_qp.append(qp)

    '''
    for qp in list_of_qp:
        if qp == search_input:
            return redirect(url_for('view_one_question_package', qp_name = search_input))
    '''
    if res:
        return render_template("view_all_question_package.html", qp_list = res)
    else:
        return redirect(url_for('view_all_question_package'))

@app.route('/invite_player/<qp_name>/<admin>')
def invite_player(qp_name, admin):
    string = f"http://127.0.0.1:5000/invite_player/{qp_name}/{admin}"
    if 'loggedin' in session or 'temp_login' in session:
        username = session['username']
        if username == admin:
            return render_template("invite_player.html", qp_name = qp_name, url = string, admin = True, guest = False, username = username)
        else:
            return render_template("invite_player.html", qp_name = qp_name, url = string, admin = False, guest = False, username = username)
    else:
        return render_template("invite_player.html", qp_name = qp_name, url = string, admin = False, guest = True, username = "")

#create game_id, pass through route to db for saving results
@app.route('/playing/<chosen_qp>/<admin>')
def in_game_show_question(chosen_qp, admin):
    url = f'localhost:5000/playing/{chosen_qp}/{admin}'

    '''
    [
        {
            "question": "I vilken stad bor Anton?",
            "answers": [
                "Lund",
                "Malmö", 
                "Staffanstorp", 
                "Eslöv"
            ],
            "correct": "Lund"
        }
    ]
    '''
    questions = ask_questions(chosen_qp)
    cursor.execute(f"select qp_id from question_package where qp_name = '{chosen_qp}'")
    qp_id = cursor.fetchone()[0]

    #return render_template("in_game_show_question.html", questions = questions, admin = True, guest = False, url = url, qp_name = chosen_qp, username = session['username'])
    #Här måste ni skicka med qp_id och username för att kunna använda det i save_results_to_db(). Result kommer från score i in_game_show_question.html
    #return render_template("in_game_show_question.html", questions = questions, admin = True, guest = False, url = url, qp_id=qp_id, username=admin)

def ask_questions(question_list):
    question_list = execute_procedure(f"sp_get_questions '{question_list}'")
    
    questions = []
    for question in question_list:
        questions.append({
            "question": question[0],
            "answers": [
                question[1],
                question[2],
                question[3],
                question[4]
            ],
            "correct": question[1]
        })
    
    return questions
#old
'''def clear_list(question_list):
    question.clear()
    correct_answer.clear()
    all_answers.clear()

@app.route('/save_results_to_db', methods = ['GET', 'POST'])
def save_results_to_db():
    if request.method == 'POST':
        result = request.form['score']
        qp_name = request.form['qp_name']
        if result > 0:
            cursor.execute(f"select qp_id from question_package where qp_name = '{qp_name}'")
            res = cursor.fetchone()
            qp_id = res[0]
            player = session['username']
            try:
                cursor.execute(f"exec sp_game_details '{qp_id}', '{player}', '{result}'")
                cursor.commit()
            except:
                cursor.execute(f"exec sp_update_results")

    return redirect(url_for('leaderboard', qp_name = qp_name))

@app.route('/leaderboard/<qp_name>')    
def show_leaderboard(qp_name):
    leaderboard = leaderboard(qp_name)

    return render_template("leaderboard.html", leaderboard=leaderboard, qp_name=qp_name)

def leaderboard(qp_name):
    cursor.execute(f"select nickname, score from vw_leaderboard where qp_name = '{qp_name}'")
    leaderboard = cursor.fetchall()

    lb = []

    for score in leaderboard:
        lb.append({
            "player": leaderboard[0],
            "score": leaderboard[1],
        })

    return lb
'''
#new
@app.route('/save_results_to_db', methods=["POST"])
def save_results_to_db():
    qp_id = request.form['qp_id']
    player = request.form['username'] #Ska egentligen vara player_id enligt dbo.game_detail
    score = request.form['score']
    try:
        cursor.execute(f"exec sp_game_details '{qp_id}', '{player}', '{score}'")
        cursor.commit()
    except:
        cursor.execute(f"exec sp_update_results")


'''
def control_answer(question_list):


def show_result():
    #show question and correct answer
    for i in question_list:
        print(i[0], i[1])

    # resultat sparas "lokalt" efter varje fråga och sammanställs. resultatet förs vidare till nästa besvarde fråga och adderas, summeras och skickas vidare... ->

    
    # när inga fler frågor finns, visa slutresultat

def save_result():
    # spara slutresultat i databas
'''