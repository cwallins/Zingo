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
    return render_template("register.html", msg = session['message'])

@app.route('/sign_in') 
def sign_in():
    return render_template("sign_in.html", msg = session['message'])

@app.route('/my_profile')
def my_profile():
    if 'loggedin' in session:
        session['message'] = ""
        cursor.execute(f"select q.qp_name, q.qp_description, u.nickname from question_package q left join [user] u on q.created_by = u.[user_id] where u.nickname = '{session['username']}'")
        game_info = cursor.fetchall()
        return render_template("my_profile.html", username = session['username'], games = game_info)
    else:
        return redirect(url_for('sign_in'))

@app.route('/profile_settings')
def profile_settings():
    return render_template("profile_settings.html")

@app.route('/create_question_package')
def create_question_package():
    if 'loggedin' in session:
        list_of_tags = get_tags()
        return render_template("create_question_package.html", tags = list_of_tags, msg = session['message'])
    else:
        return redirect(url_for('sign_in'))

@app.route('/create_question')
def create_question():
    list_of_questions = sp_get_questions(session['qp_name'])
    qna = []
    return render_template("create_question.html", qp_name = session['qp_name'], questions = list_of_questions, qna = qna, msg = session['message'])

@app.route('/edit_qp/<qp_name>')
def edit_qp(qp_name):
    session['qp_name'] = qp_name
    list_of_questions = sp_get_questions(session['qp_name'])
    qna = []
    return render_template("create_question.html", qp_name = qp_name, questions = list_of_questions, qna = qna, msg = session['message'])

@app.route('/edit_qp/<qp_name>/<question>')
def edit_q(qp_name, question):
    list_of_questions = sp_get_questions(qp_name)
    question_and_answers = get_questions_and_answers(qp_name, question)
    session['question'] = question_and_answers[0]
    return render_template("create_question.html", qp_name = qp_name, questions = list_of_questions, qna = question_and_answers)

@app.route('/view_all_question_package')
def view_all_question_package():
    cursor.execute(f"select q.qp_name, q.qp_description, u.nickname from question_package q left join [user] u on q.created_by = u.[user_id]")
    qp_list = cursor.fetchall()
    list_of_tags = get_tags()
    return render_template("view_all_question_package.html", qp_list = qp_list, tags = list_of_tags)

@app.route('/view_one_question_package/<qp_name>')
def view_one_question_package(qp_name):
    cursor.execute(f"select qp_description, created_by from question_package where qp_name = '{qp_name}'")
    qp_info = cursor.fetchone()
    qp_desc = qp_info[0]
    qp_creator = qp_info[1]
    cursor.execute(f"select nickname from [user] where user_id = '{qp_creator}'")
    qp_nick = cursor.fetchone()
    lb = leaderboard(qp_name)
    if 'username' in session:
        username = session['username']
    else:
        session['username'] = 'User'
        username = session['username']
    
    return render_template("view_one_question_package.html", qp_name = qp_name, qp_desc = qp_desc, username = username, leaderboard = lb)

@app.route('/control_qp_name_desc', methods = ['GET', 'POST'])
def control_qp_name_desc():
    qp_name = request.form['qp_name']
    qp_desc = request.form['qp_description']
    qp_tags = request.form['qp_tag']

    cursor.execute(f"select * from question_package where qp_name = '{qp_name}'")
    qp_info = cursor.fetchone()
    
    if qp_info:
        session['message'] = 'Could not proceed, the name was unfortunately already taken.'
        return redirect(url_for('create_question_package'))
    else:
        if save_qp_to_db(qp_name, qp_desc, qp_tags) == True:
            return redirect(url_for('create_question'))
        else:
            session['message'] = 'Could not continue. The title or description contains a word we do not allow.'
            return redirect(url_for('create_question_package'))

@app.route('/control_questions_answers', methods = ['GET', 'POST'])
def control_questions_answers():
    question = request.form['question']
    answer_1 = request.form['answer_1']
    answer_2 = request.form['answer_2']
    answer_3 = request.form['answer_3']
    answer_4 = request.form['answer_4']
    
    cursor.execute(f"exec sp_get_questions '{session['qp_name']}'")
    questions = cursor.fetchall()

    for q in questions:
        if question == q[0] and answer_1 == q[1] and answer_2 == q[2] and answer_3 == q[3] and answer_4 == q[4]:
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
    question_id = cursor.fetchone()[0]

    if get_question(question, answer_1, answer_2, answer_3, answer_4) == True:
        cursor.execute(f"delete from question where q_id = {question_id}")
        cursor.commit()
        msg = 'Changes confirmed!'
    else:
        msg = 'The question contained a word which we do not allow.'
    
    session['message'] = msg

    return redirect(url_for('edit_qp', qp_name = session['qp_name']))

@app.route('/add_new_user', methods = ["GET", "POST"])
def add_new_user():
    username = request.form["username"]
    password_1 = request.form["password1"]
    password_2 = request.form["password2"]
    email = request.form["email"]
    first_name = request.form["firstname"]
    last_name = request.form["lastname"]

    if password_1 != password_2:
        session['message'] = "The passwords must be the same"
        return redirect(url_for('register'))
    elif len(password_2) < 8:
        session['message'] = 'Could not proceed, the password did not meet the requirements.'
        return redirect(url_for('register'))
    else:
        cursor.execute(f"exec sp_add_user '{email}', '{password_2}', '{username}', '{first_name}', '{last_name}'")
        cursor.commit()
        session['loggedin'] = True
        session['email'] = email
        session['username'] = username
    
    if 'was_playing' in session:
        return redirect(url_for('in_game_show_question', chosen_qp = session['was_playing'], admin = session['username']))
    else:
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
            session['message'] = 'Incorrect email and password.'
    return redirect(url_for('my_profile'))

@app.route('/logout')
def user_logout():
    session.pop('loggedin', None)
    session.pop('email', None)
    session.pop('username', None)
    session.pop('was_playing', None)
    session.pop('qp_name', None)
    session['message'] = ""
    return redirect(url_for('sign_in'))

@app.route('/terms_conditions')
def terms_conditions():
    return render_template("terms_conditions.html")

@app.route('/contact_us')
def contact_us():
    first_name = ""
    last_name = ""
    email = ""
    if 'loggedin' in session:
        cursor.execute(f"select f_name, l_name, e_mail from [user] where nickname = '{session['username']}'")
        data = cursor.fetchone()
        first_name = data[0]
        last_name = data[1]
        email = data[2]

    return render_template('contact_us.html', first_name = first_name, last_name = last_name, email = email)

def apply_tags_to_qp(tag_list):
    cursor.execute(f"select qp_id from question_package where qp_name = '{session['qp_name']}'")
    qp_id = cursor.fetchone()[0]
    tags = []
    tags.append(tag_list)
    for tag in tags:
        cursor.execute(f"select tag_id from tag where tag_description = '{tag}'")
        tag_id = cursor.fetchone()[0]
        cursor.execute(f"insert into question_package_tag (qp_id, tag_id) values ({qp_id}, {tag_id})")
        cursor.commit()

def save_qp_to_db(qp_name, qp_desc, qp_tags):
    cursor.execute(f"select [user_id] from [user] where e_mail = '{session['email']}'")
    user_id = cursor.fetchone()[0]

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
        return False
    else:
        session['qp_name'] = qp_name
        cursor.execute(f"insert into question_package (qp_description, created_by, qp_name) values ('{qp_desc}', {user_id}, '{qp_name}')")
        cursor.commit()
        apply_tags_to_qp(qp_tags)
        return True
       
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
        qp_name = session['qp_name']

        cursor.execute(f"select qp_id from question_package where qp_name = '{qp_name}'")
        current_qp_id = cursor.fetchone()[0]

        cursor.execute(f"insert into question (question, answer_1_correct, answer_2, answer_3, answer_4, qp_id) values ('{question}', '{answer_1}', '{answer_2}', '{answer_3}', '{answer_4}', {current_qp_id})")
        cursor.commit()
        return True

def check_words_aginst_db(all_words):
    new_list = []

    for word in all_words:
        profanity = read_from_db("ugly_words", "*", f"where profanity = '{word}'")
        if profanity:
            new_list.append(word)

    if len(new_list) > 0:
        return new_list

@app.route('/search', methods = ['GET', 'POST'])
def search_form():
    if 'search_input' in request.form:
        search_input = request.form['search_input']

        cursor.execute(f"select q.qp_name, q.qp_description, u.nickname from question_package q full outer join [user] u on q.created_by = u.[user_id]  where q.qp_name like '%{search_input}%'")         
        res = cursor.fetchall()
    elif 'qp_tag' in request.form:
        qp_tag = request.form['qp_tag']

        cursor.execute(f"select q.qp_name, q.qp_description, u.nickname from question_package q full outer join [user] u on q.created_by = u.[user_id] join question_package_tag qt on q.qp_id = qt.qp_id join tag t on t.tag_id = qt.tag_id where t.tag_description = '{qp_tag}'")         
        res = cursor.fetchall()
    
    list_of_tags = get_tags()

    if res:
        return render_template("view_all_question_package.html", qp_list = res, tags = list_of_tags)
    else:
        session['message'] = 'Could not find any question packages, please try again.'
        return render_template('view_all_question_package.html', msg = session['message'], tags = list_of_tags)

@app.route('/playing/<chosen_qp>/<admin>')
def in_game_show_question(chosen_qp, admin):
    try:
        questions = ask_questions(chosen_qp)
        shuffle(questions)

        for question in questions:
            shuffle(question['answers'])

        cursor.execute(f"select qp_id from question_package where qp_name = '{chosen_qp}'")
        qp_id = cursor.fetchone()[0]

        if admin == 'User':
            session['message'] = "You are currently not logged in. Your score will not be saved. Do you wish to create an account?"
            session['was_playing'] = chosen_qp
        else:
            session['message'] = ""

        return render_template("in_game_show_question.html", questions = questions, admin = True, guest = False, qp_id = qp_id, username = admin, msg = session['message'])
    except:
        return redirect(url_for("view_all_question_package"))

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

@app.route('/save_results_to_db', methods = ['POST'])
def save_results_to_db():
    
    qp_id = request.form['qp_id']
    result = request.form['score']
    cursor.execute(f"select qp_name from question_package where qp_id = {qp_id}")
    qp_name = cursor.fetchone()[0]
    
    
    if session['username'] != 'User':
        cursor.execute(f"select [user_id] from [user] where nickname = '{session['username']}'")
        player = cursor.fetchone()[0]
        try:
            cursor.execute(f"exec sp_game_details {qp_id}, {player}, {result}")
            cursor.commit()
        except:
            cursor.execute(f"exec sp_update_result {qp_id}, {player}, {result}")
            cursor.commit()
    else:
        pass
    session['qp_name'] = qp_name
    session['result'] = result

    return redirect(url_for('show_leaderboard', qp_name = qp_name))

@app.route('/leaderboard/<qp_name>')
def show_leaderboard(qp_name):
    result = session['result']
    player = session['username']
    lb = leaderboard(qp_name)

    return render_template("leaderboard.html", leaderboard = lb, qp_name = qp_name, result = result, player = player)

def leaderboard(qp_name):
    cursor.execute(f"select nickname, score from vw_leaderboard where qp_name = '{qp_name}' order by score desc")
    leaderboard = cursor.fetchall()

    lb = []

    for score in leaderboard:
        lb.append({
            "player": score[0],
            "score": score[1],
        })

    return lb

def sp_get_questions(qp_name):
    cursor.execute(f"exec sp_get_questions '{qp_name}'")
    questions = cursor.fetchall()

    list_of_questions = []

    for question in questions:    
        list_of_questions.append(question[0])

    return list_of_questions

def get_questions_and_answers(qp_name, question):
    cursor.execute(f"exec sp_get_questions '{qp_name}'")
    questions = cursor.fetchall()

    question_and_answers = []
    for i in questions:
        if question in i:
            for x in i:
                question_and_answers.append(x)
    return question_and_answers

def get_tags():
    cursor.execute("select tag_description from tag")
    tags = cursor.fetchall()

    list_of_tags = []

    for tag in tags:
        # Removes any character that isn't a letter or number
        letter = filter(str.isalnum, tag)
        # Combines every letter and/or number into one string
        word = "".join(letter)
        # Adds the string(word) to list_of_tags
        list_of_tags.append(word)
        
    list_of_tags.sort()
    return list_of_tags