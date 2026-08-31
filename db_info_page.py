"""
صفحة عرض بيانات الاتصال بقاعدة البيانات وعدد السجلات في كل جدول.
"""

import customtkinter as ctk

from database import get_connection


class DbInfoPage(ctk.CTkFrame):
    def __init__(self, parent, db_path):
        super().__init__(parent, fg_color="transparent")
        self.db_path = db_path
        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(
            self, text="بيانات وقاعدة الاتصال", font=("Segoe UI", 22, "bold")
        ).pack(pady=(15, 10))

        ctk.CTkLabel(
            self,
            text=":مسار قاعدة البيانات الحالي",
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="e", padx=30, pady=(10, 2))
        self.entry_db_path = ctk.CTkEntry(
            self,
            width=550,
            height=35,
            font=("Consolas", 11),
            justify="left",
        )
        self.entry_db_path.pack(pady=5)
        self.entry_db_path.insert(0, self.db_path)
        self.entry_db_path.configure(state="readonly")

        self.scroll_db_info = ctk.CTkScrollableFrame(
            self, width=550, height=320, fg_color="#2B2B2B"
        )
        self.scroll_db_info.pack(fill="both", expand=True, padx=20, pady=10)

        btn_refresh_db = ctk.CTkButton(
            self,
            text="تحديث فحص الاتصال 🔄",
            command=self.refresh_db_info,
            height=38,
            width=250,
            font=("Segoe UI", 13, "bold"),
        )
        btn_refresh_db.pack(pady=10)

    def refresh_db_info(self):
        for widget in self.scroll_db_info.winfo_children():
            widget.destroy()

        tables = ["Students", "Grades", "Skills", "Attendance"]
        try:
            with get_connection(self.db_path) as conn:
                cursor = conn.cursor()

                ctk.CTkLabel(
                    self.scroll_db_info,
                    text="حالة الاتصال: متصل بنجاح ✅",
                    font=("Segoe UI", 14, "bold"),
                    text_color="#10B981",
                ).pack(pady=10)

                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    frame_row = ctk.CTkFrame(
                        self.scroll_db_info, fg_color="#1E1E1E"
                    )
                    frame_row.pack(fill="x", padx=10, pady=5)

                    ctk.CTkLabel(
                        frame_row,
                        text=f"جدول {table}",
                        font=("Segoe UI", 13, "bold"),
                    ).pack(side="right", padx=15, pady=8)
                    ctk.CTkLabel(
                        frame_row,
                        text=f"عدد السجلات: {count}",
                        font=("Segoe UI", 13),
                        text_color="#3B82F6",
                    ).pack(side="left", padx=15, pady=8)

        except Exception as e:
            ctk.CTkLabel(
                self.scroll_db_info,
                text=f"خطأ في الاتصال: {e} ❌",
                font=("Segoe UI", 13),
                text_color="#EF4444",
            ).pack(pady=10)
