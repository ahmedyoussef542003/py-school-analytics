import json
import os
import sys
import customtkinter as ctk

# استيراد كافة الصفحات ودوال قاعدة البيانات
from attendance_page import AttendancePage
from database import init_db
from db_info_page import DbInfoPage
from grades_page import GradesPage
from overview_dashboard import OverviewDashboardPage
from skills_page import SkillsPage
from student_report_page import StudentReportPage
from students_page import StudentsPage

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class ProfessionalSchoolApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("نظام التحليل المدرسي الشامل | Dashboard")
        self.geometry("1200x800")
        self.minsize(950, 650)
        self.resizable(True, True)

        try:
            self.state("zoomed")
        except Exception:
            pass

        # ---------------- 1. إعداد إدارة مسار قاعدة البيانات ----------------
        self.config_file = os.path.join(self.get_base_dir(), "config.json")
        self.db_path = self.load_database_path()
        init_db(self.db_path)

        # تخطيط النافذة الرئيسية (Grid Layout)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------------- 2. الشريط الجانبي (Sidebar) ----------------
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="نظام التحليل\nالمدرسي 📊",
            font=("Segoe UI", 18, "bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 25))

        # أزرار التنقل بين الصفحات
        self.btn_overview = ctk.CTkButton(
            self.sidebar_frame,
            text="نظرة عامة (الداشبورد) 📈",
            font=("Segoe UI", 13, "bold"),
            command=self.show_overview_tab,
        )
        self.btn_overview.grid(row=1, column=0, padx=15, pady=8, sticky="ew")

        self.btn_grades = ctk.CTkButton(
            self.sidebar_frame,
            text="إدخال الدرجات 📝",
            font=("Segoe UI", 13),
            command=self.show_grades_tab,
        )
        self.btn_grades.grid(row=2, column=0, padx=15, pady=8, sticky="ew")

        self.btn_skills = ctk.CTkButton(
            self.sidebar_frame,
            text="تقييم المهارات ⭐",
            font=("Segoe UI", 13),
            command=self.show_skills_tab,
        )
        self.btn_skills.grid(row=3, column=0, padx=15, pady=8, sticky="ew")

        self.btn_attendance = ctk.CTkButton(
            self.sidebar_frame,
            text="الغياب والحضور الشهري 📅",
            font=("Segoe UI", 13),
            command=self.show_attendance_tab,
        )
        self.btn_attendance.grid(row=4, column=0, padx=15, pady=8, sticky="ew")

        self.btn_students = ctk.CTkButton(
            self.sidebar_frame,
            text="إدارة الطالبات 👩‍🎓",
            font=("Segoe UI", 13),
            command=self.show_students_tab,
        )
        self.btn_students.grid(row=5, column=0, padx=15, pady=8, sticky="ew")

        self.btn_report = ctk.CTkButton(
            self.sidebar_frame,
            text="تقرير الطالب 📄",
            font=("Segoe UI", 13),
            command=self.show_report_tab,
        )
        self.btn_report.grid(row=6, column=0, padx=15, pady=8, sticky="ew")

        self.btn_db_info = ctk.CTkButton(
            self.sidebar_frame,
            text="بيانات الاتصال 🔍",
            font=("Segoe UI", 13),
            command=self.show_db_info_tab,
        )
        self.btn_db_info.grid(row=7, column=0, padx=15, pady=8, sticky="ew")

        # ---------------- 3. حاوية المحتوى الرئيسية ----------------
        self.main_container = ctk.CTkFrame(
            self, corner_radius=15, fg_color="#1E1E1E"
        )
        self.main_container.grid(
            row=0, column=1, padx=15, pady=15, sticky="nsew"
        )

        self.views = {}
        self.setup_views()

        # فتح الداشبورد كصفحة افتراضية عند تشغيل التطبيق
        self.show_overview_tab()

    # ---------------- دوال التعامل مع المسار وإعدادات الحفظ ----------------

    def get_base_dir(self):
        """الحصول على المسار الأساسي سواء للملف النصي أو الـ EXE"""
        if getattr(sys, "frozen", False):
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(__file__))

    def load_database_path(self):
        """تحميل المسار من config.json إن وجد، وإلا فتح المسار الافتراضي"""
        default_path = os.path.join(self.get_base_dir(), "school_system.db")

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    saved_path = data.get("db_path", "")
                    if saved_path and os.path.exists(saved_path):
                        return saved_path
            except Exception:
                pass

        return default_path

    def save_database_path(self, new_path):
        """حفظ المسار الجديد في config.json"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(
                    {"db_path": new_path}, f, ensure_ascii=False, indent=4
                )
        except Exception as e:
            print(f"خطأ أثناء حفظ المسار: {e}")

    def update_database_path(self, new_path):
        """دالة الاستدعاء عند تغير المسار من صفحة DbInfoPage"""
        self.db_path = new_path
        self.save_database_path(new_path)
        init_db(self.db_path)

        # تحديث متغير db_path في كل الكائنات للشاشات المفتوحة
        for view in self.views.values():
            if hasattr(view, "db_path"):
                view.db_path = new_path

    # ---------------- إعداد الواجهات والتبديل بينها ----------------

    def setup_views(self):
        """تسجيل وإعداد كافة الصفحات داخل الحاوية"""
        self.views["overview"] = OverviewDashboardPage(
            self.main_container, self.db_path
        )
        self.views["grades"] = GradesPage(self.main_container, self.db_path)
        self.views["skills"] = SkillsPage(self.main_container, self.db_path)
        self.views["attendance"] = AttendancePage(
            self.main_container, self.db_path
        )
        self.views["students"] = StudentsPage(
            self.main_container, self.db_path
        )
        self.views["report"] = StudentReportPage(
            self.main_container, self.db_path
        )

        # تمرير دالة التحديث لصفحة DbInfoPage
        self.views["db_info"] = DbInfoPage(
            self.main_container,
            self.db_path,
            on_db_change_callback=self.update_database_path,
        )

    def switch_view(self, active_key):
        """التبديل بين الواجهات بدون إعادة تحميل الكائنات"""
        for key, view in self.views.items():
            if key == active_key:
                view.pack(fill="both", expand=True, padx=10, pady=10)
            else:
                view.pack_forget()

    def reset_sidebar_colors(self):
        """إعادة تعيين ألوان أزرار القائمة الجانبية"""
        for btn in [
            self.btn_overview,
            self.btn_grades,
            self.btn_skills,
            self.btn_attendance,
            self.btn_students,
            self.btn_report,
            self.btn_db_info,
        ]:
            btn.configure(
                fg_color="transparent", text_color=("gray10", "gray90")
            )

    # ---------------- دوال استدعاء التبويبات ----------------

    def show_overview_tab(self):
        self.switch_view("overview")
        self.reset_sidebar_colors()
        self.btn_overview.configure(
            fg_color=("#3B82F6", "#1D4ED8"), text_color="white"
        )
        self.views["overview"].refresh_dashboard()

    def show_grades_tab(self):
        self.switch_view("grades")
        self.reset_sidebar_colors()
        self.btn_grades.configure(
            fg_color=("#3B82F6", "#1D4ED8"), text_color="white"
        )

    def show_skills_tab(self):
        self.switch_view("skills")
        self.reset_sidebar_colors()
        self.btn_skills.configure(
            fg_color=("#3B82F6", "#1D4ED8"), text_color="white"
        )

    def show_attendance_tab(self):
        self.switch_view("attendance")
        self.reset_sidebar_colors()
        self.btn_attendance.configure(
            fg_color=("#3B82F6", "#1D4ED8"), text_color="white"
        )

    def show_students_tab(self):
        self.switch_view("students")
        self.reset_sidebar_colors()
        self.btn_students.configure(
            fg_color=("#3B82F6", "#1D4ED8"), text_color="white"
        )
        self.views["students"].refresh_students_list()

    def show_report_tab(self):
        self.switch_view("report")
        self.reset_sidebar_colors()
        self.btn_report.configure(
            fg_color=("#3B82F6", "#1D4ED8"), text_color="white"
        )

    def show_db_info_tab(self):
        self.switch_view("db_info")
        self.reset_sidebar_colors()
        self.btn_db_info.configure(
            fg_color=("#3B82F6", "#1D4ED8"), text_color="white"
        )
        self.views["db_info"].refresh_db_info()


if __name__ == "__main__":
    app = ProfessionalSchoolApp()
    app.mainloop()