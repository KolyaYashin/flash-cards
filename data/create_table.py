import sqlite3

db = sqlite3.connect('data/cards.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS words (
                front TEXT,
                back TEXT,
                ticket INT
                )""")


db.commit()
sql.close()