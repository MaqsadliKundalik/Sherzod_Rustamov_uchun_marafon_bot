from sqlite3 import Connection

conn = Connection('data.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users(id TEXT, name TEXT, reffer TEXT, subs TEXT)")
conn.commit()
conn.close()

def add_user(key, value, id):
    conn = Connection('data.db')
    c = conn.cursor()
    if type(value) == str: value.replace("\"", "''")
    if key == 'id': c.execute(f"INSERT INTO users ({key}) VALUES (\"{value}\")")
    else: c.execute(f"UPDATE users SET {key}=\"{value}\" WHERE id='{id}' ")
    conn.commit()
    conn.close()

def get_user(id):
    conn = Connection('data.db')
    c = conn.cursor()
    user = c.execute(f"SELECT * FROM users WHERE id='{id}' ").fetchone()
    conn.commit()
    conn.close()
    return user

def get_users():
    conn = Connection('data.db')
    c = conn.cursor()
    users = c.execute(f"SELECT * FROM users").fetchall()
    conn.commit()
    conn.close()
    res = []
    for i in users:
        if res.count(i) == 0: res.append(i)
    return res

def get_res(id):
    users = get_users()
    result = []
    for i in users:
        if i[3]:
            if i[3] == '1' and i[1]:
                k = 0
                for j in users:
                    if i[0] == j[2]: k += 1
                result.append((i[0], i[1], k))
    result.sort(key=lambda x: x[2], reverse=True)
    n = 1
    for i in result:
        if str(i[0]) == str(id):
            break
        n += 1
    return result, n

