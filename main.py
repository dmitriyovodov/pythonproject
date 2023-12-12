import telebot
import sqlite3
from telebot import types
import datetime
from threading import Thread
from fnmatch import fnmatch

bot = telebot.TeleBot("6365578168:AAHgm1qmzqWB6Ed-Xou9UvAt6XYBAB9P4mo")
task_name = ""
task = ""
user_name = ""
password = ""
button_names = ["Новая задача", "Удалить задачу", "Редактировать задачу", "Посмотреть задачу", "Посмотреть все задачи",
                "Отменить действие", "Войти", "Зарегистрироваться"]
buttons = list(map(types.KeyboardButton, button_names))
used_names = button_names


@bot.message_handler(commands=["start"])
def start(message):
    """
        Starts bot by adding keyboard buttons to register or login.

        :param message: the first message of the user
        :type message: telegram message
        :returns: nothing
        :rtype: None
    """
    conn = sqlite3.connect("user.sql")
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS tasks (id int auto_increment primary key, task_name varchar(20), '
                'task varchar(100), deadline varchar(20), user_name varchar(20), password varchar(20))')
    conn.commit()
    cur.close()
    conn.close()
    markup = types.ReplyKeyboardMarkup()
    markup.row(buttons[6], buttons[7])
    bot.send_message(message.chat.id, "Привет, зайди в аккаунт или зарегистрируй новый", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def operations_manager(message):
    """
        Manages keyboard buttons input

        :param message: button input
        :type message: telegram message
        :returns: nothing
        :rtype: None
    """
    if message.text == button_names[0]:
        newTask_name_request(message)
    elif message.text == button_names[1]:
        delTask_name_request(message)
    elif message.text == button_names[2]:
        editTask_name_request(message)
    elif message.text == button_names[3]:
        viewTask_name_request(message)
    elif message.text == button_names[4]:
        viewAllTasks(message)
    elif message.text == button_names[6]:
        login_name_request(message)
    elif message.text == button_names[7]:
        register_name_request(message)


def newTask_name_request(message):
    """
         Requests name of future task

        :param message: user's message
        :type message: telegram message
        :returns: nothing
        :rtype: None
    """
    cancel_button(message, "Введите название задачи")
    bot.register_next_step_handler(message, newTask_discription_request)


def newTask_discription_request(message):
    """
        Request dicription of future task

        :param message: name
        :type message: telegram message
        :returns: nothing
        :rtype: None
    """
    if cancelling(message):
        return
    global task_name
    task_name = message.text.strip()
    if task_name in used_names:
        default_buttons(message, "Имя уже использовано, попробуйте использовать другое")
        return
    bot.send_message(message.chat.id, "Введите описание")
    bot.register_next_step_handler(message, newTask_deadline_request)


def newTask_deadline_request(message):
    """
        Request deadline date of future task

        :param message: discription
        :type message: telegram message
        :returns: nothing
        :rtype: None
    """
    if cancelling(message):
        return
    global task
    task = message.text.strip()
    bot.send_message(message.chat.id, "Введите дату дедлайна в формате: 'дд/мм/гг'")
    bot.register_next_step_handler(message, newTask)


def newTask(message):
    """
        Adds new task to sqlite3 table

        :param message: deadline date
        :type message: telegram message
        :returns: nothing
        :rtype: None
    """
    if cancelling(message):
        return
    deadline = message.text.strip()
    if not fnmatch(deadline, "??/??/??"):
        default_buttons(message, "Дедлайн введён неправильно")
        return
    used_names.append(task_name)
    conn = sqlite3.connect("user.sql")
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO tasks (task_name, task, deadline, user_name, password) VALUES (?,?,?,?,?)',
        (task_name, task, deadline, user_name, password))
    conn.commit()
    cur.close()
    conn.close()
    default_buttons(message, "Задача добавлена в список!")


def delTask_name_request(message):
    """
        Request name of task that is being deleted

        :param message: button input
        :type message: telegram message
        :returns: nothing
        :rtype: None
    """
    cancel_button(message, "Введите название удаляемой задачи")
    bot.register_next_step_handler(message, delTask)


def delTask(message):
    """
        Deletes task from sqlite3 table

        :param message: name
        :type message: telegram message
        :returns: nothing
        :rtype: None
    """
    global task_name
    if cancelling(message):
        return
    task_name = message.text.strip()
    conn = sqlite3.connect("user.sql")
    cur = conn.cursor()
    cur.execute(
        'DELETE FROM tasks WHERE task_name = ? AND user_name = ?', (task_name, user_name))
    conn.commit()
    cur.close()
    conn.close()
    default_buttons(message, f"Задача {task_name} удалена!")


def editTask_name_request(message):
    """
        Request name of task that is being edited

        :param message: button input
        :type message: telegram message
        :returns: nothing
        :rtype: None
    """
    cancel_button(message, "Введите название задачи, которую вы хотите изменить")
    bot.register_next_step_handler(message, editTask_newdis_request)


def editTask_newdis_request(message):
    """
        Request new discription of task that is being edited

        :param message: name
        :type message: telegram message
        :returns: nothing
        :rtype: None
    """
    if cancelling(message):
        return
    global task_name
    task_name = message.text.strip()
    bot.send_message(message.chat.id, "Введите новое описание")
    bot.register_next_step_handler(message, editTask_newdeadline_request)


def editTask_newdeadline_request(message):
    """
        Request new deadline date of task that is being edited

        :param message: discription
        :type message: telegram message
        :returns: nothing
        :rtype: None
    """
    if cancelling(message):
        return
    global task
    task = message.text.strip()
    bot.send_message(message.chat.id, "Введите новый дедлайн в формате: 'дд/мм/гг'")
    bot.register_next_step_handler(message, editTask)


def editTask(message):
    """
        Edites task from sqlite3 table

        :param message: deadline date
        :type message: telegram message
        :returns: nothing
        :rtype: None
    """
    if cancelling(message):
        return
    deadline = message.text.strip()
    if not fnmatch(deadline, "??/??/??"):
        default_buttons(message, "Дедлайн введён неправильно")
        return
    conn = sqlite3.connect("user.sql")
    cur = conn.cursor()
    cur.execute(
        'UPDATE tasks SET task = ? WHERE task_name = ? AND user_name = ? ',
        (task, task_name, user_name))
    cur.execute(
        'UPDATE tasks SET deadline = ? WHERE task_name = ? AND user_name = ? ',
        (deadline, task_name, user_name))
    conn.commit()
    cur.close()
    conn.close()
    default_buttons(message, f"Задача {task_name} изменена!")


def viewAllTasks(message):
    """
        Shows names of all tasks from sqlite3

        :param message: button input
        :type message: telegram message
        :returns: nothing
        :rtype: None
    """
    conn = sqlite3.connect("user.sql")
    cur = conn.cursor()
    cur.execute(
        'SELECT * FROM tasks')
    tasks = cur.fetchall()
    s = ""
    c = 0
    for i in tasks:
        if i[1] != "task0":
            if i[4] == user_name:
                c += 1
                s += str(c) + ") " + i[1] + "\n"
    if s == "":
        bot.send_message(message.chat.id, "Пока задач нет")
    else:
        bot.send_message(message.chat.id, s)
    cur.close()
    conn.close()


def viewTask_name_request(message):
    """
        Request name of task that is being viewed

        :param message: button input
        :type message: telegram message
        :returns: nothing
        :rtype: None
    """
    cancel_button(message, "Введите название задачи, которую вы хотите посмотреть")
    bot.register_next_step_handler(message, viewTask)


def viewTask(message):
    """
        Shows name, discription, deadline date of task from sqlite3

        :param message: discription
        :type message: telegram message
        :returns: nothing
        :rtype: None
    """
    if cancelling(message):
        return
    conn = sqlite3.connect("user.sql")
    cur = conn.cursor()
    cur.execute(
        'SELECT * FROM tasks')
    tasks = cur.fetchall()
    for i in tasks:
        if i[1] == message.text.strip() and i[4] == user_name and i[1] != "task0":
            s = f"{i[1]}\n{i[2]}\n{i[3]}"
            break
    else:
        s = "Такой задачи не существует"
    cur.close()
    conn.close()
    default_buttons(message, s)


def cancel_button(message, text):
    """
        Puts up 'Cancel' button

        :param message: message from previous function
        :param text: text that will be sent to the user
        :type message: telegram message
        :type text: string
        :returns: nothing
        :rtype: None
    """
    markup = types.ReplyKeyboardMarkup()
    markup.row(buttons[5])
    bot.send_message(message.chat.id, text, reply_markup=markup)


def default_buttons(message, text):
    """
        Puts up 'Create', 'Delete', 'Edit', 'ViewAll', 'View' buttons

        :param message: message from previous function
        :param text: text that will be sent to the user
        :type message: telegram message
        :type text: string
        :returns: nothing
        :rtype: None
    """

    markup = types.ReplyKeyboardMarkup()
    markup.row(buttons[0], buttons[1], buttons[2])
    markup.row(buttons[3], buttons[4])
    bot.send_message(message.chat.id, text, reply_markup=markup)


def cancelling(message, text="Действие отменено"):
    """
        Returns True if 'Cancel' button was pressed

        :param message: message from previous function
        :param text: text that will be sent to the user
        :type message: telegram message
        :type text: string
        :returns: True/False
        :rtype: bool
    """
    if message.text == button_names[5]:
        default_buttons(message, text)
        return True
    return False


def login_name_request(message):
    """
        Requests user_name

        :param message: button input
        :type message: telegram message
        :returns: nothing
        :rtype: None
    """
    markup = types.ReplyKeyboardMarkup()
    bot.send_message(message.chat.id, "Введите своё имя", reply_markup=markup)
    bot.register_next_step_handler(message, login_password_request)


def login_password_request(message):
    """
        Requests password

        :param message: user_name
        :type message: telegram message
        :returns: nothing
        :rtype: None
    """
    global user_name
    user_name = message.text
    markup = types.ReplyKeyboardMarkup()
    bot.send_message(message.chat.id, "Введите пароль", reply_markup=markup)
    bot.register_next_step_handler(message, login)


def login(message):
    """
        Logins in an account

        :param message: password
        :type message: telegram message
        :returns: nothing
        :rtype: None
    """
    global password
    password = message.text
    conn = sqlite3.connect("user.sql")
    cur = conn.cursor()
    cur.execute(
        'SELECT * FROM tasks')
    tasks = cur.fetchall()
    accounts = set()
    for i in tasks:
        accounts.add((i[4], i[5]))
    cur.close()
    conn.close()
    if (user_name, password) in accounts:
        default_buttons(message, "Вы зашли в аккаунт")
    else:
        markup = types.ReplyKeyboardMarkup()
        markup.row(buttons[6], buttons[7])
        bot.send_message(message.chat.id, "Неправильное имя или пароль аккаунта, попробуйте снова", reply_markup=markup)


def register_name_request(message):
    """
        Requests user_name

        :param message: button input
        :type message: telegram message
        :returns: nothing
        :rtype: None
    """
    markup = types.ReplyKeyboardMarkup()
    bot.send_message(message.chat.id, "Введите своё имя", reply_markup=markup)
    bot.register_next_step_handler(message, register_password_request)


def register_password_request(message):
    """
        Requests password

        :param message: user_name
        :type message: telegram message
        :returns: nothing
        :rtype: None
    """
    global user_name
    user_name = message.text
    conn = sqlite3.connect("user.sql")
    cur = conn.cursor()
    cur.execute(
        'SELECT * FROM tasks')
    tasks = cur.fetchall()
    user_names = set()
    for i in tasks:
        user_names.add(i[4])
    cur.close()
    conn.close()
    if user_name not in user_names:
        bot.send_message(message.chat.id, "Придумайте пароль")
        bot.register_next_step_handler(message, register)
    else:
        markup = types.ReplyKeyboardMarkup()
        markup.row(buttons[6], buttons[7])
        bot.send_message(message.chat.id, "Имя занято, попробуйте использовать другое", reply_markup=markup)


def register(message):
    """
        Creates new account and starts deadline date checker

        :param message: password
        :type message: telegram message
        :returns: nothing
        :rtype: None
    """
    global password
    password = message.text
    conn = sqlite3.connect("user.sql")
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO tasks (task_name, task, deadline, user_name, password) VALUES (?,?,?,?,?)',
        ("task0", "...", "00/00/00", user_name, password))
    conn.commit()
    t = Thread(target=deadline_message, args=(message,))
    t.start()
    cur.close()
    conn.close()
    default_buttons(message, "Пользователь зарегистрирован!")
    # bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAJm3WV4U5ub26eUHZPVGBjIRzUZMVubAAIQOAACBx4gSEXdJFaiRU3oMwQ')


def deadline_message(message):
    """
        Checks deadline dates and sends message when needed

        :param message: message from another function
        :type message: telegram message
        :returns: nothing
        :rtype: None
    """
    mentioned_tasks = []
    while True:
        cur_date = datetime.datetime.today()
        tomorrow = datetime.timedelta(days=1) + cur_date
        conn = sqlite3.connect("user.sql")
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM tasks')
        tasks = cur.fetchall()
        for i in tasks:
            if i not in mentioned_tasks and i[4] == user_name:
                if tomorrow.strftime('%d/%m/%y') == i[3]:
                    bot.send_message(message.chat.id, f"Скоро дедлайн задачи {i[1]}!")
                mentioned_tasks.append(i)
        cur.close()
        conn.close()


bot.polling(none_stop=True)
