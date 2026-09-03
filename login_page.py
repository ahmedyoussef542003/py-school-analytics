import customtkinter as ctk
from database import verify_login


class LoginWindow(ctk.CTkFrame):

    def __init__(self, parent, db_path, on_login_success):
        super().__init__(parent, fg_color="transparent")
        self.db_path = db_path
        self.on_login_success = on_login_success
        self._build_ui()

    def _build_ui(self):
        # كارت تسجيل الدخول
        card = ctk.CTkFrame(
            self,
            fg_color="#1E293B",
            corner_radius=15,
            border_width=1,
            border_color="#334155",
            width=380,
            height=420,
        )
        card.pack(expand=True, pady=40)
        card.pack_propagate(False)

        ctk.CTkLabel(
            card, text="🔒 تسجيل الدخول", font=("Segoe UI", 22, "bold")
        ).pack(pady=(30, 10))

        ctk.CTkLabel(
            card,
            text="مرحباً بك في نظام التحليل المدرسي",
            font=("Segoe UI", 12),
            text_color="#94A3B8",
        ).pack(pady=(0, 20))

        # مدخلات البيانات
        self.user_entry = ctk.CTkEntry(
            card,
            placeholder_text="اسم المستخدم (12345)",
            width=280,
            height=40,
            justify="right",
        )
        self.user_entry.pack(pady=10)

        self.pass_entry = ctk.CTkEntry(
            card,
            placeholder_text="كلمة المرور (0123456789)",
            show="*",
            width=280,
            height=40,
            justify="right",
        )
        self.pass_entry.pack(pady=10)

        self.msg_label = ctk.CTkLabel(
            card, text="", font=("Segoe UI", 11), text_color="#EF4444"
        )
        self.msg_label.pack(pady=5)

        # زر الدخول
        btn_login = ctk.CTkButton(
            card,
            text="دخول النظام ❯",
            font=("Segoe UI", 13, "bold"),
            fg_color="#3B82F6",
            hover_color="#2563EB",
            width=280,
            height=40,
            command=self.handle_login,
        )
        btn_login.pack(pady=15)

    def handle_login(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()

        user_info = verify_login(self.db_path, username, password)
        if user_info:
            name, role = user_info
            self.on_login_success(name, role)
        else:
            self.msg_label.configure(
                text="اسم المستخدم أو كلمة المرور غير صحيحة"
            )