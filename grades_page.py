"""
صفحة رصد درجات الاختبارات.
"""

import customtkinter as ctk
from tkinter import StringVar
import re

from database import get_connection, get_or_create_student, get_all_students, get_student_by_name


class GradesPage(ctk.CTkFrame):
    def __init__(self, parent, db_path):
        super().__init__(parent, fg_color="#FFFFFF")
        self.db_path = db_path
        self.all_students = []
        self.student_names = []
        self.current_matches = []
        self._build_ui()
        self._load_students()

    # =========================================================
    # قائمة المواد الدراسية في السعودية (المرحلة الابتدائية)
    # =========================================================
    
    SUBJECTS = [
        "القرآن الكريم",
        "التوحيد",
        "الفقه",
        "الحديث",
        "التفسير",
        "اللغة العربية",
        "الرياضيات",
        "العلوم",
        "الدراسات الإسلامية",
        "الدراسات الاجتماعية",
        "التربية الأسرية",
        "التربية الفنية",
        "التربية البدنية",
        "الحاسب الآلي",
        "اللغة الإنجليزية",
        "المهارات الحياتية",
    ]

    TEACHERS = [
        "أ. سارة أحمد",
        "أ. نورة محمد",
        "أ. فاطمة علي",
        "أ. منى خالد",
        "أ. حصة عبدالله",
        "أ. ليلى سلمان",
        "أ. عائشة عمر",
        "أ. مها سعيد",
        "أ. شيخة إبراهيم",
        "أ. نوال حسن",
    ]

    YEARS = [
        "2020 - 2021",
        "2021 - 2022",
        "2022 - 2023",
        "2023 - 2024",
        "2024 - 2025",
        "2025 - 2026",
        "2026 - 2027",
        "2027 - 2028",
        "2028 - 2029",
        "2029 - 2030",
    ]

    # =========================================================
    # بناء الواجهة
    # =========================================================

    def _create_input(self, parent, label_text, row, column, **kwargs):
        """إنشاء حقل إدخال مع تسمية"""
        lbl = ctk.CTkLabel(
            parent, 
            text=label_text, 
            font=("Cairo", 16, "bold"),
            text_color="#0F172A"
        )
        lbl.grid(row=row, column=column, padx=15, pady=(12, 4), sticky="e")
        
        entry = ctk.CTkEntry(
            parent,
            width=450,
            height=45,
            justify="right",
            font=("Cairo", 15),
            fg_color="#F8FAFC",
            border_color="#CBD5E1",
            border_width=2,
            corner_radius=10,
            **kwargs
        )
        entry.grid(row=row, column=column + 1, padx=15, pady=(8, 8), sticky="w")
        return entry

    def _build_ui(self):
        # العنوان
        ctk.CTkLabel(
            self, 
            text="📝 رصد درجات الاختبارات", 
            font=("Cairo", 28, "bold"),
            text_color="#0F172A"
        ).pack(pady=(20, 25))

        # إطار التمرير
        scroll = ctk.CTkScrollableFrame(
            self, 
            width=900, 
            height=650, 
            fg_color="transparent"
        )
        scroll.pack(fill="both", expand=True, padx=30, pady=15)

        # =========================================================
        # الصف 0: اسم الطالبة (مع زر للبحث)
        # =========================================================
        
        lbl_student = ctk.CTkLabel(
            scroll, 
            text="👩 اسم الطالبة الثلاثي:", 
            font=("Cairo", 16, "bold"),
            text_color="#0F172A"
        )
        lbl_student.grid(row=0, column=0, padx=15, pady=(12, 4), sticky="e")
        
        # إطار لحقل الإدخال والزر
        student_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        student_frame.grid(row=0, column=1, padx=15, pady=(8, 8), sticky="w")
        
        # حقل الإدخال
        self.student_var = StringVar()
        self.student_entry = ctk.CTkEntry(
            student_frame,
            width=350,
            height=45,
            justify="right",
            font=("Cairo", 15),
            fg_color="#F8FAFC",
            border_color="#CBD5E1",
            border_width=2,
            corner_radius=10,
            textvariable=self.student_var
        )
        self.student_entry.pack(side="left", padx=(0, 10))
        self.student_entry.bind("<KeyRelease>", self.on_student_type)
        
        # ✅ زر البحث عن الطالبات
        self.search_btn = ctk.CTkButton(
            student_frame,
            text="🔍 بحث",
            width=80,
            height=45,
            font=("Cairo", 14, "bold"),
            fg_color="#3B82F6",
            hover_color="#2563EB",
            corner_radius=10,
            command=self.show_student_suggestions
        )
        self.search_btn.pack(side="left")

        # ✅ حاوية القائمة المنسدلة (ستظهر عند الحاجة)
        self.suggestion_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        self.suggestion_frame.grid(row=1, column=1, padx=15, pady=(0, 5), sticky="w")
        self.suggestion_frame.grid_remove()  # مخفية افتراضياً

        # ✅ أزرار الاقتراحات (ستظهر ديناميكياً)
        self.suggestion_buttons = []

        # =========================================================
        # باقي الحقول
        # =========================================================
        
        # السنة الدراسية
        lbl_year = ctk.CTkLabel(
            scroll, 
            text="📅 السنة الدراسية:", 
            font=("Cairo", 16, "bold"),
            text_color="#0F172A"
        )
        lbl_year.grid(row=2, column=0, padx=15, pady=(12, 4), sticky="e")
        
        self.g_year = ctk.CTkComboBox(
            scroll,
            values=self.YEARS,
            width=450,
            height=45,
            justify="right",
            state="readonly",
            font=("Cairo", 15),
            fg_color="#F8FAFC",
            border_color="#CBD5E1",
            border_width=2,
            corner_radius=10,
            button_color="#3B82F6",
            button_hover_color="#2563EB"
        )
        self.g_year.set("2025 - 2026")
        self.g_year.grid(row=2, column=1, padx=15, pady=(8, 8), sticky="w")

        # الفصل الدراسي
        lbl_term = ctk.CTkLabel(
            scroll, 
            text="📖 الفصل الدراسي:", 
            font=("Cairo", 16, "bold"),
            text_color="#0F172A"
        )
        lbl_term.grid(row=3, column=0, padx=15, pady=(12, 4), sticky="e")
        
        self.g_term = ctk.CTkComboBox(
            scroll,
            values=["الفصل الأول", "الفصل الثاني"],
            width=450,
            height=45,
            justify="right",
            state="readonly",
            font=("Cairo", 15),
            fg_color="#F8FAFC",
            border_color="#CBD5E1",
            border_width=2,
            corner_radius=10,
            button_color="#3B82F6",
            button_hover_color="#2563EB"
        )
        self.g_term.set("الفصل الأول")
        self.g_term.grid(row=3, column=1, padx=15, pady=(8, 8), sticky="w")

        # القسم
        lbl_sec = ctk.CTkLabel(
            scroll, 
            text="🏫 القسم:", 
            font=("Cairo", 16, "bold"),
            text_color="#0F172A"
        )
        lbl_sec.grid(row=4, column=0, padx=15, pady=(12, 4), sticky="e")
        
        self.g_section = ctk.CTkComboBox(
            scroll,
            values=["عام", "تحفيظ"],
            width=450,
            height=45,
            justify="right",
            state="readonly",
            font=("Cairo", 15),
            fg_color="#F8FAFC",
            border_color="#CBD5E1",
            border_width=2,
            corner_radius=10,
            button_color="#3B82F6",
            button_hover_color="#2563EB"
        )
        self.g_section.set("عام")
        self.g_section.grid(row=4, column=1, padx=15, pady=(8, 8), sticky="w")

        # الصف الدراسي
        self.g_grade = self._create_input(
            scroll, "📚 الصف الدراسي:", 5, 0
        )

        # الفصل
        self.g_class = self._create_input(
            scroll, "📋 الفصل:", 6, 0
        )

        # المادة
        lbl_subject = ctk.CTkLabel(
            scroll, 
            text="📘 المادة:", 
            font=("Cairo", 16, "bold"),
            text_color="#0F172A"
        )
        lbl_subject.grid(row=7, column=0, padx=15, pady=(12, 4), sticky="e")
        
        self.g_subject = ctk.CTkComboBox(
            scroll,
            values=self.SUBJECTS,
            width=450,
            height=45,
            justify="right",
            state="readonly",
            font=("Cairo", 15),
            fg_color="#F8FAFC",
            border_color="#CBD5E1",
            border_width=2,
            corner_radius=10,
            button_color="#3B82F6",
            button_hover_color="#2563EB"
        )
        self.g_subject.set("اختر المادة...")
        self.g_subject.grid(row=7, column=1, padx=15, pady=(8, 8), sticky="w")

        # اسم المعلمة
        lbl_teacher = ctk.CTkLabel(
            scroll, 
            text="👩‍🏫 اسم المعلمة:", 
            font=("Cairo", 16, "bold"),
            text_color="#0F172A"
        )
        lbl_teacher.grid(row=8, column=0, padx=15, pady=(12, 4), sticky="e")
        
        self.g_teacher = ctk.CTkComboBox(
            scroll,
            values=self.TEACHERS,
            width=450,
            height=45,
            justify="right",
            state="readonly",
            font=("Cairo", 15),
            fg_color="#F8FAFC",
            border_color="#CBD5E1",
            border_width=2,
            corner_radius=10,
            button_color="#3B82F6",
            button_hover_color="#2563EB"
        )
        self.g_teacher.set("اختر المعلمة...")
        self.g_teacher.grid(row=8, column=1, padx=15, pady=(8, 8), sticky="w")

        # نوع الاختبار
        self.g_exam = self._create_input(
            scroll, "📝 نوع الاختبار:", 9, 0
        )

        # الدرجة المستحقة
        self.g_score = self._create_input(
            scroll, "⭐ الدرجة المستحقة:", 10, 0
        )

        # الدرجة العظمى
        self.g_max = self._create_input(
            scroll, "🎯 الدرجة العظمى:", 11, 0
        )

        # =========================================================
        # زر الحفظ
        # =========================================================
        
        btn_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        btn_frame.grid(row=12, column=0, columnspan=2, pady=25)

        btn = ctk.CTkButton(
            btn_frame,
            text="💾 حفظ الدرجة في قاعدة البيانات",
            command=self.save_grade,
            height=55,
            width=500,
            font=("Cairo", 18, "bold"),
            fg_color="#10B981",
            hover_color="#059669",
            text_color="white",
            corner_radius=14,
            border_width=1,
            border_color="#059669"
        )
        btn.pack()

        # =========================================================
        # حالة الحفظ
        # =========================================================
        
        self.g_status = ctk.CTkLabel(
            scroll, 
            text="", 
            font=("Cairo", 15, "bold")
        )
        self.g_status.grid(row=13, column=0, columnspan=2, pady=12)

    # =========================================================
    # دوال القائمة المنسدلة للطالبات (طريقة جديدة تعمل 100%)
    # =========================================================

    def _load_students(self):
        """تحميل جميع الطالبات من قاعدة البيانات"""
        try:
            self.all_students = get_all_students(self.db_path)
            self.student_names = [s[1] for s in self.all_students]
        except Exception as e:
            print(f"خطأ في تحميل الطلاب: {e}")
            self.student_names = []

    def on_student_type(self, event):
        """عند كتابة اسم الطالبة - البحث وعرض الاقتراحات"""
        text = self.student_entry.get().strip()
        
        # إخفاء القائمة إذا كان الحقل فارغاً
        if not text:
            self.suggestion_frame.grid_remove()
            return

        # البحث عن الأسماء المتطابقة
        self.current_matches = [name for name in self.student_names if text in name]
        
        if self.current_matches:
            self.show_suggestions(self.current_matches)
        else:
            self.suggestion_frame.grid_remove()

    def show_student_suggestions(self):
        """✅ عرض قائمة الاقتراحات عند الضغط على زر البحث"""
        text = self.student_entry.get().strip()
        
        if not text:
            # إذا كان الحقل فارغاً، عرض كل الطالبات
            self.current_matches = self.student_names[:10]  # عرض أول 10 فقط
        else:
            self.current_matches = [name for name in self.student_names if text in name]
        
        if self.current_matches:
            self.show_suggestions(self.current_matches)
        else:
            self.suggestion_frame.grid_remove()

    def show_suggestions(self, matches):
        """✅ عرض أزرار الاقتراحات"""
        # تنظيف الأزرار القديمة
        for btn in self.suggestion_buttons:
            btn.destroy()
        self.suggestion_buttons.clear()
        
        # إظهار الإطار
        self.suggestion_frame.grid()
        
        # إنشاء أزرار جديدة لكل اقتراح
        for i, name in enumerate(matches[:10]):  # عرض أول 10 اقتراحات فقط
            btn = ctk.CTkButton(
                self.suggestion_frame,
                text=name,
                font=("Cairo", 14),
                fg_color="#F8FAFC",
                text_color="#0F172A",
                hover_color="#DBEAFE",
                anchor="w",
                height=35,
                corner_radius=8,
                border_width=1,
                border_color="#CBD5E1",
                command=lambda n=name: self.select_student(n)
            )
            btn.pack(fill="x", pady=2)
            self.suggestion_buttons.append(btn)

    def select_student(self, selected_name):
        """✅ اختيار الطالبة من القائمة - يعمل 100%"""
        # تعيين الاسم في حقل الإدخال
        self.student_entry.delete(0, "end")
        self.student_entry.insert(0, selected_name)
        
        # إخفاء القائمة
        self.suggestion_frame.grid_remove()
        
        # تعبئة بيانات الطالبة
        self._auto_fill_student_data(selected_name)

    def _auto_fill_student_data(self, student_name):
        """تعبئة بيانات الطالبة تلقائياً عند الاختيار"""
        try:
            student = get_student_by_name(self.db_path, student_name)
            if student:
                # تعبئة الصف الدراسي
                self.g_grade.delete(0, "end")
                self.g_grade.insert(0, student[2])
                
                # تعبئة الفصل
                self.g_class.delete(0, "end")
                self.g_class.insert(0, student[3])
                
                # تعبئة القسم
                section = student[4]
                if section in ["عام", "تحفيظ"]:
                    self.g_section.set(section)
                
                self.g_status.configure(
                    text=f"✅ تم تحميل بيانات الطالبة: {student_name}",
                    text_color="#10B981"
                )
            else:
                self.g_status.configure(
                    text="⚠️ لم يتم العثور على الطالبة في قاعدة البيانات",
                    text_color="#F59E0B"
                )
        except Exception as e:
            print(f"خطأ في تحميل بيانات الطالبة: {e}")

    # =========================================================
    # دالة حفظ الدرجة
    # =========================================================

    def save_grade(self):
        student = self.student_entry.get().strip()
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

        # التحقق من صحة البيانات
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
                text="⚠️ يرجى تعبئة جميع الحقول!", 
                text_color="#EF4444"
            )
            return

        if subject == "اختر المادة..." or subject not in self.SUBJECTS:
            self.g_status.configure(
                text="⚠️ يرجى اختيار مادة صحيحة من القائمة!", 
                text_color="#EF4444"
            )
            return

        if teacher == "اختر المعلمة..." or teacher not in self.TEACHERS:
            self.g_status.configure(
                text="⚠️ يرجى اختيار معلمة صحيحة من القائمة!", 
                text_color="#EF4444"
            )
            return

        try:
            score = float(score_str)
            max_score = float(max_str)
            
            if score < 0 or max_score <= 0:
                self.g_status.configure(
                    text="⚠️ الدرجة يجب أن تكون أرقاماً موجبة!", 
                    text_color="#EF4444"
                )
                return
            
            if score > max_score:
                self.g_status.configure(
                    text="⚠️ الدرجة المستحقة لا يمكن أن تتجاوز الدرجة العظمى!", 
                    text_color="#EF4444"
                )
                return
                
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
                text=f"✅ تم حفظ درجة {subject} للطالبة {student} بنجاح!",
                text_color="#10B981"
            )
            
            self.g_score.delete(0, "end")
            self.g_max.delete(0, "end")
            self.g_exam.delete(0, "end")
            
            self._load_students()
            
        except ValueError:
            self.g_status.configure(
                text="⚠️ خطأ: يرجى كتابة أرقام فقط في الدرجات!",
                text_color="#EF4444",
            )
        except Exception as e:
            self.g_status.configure(text=f"⚠️ خطأ: {e}", text_color="#EF4444")