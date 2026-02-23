from datetime import date
from decimal import Decimal

from smartbudget.ai import categorize_transaction
from smartbudget.ledger import Ledger


def test_keyword_categorization():
    assert categorize_transaction("Uber para reunião") == "Transporte"
    assert categorize_transaction("Mercado semanal") == "Alimentação"


def test_monthly_summary_and_insight():
    ledger = Ledger()
    d = date(2026, 2, 10)

    ledger.add_income(Decimal("3000"), "Salário", d)
    ledger.add_expense(Decimal("900"), "aluguel", d)
    ledger.add_expense(Decimal("400"), "mercado", d)

    summary = ledger.monthly_summary(2026, 2)
    assert summary.total_income == Decimal("3000")
    assert summary.total_expense == Decimal("1300")
    assert summary.balance == Decimal("1700")

    insight = ledger.monthly_insight(2026, 2)
    assert "Moradia" in insight
