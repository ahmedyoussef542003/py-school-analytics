from tkinter import messagebox
import customtkinter as ctk

from database import (
    delete_student_by_id,
    get_all_students,
    get_student_by_id,
    update_student,
    search_students
)


class StudentsPage(ctk.CTkFrame):

    def __init__(self, parent, db_path):
        # خلفية بيضاء
        super().__init__(parent, fg_color="#FFFFFF")
        self.db_path = db_path
        self.all_students = []  # لتخزين جميع الطلاب للبحث

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        # =========================================================
        # عنوان الصفحة مع إحصائيات
        # =========================================================
        
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(10, 15), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(
            header_frame, 
            text="👩‍🎓 إدارة الطالبات", 
            font=("Cairo", 24, "bold"),
            text_color="#0F172A"
        )
        self.title_label.pack(side="left", padx=10)
        
        self.stats_label = ctk.CTkLabel(
            header_frame,
            text="",
            font=("Cairo", 14),
            text_color="#64748B"
        )
        self.stats_label.pack(side="right", padx=10)

        # =========================================================
        # شريط البحث
        # =========================================================
        
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        search_frame.grid_columnconfigure(0, weight=1)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 ابحث عن طالبة بالاسم...",
            font=("Cairo", 14),
            fg_color="#F8FAFC",
            border_color="#CBD5E1",
            height=40,
            corner_radius=10
        )
        self.search_entry.pack(fill="x", padx=10)
        self.search_entry.bind("<KeyRelease>", self.filter_students)

        # =========================================================
        # إطار التمرير لعرض الطالبات
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
            row=2, column=0, padx=20, pady=10, sticky="nsew"
        )
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.refresh_students_list()

    # =========================================================
    # دوال البحث والفلترة
    # =========================================================
    
    def filter_students(self, event=None):
        """فلترة الطلاب حسب نص البحث"""
        search_text = self.search_entry.get().strip()
        
        if not search_text:
            # عرض جميع الطلاب
            self.display_students(self.all_students)
            return
        
        # البحث عن الطلاب المطابقين
        try:
            filtered = search_students(self.db_path, search_text)
            self.display_students(filtered)
        except Exception as e:
            print(f"خطأ في البحث: {e}")
            self.display_students([])

    # =========================================================
    # دوال عرض الطلاب
    # =========================================================
    
    def refresh_students_list(self):
        """تحديث قائمة الطلاب"""
        try:
            self.all_students = get_all_students(self.db_path)
            self.display_students(self.all_students)
        except Exception as e:
            messagebox.showerror(
                "خطأ", f"حدث خطأ أثناء جلب بيانات الطالبات:\n{e}"
            )
            self.display_students([])

    def display_students(self, students):
        """عرض قائمة الطلاب في الواجهة"""
        
        # تفريغ الواجهة القديمة
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # تحديث عدد الطلاب
        total = len(students)
        self.stats_label.configure(text=f"إجمالي الطالبات: {total} طالبة")

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
            item_frame.grid_columnconfigure(0, weight=3)
            item_frame.grid_columnconfigure(1, weight=1)

            # =========================================================
            # معلومات الطالبة
            # =========================================================
            
            info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
            info_frame.grid(row=0, column=0, sticky="w", padx=15, pady=10)
            
            # الصف الأول: اسم الطالبة مع رقم تسلسلي
            name_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            name_frame.pack(anchor="w")
            
            serial_label = ctk.CTkLabel(
                name_frame,
                text=f"#{index + 1}",
                font=("Cairo", 12, "bold"),
                text_color="#94A3B8",
                width=35
            )
            serial_label.pack(side="left", padx=(0, 8))
            
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
            # الأزرار (تعديل - حذف)
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
                command=lambda id=s_id: self.open_edit_window(id)
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
            # تأثير Hover على البطاقة
            # =========================================================
            
            def on_enter(e, frame=item_frame):
                frame.configure(fg_color="#F1F5F9", border_color="#3B82F6")
            
            def on_leave(e, frame=item_frame, bg=bg_color):
                frame.configure(fg_color=bg, border_color="#E2E8F0")
            
            item_frame.bind("<Enter>", on_enter)
            item_frame.bind("<Leave>", on_leave)

    # =========================================================
    # نافذة تعديل بيانات الطالبة
    # =========================================================
    
    def open_edit_window(self, student_id):
        """فتح نافذة تعديل بيانات الطالبة"""
        
        # جلب بيانات الطالبة
        try:
            student = get_student_by_id(self.db_path, student_id)
            if not student:
                messagebox.showerror("خطأ", "لم يتم العثور على الطالبة!")
                return
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ: {e}")
            return
        
        # إنشاء نافذة جديدة
        edit_window = ctk.CTkToplevel(self)
        edit_window.title("تعديل بيانات الطالبة")
        edit_window.geometry("550x650")
        edit_window.resizable(False, False)
        edit_window.grab_set()  # جعل النافذة مشروطة
        
        # جعل النافذة في المنتصف
        edit_window.update_idletasks()
        width = 550
        height = 650
        x = (edit_window.winfo_screenwidth() // 2) - (width // 2)
        y = (edit_window.winfo_screenheight() // 2) - (height // 2)
        edit_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # =========================================================
        # محتوى نافذة التعديل
        # =========================================================
        
        # العنوان
        title_label = ctk.CTkLabel(
            edit_window,
            text="✏️ تعديل بيانات الطالبة",
            font=("Cairo", 24, "bold"),
            text_color="#0F172A"
        )
        title_label.pack(pady=(25, 10))
        
        # خط فاصل
        separator = ctk.CTkFrame(
            edit_window,
            fg_color="#E2E8F0",
            height=2
        )
        separator.pack(fill="x", padx=40, pady=10)
        
        # =========================================================
        # نموذج الإدخال
        # =========================================================
        
        form_frame = ctk.CTkFrame(edit_window, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=40, pady=10)
        
        # ID الطالبة (للقراءة فقط)
        id_frame = ctk.CTkFrame(form_frame, fg_color="#F1F5F9", corner_radius=8)
        id_frame.pack(fill="x", pady=(0, 15))
        
        id_label = ctk.CTkLabel(
            id_frame,
            text=f"🆔 رقم الطالبة: {student_id}",
            font=("Cairo", 15, "bold"),
            text_color="#475569"
        )
        id_label.pack(pady=10)
        
        # حقل الاسم
        name_label = ctk.CTkLabel(
            form_frame,
            text="👩 اسم الطالبة:",
            font=("Cairo", 14, "bold"),
            text_color="#0F172A"
        )
        name_label.pack(anchor="w", pady=(5, 2))
        
        name_entry = ctk.CTkEntry(
            form_frame,
            font=("Cairo", 14),
            fg_color="#F8FAFC",
            border_color="#CBD5E1",
            height=45
        )
        name_entry.pack(fill="x", pady=(0, 10))
        name_entry.insert(0, student[1])  # student_name
        
        # حقل الصف
        grade_label = ctk.CTkLabel(
            form_frame,
            text="📚 الصف الدراسي:",
            font=("Cairo", 14, "bold"),
            text_color="#0F172A"
        )
        grade_label.pack(anchor="w", pady=(5, 2))
        
        grade_entry = ctk.CTkEntry(
            form_frame,
            font=("Cairo", 14),
            fg_color="#F8FAFC",
            border_color="#CBD5E1",
            height=45
        )
        grade_entry.pack(fill="x", pady=(0, 10))
        grade_entry.insert(0, student[2])  # grade_level
        
        # حقل الفصل
        class_label = ctk.CTkLabel(
            form_frame,
            text="📖 الفصل:",
            font=("Cairo", 14, "bold"),
            text_color="#0F172A"
        )
        class_label.pack(anchor="w", pady=(5, 2))
        
        class_entry = ctk.CTkEntry(
            form_frame,
            font=("Cairo", 14),
            fg_color="#F8FAFC",
            border_color="#CBD5E1",
            height=45
        )
        class_entry.pack(fill="x", pady=(0, 10))
        class_entry.insert(0, student[3])  # class_name
        
        # حقل الشعبة
        section_label = ctk.CTkLabel(
            form_frame,
            text="🏫 الشعبة:",
            font=("Cairo", 14, "bold"),
            text_color="#0F172A"
        )
        section_label.pack(anchor="w", pady=(5, 2))
        
        section_entry = ctk.CTkEntry(
            form_frame,
            font=("Cairo", 14),
            fg_color="#F8FAFC",
            border_color="#CBD5E1",
            height=45
        )
        section_entry.pack(fill="x", pady=(0, 10))
        section_entry.insert(0, student[4])  # section

        # =========================================================
        # أزرار الإجراءات (الحفظ والإلغاء)
        # =========================================================
        
        btn_frame = ctk.CTkFrame(edit_window, fg_color="transparent")
        btn_frame.pack(pady=(10, 25))
        
        # =========================================================
        # دالة حفظ التغييرات
        # =========================================================
        
        def save_changes():
            """حفظ التغييرات في قاعدة البيانات"""
            new_name = name_entry.get().strip()
            new_grade = grade_entry.get().strip()
            new_class = class_entry.get().strip()
            new_section = section_entry.get().strip()
            
            # التحقق من صحة البيانات
            if not new_name:
                messagebox.showerror("خطأ", "⚠️ يرجى إدخال اسم الطالبة!")
                name_entry.focus()
                return
            
            if not new_grade:
                messagebox.showerror("خطأ", "⚠️ يرجى إدخال الصف الدراسي!")
                grade_entry.focus()
                return
            
            if not new_class:
                messagebox.showerror("خطأ", "⚠️ يرجى إدخال الفصل!")
                class_entry.focus()
                return
            
            if not new_section:
                messagebox.showerror("خطأ", "⚠️ يرجى إدخال الشعبة!")
                section_entry.focus()
                return
            
            # تأكيد الحفظ
            confirm = messagebox.askyesno(
                "تأكيد الحفظ",
                f"هل أنت متأكد من حفظ التغييرات للطالبة:\n\n'{new_name}'؟"
            )
            
            if confirm:
                try:
                    # تحديث قاعدة البيانات
                    update_student(
                        self.db_path,
                        student_id,
                        new_name,
                        new_grade,
                        new_class,
                        new_section
                    )
                    
                    messagebox.showinfo(
                        "✅ تم التحديث",
                        f"تم تحديث بيانات الطالبة '{new_name}' بنجاح!"
                    )
                    
                    edit_window.destroy()  # إغلاق نافذة التعديل
                    self.refresh_students_list()  # تحديث القائمة الرئيسية
                    
                except Exception as e:
                    messagebox.showerror(
                        "خطأ",
                        f"حدث خطأ أثناء تحديث البيانات:\n{e}"
                    )
        
        # =========================================================
        # دالة إلغاء التعديل
        # =========================================================
        
        def cancel_changes():
            """إلغاء التعديل وإغلاق النافذة"""
            # التحقق من وجود تغييرات
            current_name = name_entry.get().strip()
            current_grade = grade_entry.get().strip()
            current_class = class_entry.get().strip()
            current_section = section_entry.get().strip()
            
            original_name = student[1]
            original_grade = student[2]
            original_class = student[3]
            original_section = student[4]
            
            # إذا كانت هناك تغييرات
            if (current_name != original_name or 
                current_grade != original_grade or 
                current_class != original_class or 
                current_section != original_section):
                
                if not messagebox.askyesno(
                    "تأكيد الإلغاء",
                    "⚠️ لديك تغييرات غير محفوظة!\n\nهل تريد إلغاء التعديلات؟"
                ):
                    return
            
            edit_window.destroy()
        
        # =========================================================
        # زر الحفظ (باللون الأخضر)
        # =========================================================
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="💾 حفظ التغييرات",
            font=("Cairo", 16, "bold"),
            fg_color="#10B981",
            hover_color="#059669",
            text_color="white",
            width=180,
            height=50,
            corner_radius=12,
            command=save_changes
        )
        save_btn.pack(side="left", padx=15)
        
        # =========================================================
        # زر الإلغاء (باللون الأحمر)
        # =========================================================
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="❌ إلغاء",
            font=("Cairo", 16, "bold"),
            fg_color="#EF4444",
            hover_color="#DC2626",
            text_color="white",
            width=180,
            height=50,
            corner_radius=12,
            command=cancel_changes
        )
        cancel_btn.pack(side="left", padx=15)
        
        # =========================================================
        # ربط مفاتيح الاختصار
        # =========================================================
        
        edit_window.bind("<Return>", lambda e: save_changes())
        edit_window.bind("<Escape>", lambda e: cancel_changes())

    # =========================================================
    # دالة تأكيد الحذف
    # =========================================================
    
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