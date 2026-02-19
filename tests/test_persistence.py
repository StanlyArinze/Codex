from datetime import date
from decimal import Decimal

from smartbudget.models import Transaction, TransactionType
from smartbudget.repositories import TransactionRepository


def test_repository_persists_transactions(tmp_path):
    repo = TransactionRepository(db_path=str(tmp_path / "smartbudget.db"))

    txn = Transaction(
        amount=Decimal("123.45"),
        description="Mercado",
        date=date(2026, 2, 19),
        category="Alimentação",
        type=TransactionType.EXPENSE,
    )

    repo.insert_transaction(txn)

    loaded = repo.list_transactions()
    assert len(loaded) == 1
    assert loaded[0].description == "Mercado"
    assert loaded[0].amount == Decimal("123.45")
    assert loaded[0].type is TransactionType.EXPENSE
