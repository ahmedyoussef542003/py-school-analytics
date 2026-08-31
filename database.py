"""
كل ما يخص قاعدة البيانات (الاتصال، إنشاء الجداول، إضافة/جلب الطالبة)
بحيث تستخدمه أي صفحة (page) بدون تكرار الكود.
"""

import sqlite3


def get_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path):
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT UNIQUE NOT NULL,
                grade_level TEXT NOT NULL,
                class_name TEXT NOT NULL,
                section TEXT NOT NULL DEFAULT 'عام'
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Grades (
                grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                academic_year TEXT NOT NULL DEFAULT '2025 - 2026',
                subject TEXT NOT NULL,
                teacher_name TEXT NOT NULL,
                exam_type TEXT NOT NULL,
                score REAL NOT NULL,
                max_score REAL NOT NULL,
                percentage REAL NOT NULL,
                term TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES Students (student_id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Skills (
                skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                subject TEXT NOT NULL,
                skill_name TEXT NOT NULL,
                is_mastered INTEGER NOT NULL,
                FOREIGN KEY (student_id) REFERENCES Students (student_id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Attendance (
                attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                month_year TEXT NOT NULL,
                total_days INTEGER NOT NULL,
                attended_days INTEGER NOT NULL,
                FOREIGN KEY (student_id) REFERENCES Students (student_id) ON DELETE CASCADE
            )
        """)
        conn.commit()


def get_or_create_student(cursor, name, grade, cls_name, section="عام"):
    cursor.execute(
        "SELECT student_id, section, grade_level, class_name FROM Students WHERE student_name = ?",
        (name,),
    )
    row = cursor.fetchone()
    if row:
        student_id = row[0]
        if (
            (section != "عام" and row[1] != section)
            or (grade != "غير محدد" and row[2] != grade)
            or (cls_name != "غير محدد" and row[3] != cls_name)
        ):
            cursor.execute(
                "UPDATE Students SET section = ?, grade_level = ?, class_name = ? WHERE student_id = ?",
                (
                    section if section != "عام" else row[1],
                    grade if grade != "غير محدد" else row[2],
                    cls_name if cls_name != "غير محدد" else row[3],
                    student_id,
                ),
            )
        return student_id

    cursor.execute(
        "INSERT INTO Students (student_name, grade_level, class_name, section) VALUES (?, ?, ?, ?)",
        (name, grade, cls_name, section),
    )
    return cursor.lastrowid
