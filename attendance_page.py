"""
صفحة رصد الحضور والغياب الشهري.
"""

import customtkinter as ctk

from database import get_connection, get_or_create_student


class AttendancePage(ctk.CTkFrame):
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
            self,
            text="رصد الحضور والغياب الشهري",
            font=("Segoe UI", 22, "bold"),
        ).pack(pady=(15, 20))

        self.a_student = self._create_input(self, "اسم الطالبة:")
        self.a_month = self._create_input(self, "الشهر والسنة (YYYY-MM):")
        self.a_total_days = self._create_input(
            self, "إجمالي الأيام المستحقة (مثال: 20):"
        )
        self.a_attended_days = self._create_input(
            self, "عدد أيام الحضور الفعلية:"
        )

        btn_a = ctk.CTkButton(
            self,
            text="حفظ ملخص الحضور الشهري",
            command=self.save_attendance,
            height=42,
            width=500,
            font=("Segoe UI", 14, "bold"),
            fg_color="#EF4444",
            hover_color="#DC2626",
        )
        btn_a.pack(pady=20)
        self.a_status = ctk.CTkLabel(self, text="", font=("Segoe UI", 13))
        self.a_status.pack()

    def save_attendance(self):
        student = self.a_student.get().strip()
        month_year = self.a_month.get().strip()
        total_str = self.a_total_days.get().strip()
        attended_str = self.a_attended_days.get().strip()

        if not all([student, month_year, total_str, attended_str]):
            self.a_status.configure(
                text="يرجى إدخال جميع البيانات!", text_color="#EF4444"
            )
            return

        try:
            total_days = int(total_str)
            attended_days = int(attended_str)

            if attended_days > total_days:
                self.a_status.configure(
                    text="خطأ: أيام الحضور لا يمكن أن تتجاوز الإجمالي!",
                    text_color="#EF4444",
                )
                return

            with get_connection(self.db_path) as conn:
                cursor = conn.cursor()
                student_id = get_or_create_student(
                    cursor, student, "غير محدد", "غير محدد", "عام"
                )

                cursor.execute(
                    """
                    INSERT INTO Attendance (student_id, month_year, total_days, attended_days) 
                    VALUES (?, ?, ?, ?)
                """,
                    (student_id, month_year, total_days, attended_days),
                )

                conn.commit()

            self.a_status.configure(
                text="تم حفظ بيانات الحضور الشهري بنجاح!", text_color="#10B981"
            )
            self.a_attended_days.delete(0, "end")
        except ValueError:
            self.a_status.configure(
                text="خطأ: يرجى كتابة أرقام صحيحة في عدد الأيام!",
                text_color="#EF4444",
            )
        except Exception as e:
            self.a_status.configure(text=f"خطأ: {e}", text_color="#EF4444")
