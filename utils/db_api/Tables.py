import psycopg2
from data import config


class DataBase:
    def __init__(self, path_to_db):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return psycopg2.connect(dsn=config.postgres_url)

    def execute(self, sql: str, params: tuple=None, fetchone: bool = False, fetchall: bool = False,
                commit: bool = False):
        if not params:
            params = tuple()

        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, params)

        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()

        connection.close()
        return data

    def create_table_users(self):
        sql = "CREATE TABLE IF NOT EXISTS Users(id INT PRIMARY KEY, group_name TEXT, full_name TEXT, language TEXT)"
        self.execute(sql, commit=True)

    def create_table_questions(self):
        sql = "CREATE TABLE IF NOT EXISTS questions(id INT, theme TEXT, question TEXT, student TEXT, code INT)"
        self.execute(sql=sql, commit=True)

    def create_table_answers(self):
        sql = "CREATE TABLE IF NOT EXISTS answers(id INT, question TEXT, answer TEXT, code INT)"
        self.execute(sql=sql, commit=True)

    def main_db(self):
        self.create_table_answers()
        self.create_table_questions()
        self.create_table_users()

    def insert_into_table(self, table: str, values: tuple):
        if table == "Users":
            sql_users = f"INSERT INTO Users(id, group_name, full_name, language) VALUES (?, ?, ?, ?)"
            self.execute(sql=sql_users, params=values, commit=True)
        if table == "questions":
            parameters_questions = "(id, theme, question, student, code)"
            sql_questions = f"INSERT INTO questions{parameters_questions} VALUES (?, ?, ?, ?, ?)"
            self.execute(sql=sql_questions, params=values, commit=True)
        if table == "answers":
            parameters_answers = "(id, question, answer, code)"
            sql_answers = f"INSERT INTO answers{parameters_answers} VALUES (?, ?, ?, ?)"
            self.execute(sql=sql_answers, params=values, commit=True)

    def check_existance(self, table: str, criteria: str, id: int):
        sql = f"SELECT * FROM {table} WHERE {criteria}={id}"
        return self.execute(sql=sql, fetchone=True)

    def get_language(self, id):
        sql = f"SELECT language FROM Users WHERE id={id}"
        result = self.execute(sql=sql, fetchone=True)
        return result[0]

    # it returns (element,), only 1 element
    def get_from_table(self, element: str, table: str, unique: str, argument: str):
        sql = f"SELECT {element} FROM {table} WHERE {unique}={argument}"
        result = self.execute(sql=sql, fetchone=True)
        return result[0]

    def get_all_students(self):
        sql = "SELECT id FROM Users"
        return self.execute(sql, fetchall=True)

    def delete_user(self, id):
        sql = f"DELETE FROM Users WHERE id={id}"
        self.execute(sql=sql, commit=True)

    def delete_table(self, table: str):
        sql = f"DROP TABLE {table}"
        self.execute(sql, commit=True)
