import os
import customtkinter as ctk
from PIL import Image

class WelcomePage(ctk.CTkFrame):
    """صفحة الترحيب المحسّنة بناءً على التصميم المطلوب"""

    def __init__(self, parent, controller):
        # خلفية بيضاء ناصعة
        super().__init__(parent, fg_color="#FFFFFF", corner_radius=0)
        self.controller = controller

        # تقسيم الصفحة لعمودين
        self.grid_columnconfigure(0, weight=1)  # الجزء الأيسر
        self.grid_columnconfigure(1, weight=1)  # الجزء الأيمن
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)  # للفوتر

        # تهيئة الأقسام
        self.setup_left_section()
        self.setup_right_section()
        self.setup_footer()

    # ========================== القسم الأيسر ==========================
    def setup_left_section(self):
        """إعداد الجزء الأيسر مع النصوص المطلوبة"""
        left_frame = ctk.CTkFrame(self, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=30)

        # حاوية رئيسية
        main_container = ctk.CTkFrame(
            left_frame,
            fg_color="transparent",
            corner_radius=25,
        )
        main_container.pack(expand=True, fill="both")

        # العنوان الرئيسي - كما هو مطلوب في الصورة
        welcome_title = ctk.CTkLabel(
            main_container,
            text="أهلاً بك في منصة متابعة أداء الطالب 👋",
            font=("Segoe UI", 32, "bold"),
            text_color="#0F172A",
            anchor="center",
        )
        welcome_title.pack(pady=(10, 8))

        # النص الفرعي
        subtitle = ctk.CTkLabel(
            main_container,
            text="النظام الشامل لإدارة الدرجات، المهارات، والتحليل المدرسي",
            font=("Segoe UI", 16),
            text_color="#475569",
            wraplength=450,
            justify="center",
        )
        subtitle.pack(pady=(0, 25))

        # إضافة اللوجو والعلم
        self.load_logo_with_flag(main_container)

    def load_logo_with_flag(self, parent_frame):
        """عرض اللوجو والعلم السعودي"""
        logo_container = ctk.CTkFrame(parent_frame, fg_color="transparent")
        logo_container.pack(expand=True, pady=10)

        # ===== اللوجو =====
        logo_path = os.path.join(os.path.dirname(__file__), "assets", "school_logo.png")

        if os.path.exists(logo_path):
            try:
                pil_image = Image.open(logo_path)
                ctk_image = ctk.CTkImage(
                    light_image=pil_image, 
                    dark_image=pil_image, 
                    size=(350, 350)
                )
                logo_label = ctk.CTkLabel(
                    logo_container, 
                    image=ctk_image, 
                    text=""
                )
                logo_label.pack()
            except Exception:
                self._draw_placeholder_logo(logo_container)
        else:
            self._draw_placeholder_logo(logo_container)

        # ===== العلم السعودي المحسّن =====
        flag_banner = ctk.CTkFrame(
            logo_container,
            fg_color="#1B5E20",
            corner_radius=12,
            height=50,
            width=300,
            border_color="#2E7D32",
            border_width=1,
        )
        flag_banner.pack(pady=(15, 5))
        flag_banner.pack_propagate(False)

        # محتوى العلم
        flag_content = ctk.CTkFrame(flag_banner, fg_color="transparent")
        flag_content.place(relx=0.5, rely=0.5, anchor="center")

        # العلم السعودي والنص
        flag_label = ctk.CTkLabel(
            flag_content,
            text="🇸🇦  المملكة العربية السعودية",
            font=("Segoe UI", 15, "bold"),
            text_color="#FFFFFF",
        )
        flag_label.pack(side="left", padx=5)

        # أيقونة السيف
        sword_icon = ctk.CTkLabel(
            flag_content,
            text="⚔️",
            font=("Segoe UI", 18),
        )
        sword_icon.pack(side="left", padx=(5, 0))

    def _draw_placeholder_logo(self, parent_frame):
        """لوجو افتراضي مع منصة التعليم"""
        placeholder_frame = ctk.CTkFrame(
            parent_frame,
            width=300,
            height=300,
            corner_radius=150,
            fg_color="#EFF6FF",
            border_color="#3B82F6",
            border_width=3,
        )
        placeholder_frame.pack()
        placeholder_frame.pack_propagate(False)

        # أيقونة منصة التعليم
        icon_label = ctk.CTkLabel(
            placeholder_frame,
            text="📚\n🎓",
            font=("Segoe UI", 80),
            text_color="#2563EB",
        )
        icon_label.place(relx=0.5, rely=0.4, anchor="center")

        # نص "منصة التعليم"
        platform_text = ctk.CTkLabel(
            placeholder_frame,
            text="منصة التعليم",
            font=("Segoe UI", 18, "bold"),
            text_color="#1E293B",
        )
        platform_text.place(relx=0.5, rely=0.75, anchor="center")

    # ========================== القسم الأيمن ==========================
    def setup_right_section(self):
        """إعداد الجزء الأيمن مع الأزرار المطلوبة"""
        right_frame = ctk.CTkFrame(self, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(20, 50), pady=(30, 20))

        # حاوية رئيسية بيضاء
        glass_frame = ctk.CTkFrame(
            right_frame,
            fg_color="#FFFFFF",
            corner_radius=20,
            border_width=1,
            border_color="#E2E8F0",
        )
        glass_frame.pack(expand=True, fill="both", padx=5, pady=5)

        # مسافة علوية
        spacer_top = ctk.CTkFrame(glass_frame, fg_color="transparent", height=15)
        spacer_top.pack(fill="x")

        # الأزرار الرئيسية - كما هو مطلوب في الصورة
        buttons_data = [
            ("📊  نظرة عامة", "#3B82F6", "#2563EB"),
            ("✏️  إدخال الدرجات", "#8B5CF6", "#7C3AED"),
            ("⭐  تقييم المهارات", "#EC4899", "#DB2777"),
            ("📅  الغياب والحضور", "#F59E0B", "#D97706"),
            ("👩‍🎓  إدارة الطالبات", "#10B981", "#059669"),
            ("📄  تقرير الطالب", "#6366F1", "#4F46E5"),
            ("🔍  بيانات الاتصال", "#64748B", "#475569"),
        ]

        # حاوية للأزرار
        buttons_container = ctk.CTkFrame(glass_frame, fg_color="transparent")
        buttons_container.pack(fill="both", expand=True, padx=20, pady=(10, 15))

        for text, color, hover_color in buttons_data:
            btn = ctk.CTkButton(
                buttons_container,
                text=text,
                font=("Segoe UI", 15, "bold"),
                height=45,
                corner_radius=10,
                fg_color=color,
                hover_color=hover_color,
                text_color="#FFFFFF",
                border_spacing=10,
                anchor="w",
            )
            btn.pack(fill="x", pady=5)

        # إضافة زر خروج
        exit_btn = ctk.CTkButton(
            glass_frame,
            text="🚪  خروج",
            font=("Segoe UI", 14, "bold"),
            height=40,
            corner_radius=10,
            fg_color="#EF4444",
            hover_color="#DC2626",
            text_color="#FFFFFF",
            command=self.quit_app,
            border_spacing=10,
        )
        exit_btn.pack(pady=(0, 15), padx=20, fill="x")

    # ========================== الفوتر ==========================
    def setup_footer(self):
        """إضافة شريط سفلي"""
        footer = ctk.CTkFrame(
            self,
            fg_color="transparent",
            height=40,
        )
        footer.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20)

        # خط فاصل
        separator = ctk.CTkFrame(
            footer,
            fg_color="#E2E8F0",
            height=1,
        )
        separator.pack(fill="x", pady=(0, 8))

        # محتوى الفوتر
        footer_content = ctk.CTkFrame(footer, fg_color="transparent")
        footer_content.pack(fill="x")

        # جهة اليمين: معلومات
        left_footer = ctk.CTkFrame(footer_content, fg_color="transparent")
        left_footer.pack(side="left")

        # نص "منصة التعليم"
        platform_label = ctk.CTkLabel(
            left_footer,
            text="📚 منصة التعليم",
            font=("Segoe UI", 12, "bold"),
            text_color="#475569",
        )
        platform_label.pack(side="left", padx=5)

        # جهة اليسار: معلومات إضافية
        right_footer = ctk.CTkFrame(footer_content, fg_color="transparent")
        right_footer.pack(side="right")

        # "المملكة العربية السعودية"
        country_label = ctk.CTkLabel(
            right_footer,
            text="🇸🇦 المملكة العربية السعودية",
            font=("Segoe UI", 12),
            text_color="#475569",
        )
        country_label.pack(side="left", padx=5)

    # ========================== دوال التحكم ==========================
    def show_overview(self):
        """عرض صفحة النظرة العامة"""
        if hasattr(self.controller, 'show_overview_tab'):
            self.controller.show_overview_tab()

    def show_grades(self):
        """عرض صفحة الدرجات"""
        if hasattr(self.controller, 'show_grades_tab'):
            self.controller.show_grades_tab()

    def show_skills(self):
        """عرض صفحة المهارات"""
        if hasattr(self.controller, 'show_skills_tab'):
            self.controller.show_skills_tab()

    def show_attendance(self):
        """عرض صفحة الغياب"""
        if hasattr(self.controller, 'show_attendance_tab'):
            self.controller.show_attendance_tab()

    def show_students(self):
        """عرض صفحة الطالبات"""
        if hasattr(self.controller, 'show_students_tab'):
            self.controller.show_students_tab()

    def show_report(self):
        """عرض صفحة التقرير"""
        if hasattr(self.controller, 'show_report_tab'):
            self.controller.show_report_tab()

    def show_db_info(self):
        """عرض صفحة معلومات قاعدة البيانات"""
        if hasattr(self.controller, 'show_db_info_tab'):
            self.controller.show_db_info_tab()

    def quit_app(self):
        """إغلاق التطبيق"""
        if hasattr(self.controller, 'quit'):
            self.controller.quit()
        else:
            self.winfo_toplevel().quit()