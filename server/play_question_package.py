from db_zingo import read_from_db, update_db, execute_procedure
from random import shuffle
import pyodbc
import time

chosen_qp = "Blandade sportfrågor"

def play_question_game(chosen_qp):
    question_list = execute_procedure(f"sp_get_questions '{chosen_qp}'")
    shuffle(question_list)
    
    ask_questions(question_list)

def ask_questions(question_list):
    #1. en lista med frågor samt svarsalternativ kommer IN

    #X. en fråga samt svarsalternativ ska skickas UT

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
'''
def display_awnsers(question_list):

def show_result():
    #show question and correct answer
    for i in question_list:
        print(i[0], i[1])

    # resultat sparas "lokalt" efter varje fråga och sammanställs. resultatet förs vidare till nästa besvarde fråga och adderas, summeras och skickas vidare... ->

    
    # när inga fler frågor finns, visa slutresultat

def save_result():
    # spara slutresultat i databas'''

