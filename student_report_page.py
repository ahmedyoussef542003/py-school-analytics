import sqlite3
import customtkinter as ctk


class StudentReportPage(ctk.CTkFrame):

    def __init__(self, parent, db_path):
        # تغيير الخلفية إلى أبيض
        super().__init__(
            parent,
            fg_color="#FFFFFF"
        )

        self.db_path = db_path
        self.setup_ui()

    # =========================================================
    # Setup UI
    # =========================================================

    def setup_ui(self):

        # =====================================================
        # Title
        # =====================================================

        title = ctk.CTkLabel(
            self,
            text="تقرير طالبة مفصل",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=22,
                weight="bold"
            ),
            text_color="#0F172A"  # لون غامق
        )

        title.pack(
            pady=(10, 15)
        )

        # =====================================================
        # Search Frame
        # =====================================================

        search_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        search_frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # =====================================================
        # Search Button
        # =====================================================

        search_btn = ctk.CTkButton(
            search_frame,
            text="🔍 عرض التقرير",
            command=self.load_report,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=12,
                weight="bold"
            ),
            fg_color="#3B82F6",
            hover_color="#2563EB",
            text_color="white"
        )

        search_btn.pack(
            side="left",
            padx=10
        )

        # =====================================================
        # Student Entry
        # =====================================================

        self.student_entry = ctk.CTkEntry(
            search_frame,
            width=350,
            placeholder_text="ادخل اسم الطالبة...",
            justify="right",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
                weight="normal"
            ),
            fg_color="#F8FAFC",
            border_color="#CBD5E1",
            text_color="#0F172A"
        )

        self.student_entry.pack(
            side="right",
            padx=5
        )

        # =====================================================
        # Search Label
        # =====================================================

        search_label = ctk.CTkLabel(
            search_frame,
            text="اسم الطالبة للبحث:",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=14,
                weight="normal"
            ),
            anchor="e",
            text_color="#0F172A"
        )

        search_label.pack(
            side="right",
            padx=(5, 10)
        )

        # =====================================================
        # Scrollable Container - تغيير الخلفية إلى أبيض
        # =====================================================

        self.container = ctk.CTkScrollableFrame(
            self,
            fg_color="#F8FAFC",  # أبيض فاتح
            corner_radius=10
        )

        self.container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

    # =========================================================
    # Render Table
    # =========================================================

    def render_table(self, title, headers, rows):

        # =====================================================
        # Main Table Frame - تغيير إلى أبيض
        # =====================================================

        table_frame = ctk.CTkFrame(
            self.container,
            fg_color="#FFFFFF",  # أبيض
            corner_radius=8,
            border_width=1,
            border_color="#E2E8F0"
        )

        table_frame.pack(
            fill="x",
            expand=True,
            padx=10,
            pady=10
        )

        # =====================================================
        # Table Title
        # =====================================================

        lbl_title = ctk.CTkLabel(
            table_frame,
            text=title,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=15,
                weight="bold"
            ),
            text_color="#2563EB",  # أزرق غامق
            anchor="e"
        )

        lbl_title.pack(
            fill="x",
            anchor="e",
            padx=12,
            pady=(8, 4)
        )

        # =====================================================
        # Header - تغيير إلى فاتح
        # =====================================================

        h_frame = ctk.CTkFrame(
            table_frame,
            fg_color="#F1F5F9",  # رمادي فاتح
            height=30
        )

        h_frame.pack(
            fill="x",
            padx=8,
            pady=2
        )

        # =====================================================
        # RTL Visual Order
        # =====================================================

        display_headers = headers[::-1]

        for idx, header in enumerate(display_headers):

            label = ctk.CTkLabel(
                h_frame,
                text=str(header),
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=12,
                    weight="bold"
                ),
                text_color="#0F172A",  # غامق
                anchor="center"
            )

            label.grid(
                row=0,
                column=idx,
                sticky="nsew",
                padx=4,
                pady=4
            )

            h_frame.grid_columnconfigure(
                idx,
                weight=1
            )

        # =====================================================
        # No Data
        # =====================================================

        if not rows:

            no_data = ctk.CTkLabel(
                table_frame,
                text="لا توجد بيانات متاحة",
                text_color="#64748B",  # رمادي
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=13,
                    weight="normal"
                )
            )

            no_data.pack(
                pady=10
            )

            return

        # =====================================================
        # Table Rows - تغيير الألوان إلى فاتحة
        # =====================================================

        for r_idx, row in enumerate(rows):

            # ألوان صفوف متناوبة فاتحة
            bg = (
                "#F8FAFC"  # رمادي فاتح جداً
                if r_idx % 2 == 0
                else "#FFFFFF"  # أبيض
            )

            r_frame = ctk.CTkFrame(
                table_frame,
                fg_color=bg
            )

            r_frame.pack(
                fill="x",
                padx=8,
                pady=1
            )

            # -------------------------------------------------
            # Reverse row for RTL visual order
            # -------------------------------------------------

            display_row = row[::-1]

            for c_idx, value in enumerate(display_row):

                if value is None:
                    value = ""

                label = ctk.CTkLabel(
                    r_frame,
                    text=str(value),
                    font=ctk.CTkFont(
                        family="Segoe UI",
                        size=12,
                        weight="normal"
                    ),
                    anchor="center",
                    text_color="#0F172A"  # غامق
                )

                label.grid(
                    row=0,
                    column=c_idx,
                    sticky="nsew",
                    padx=4,
                    pady=3
                )

                r_frame.grid_columnconfigure(
                    c_idx,
                    weight=1
                )

    # =========================================================
    # Load Student Report
    # =========================================================

    def load_report(self):

        # =====================================================
        # Clear Previous Report
        # =====================================================

        for child in self.container.winfo_children():
            child.destroy()

        # =====================================================
        # Get Student Name
        # =====================================================

        name = self.student_entry.get().strip()

        if not name:
            return

        # =====================================================
        # Database Connection
        # =====================================================

        conn = sqlite3.connect(
            self.db_path
        )

        cur = conn.cursor()

        try:

            # =================================================
            # Student Information
            # =================================================

            cur.execute(
                """
                SELECT
                    student_id,
                    student_name,
                    grade_level,
                    class_name,
                    section
                FROM Students
                WHERE student_name LIKE ?
                """,
                (f"%{name}%",)
            )

            student = cur.fetchone()

            # =================================================
            # Student Not Found
            # =================================================

            if not student:

                error_label = ctk.CTkLabel(
                    self.container,
                    text="لم يتم العثور على الطالبة!",
                    text_color="#EF4444",  # أحمر
                    font=ctk.CTkFont(
                        family="Segoe UI",
                        size=16,
                        weight="bold"
                    )
                )

                error_label.pack(
                    pady=20
                )

                return

            # =================================================
            # Student Data
            # =================================================

            (
                st_id,
                st_name,
                st_grade,
                st_class,
                st_section
            ) = student

            # =================================================
            # Student Information Frame - تغيير إلى أبيض
            # =================================================

            info_frame = ctk.CTkFrame(
                self.container,
                fg_color="#FFFFFF",  # أبيض
                corner_radius=8,
                border_width=1,
                border_color="#E2E8F0"
            )

            info_frame.pack(
                fill="x",
                padx=10,
                pady=10
            )

            # =================================================
            # Student Name
            # =================================================

            ctk.CTkLabel(
                info_frame,
                text=f"اسم الطالبة: {st_name}",
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=15,
                    weight="bold"
                ),
                text_color="#2563EB",  # أزرق
                anchor="e"
            ).pack(
                fill="x",
                anchor="e",
                padx=15,
                pady=(10, 4)
            )

            # =================================================
            # Grade
            # =================================================

            ctk.CTkLabel(
                info_frame,
                text=f"الصف: {st_grade}",
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=13,
                    weight="normal"
                ),
                text_color="#0F172A",  # غامق
                anchor="e"
            ).pack(
                fill="x",
                anchor="e",
                padx=15,
                pady=2
            )

            # =================================================
            # Class
            # =================================================

            ctk.CTkLabel(
                info_frame,
                text=f"الفصل: {st_class}",
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=13,
                    weight="normal"
                ),
                text_color="#0F172A",
                anchor="e"
            ).pack(
                fill="x",
                anchor="e",
                padx=15,
                pady=2
            )

            # =================================================
            # Section
            # =================================================

            ctk.CTkLabel(
                info_frame,
                text=f"القسم: {st_section}",
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=13,
                    weight="normal"
                ),
                text_color="#0F172A",
                anchor="e"
            ).pack(
                fill="x",
                anchor="e",
                padx=15,
                pady=(2, 10)
            )

            # =================================================
            # 1. Grades
            # =================================================

            cur.execute(
                """
                SELECT
                    subject,
                    exam_type,
                    score,
                    max_score
                FROM Grades
                WHERE student_id = ?
                """,
                (st_id,)
            )

            grades = []

            for subject, exam_type, score, max_score in cur.fetchall():

                score_text = f"{score} / {max_score}"

                grades.append([
                    subject,
                    exam_type,
                    score_text
                ])

            self.render_table(
                "سجل الدرجات والتقييمات",
                [
                    "المادة",
                    "نوع الاختبار",
                    "الدرجة"
                ],
                grades
            )

            # =================================================
            # 2. Attendance
            # =================================================

            cur.execute(
                """
                SELECT
                    month_year,
                    total_days,
                    attended_days
                FROM Attendance
                WHERE student_id = ?
                """,
                (st_id,)
            )

            attendance = []

            for (
                month_year,
                total_days,
                attended_days
            ) in cur.fetchall():

                absent_days = (
                    total_days - attended_days
                )

                attendance.append([
                    month_year,
                    total_days,
                    attended_days,
                    absent_days
                ])

            self.render_table(
                "سجل الحضور والغياب الشهري",
                [
                    "الشهر",
                    "إجمالي الأيام",
                    "أيام الحضور",
                    "أيام الغياب"
                ],
                attendance
            )

            # =================================================
            # 3. Skills
            # =================================================

            cur.execute(
                """
                SELECT
                    subject,
                    skill_name,
                    is_mastered
                FROM Skills
                WHERE student_id = ?
                """,
                (st_id,)
            )

            raw_skills = cur.fetchall()

            skills = []

            for (
                subject,
                skill_name,
                is_mastered
            ) in raw_skills:

                if is_mastered == 1:
                    status = "✅ متقن"
                else:
                    status = "❌ غير متقن"

                skills.append([
                    subject,
                    skill_name,
                    status
                ])

            self.render_table(
                "تقييم المهارات الأكاديمية",
                [
                    "المادة",
                    "المهارة",
                    "الحالة"
                ],
                skills
            )

        finally:

            # =================================================
            # Close Database
            # =================================================

            conn.close()