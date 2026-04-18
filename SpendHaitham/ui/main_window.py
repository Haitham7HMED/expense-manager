import tkinter as tk
from tkinter import messagebox, ttk
from typing import List
from models.transaction import Transaction, TransactionType
from services.data_service import DataService
from services.chart_service import ChartService


class MainWindow:
    """النافذة الرئيسية للتطبيق"""

    def __init__(self, root):
        self.root = root
        self.root.title("💰 Expense Manager - Clean Edition")
        self.root.geometry("800x900")
        self.root.configure(bg="#f0f2f5")

        self.transactions: List[Transaction] = []
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        """إعداد واجهة المستخدم"""
        # العنوان
        title = tk.Label(self.root, text="💰 مدير المصاريف الشخصية 📊",
                         font=("Segoe UI", 20, "bold"), bg="#f0f2f5", fg="#1a1a2e")
        title.pack(pady=20)

        # أزرار الرسوم
        self._create_chart_buttons()

        # نموذج الإضافة
        self._create_add_form()

        # الملخص
        self.summary_frame = tk.LabelFrame(self.root, text="📊 الملخص",
                                           font=("Segoe UI", 12, "bold"),
                                           bg="white", fg="#2d3436", padx=20, pady=15)
        self.summary_frame.pack(pady=20, padx=20, fill="x")

        # إطار الرسوم
        self.chart_frame = tk.Frame(self.root, bg="#f8f9fa", relief="sunken", bd=2)
        self.chart_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # قائمة المعاملات
        self._create_transaction_list()

    def _create_chart_buttons(self):
        """إنشاء أزرار الرسوم البيانية"""
        btn_frame = tk.Frame(self.root, bg="#f0f2f5")
        btn_frame.pack(pady=10)

        buttons = [
            ("📈 مخطط دائري", self._show_pie_chart),
            ("📊 مخطط شريطي", self._show_bar_chart),
            ("🔄 تحديث", self._refresh_data)
        ]

        for text, command in buttons:
            btn = tk.Button(btn_frame, text=text, command=command,
                            bg="#3498db", fg="white", font=("Segoe UI", 11, "bold"),
                            padx=20, pady=8, cursor="hand2")
            btn.pack(side="left", padx=8)

    def _create_add_form(self):
        """نموذج إضافة معاملة"""
        form_frame = tk.LabelFrame(self.root, text="➕ إضافة معاملة جديدة",
                                   font=("Segoe UI", 12, "bold"), padx=20, pady=15)
        form_frame.pack(pady=20, padx=20, fill="x")

        # الوصف
        tk.Label(form_frame, text="الوصف:", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="e", pady=8)
        self.desc_entry = tk.Entry(form_frame, font=("Segoe UI", 11), width=30)
        self.desc_entry.grid(row=0, column=1, pady=8, padx=(10, 20), sticky="ew")

        # المبلغ
        tk.Label(form_frame, text="المبلغ:", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="e", pady=8)
        self.amount_entry = tk.Entry(form_frame, font=("Segoe UI", 11), width=15)
        self.amount_entry.grid(row=1, column=1, pady=8, padx=(10, 20), sticky="w")

        # النوع
        tk.Label(form_frame, text="النوع:", font=("Segoe UI", 10)).grid(row=2, column=0, sticky="e", pady=8)
        self.type_var = tk.StringVar(value=TransactionType.EXPENSE.value)
        type_combo = ttk.Combobox(form_frame, textvariable=self.type_var,
                                  values=[t.value for t in TransactionType],
                                  state="readonly", font=("Segoe UI", 11), width=12)
        type_combo.grid(row=2, column=1, pady=8, padx=(10, 20), sticky="w")

        # زر الإضافة
        add_btn = tk.Button(form_frame, text="إضافة المعاملة", command=self._add_transaction,
                            bg="#27ae60", fg="white", font=("Segoe UI", 12, "bold"),
                            padx=30, pady=10)
        add_btn.grid(row=3, column=0, columnspan=2, pady=20)

        form_frame.columnconfigure(1, weight=1)

    def _create_transaction_list(self):
        """قائمة المعاملات"""
        list_frame = tk.LabelFrame(self.root, text="📋 آخر المعاملات",
                                   font=("Segoe UI", 12, "bold"), padx=10, pady=10)
        list_frame.pack(pady=10, padx=20, fill="x")

        columns = ("التاريخ", "الوصف", "المبلغ", "النوع")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=6)

        # تهيئة الأعمدة
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140, anchor="center")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _add_transaction(self):
        """إضافة معاملة جديدة"""
        try:
            desc = self.desc_entry.get().strip()
            amount = float(self.amount_entry.get())
            trans_type = TransactionType(self.type_var.get())

            if not desc or len(desc) < 2:
                raise ValueError("الوصف قصير جداً")
            if amount <= 0:
                raise ValueError("المبلغ يجب أن يكون أكبر من صفر")

            transaction = Transaction.create(desc, amount, trans_type)
            self.transactions.append(transaction)

            DataService.save_transactions(self.transactions)
            self._update_ui()

            self.desc_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)

            messagebox.showinfo("✅ تم", f"تم إضافة:\n{transaction.description}\n{transaction.amount} ر.س")

        except ValueError as e:
            messagebox.showerror("❌ خطأ", str(e))
        except Exception as e:
            messagebox.showerror("❌ خطأ", "حدث خطأ غير متوقع")

    def _load_data(self):
        """تحميل البيانات"""
        self.transactions = DataService.load_transactions()
        self._update_ui()

    def _update_ui(self):
        """تحديث الواجهة"""
        self._update_summary()
        self._update_transaction_list()

    def _update_summary(self):
        """تحديث الملخص"""
        summary = DataService.get_summary(self.transactions)

        summary_text = f"""
الدخل: {summary['income']:,.2f} ر.س 💰
المصروفات: {summary['expense']:,.2f} ر.س 💸
الرصيد: {summary['balance']:,.2f} ر.س {'✅' if summary['balance'] >= 0 else '❌'}
المعاملات: {summary['total_count']} 📊
        """

        for widget in self.summary_frame.winfo_children():
            widget.destroy()

        tk.Label(self.summary_frame, text=summary_text, font=("Consolas", 12),
                 bg="white", fg="#2d3436", justify="center").pack(pady=15)

    def _update_transaction_list(self):
        """تحديث قائمة المعاملات"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        recent = self.transactions[-10:]
        for t in recent:
            amount_str = f"+{t.amount}" if t.type == TransactionType.INCOME else f"-{t.amount}"
            self.tree.insert("", "end", values=(
                t.date[:16], t.description, amount_str, t.type.value
            ))

    def _show_pie_chart(self):
        """عرض المخطط الدائري"""
        ChartService.create_pie_chart(self.transactions, self.chart_frame)

    def _show_bar_chart(self):
        """عرض المخطط الشريطي"""
        summary = DataService.get_summary(self.transactions)
        ChartService.create_bar_chart(summary, self.chart_frame)

    def _refresh_data(self):
        """تحديث البيانات"""
        self._load_data()
        messagebox.showinfo("✅ تم", "تم تحديث البيانات بنجاح!")