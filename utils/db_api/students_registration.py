import sqlite3


class Students:
    def __init__(self, path_to_db="students.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple=None, fetchone=False,
                fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()
        connection = self.connection
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
        sql = "CREATE TABLE IF NOT EXISTS students(id INT PRIMARY KEY, group_ TEXT, full_name TEXT, language TEXT);"
        self.execute(sql, commit=True)

    def add_student(self, id, group, full_name, language):
        sql = "INSERT INTO students(id, group_, full_name, language) VALUES (?, ?, ?, ?)"
        parameters = (id, group, full_name, language)
        self.execute(sql, parameters=parameters, commit=True)

    def check(self, id):
        sql = f"SELECT * FROM students WHERE id={id}"
        return self.execute(sql, fetchone=True)

    def get_language(self, id) -> str:
        try:
            sql = f"SELECT language FROM students WHERE id={id}"
            return self.execute(sql, fetchone=True)[0]
        except TypeError:
            pass

    def get_info(self, id):
        sql_name = f"SELECT full_name FROM students WHERE id={id}"
        sql_group = f"SELECT group_ FROM students WHERE id=?"
        name = self.execute(sql_name, fetchone=True)
        group = self.execute(sql_group, parameters=(id,), fetchone=True)
        return f"Имя: {name[0]}, Группа: {group[0]}"

    def get_all_students(self):
        sql = "SELECT id FROM students"
        return self.execute(sql=sql, fetchall=True)

    def delete_for_edit(self, id):
        sql = f"DELETE FROM students WHERE id={id}"
        self.execute(sql=sql, commit=True)

    def delete(self):
        sql = "DROP TABLE students"
        self.execute(sql)


db_students = Students()
# db_students.create_table_users()
