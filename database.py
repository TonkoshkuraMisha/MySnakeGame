import sqlite3

db = sqlite3.connect('MySnake.sqlite')

cursor = db.cursor()
cursor.execute("""
create table if not exists RECORDS (
    name text,
    score integer
)""")


def insert_result(name, score):
    cursor.execute("""
    insert into RECORDS values (?, ?)
    """, (name, score))
    db.commit()


def get_best():
    cursor.execute("""
    SELECT name user, max(score) score FROM RECORDS
    GROUP by name
    ORDER by score DESC
    LIMIT 3
    """)
    return cursor.fetchall()

# insert_result('Tolja', 512)
# print(get_best())

# cursor.close()