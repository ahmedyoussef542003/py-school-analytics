from tkinter import messagebox
import customtkinter as ctk

from database import delete_student_by_id, get_all_students


class StudentsPage(ctk.CTkFrame):

    def __init__(self, parent, db_path):
        super().__init__(parent, fg_color="transparent")
        self.db_path = db_path

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # عنوان الصفحة
        self.title_label = ctk.CTkLabel(
            self, text="إدارة الطالبات 👩‍🎓", font=("Segoe UI", 20, "bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(10, 20))

        # إطار التمرير لعرض الطالبات
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self, label_text="قائمة الطالبات المسجلات"
        )
        self.scrollable_frame.grid(
            row=1, column=0, padx=20, pady=10, sticky="nsew"
        )
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.refresh_students_list()

    def refresh_students_list(self):
        # تفريغ الواجهة القديمة
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        try:
            students = get_all_students(self.db_path)
        except Exception as e:
            messagebox.showerror(
                "خطأ", f"حدث خطأ أثناء جلب بيانات الطالبات:\n{e}"
            )
            return

        if not students:
            no_data_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="لا يوجد طالبات مسجلات في قاعدة البيانات حالياً.",
                font=("Segoe UI", 14),
            )
            no_data_label.pack(pady=20)
            return

        for s_id, s_name, s_grade, s_class, s_section in students:
            item_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#2B2B2B")
            item_frame.pack(fill="x", expand=True, padx=10, pady=5)
            item_frame.grid_columnconfigure(0, weight=1)

            # تفاصيل الطالبة
            details_text = f"{s_name} | الصف: {s_grade} | الفصل: {s_class} | الشعبة: {s_section}"
            name_label = ctk.CTkLabel(
                item_frame,
                text=details_text,
                font=("Segoe UI", 13),
                anchor="w",
            )
            name_label.grid(row=0, column=0, padx=15, pady=12, sticky="w")

            # زر الحذف
            btn_delete = ctk.CTkButton(
                item_frame,
                text="حذف 🗑️",
                fg_color="#DC2626",
                hover_color="#991B1B",
                width=90,
                command=lambda id=s_id, name=s_name: self.confirm_delete(
                    id, name
                ),
            )
            btn_delete.grid(row=0, column=1, padx=15, pady=10)

    def confirm_delete(self, student_id, student_name):
        confirm = messagebox.askyesno(
            "تأكيد الحذف",
            f"هل أنت متأكد من حذف الطالبة:\n'{student_name}' ؟\n\nتنبيه: سيتم حذف جميع درجاتها، تقييماتها، وسجل غيابها تلقائياً.",
        )
        if confirm:
            try:
                delete_student_by_id(self.db_path, student_id)
                messagebox.showinfo("تم الحذف", "تم حذف الطالبة بنجاح.")
                self.refresh_students_list()
            except Exception as e:
                messagebox.showerror(
                    "خطأ", f"حدث خطأ أثناء محاولة الحذف:\n{e}"
                )