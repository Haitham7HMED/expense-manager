import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from collections import defaultdict
from typing import List
from models.transaction import Transaction, TransactionType


class ChartService:
    """خدمة الرسوم البيانية"""

    @staticmethod
    def create_pie_chart(transactions: List[Transaction], parent_frame) -> None:
        """مخطط دائري للمصروفات"""
        expenses = [t for t in transactions if t.type == TransactionType.EXPENSE]

        if not expenses:
            return

        # تجميع حسب الوصف
        expense_dict = defaultdict(float)
        for t in expenses:
            category = t.description[:10].upper()  # أول 10 أحرف
            expense_dict[category] += t.amount

        labels = list(expense_dict.keys())
        sizes = list(expense_dict.values())

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.set_title('📊 توزيع المصروفات', fontsize=16, fontweight='bold')

        ChartService._display_chart(fig, parent_frame)

    @staticmethod
    def create_bar_chart(summary: dict, parent_frame) -> None:
        """مخطط شريطي للدخل والمصروفات"""
        categories = ['الدخل 💰', 'المصروفات 💸']
        values = [summary['income'], summary['expense']]

        fig, ax = plt.subplots(figsize=(8, 6))
        bars = ax.bar(categories, values, color=['#27ae60', '#e74c3c'], alpha=0.8)
        ax.set_title('📈 مقارنة الدخل والمصروفات', fontsize=16, fontweight='bold')
        ax.set_ylabel('المبلغ (ريال)')

        # إضافة القيم
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{value:,.0f}', ha='center', va='bottom', fontweight='bold')

        ChartService._display_chart(fig, parent_frame)

    @staticmethod
    def _display_chart(fig, parent_frame) -> None:
        """عرض الرسم البياني"""
        # مسح الإطار السابق
        for widget in parent_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)