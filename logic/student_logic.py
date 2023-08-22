from data_access.database_manager import \
    create_connection, \
    create_student_table, \
    insert_student, \
    get_all_students, \
    delete_student


class StudentLogic:
    def __init__(self):
        self.conn = create_connection()
        if self.conn:
            create_student_table(self.conn)
        else:
            raise Exception("Could not establish a database connection")

    def add_student(self, name, class_):
        insert_student(self.conn, name, class_)

    def get_all_students(self):
        return get_all_students(self.conn)

    def delete_student(self, student_id):
        delete_student(self.conn, student_id)

    def close_connection(self):
        self.conn.close()
