import sqlite3



def add_sub(user_id):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"INSERT INTO users (user_id) VALUES ({user_id})")
    db.commit()


def check_sub(user_id):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
    if sql_cur.fetchall() == []:
        return False
    else:
        return True

def check_cat(user_id):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"SELECT categories from categories JOIN users on categories.id_user=users.id where user_id = '{user_id}'")
    if(sql_cur.fetchall() == []):
        return False
    else:
        return True

def ret_cat(user_id):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"SELECT categories from categories JOIN users on categories.id_user=users.id where user_id = '{user_id}'")
    return sql_cur.fetchall()[0][0]

def add_cat(user_id,cat):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"INSERT INTO categories (categories,id_user) SELECT '{cat}', id FROM users where user_id = '{user_id}' ")
    db.commit()

def del_cat(user_id):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"DELETE FROM categories WHERE categories.id IN (SELECT categories.Id FROM categories INNER JOIN users  ON users.id=categories.id_user  WHERE user_id='{user_id}') ")
    db.commit()

def check_kw(user_id):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"SELECT keywords from keywords JOIN users on keywords.id_user=users.id where user_id = '{user_id}'")
    if(sql_cur.fetchall() == []):
        return False
    else:
        return True

def ret_kw(user_id):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"SELECT keywords from keywords JOIN users on keywords.id_user=users.id where user_id = '{user_id}'")
    return sql_cur.fetchall()[0][0]

def add_kw(user_id,kw):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"INSERT INTO keywords (keywords,id_user) SELECT '{kw}', id FROM users where user_id = '{user_id}' ")
    db.commit()

def del_kw(user_id):
    db = sqlite3.connect("db.db")
    sql_cur = db.cursor()
    sql_cur.execute(f"DELETE FROM keywords WHERE keywords.id IN (SELECT keywords.Id FROM keywords INNER JOIN users  ON users.id=keywords.id_user  WHERE user_id='{user_id}') ")
    db.commit()

if __name__=="__main__": #для дебага
    pass