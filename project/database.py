import sqlite3


def create_database():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS playerы
                 (id INTEGER PRIMARY KEY, health INTEGER, speed INTEGER, jump INTEGER, radition_protection INTEGER, pick INTEGER, strength INTEGER, cartridges INTEGER, price INTEGER)''')
    conn.commit()
    conn.close()


def reset_database():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM player')
    conn.commit()
    conn.close()


def write_to_database(data):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('REPLACE INTO player VALUES (?, ?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    conn.close()

def load_database():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM player')
    data = c.fetchone()
    conn.close()
    return list(data)



def load(data):
    
    player_dann = [data[0], round(5 * (1.2) ** data[1]), round(5 * (1.1) ** data[2]), data[3], round(100 * 1.9 ** data[4]), round(30 * 1.2 ** data[5]), data[6]]
    return list(player_dann)














