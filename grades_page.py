"""
صفحة رصد درجات الاختبارات.
"""

import customtkinter as ctk

from database import get_connection, get_or_create_student


class GradesPage(ctk.CTkFrame):
    def __init__(self, parent, db_path):
        super().__init__(parent, fg_color="transparent")
        self.db_path = db_path
        self._build_ui()

    def _create_input(self, parent, label_text):
        lbl = ctk.CTkLabel(parent, text=label_text, font=("Segoe UI", 13))
        lbl.pack(anchor="e", padx=50, pady=(6, 2))
        entry = ctk.CTkEntry(
            parent,
            width=500,
            height=38,
            justify="right",
            font=("Segoe UI", 13),
        )
        entry.pack(pady=4)
        return entry

    def _build_ui(self):
        ctk.CTkLabel(
            self, text="رصد درجات الاختبارات", font=("Segoe UI", 22, "bold")
        ).pack(pady=(15, 20))

        scroll = ctk.CTkScrollableFrame(
            self, width=600, height=520, fg_color="transparent"
        )
        scroll.pack(fill="both", expand=True)

        self.g_student = self._create_input(scroll, "اسم الطالبة الثلاثي:")

        lbl_year = ctk.CTkLabel(
            scroll, text="السنة الدراسية:", font=("Segoe UI", 13)
        )
        lbl_year.pack(anchor="e", padx=50, pady=(5, 2))
        self.g_year = ctk.CTkComboBox(
            scroll,
            values=[
                "2023 - 2024",
                "2024 - 2025",
                "2025 - 2026",
                "2026 - 2027",
            ],
            width=500,
            height=38,
            justify="right",
            state="readonly",
        )
        self.g_year.set("2025 - 2026")
        self.g_year.pack(pady=4)

        lbl_term = ctk.CTkLabel(
            scroll, text="الفصل الدراسي:", font=("Segoe UI", 13)
        )
        lbl_term.pack(anchor="e", padx=50, pady=(5, 2))
        self.g_term = ctk.CTkComboBox(
            scroll,
            values=["الفصل الأول", "الفصل الثاني"],
            width=500,
            height=38,
            justify="right",
            state="readonly",
        )
        self.g_term.set("الفصل الأول")
        self.g_term.pack(pady=4)

        lbl_sec = ctk.CTkLabel(scroll, text="القسم:", font=("Segoe UI", 13))
        lbl_sec.pack(anchor="e", padx=50, pady=(5, 2))
        self.g_section = ctk.CTkComboBox(
            scroll,
            values=["عام", "تحفيظ"],
            width=500,
            height=38,
            justify="right",
            state="readonly",
        )
        self.g_section.set("عام")
        self.g_section.pack(pady=4)

        self.g_grade = self._create_input(scroll, "الصف الدراسي:")
        self.g_class = self._create_input(scroll, "الفصل:")
        self.g_subject = self._create_input(scroll, "المادة:")
        self.g_teacher = self._create_input(scroll, "اسم المعلمة:")
        self.g_exam = self._create_input(scroll, "نوع الاختبار:")
        self.g_score = self._create_input(scroll, "الدرجة المستحقة:")
        self.g_max = self._create_input(scroll, "الدرجة العظمى:")

        btn = ctk.CTkButton(
            scroll,
            text="حفظ الدرجة في قاعدة البيانات",
            command=self.save_grade,
            height=42,
            width=500,
            font=("Segoe UI", 14, "bold"),
            fg_color="#2563EB",
            hover_color="#1D4ED8",
        )
        btn.pack(pady=20)

        self.g_status = ctk.CTkLabel(scroll, text="", font=("Segoe UI", 13))
        self.g_status.pack()

    def save_grade(self):
        student = self.g_student.get().strip()
        academic_year = self.g_year.get()
        term = self.g_term.get()
        section = self.g_section.get()
        grade_lvl = self.g_grade.get().strip()
        cls_name = self.g_class.get().strip()
        subject = self.g_subject.get().strip()
        teacher = self.g_teacher.get().strip()
        exam = self.g_exam.get().strip()
        score_str = self.g_score.get().strip()
        max_str = self.g_max.get().strip()

        if not all([
            student,
            grade_lvl,
            cls_name,
            subject,
            teacher,
            exam,
            score_str,
            max_str,
        ]):
            self.g_status.configure(
                text="يرجى تعبئة جميع الحقول!", text_color="#EF4444"
            )
            return

        try:
            score = float(score_str)
            max_score = float(max_str)
            percentage = (score / max_score) * 100

            with get_connection(self.db_path) as conn:
                cursor = conn.cursor()

                student_id = get_or_create_student(
                    cursor, student, grade_lvl, cls_name, section
                )

                cursor.execute(
                    """
                    INSERT INTO Grades (student_id, academic_year, subject, teacher_name, exam_type, score, max_score, percentage, term)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        student_id,
                        academic_year,
                        subject,
                        teacher,
                        exam,
                        score,
                        max_score,
                        percentage,
                        term,
                    ),
                )

                conn.commit()

            self.g_status.configure(
                text="تم حفظ الدرجة بنجاح!", text_color="#10B981"
            )
            self.g_score.delete(0, "end")
        except ValueError:
            self.g_status.configure(
                text="خطأ: يرجى كتابة أرقام فقط في الدرجات!",
                text_color="#EF4444",
            )
        except Exception as e:
            self.g_status.configure(text=f"خطأ: {e}", text_color="#EF4444")
