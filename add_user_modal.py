import customtkinter as ctk
from database import add_new_user


class AddUserModal(ctk.CTkToplevel):

    def __init__(self, parent, db_path):
        super().__init__(parent)
        self.db_path = db_path

        self.title("إضافة مستخدم جديد")
        self.geometry("400x460")
        self.resizable(False, False)

        # جعل النافذة تظهر فوق جميع النوافذ الأخرى
        self.attributes("-topmost", True)
        self._build_ui()

    def _build_ui(self):
        card = ctk.CTkFrame(self, fg_color="#1E293B", corner_radius=12)
        card.pack(fill="both", expand=True, padx=15, pady=15)

        ctk.CTkLabel(
            card, text="👤 إضافة مستخدم جديد", font=("Segoe UI", 16, "bold")
        ).pack(pady=(20, 15))

        # الاسم الكامل
        self.ent_name = ctk.CTkEntry(
            card, placeholder_text="الاسم بالكامل", width=280, justify="right"
        )
        self.ent_name.pack(pady=8)

        # اسم المستخدم (اليوزر)
        self.ent_user = ctk.CTkEntry(
            card,
            placeholder_text="اسم المستخدم (اليوزر)",
            width=280,
            justify="right",
        )
        self.ent_user.pack(pady=8)

        # كلمة المرور
        self.ent_pass = ctk.CTkEntry(
            card,
            placeholder_text="كلمة المرور",
            show="*",
            width=280,
            justify="right",
        )
        self.ent_pass.pack(pady=8)

        # الدور / الرتبة
        self.ent_role = ctk.CTkEntry(
            card,
            placeholder_text="الوظيفة / الدور (مثال: أستاذ / مشرف)",
            width=280,
            justify="right",
        )
        self.ent_role.pack(pady=8)

        # رسائل الخطأ أو النجاح
        self.msg_label = ctk.CTkLabel(card, text="", font=("Segoe UI", 11))
        self.msg_label.pack(pady=5)

        # زر الحفظ
        ctk.CTkButton(
            card,
            text="حفظ المستخدم",
            font=("Segoe UI", 13, "bold"),
            fg_color="#10B981",
            hover_color="#059669",
            width=280,
            height=38,
            command=self.save_user,
        ).pack(pady=15)

    def save_user(self):
        name = self.ent_name.get().strip()
        username = self.ent_user.get().strip()
        password = self.ent_pass.get().strip()
        role = self.ent_role.get().strip() or "أستاذ"

        if not name or not username or not password:
            self.msg_label.configure(
                text="⚠️ يرجى ملء الحقول الأساسية", text_color="#EF4444"
            )
            return

        # استدعاء دالة إضافة المستخدم من ملف database.py
        success, msg = add_new_user(
            self.db_path, username, password, name, role
        )

        if success:
            self.msg_label.configure(text=f"✅ {msg}", text_color="#10B981")
            self.after(1200, self.destroy)  # إغلاق النافذة بعد النجاح
        else:
            self.msg_label.configure(text=f"❌ {msg}", text_color="#EF4444")