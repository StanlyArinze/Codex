from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


@dataclass(slots=True)
class Transaction:
    amount: Decimal
    description: str
    date: date
    category: str
    type: TransactionType


@dataclass(slots=True)
class MonthlySummary:
    month: str
    total_income: Decimal
    total_expense: Decimal

    @property
    def balance(self) -> Decimal:
        return self.total_income - self.total_expense
