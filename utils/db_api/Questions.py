import sqlite3


class Questions:
    def __init__(self, path_to_db="main.db"):
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
        sql = ("CREATE TABLE IF NOT EXISTS questions(id INT, theme TEXT, question TEXT, question_code INT, student TEXT)")
        self.execute(sql, commit=True)

    def add_question(self, id, theme, question, code, student):
        sql = "INSERT INTO questions(id, theme, question, question_code, student) VALUES (?, ?, ?, ?, ?)"
        parameters = (id, theme, question, code, student)
        self.execute(sql, parameters, commit=True)

    def get_receiver(self, code):
        sql = f"SELECT id FROM questions WHERE question_code={code}"
        return self.execute(sql, fetchone=True)

    def delete_question(self, code):
        sql = f"DELETE FROM questions WHERE question_code = {code}"
        self.execute(sql, commit=True)

    def get_question(self, code):
        sql = f"SELECT question FROM questions WHERE question_code = {code}"
        return self.execute(sql=sql, fetchone=True)

    def get_student(self, code):
        sql = f"SELECT student FROM questions WHERE question_code = {code}"
        return self.execute(sql=sql, fetchone=True)

    def check_existence(self, code):
        sql = f"SELECT * FROM questions WHERE question_code={code}"
        return self.execute(sql=sql, fetchone=True)

    def get_id(self, code):
        try:
            sql = f"SELECT id FROM questions WHERE question_code={code}"
            return self.execute(sql, fetchone=True)[0]
        except TypeError:
            pass

    def delete_all(self):
        sql = "DROP TABLE questions"
        self.execute(sql)


questions = Questions()

# def logger(statement):
#     print(f"""
#     -----------------------------------------------------
#     executing:
#     {statement}
#     ---------------------------------------
#         """)
