from tkinter import ttk
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import get_connection

plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'Tahoma']
plt.rcParams['axes.unicode_minus'] = False


class OverviewDashboardPage(ctk.CTkFrame):

    def __init__(self, parent, db_path):
        # تغيير الخلفية إلى أبيض
        super().__init__(parent, fg_color="#FFFFFF")
        self.db_path = db_path

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------------- 1. شريط الفلاتر الجانبي ----------------
        self.sidebar = ctk.CTkScrollableFrame(
            self, width=220, fg_color="#F8FAFC"  # تغيير إلى أبيض فاتح
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # فلتر نوع الامتحان
        ctk.CTkLabel(
            self.sidebar,
            text="نوع الامتحان",
            font=("Segoe UI", 12, "bold"),
            text_color="#0F172A",  # تغيير إلى غامق
        ).pack(anchor="w", padx=10, pady=(10, 2))
        self.filter_exam = ctk.CTkOptionMenu(
            self.sidebar, 
            values=["All"], 
            command=self.refresh_dashboard,
            fg_color="#FFFFFF",
            button_color="#E2E8F0",
            button_hover_color="#CBD5E1",
            text_color="#0F172A",
        )
        self.filter_exam.pack(fill="x", padx=10, pady=2)

        # فلتر القسم
        ctk.CTkLabel(
            self.sidebar,
            text="القسم",
            font=("Segoe UI", 12, "bold"),
            text_color="#0F172A",
        ).pack(anchor="w", padx=10, pady=(8, 2))
        self.filter_section = ctk.CTkOptionMenu(
            self.sidebar, 
            values=["All"], 
            command=self.refresh_dashboard,
            fg_color="#FFFFFF",
            button_color="#E2E8F0",
            button_hover_color="#CBD5E1",
            text_color="#0F172A",
        )
        self.filter_section.pack(fill="x", padx=10, pady=2)

        # فلتر الصف
        ctk.CTkLabel(
            self.sidebar,
            text="الصف",
            font=("Segoe UI", 12, "bold"),
            text_color="#0F172A",
        ).pack(anchor="w", padx=10, pady=(8, 2))
        self.filter_grade = ctk.CTkOptionMenu(
            self.sidebar, 
            values=["All"], 
            command=self.refresh_dashboard,
            fg_color="#FFFFFF",
            button_color="#E2E8F0",
            button_hover_color="#CBD5E1",
            text_color="#0F172A",
        )
        self.filter_grade.pack(fill="x", padx=10, pady=2)

        # فلتر السنة الدراسية
        ctk.CTkLabel(
            self.sidebar,
            text="السنة الدراسية",
            font=("Segoe UI", 12, "bold"),
            text_color="#0F172A",
        ).pack(anchor="w", padx=10, pady=(8, 2))
        self.filter_year = ctk.CTkOptionMenu(
            self.sidebar, 
            values=["All"], 
            command=self.refresh_dashboard,
            fg_color="#FFFFFF",
            button_color="#E2E8F0",
            button_hover_color="#CBD5E1",
            text_color="#0F172A",
        )
        self.filter_year.pack(fill="x", padx=10, pady=2)

        # فلتر اسم الطالب
        ctk.CTkLabel(
            self.sidebar,
            text="اسم الطالب",
            font=("Segoe UI", 12, "bold"),
            text_color="#0F172A",
        ).pack(anchor="w", padx=10, pady=(8, 2))
        self.filter_student = ctk.CTkOptionMenu(
            self.sidebar, 
            values=["All"], 
            command=self.refresh_dashboard,
            fg_color="#FFFFFF",
            button_color="#E2E8F0",
            button_hover_color="#CBD5E1",
            text_color="#0F172A",
        )
        self.filter_student.pack(fill="x", padx=10, pady=2)

        # فلتر المادة
        ctk.CTkLabel(
            self.sidebar,
            text="المادة",
            font=("Segoe UI", 12, "bold"),
            text_color="#0F172A",
        ).pack(anchor="w", padx=10, pady=(8, 2))
        self.filter_subject = ctk.CTkOptionMenu(
            self.sidebar, 
            values=["All"], 
            command=self.refresh_dashboard,
            fg_color="#FFFFFF",
            button_color="#E2E8F0",
            button_hover_color="#CBD5E1",
            text_color="#0F172A",
        )
        self.filter_subject.pack(fill="x", padx=10, pady=2)

        # ---------------- 2. منطقة المحتوى الرئيسية ----------------
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            self.main_content,
            text="نظرة عامة لأداء الطلاب خلال الدراسة",
            font=("Segoe UI", 22, "bold"),
            text_color="#0F172A",  # تغيير إلى غامق
        ).grid(row=0, column=0, pady=(0, 15))

        # ---------------- 3. بطاقات المؤشرات KPIs ----------------
        self.kpi_frame = ctk.CTkFrame(
            self.main_content, fg_color="transparent"
        )
        self.kpi_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        for i in range(5):
            self.kpi_frame.grid_columnconfigure(i, weight=1)

        self.kpi_total = self.create_kpi_card(
            self.kpi_frame, 0, "العدد الكلي للطلاب", "0", "#F0F9FF", "#0F172A"
        )
        self.kpi_avg = self.create_kpi_card(
            self.kpi_frame, 1, "متوسط الدرجات", "0.00", "#F0FDF4", "#0F172A"
        )
        self.kpi_pass = self.create_kpi_card(
            self.kpi_frame, 2, "% نسبة النجاح", "0.00", "#FEFCE8", "#854D0E"
        )
        self.kpi_improve = self.create_kpi_card(
            self.kpi_frame, 3, "عدد الطلاب للتحسين", "0", "#FEF3C7", "#92400E"
        )
        self.kpi_struggle = self.create_kpi_card(
            self.kpi_frame,
            4,
            "عدد الطلاب المتعثرين",
            "0",
            "#FEE2E2",
            "#991B1B",
        )

        # ---------------- 4. حاوية الرسم البياني ----------------
        self.chart_container = ctk.CTkFrame(
            self.main_content, fg_color="#F8FAFC", height=230  # تغيير إلى أبيض فاتح
        )
        self.chart_container.grid(
            row=2, column=0, sticky="nsew", pady=(0, 15)
        )
        self.chart_canvas = None

        # ---------------- 5. الجدول التفصيلي ----------------
        self.table_frame = ctk.CTkFrame(
            self.main_content, fg_color="#F8FAFC", height=200  # تغيير إلى أبيض فاتح
        )
        self.table_frame.grid(row=3, column=0, sticky="nsew")

        self.setup_table()
        self.populate_filters()
        self.refresh_dashboard()

    def create_kpi_card(self, parent, col, title, value, bg_color, text_color):
        card = ctk.CTkFrame(
            parent, fg_color=bg_color, corner_radius=10, border_width=1,
            border_color="#E2E8F0"
        )
        card.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")

        lbl_val = ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 24, "bold"),
            text_color=text_color,
        )
        lbl_val.pack(pady=(10, 0))

        lbl_title = ctk.CTkLabel(
            card, text=title, font=("Segoe UI", 11), text_color=text_color
        )
        lbl_title.pack(pady=(0, 10))

        return lbl_val

    def _update_single_filter(self, cursor, query, menu, current_val, reverse_words=False):
        """دالة مساعدة لربط القوائم وحفظ خيار المستخدم الحالي مع ضبط اتجاه الكلمات"""
        cursor.execute(query)
        items = [
            str(r[0])
            for r in cursor.fetchall()
            if r[0] is not None and str(r[0]).strip() != ""
        ]
        
        cleaned_items = sorted(list(set(items)))
        
        if reverse_words:
            display_options = ["All"] + [" ".join(item.split()[::-1]) for item in cleaned_items]
        else:
            display_options = ["All"] + cleaned_items

        menu.configure(values=display_options)
        if current_val in display_options:
            menu.set(current_val)
        else:
            menu.set("All")

    def populate_filters(self):
        """جلب ديناميكي ودقيق لكافة الفلاتر من قاعدة البيانات"""
        try:
            with get_connection(self.db_path) as conn:
                cursor = conn.cursor()

                # 1. نوع الامتحان (من جدول Grades)
                self._update_single_filter(
                    cursor,
                    "SELECT DISTINCT exam_type FROM Grades WHERE exam_type IS NOT NULL AND TRIM(exam_type) != ''",
                    self.filter_exam,
                    self.filter_exam.get(),
                )

                # 2. القسم (من جدول Students)
                self._update_single_filter(
                    cursor,
                    "SELECT DISTINCT section FROM Students WHERE section IS NOT NULL AND TRIM(section) != ''",
                    self.filter_section,
                    self.filter_section.get(),
                )

                # 3. الصف (من جدول Students)
                self._update_single_filter(
                    cursor,
                    "SELECT DISTINCT grade_level FROM Students WHERE grade_level IS NOT NULL AND TRIM(grade_level) != ''",
                    self.filter_grade,
                    self.filter_grade.get(),
                )

                # 4. السنة الدراسية (من جدول Grades)
                self._update_single_filter(
                    cursor,
                    "SELECT DISTINCT academic_year FROM Grades WHERE academic_year IS NOT NULL AND TRIM(academic_year) != ''",
                    self.filter_year,
                    self.filter_year.get(),
                )

                # 5. اسم الطالب (تطبيق عكس اتجاه الكلمات لتعديل المحاذاة)
                self._update_single_filter(
                    cursor,
                    "SELECT DISTINCT student_name FROM Students WHERE student_name IS NOT NULL AND TRIM(student_name) != ''",
                    self.filter_student,
                    self.filter_student.get(),
                    reverse_words=True
                )

                # 6. المادة (من جدول Grades)
                self._update_single_filter(
                    cursor,
                    "SELECT DISTINCT subject FROM Grades WHERE subject IS NOT NULL AND TRIM(subject) != ''",
                    self.filter_subject,
                    self.filter_subject.get(),
                )
        except Exception as e:
            print(f"Filter Load Error: {e}")

    def setup_table(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#FFFFFF",  # تغيير إلى أبيض
            foreground="#0F172A",  # تغيير إلى غامق
            fieldbackground="#FFFFFF",  # تغيير إلى أبيض
            rowheight=28,
        )
        style.configure(
            "Treeview.Heading",
            background="#F1F5F9",  # تغيير إلى رمادي فاتح
            foreground="#0F172A",  # تغيير إلى غامق
            font=("Segoe UI", 10, "bold"),
        )
        # تغيير لون التحديد
        style.map(
            "Treeview",
            background=[("selected", "#3B82F6")],
            foreground=[("selected", "white")],
        )

        cols = (
            "student_name",
            "grade_level",
            "followup",
            "failed_count",
            "absence",
            "status",
        )
        self.tree = ttk.Treeview(
            self.table_frame, columns=cols, show="headings", height=6
        )

        headers = {
            "student_name": "اسم الطالب",
            "grade_level": "الصف الدراسي",
            "followup": "متابعة الطالب",
            "failed_count": "عدد المواد الراسب بها",
            "absence": "نسبة الغياب",
            "status": "التقدير العام للطالب",
        }

        for col, text in headers.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, anchor="center", width=120)

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

    def refresh_dashboard(self, *args):
        self.populate_filters()

        student_conditions = []
        grade_conditions = []
        params_student = []
        params_grade = []

        if self.filter_section.get() != "All":
            student_conditions.append("s.section = ?")
            params_student.append(self.filter_section.get())

        if self.filter_grade.get() != "All":
            student_conditions.append("s.grade_level = ?")
            params_student.append(self.filter_grade.get())

        if self.filter_student.get() != "All":
            # إعادة ترتيب الكلمات للنص الحقيقي قبل الاستعلام
            selected_student = " ".join(self.filter_student.get().split()[::-1])
            student_conditions.append("s.student_name = ?")
            params_student.append(selected_student)

        if self.filter_exam.get() != "All":
            grade_conditions.append("g.exam_type = ?")
            params_grade.append(self.filter_exam.get())

        if self.filter_subject.get() != "All":
            grade_conditions.append("g.subject = ?")
            params_grade.append(self.filter_subject.get())

        if self.filter_year.get() != "All":
            grade_conditions.append("g.academic_year = ?")
            params_grade.append(self.filter_year.get())

        where_student = (
            " WHERE " + " AND ".join(student_conditions)
            if student_conditions
            else ""
        )
        where_grade = (
            " WHERE " + " AND ".join(grade_conditions)
            if grade_conditions
            else ""
        )

        all_params = params_grade + params_student

        with get_connection(self.db_path) as conn:
            cursor = conn.cursor()

            query = f"""
            WITH SubjectScores AS (
                SELECT 
                    g.student_id,
                    g.subject,
                    SUM(g.score) AS total_score,
                    SUM(g.max_score) AS total_max,
                    (SUM(g.score) * 100.0 / NULLIF(SUM(g.max_score), 0)) AS subject_percentage
                FROM Grades g
                {where_grade}
                GROUP BY g.student_id, g.subject
            ),
            StudentSummary AS (
                SELECT 
                    s.student_id,
                    s.student_name,
                    s.grade_level,
                    COUNT(CASE WHEN sub.subject_percentage < 60 THEN 1 END) AS failed_subjects_count,
                    COALESCE((SUM(sub.total_score) * 100.0 / NULLIF(SUM(sub.total_max), 0)), 0) AS overall_percentage
                FROM Students s
                INNER JOIN SubjectScores sub ON s.student_id = sub.student_id
                {where_student}
                GROUP BY s.student_id
            )
            SELECT 
                student_name,
                grade_level,
                failed_subjects_count,
                overall_percentage,
                CASE 
                    WHEN failed_subjects_count > 0 THEN 'متعثر'
                    WHEN overall_percentage >= 85 THEN 'ممتاز'
                    WHEN overall_percentage >= 75 THEN 'جيد جداً'
                    WHEN overall_percentage >= 60 THEN 'جيد'
                    ELSE 'متعثر'
                END AS grade_status,
                CASE 
                    WHEN failed_subjects_count > 0 THEN 'خطر عالٍ'
                    WHEN overall_percentage >= 60 AND overall_percentage < 75 THEN 'متابعة'
                    ELSE ''
                END AS student_followup
            FROM StudentSummary;
            """
            cursor.execute(query, all_params)
            rows = cursor.fetchall()

        total_students = len(rows)
        struggling_count = sum(1 for r in rows if r[4] == "متعثر")
        improving_count = sum(1 for r in rows if r[5] == "متابعة")
        avg_score = (
            sum(r[3] for r in rows) / total_students if total_students > 0 else 0
        )
        pass_rate = (
            ((total_students - struggling_count) / total_students)
            if total_students > 0
            else 0
        )

        self.kpi_total.configure(text=str(total_students))
        self.kpi_avg.configure(text=f"{avg_score:.2f}")
        self.kpi_pass.configure(text=f"{pass_rate:.2f}")
        self.kpi_improve.configure(text=str(improving_count))
        self.kpi_struggle.configure(text=str(struggling_count))

        for item in self.tree.get_children():
            self.tree.delete(item)

        for r in rows:
            self.tree.insert(
                "",
                "end",
                values=(r[0], r[1], r[5], r[2], "0.00", r[4]),
            )

        self.render_bar_chart(rows)

    def render_bar_chart(self, rows):
        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()

        categories = ["جيد جداً", "جيد", "ممتاز", "متعثر"]
        counts = [
            sum(1 for r in rows if r[4] == "جيد جداً"),
            sum(1 for r in rows if r[4] == "جيد"),
            sum(1 for r in rows if r[4] == "ممتاز"),
            sum(1 for r in rows if r[4] == "متعثر"),
        ]
        colors = ["#78E5A0", "#E6C86E", "#78E5A0", "#F56969"]

        fig, ax = plt.subplots(figsize=(8, 2.2), facecolor="#F8FAFC")  # تغيير الخلفية
        ax.set_facecolor("#F8FAFC")  # تغيير الخلفية

        bars = ax.barh(categories, counts, color=colors, height=0.55)

        ax.tick_params(colors="#0F172A", labelsize=10)  # تغيير لون النص
        ax.spines["bottom"].set_color("#CBD5E1")
        ax.spines["left"].set_color("#CBD5E1")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_title(
            "عدد الطلاب لكل تقدير", color="#0F172A", fontname="Segoe UI", fontsize=12
        )

        for bar in bars:
            width = bar.get_width()
            if width > 0:
                ax.text(
                    width + 0.05,
                    bar.get_y() + bar.get_height() / 2,
                    f"{int(width)}",
                    ha="left",
                    va="center",
                    color="#0F172A",  # تغيير إلى غامق
                    fontweight="bold",
                )

        fig.tight_layout()

        self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(
            fill="both", expand=True, padx=5, pady=5
        )
        plt.close(fig)