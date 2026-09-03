from tkinter import messagebox
import customtkinter as ctk

from database import delete_student_by_id, get_all_students


class StudentsPage(ctk.CTkFrame):

    def __init__(self, parent, db_path):
        # خلفية بيضاء
        super().__init__(parent, fg_color="#FFFFFF")
        self.db_path = db_path

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # =========================================================
        # عنوان الصفحة مع إحصائيات
        # =========================================================
        
        # إطار العنوان
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(10, 20), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        
        # العنوان الرئيسي
        self.title_label = ctk.CTkLabel(
            header_frame, 
            text="👩‍🎓 إدارة الطالبات", 
            font=("Cairo", 24, "bold"),
            text_color="#0F172A"
        )
        self.title_label.pack(side="left", padx=10)
        
        # إحصائيات الطالبات (سيتم تحديثها)
        self.stats_label = ctk.CTkLabel(
            header_frame,
            text="",
            font=("Cairo", 14),
            text_color="#64748B"
        )
        self.stats_label.pack(side="right", padx=10)

        # =========================================================
        # إطار التمرير لعرض الطالبات (بتصميم بطاقات)
        # =========================================================
        
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self, 
            label_text="📋 قائمة الطالبات المسجلات",
            fg_color="#F8FAFC",
            label_fg_color="#F8FAFC",
            label_text_color="#0F172A",
            label_font=("Cairo", 16, "bold")
        )
        self.scrollable_frame.grid(
            row=1, column=0, padx=20, pady=10, sticky="nsew"
        )
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.refresh_students_list()

    def refresh_students_list(self):
        """تحديث قائمة الطلاب وعرضها على شكل بطاقات"""
        
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

        # تحديث إحصائيات الطالبات
        total_students = len(students)
        self.stats_label.configure(text=f"إجمالي الطالبات: {total_students} طالبة")

        if not students:
            # عرض رسالة عند عدم وجود بيانات
            no_data_frame = ctk.CTkFrame(
                self.scrollable_frame,
                fg_color="transparent"
            )
            no_data_frame.pack(expand=True, fill="both", pady=50)
            
            no_data_icon = ctk.CTkLabel(
                no_data_frame,
                text="📭",
                font=("Segoe UI", 60)
            )
            no_data_icon.pack()
            
            no_data_label = ctk.CTkLabel(
                no_data_frame,
                text="لا يوجد طالبات مسجلات في قاعدة البيانات",
                font=("Cairo", 18, "bold"),
                text_color="#64748B"
            )
            no_data_label.pack(pady=10)
            
            no_data_sub = ctk.CTkLabel(
                no_data_frame,
                text="يمكنك إضافة طالبات جديدة من قائمة إدخال البيانات",
                font=("Cairo", 14),
                text_color="#94A3B8"
            )
            no_data_sub.pack()
            return

        # عرض الطالبات على شكل بطاقات
        for index, (s_id, s_name, s_grade, s_class, s_section) in enumerate(students):
            # =========================================================
            # بطاقة الطالبة
            # =========================================================
            
            # لون خلفية متناوب للبطاقات
            bg_color = "#FFFFFF" if index % 2 == 0 else "#FAFBFC"
            
            item_frame = ctk.CTkFrame(
                self.scrollable_frame,
                fg_color=bg_color,
                corner_radius=12,
                border_width=1,
                border_color="#E2E8F0",
            )
            item_frame.pack(fill="x", padx=10, pady=6)
            item_frame.grid_columnconfigure(0, weight=3)  # معلومات الطالبة
            item_frame.grid_columnconfigure(1, weight=1)  # الأزرار

            # =========================================================
            # الجانب الأيسر: معلومات الطالبة
            # =========================================================
            
            info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
            info_frame.grid(row=0, column=0, sticky="w", padx=15, pady=10)
            
            # الصف الأول: اسم الطالبة مع أيقونة ورقم تسلسلي
            name_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            name_frame.pack(anchor="w")
            
            # رقم تسلسلي
            serial_label = ctk.CTkLabel(
                name_frame,
                text=f"#{index + 1}",
                font=("Cairo", 12, "bold"),
                text_color="#94A3B8",
                width=35
            )
            serial_label.pack(side="left", padx=(0, 8))
            
            # اسم الطالبة مع أيقونة
            name_label = ctk.CTkLabel(
                name_frame,
                text=f"👩 {s_name}",
                font=("Cairo", 17, "bold"),
                text_color="#0F172A"
            )
            name_label.pack(side="left")
            
            # الصف الثاني: تفاصيل الطالبة
            details_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            details_frame.pack(anchor="w", pady=(4, 0))
            
            # تفاصيل الصف
            details = [
                ("📚", f"الصف: {s_grade}"),
                ("📖", f"الفصل: {s_class}"),
                ("🏫", f"الشعبة: {s_section}")
            ]
            
            for icon, text in details:
                detail_label = ctk.CTkLabel(
                    details_frame,
                    text=f"{icon} {text}",
                    font=("Cairo", 13),
                    text_color="#475569"
                )
                detail_label.pack(side="left", padx=(0, 15))

            # =========================================================
            # الجانب الأيمن: أزرار التحكم
            # =========================================================
            
            btn_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
            btn_frame.grid(row=0, column=1, sticky="e", padx=15, pady=10)
            
            # زر التعديل
            btn_edit = ctk.CTkButton(
                btn_frame,
                text="✏️ تعديل",
                font=("Cairo", 13, "bold"),
                fg_color="#3B82F6",
                hover_color="#2563EB",
                text_color="white",
                width=80,
                height=35,
                corner_radius=8,
                command=lambda id=s_id: self.edit_student(id)
            )
            btn_edit.pack(side="left", padx=(0, 8))
            
            # زر الحذف
            btn_delete = ctk.CTkButton(
                btn_frame,
                text="🗑️ حذف",
                font=("Cairo", 13, "bold"),
                fg_color="#EF4444",
                hover_color="#DC2626",
                text_color="white",
                width=80,
                height=35,
                corner_radius=8,
                command=lambda id=s_id, name=s_name: self.confirm_delete(id, name),
            )
            btn_delete.pack(side="left")

            # =========================================================
            # إضافة تأثير Hover للبطاقة
            # =========================================================
            
            def on_enter(e, frame=item_frame):
                frame.configure(fg_color="#F1F5F9", border_color="#3B82F6")
            
            def on_leave(e, frame=item_frame, bg=bg_color):
                frame.configure(fg_color=bg, border_color="#E2E8F0")
            
            item_frame.bind("<Enter>", on_enter)
            item_frame.bind("<Leave>", on_leave)

    def confirm_delete(self, student_id, student_name):
        """تأكيد حذف الطالبة"""
        confirm = messagebox.askyesno(
            "تأكيد الحذف",
            f"⚠️ هل أنت متأكد من حذف الطالبة:\n\n'{student_name}' ؟\n\n"
            f"📌 سيتم حذف جميع البيانات المرتبطة بها:\n"
            f"• الدرجات\n"
            f"• تقييم المهارات\n"
            f"• سجل الحضور والغياب",
            icon="warning"
        )
        if confirm:
            try:
                delete_student_by_id(self.db_path, student_id)
                messagebox.showinfo(
                    "✅ تم الحذف", 
                    f"تم حذف الطالبة '{student_name}' بنجاح."
                )
                self.refresh_students_list()
            except Exception as e:
                messagebox.showerror(
                    "خطأ", f"حدث خطأ أثناء محاولة الحذف:\n{e}"
                )

    def edit_student(self, student_id):
        """فتح نافذة تعديل بيانات الطالبة"""
        # يمكن إضافة نافذة تعديل هنا
        messagebox.showinfo(
            "تعديل بيانات",
            f"سيتم فتح نافذة تعديل بيانات الطالبة رقم: {student_id}"
        )

    # =========================================================
    # طريقة إضافية لترتيب الطلاب أبجدياً
    # =========================================================
    
    def sort_students(self, students, by="name"):
        """ترتيب الطلاب حسب الاسم أو الصف"""
        if by == "name":
            return sorted(students, key=lambda x: x[1])
        elif by == "grade":
            return sorted(students, key=lambda x: x[2])
        return students