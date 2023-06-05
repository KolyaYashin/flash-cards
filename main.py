import sqlite3
import data.create_table

db = sqlite3.connect('data/cards.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS words (
                user_id BIGINT,
                en TEXT,
                ru TEXT,
                tag TEXT,
                date DATE,
                total SMALLINT,
                successful SMALLINT,
                winrate FLOAT,
                coef FLOAT
                )""")



db.commit()
sql.close()