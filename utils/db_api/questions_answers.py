import sqlite3


class Answers:
    def __init__(self, path_to_db="answers_from_teacher.db"):
        self.path_to_db = path_to_db

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

    def create_table_users(self):
        sql = ("CREATE TABLE IF NOT EXISTS answers(question TEXT, code INT, student TEXT, answer TEXT)")
        self.execute(sql, commit=True)

    def add_answer(self, question, code, student, answer):
        sql = "INSERT INTO answers(question, code, student, answer) VALUES (?, ?, ?, ?)"
        param = (question, code, student, answer)
        self.execute(sql=sql, parameters=param, commit=True)

    def check(self, code):
        sql = f"SELECT * FROM answers WHERE code={code}"
        return self.execute(sql=sql, fetchone=True)

    def get_question(self, code):
        try:
            sql = f"SELECT question FROM answers WHERE code = {code}"
            return self.execute(sql=sql, fetchone=True)[0]
        except TypeError:
            pass

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
