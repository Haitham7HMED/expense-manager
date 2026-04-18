import json
import os
from typing import List
from models.transaction import Transaction, TransactionType


class DataService:
    """خدمة إدارة البيانات"""

    FILE_NAME = "expenses.json"

    @staticmethod
    def save_transactions(transactions: List[Transaction]) -> None:
        """حفظ قائمة المعاملات"""
        data = [t.to_dict() for t in transactions]
        with open(DataService.FILE_NAME, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def load_transactions() -> List[Transaction]:
        """تحميل المعاملات"""
        if not os.path.exists(DataService.FILE_NAME):
            return []

        try:
            with open(DataService.FILE_NAME, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Transaction.from_dict(t) for t in data]
        except:
            return []

    @staticmethod
    def get_summary(transactions: List[Transaction]) -> dict:
        """حساب الملخص"""
        income = sum(t.amount for t in transactions if t.type == TransactionType.INCOME)
        expense = sum(t.amount for t in transactions if t.type == TransactionType.EXPENSE)
        return {
            'income': round(income, 2),
            'expense': round(expense, 2),
            'balance': round(income - expense, 2),
            'total_count': len(transactions)
        }