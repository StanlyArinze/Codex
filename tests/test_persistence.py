from datetime import date
from decimal import Decimal

from smartbudget.models import Transaction, TransactionType
from smartbudget.repositories import TransactionRepository


def test_repository_persists_transactions(tmp_path):
    repo = TransactionRepository(db_path=str(tmp_path / "smartbudget.db"))
    ok, created = repo.create_user("Ana", "ana@example.com", "1234")
    assert ok
    user_id = int(created)

    txn = Transaction(
        amount=Decimal("123.45"),
        description="Mercado",
        date=date(2026, 2, 19),
        category="Alimentação",
        type=TransactionType.EXPENSE,
    )

    repo.insert_transaction(user_id, txn)

    loaded = repo.list_transactions(user_id)
    assert len(loaded) == 1
    assert loaded[0].description == "Mercado"
    assert loaded[0].amount == Decimal("123.45")
    assert loaded[0].type is TransactionType.EXPENSE


def test_user_authentication_roundtrip(tmp_path):
    repo = TransactionRepository(db_path=str(tmp_path / "smartbudget.db"))
    ok, created = repo.create_user("Bruno", "bruno@example.com", "abcd")
    assert ok
    assert int(created) > 0

    login_ok, payload = repo.authenticate_user("bruno@example.com", "abcd")
    assert login_ok
    user_id, name = payload
    assert user_id == int(created)
    assert name == "Bruno"
