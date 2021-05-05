from db_zingo import read_from_db, update_db, execute_procedure, cursor
from random import shuffle
from flask import Flask, redirect, url_for, render_template, request, session
import pyodbc
import time


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

def save_qp_to_db1(qp_name, qp_desc, qp_tags):
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
        print(word)
        print('true')

    else:
        print('false')
        session['qp_name'] = qp_name
        print(f"{session['email']}")
        print(qp_name)
        print(qp_desc)
        print(qp_tags)
        print(user_id)
        cursor.execute(f"insert into question_package (qp_description, created_by, qp_name) values ('{qp_desc}', {user_id}, '{qp_name}')")
        cursor.commit()
        apply_tags_to_qp(qp_tags)
        

    

def get_question(question, answer_1, answer_2, answer_3, answer_4):
    # get form from client
    
    # split words into list and remove non-alphnum chars
    ql = []
    nt = []
    ql.append(question.split(" "))
    ql.append(answer_1.split(" "))
    ql.append(answer_2.split(" "))
    ql.append(answer_3.split(" "))
    ql.append(answer_4.split(" "))
    for i in ql:
        for x in i:
            y = filter(str.isalnum, x)
            t = "".join(y)
            nt.append(t)
    # check if words exist in db table for profanity words
    if check_words_aginst_db(nt):
        word = check_words_aginst_db(nt)
        print(word) #wip
        print('true') #wip
    else:
        #-- before running: !Control that a session with qp_name is created during creation of new qp!
        qp_name = session['qp_name']

        current_qp_id = cursor.execute(f"select qp_id from question_package where qp_name = '{qp_name}'")
        cursor.execute(f"insert into Zingo_DB.dbo.question (question, answer_1_correct, answer_2, answer_3, answer_4, qp_id) values ('{question}', '{answer_1}', '{answer_2}', '{answer_3}', '{answer_4}', '{current_qp_id}')")
        cursor.commit()
        print('false') #wip

def check_words_aginst_db(all_words):
    # all_words = list
    # returns a list of profanity words
    l = []

    for word in all_words:
        profanity = read_from_db("ugly_words", "*", f"where profanity = '{word}'")
        if profanity:
            l.append(word)

    if len(l) > 0:
        return l