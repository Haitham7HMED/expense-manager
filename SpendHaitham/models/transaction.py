from datetime import datetime
from typing import Optional
from dataclasses import dataclass
from enum import Enum


class TransactionType(Enum):
    EXPENSE = "مصروف"
    INCOME = "دخل"


@dataclass
class Transaction:
    """نموذج المعاملة"""
    id: str
    date: str
    description: str
    amount: float
    type: TransactionType

    @classmethod
    def create(cls, description: str, amount: float, trans_type: TransactionType) -> 'Transaction':
        """إنشاء معاملة جديدة"""
        return cls(
            id=str(datetime.now().timestamp()),
            date=datetime.now().strftime("%Y-%m-%d %H:%M"),
            description=description,
            amount=round(amount, 2),
            type=trans_type
        )

    def to_dict(self) -> dict:
        """تحويل إلى dictionary"""
        return {
            'id': self.id,
            'date': self.date,
            'description': self.description,
            'amount': self.amount,
            'type': self.type.value
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Transaction':
        """تحويل من dictionary"""
        return cls(
            id=data['id'],
            date=data['date'],
            description=data['description'],
            amount=float(data['amount']),
            type=TransactionType(data['type'])
        )