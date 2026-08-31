"""
صفحة تقييم المهارات (فيها صفوف ديناميكية يقدر المستخدم يضيف/يشيل منها).
"""

import customtkinter as ctk

from database import get_connection, get_or_create_student


class SkillsPage(ctk.CTkFrame):
    def __init__(self, parent, db_path):
        super().__init__(parent, fg_color="transparent")
        self.db_path = db_path
        self.skill_rows = []
        self._build_ui()
        self.add_skill_row()

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
            self, text="تقييم المهارات", font=("Segoe UI", 22, "bold")
        ).pack(pady=(10, 10))

        scroll_skills = ctk.CTkScrollableFrame(
            self, width=600, height=520, fg_color="transparent"
        )
        scroll_skills.pack(fill="both", expand=True)

        self.s_student = self._create_input(scroll_skills, "اسم الطالبة:")
        self.s_subject = self._create_input(scroll_skills, "المادة:")

        ctk.CTkLabel(
            scroll_skills,
            text="المهارات والتقييم:",
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="e", padx=50, pady=(15, 5))

        self.skills_container = ctk.CTkFrame(
            scroll_skills, fg_color="transparent"
        )
        self.skills_container.pack(fill="x", padx=50, pady=5)

        btn_add_skill = ctk.CTkButton(
            scroll_skills,
            text="+ إضافة مهارة أخرى",
            command=self.add_skill_row,
            height=32,
            width=200,
            font=("Segoe UI", 12, "bold"),
            fg_color="#374151",
            hover_color="#4B5563",
        )
        btn_add_skill.pack(anchor="e", padx=50, pady=5)

        btn_s = ctk.CTkButton(
            scroll_skills,
            text="حفظ جميع المهارات",
            command=self.save_skill,
            height=42,
            width=500,
            font=("Segoe UI", 14, "bold"),
            fg_color="#10B981",
            hover_color="#059669",
        )
        btn_s.pack(pady=20)

        self.s_status = ctk.CTkLabel(
            scroll_skills, text="", font=("Segoe UI", 13)
        )
        self.s_status.pack()

    def add_skill_row(self):
        row_frame = ctk.CTkFrame(self.skills_container, fg_color="transparent")
        row_frame.pack(fill="x", pady=4)

        btn_remove = ctk.CTkButton(
            row_frame,
            text="✕",
            width=30,
            height=36,
            fg_color="#EF4444",
            hover_color="#B91C1C",
            command=lambda: self.remove_skill_row(row_frame),
        )
        btn_remove.pack(side="left", padx=(0, 5))

        combo_status = ctk.CTkComboBox(
            row_frame,
            values=["متقن", "غير متقن"],
            width=130,
            height=36,
            justify="right",
            state="readonly",
        )
        combo_status.set("متقن")
        combo_status.pack(side="left", padx=5)

        entry_skill = ctk.CTkEntry(
            row_frame,
            placeholder_text="اسم المهارة",
            width=320,
            height=36,
            justify="right",
            font=("Segoe UI", 13),
        )
        entry_skill.pack(side="right", fill="x", expand=True)

        self.skill_rows.append({
            "frame": row_frame,
            "entry": entry_skill,
            "combo": combo_status,
        })

    def remove_skill_row(self, row_frame):
        if len(self.skill_rows) <= 1:
            return
        self.skill_rows = [
            r for r in self.skill_rows if r["frame"] != row_frame
        ]
        row_frame.destroy()

    def save_skill(self):
        student = self.s_student.get().strip()
        subject = self.s_subject.get().strip()

        if not student or not subject:
            self.s_status.configure(
                text="يرجى كتابة اسم الطالبة والمادة!", text_color="#EF4444"
            )
            return

        valid_entries = []
        for r in self.skill_rows:
            sk_name = r["entry"].get().strip()
            is_m = 1 if r["combo"].get() == "متقن" else 0
            if sk_name:
                valid_entries.append((sk_name, is_m))

        if not valid_entries:
            self.s_status.configure(
                text="يرجى كتابة مهارة واحدة على الأقل!", text_color="#EF4444"
            )
            return

        with get_connection(self.db_path) as conn:
            cursor = conn.cursor()
            student_id = get_or_create_student(
                cursor, student, "غير محدد", "غير محدد", "عام"
            )

            for sk_name, is_m in valid_entries:
                cursor.execute(
                    "INSERT INTO Skills (student_id, subject, skill_name, is_mastered) VALUES (?, ?, ?, ?)",
                    (student_id, subject, sk_name, is_m),
                )

            conn.commit()

        self.s_status.configure(
            text=f"تم حفظ ({len(valid_entries)}) مهارة بنجاح!",
            text_color="#10B981",
        )

        for item in self.skill_rows:
            item["frame"].destroy()
        self.skill_rows.clear()
        self.add_skill_row()
