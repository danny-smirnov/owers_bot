import sqlite3

def add_client(user_id):  # Регистрация пользователя, добавление его user_id в бд
    try:
        con = sqlite3.connect('owers.db')
        cursor = con.cursor()
        cursor.execute("INSERT INTO client(user_id) VALUES (?)", (user_id,))
        con.commit()
        con.close()
    except:
        con.close()
        print('add_client_error')



def check_user_in_db(user_id):  # Проверка наличия пользователя в базе данных
    con = sqlite3.connect('owers.db')  # Возвращает True, если пользователь есть в бд, иначе False
    cursor = con.cursor()
    a = cursor.execute("SELECT * FROM client WHERE user_id = (?)", (user_id,))
    if a.fetchall() == []:
        con.close()
        return False
    con.close()
    return True


def get_state(user_id):  # Получает состояние пользователя на данный момент
    con = sqlite3.connect('owers.db')  # Возвращается число, которое связано с каким-либо состоянием
    cursor = con.cursor()
    a = cursor.execute("SELECT state FROM client WHERE user_id = (?)", (user_id,)).fetchone()
    con.close()
    return a[0]


def set_state(user_id, state):  # Записывает новое состояние пользователя в базу данных
    try:
        con = sqlite3.connect('owers.db')
        cursor = con.cursor()
        cursor.execute("UPDATE client SET state = (?) WHERE user_id = (?)", (state, user_id))
        con.commit()
        con.close()
    except:
        con.close()
        print('state_error')


def add_debt(ower, owe_to, amount, comment):  # Записывает новое состояние пользователя в базу данных
    try:
        con = sqlite3.connect('owers.db')
        cursor = con.cursor()
        cursor.execute("INSERT INTO history(ower, owe_to, amount, comment) VALUES (?, ?, ?, ?)", (ower, owe_to, amount, comment))
        con.commit()
        con.close()
    except:
        con.close()
        print('state_error')


def show_all_debts():
    con = sqlite3.connect('owers.db')  # Возвращается число, которое связано с каким-либо состоянием
    cursor = con.cursor()
    a = cursor.execute("SELECT * FROM history").fetchall()
    con.close()
    return a