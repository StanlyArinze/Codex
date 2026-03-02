from __future__ import annotations

from datetime import date
from decimal import Decimal

from .ledger import Ledger


def demo() -> None:
    ledger = Ledger()
    today = date.today()

    ledger.add_income(Decimal("4500"), "Salário", today)
    ledger.add_expense(Decimal("120"), "Uber para o trabalho", today)
    ledger.add_expense(Decimal("350"), "mercado do mês", today)
    ledger.add_expense(Decimal("89.90"), "Assinatura de streaming", today)

    summary = ledger.monthly_summary(today.year, today.month)

    print(f"Mês: {summary.month}")
    print(f"Receita: R$ {summary.total_income}")
    print(f"Gastos: R$ {summary.total_expense}")
    print(f"Saldo: R$ {summary.balance}")
    print(f"Insight: {ledger.monthly_insight(today.year, today.month)}")


if __name__ == "__main__":
    demo()
