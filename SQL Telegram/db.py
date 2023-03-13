import sqlite3

with sqlite3.connect('database.db', check_same_thread=False) as db:
    cursor = db.cursor()

def test_table(user_id: str, user_name: str, user_data: str):
    cursor.execute('INSERT INTO test (user_id, user_name, user_data) VALUES(?, ?, ?)',
                       (user_id, user_name, user_data))
    db.commit()

# def test_table2(user_data: str):
#     update = "UPDATE test SET user_id = ?, where user_data "
#     cursor.executemany(user_data, update)
#     db.commit()

class DBService:
    def get_data(self):
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        data = cursor.execute('SELECT user_id, user_data FROM test').fetchall()
        return data

    def line(self):
        file = open("1.txt", "r")
        text = f'{file.readline()}{file.readline()}{file.readline()}{file.readline()}'
        print(text)

    def update_data(self):
        pass

    def create_data(self):
        pass

    def delete_data(self):
        pass
