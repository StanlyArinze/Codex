from __future__ import annotations

from collections import defaultdict
from datetime import date
from decimal import Decimal

from .ai import categorize_transaction, generate_monthly_insight
from .models import MonthlySummary, Transaction, TransactionType


class Ledger:
    def __init__(self) -> None:
        self._transactions: list[Transaction] = []

    @property
    def transactions(self) -> tuple[Transaction, ...]:
        return tuple(self._transactions)

    def add_income(self, amount: Decimal, description: str, when: date) -> Transaction:
        txn = Transaction(
            amount=amount,
            description=description,
            date=when,
            category="Receita",
            type=TransactionType.INCOME,
        )
        self._transactions.append(txn)
        return txn

    def add_expense(self, amount: Decimal, description: str, when: date) -> Transaction:
        txn = Transaction(
            amount=amount,
            description=description,
            date=when,
            category=categorize_transaction(description),
            type=TransactionType.EXPENSE,
        )
        self._transactions.append(txn)
        return txn

    def monthly_summary(self, year: int, month: int) -> MonthlySummary:
        income = Decimal("0")
        expense = Decimal("0")
        for txn in self._transactions:
            if txn.date.year == year and txn.date.month == month:
                if txn.type is TransactionType.INCOME:
                    income += txn.amount
                else:
                    expense += txn.amount

        return MonthlySummary(
            month=f"{year:04d}-{month:02d}",
            total_income=income,
            total_expense=expense,
        )

    def top_expense_category(self, year: int, month: int) -> str:
        totals: dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
        for txn in self._transactions:
            if txn.type is TransactionType.EXPENSE and txn.date.year == year and txn.date.month == month:
                totals[txn.category] += txn.amount

        if not totals:
            return "Sem gastos"

        return max(totals.items(), key=lambda item: item[1])[0]

    def monthly_insight(self, year: int, month: int) -> str:
        summary = self.monthly_summary(year, month)
        top_category = self.top_expense_category(year, month)
        return generate_monthly_insight(summary.total_income, summary.total_expense, top_category)
