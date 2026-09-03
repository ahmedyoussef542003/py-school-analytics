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


def get_all_students(db_path):
    """جلب جميع الطالبات مرتبات بالأسم"""
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT student_id, student_name, grade_level, class_name, section 
            FROM Students 
            ORDER BY student_name
        """
        )
        return cursor.fetchall()


def delete_student_by_id(db_path, student_id):
    """حذف الطالبة مع كافة سجلاتها بفضل PRAGMA foreign_keys = ON"""
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM Students WHERE student_id = ?", (student_id,)
        )
        conn.commit()


# =========================================================
# ✅ الدوال الجديدة المضافة لتعديل بيانات الطالبة
# =========================================================

def get_student_by_id(db_path, student_id):
    """
    جلب بيانات طالبة محددة باستخدام ID
    """
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT student_id, student_name, grade_level, class_name, section
            FROM Students
            WHERE student_id = ?
            """,
            (student_id,)
        )
        return cursor.fetchone()


def update_student(db_path, student_id, name, grade_level, class_name, section):
    """
    تحديث بيانات طالبة موجودة
    """
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        
        # التحقق من وجود الطالبة
        cursor.execute(
            "SELECT student_id FROM Students WHERE student_id = ?",
            (student_id,)
        )
        if not cursor.fetchone():
            raise ValueError(f"الطالبة رقم {student_id} غير موجودة")
        
        # تحديث البيانات
        cursor.execute(
            """
            UPDATE Students
            SET student_name = ?,
                grade_level = ?,
                class_name = ?,
                section = ?
            WHERE student_id = ?
            """,
            (name, grade_level, class_name, section, student_id)
        )
        conn.commit()
        return True


def search_students(db_path, search_term):
    """
    البحث عن طالبات حسب الاسم
    """
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT student_id, student_name, grade_level, class_name, section 
            FROM Students 
            WHERE student_name LIKE ?
            ORDER BY student_name
            """,
            (f"%{search_term}%",)
        )
        return cursor.fetchall()


def get_students_count(db_path):
    """
    الحصول على عدد الطالبات الكلي
    """
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Students")
        return cursor.fetchone()[0]


def get_student_by_name(db_path, name):
    """
    جلب بيانات طالبة باستخدام الاسم
    """
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT student_id, student_name, grade_level, class_name, section
            FROM Students
            WHERE student_name = ?
            """,
            (name,)
        )
        return cursor.fetchone()


def get_students_by_grade(db_path, grade_level):
    """
    جلب جميع الطالبات في صف معين
    """
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT student_id, student_name, grade_level, class_name, section 
            FROM Students 
            WHERE grade_level = ?
            ORDER BY student_name
            """,
            (grade_level,)
        )
        return cursor.fetchall()


def get_students_by_section(db_path, section):
    """
    جلب جميع الطالبات في شعبة معينة
    """
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT student_id, student_name, grade_level, class_name, section 
            FROM Students 
            WHERE section = ?
            ORDER BY student_name
            """,
            (section,)
        )
        return cursor.fetchall()
