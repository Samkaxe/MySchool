import sqlite3


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect("student_database.db")
        print("Connected to SQLite database")
    except sqlite3.Error as e:
        print(e)

    return conn


def create_student_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                class TEXT NOT NULL
            )
        """)
        print("Student table created")
    except sqlite3.Error as e:
        print(e)


def insert_student(conn, name, class_):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO students (name, class) VALUES (?, ?)
        """, (name, class_))
        conn.commit()
        print("Student data inserted")
    except sqlite3.Error as e:
        print(e)


def get_all_students(conn):
    students = []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        for row in rows:
            student = {
                "id": row[0],
                "name": row[1],
                "class": row[2]
            }
            students.append(student)
    except sqlite3.Error as e:
        print(e)
    return students


def delete_student(conn, student_id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        print(f"Student with ID {student_id} deleted")
    except sqlite3.Error as e:
        print(e)


def main():
    conn = create_connection()
    if conn:

        students = get_all_students(conn)
        print("List of students:")
        for student in students:
            print(student)

        delete_student_id = 1
        delete_student(conn, delete_student_id)

        conn.close()


if __name__ == "__main__":
    main()
