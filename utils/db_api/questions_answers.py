import sqlite3
from data import config

class Answers: #переименовать
    def __init__(self):
        self.path_to_db = "answers_from_taecher.db"

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple=None, fetchone=False,
                fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()
        connection = self.connection
        # connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    # def list(self, table: str, fields="*"):
    #     sql = f"SELECT {fields} FROM {table}"
    #     result = self.execute(sql=sql)
    #     return result[0] if result else None
    #
    # def delete(self, table: str, id: int):
    #     self.execute(f"DELETE FROM {table} WHERE id={id}")

    # def get(self, table: str, id:int, fields="*"):
    #     sql = f"SELECT {fields} FROM {table} WHERE id={id}"
    #     result = self.execute(sql=sql, fetchone=True)
    #     return result[0] if result else None

    # def add(self, table: str, values: tuple):
    #     sql = f"INSERT INTO {table} {values}(question, code, student, answer) VALUES {values}(?, ?, ?, ?)"
    #     self.execute(sql, commit=True)

    def create_table_users(self):
        sql = ("CREATE TABLE IF NOT EXISTS answers(question TEXT, code INT, student TEXT, answer TEXT)")
        self.execute(sql, commit=True)

    def add_answer(self, question, code, student, answer):
        sql = "INSERT INTO answers(question, code, student, answer) VALUES (?, ?, ?, ?)"
        param = (question, code, student, answer)
        self.execute(sql=sql, parameters=param, commit=True)
        # self.add("answer", param)

    def check(self, code):
        sql = f"SELECT * FROM answers WHERE code={code}"
        return self.execute(sql=sql, fetchone=True)

    def get_question(self, code):
        # try:
        sql = f"SELECT question FROM answers WHERE code = {code}"
        print(f"Question: {self.execute(sql=sql, fetchone=True)[0]}")
        return self.execute(sql=sql, fetchone=True)[0]
        # except TypeError:
        #     pass

    def get_student(self, code):
        try:
            sql = f"SELECT student FROM answers WHERE code = {code}"
            return self.execute(sql=sql, fetchone=True)[0]
        except TypeError:
            pass

    def get_answer(self, code):
        try:
            sql = f"SELECT answer FROM answers WHERE code = {code}"
            return self.execute(sql=sql, fetchone=True)[0]
        except TypeError:
            pass


    def delete_all(self):
        sql = "DROP TABLE answers"
        self.execute(sql)


answers = Answers()
