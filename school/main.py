import os
import flask
from pprint import pprint
from flask import Flask  # Подключаем Flask
from flask import render_template  # Подключаем библиотеку для работы с шаблонами
import sqlite3 as sq  # Подключаем библиотеку для работы с базой данных
from flask import url_for
from sqlalchemy import create_engine, text 
from flask import request  # Для обработка запросов из форм
from flask import redirect  # Для автоматического перенаправления
import datetime  # Для получения текущей даты и врмени
import pymysql
#pymysql.install_as_MySQLdb()

username = "root"
passwd = "12345"
db_name = "database_school"



sq = pymysql.connect(host = "localhost",port = 8889,user= "root",password = passwd, database = db_name, cursorclass = pymysql.cursors.DictCursor)



app = Flask(__name__)


@app.route("/")
def page():
	return render_template("web_page.html")
@app.route('/index')
def index():
    all_students = get_all_students()
    return render_template("index.html", data=all_students, number=len(all_students))


@app.route("/student/<int:student_id>", methods=['GET', 'POST'])
def student(student_id):
    student_info = get_student_info(student_id)
    task_info = get_student_tasks_info(student_id)
    if request.method == "POST":  # Если были переданы данные из формы методом POST
        print("запрос отправлен")
        if 'delete-button' in request.form:  # Если была нажата кнопка delete_button
            print("Нажата клавиша удалить")
            student_delete_all_tasks(student_id)  # То вызываем фукнцию удаления всех сообщений пользователя
        elif 'new-task' in request.form:
            print(request.form['task'])
            for item in request.form:
                print(item)
            add_task(student_id, request.form['task'])
        return redirect('/student/' + str(student_id))
    return render_template('student.html', student_info=student_info, task_info=task_info)


def tasks(student_id):
    student_tasks = get_student_tasks_info(student_id)
    return render_template('student.html', student_tasks=student_tasks)


def get_all_students():  # Получить список информации о всех пользователях
	connection = sq.cursor()
	all_students = [] 
	connection.execute("SELECT * FROM students")# Выполняем запрос и получаем таблицу с результатов
	all_students_table = connection.fetchall()
	for item in all_students_table:
		dict_item = dict(item)
		all_students.append(dict_item)
	connection.close()  # Закрываем подключение к базе

	# all_students = [row for row in all_students_table]  # Создаем список строк из таблицы
	pprint((all_students))
	return all_students


def get_student_tasks_info(student_id):
    student_tasks_info = []
    connection = sq.cursor()
    connection.execute("select * from tasks where student_id = %s",student_id)
    student_tasks_info_table = connection.fetchall()
    for item in student_tasks_info_table:
        dict_item = dict(item)
        student_tasks_info.append(dict_item)

    connection.close()

    return student_tasks_info


def get_student_info(student_id):
	connection = sq.cursor()
	student_info = []
	connection.execute("SELECT * FROM students WHERE student_id = %s",student_id)
	student_info_table = connection.fetchall()
	for item in student_info_table:
		item = dict(item)
		student_info.append(item)
	connection.close()
	return student_info[0]


def add_task(student_id, message_text):  # Сохранить сообщение пользователя в базу
	connection = sq.cursor()
	current_time = datetime.datetime.now()  # Получаем теущие дату и время
	# Записываем данные в таблицу
	task = message_text
	connection.execute("INSERT INTO tasks(student_id, task, date) VALUES (%s, %s, %s)",(
		student_id, message_text, current_time))
	sq.commit()  # Применяем транзакцию
	connection.close()
	return
  


def student_delete_all_tasks(student_id):
	connection = sq.cursor()
	connection.execute("DELETE FROM tasks WHERE student_id = %s",student_id)
	sq.commit()  # Применяем транзакцию
	connection.close()
	return


if __name__ == "__main__":
    app.run(debug=True)
