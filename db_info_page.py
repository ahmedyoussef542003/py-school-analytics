"""
صفحة عرض بيانات الاتصال بقاعدة البيانات وعدد السجلات مع زر اختيار المسار المحفوظ.
"""

from tkinter import filedialog
import customtkinter as ctk

from database import get_connection


class DbInfoPage(ctk.CTkFrame):

    def __init__(self, parent, db_path, on_db_change_callback=None):
        super().__init__(parent, fg_color="transparent")
        self.db_path = db_path
        self.on_db_change_callback = on_db_change_callback
        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(
            self, text="بيانات وقاعدة الاتصال", font=("Segoe UI", 22, "bold")
        ).pack(pady=(15, 10))

        # إطار أفقي للمسار مع زر البراوز (Browse)
        frame_path = ctk.CTkFrame(self, fg_color="transparent")
        frame_path.pack(pady=5)

        ctk.CTkLabel(
            frame_path,
            text=":مسار قاعدة البيانات الحالي",
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="e", padx=5, pady=(5, 2))

        self.entry_db_path = ctk.CTkEntry(
            frame_path,
            width=420,
            height=35,
            font=("Consolas", 11),
            justify="left",
        )
        self.entry_db_path.pack(side="left", padx=(0, 5))
        self.entry_db_path.insert(0, self.db_path)
        self.entry_db_path.configure(state="readonly")

        # زر اختيار مسار جديد
        btn_browse = ctk.CTkButton(
            frame_path,
            text="تغيير المسار 📁",
            command=self.browse_new_db,
            width=120,
            height=35,
            font=("Segoe UI", 12, "bold"),
        )
        btn_browse.pack(side="right")

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

    def browse_new_db(self):
        """فتح نافذة اختيار الملفات واستدعاء دالة الحفظ والتحديث"""
        selected_file = filedialog.askopenfilename(
            title="اختر ملف قاعدة البيانات",
            filetypes=[("SQLite Database", "*.db"), ("All Files", "*.*")],
        )

        if selected_file:
            self.db_path = selected_file

            # تحديث حقل المسار المعروض
            self.entry_db_path.configure(state="normal")
            self.entry_db_path.delete(0, "end")
            self.entry_db_path.insert(0, self.db_path)
            self.entry_db_path.configure(state="readonly")

            # إبلاغ main.py بالتعديل لحفظه في config.json وتطبيقه على باقي الصفحات
            if self.on_db_change_callback:
                self.on_db_change_callback(self.db_path)

            # إعادة فحص الاتصال وقراءة السجلات من الملف الجديد
            self.refresh_db_info()

    def refresh_db_info(self):
        """إعادة فحص الاتصال وحساب السجلات داخل الجداول"""
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