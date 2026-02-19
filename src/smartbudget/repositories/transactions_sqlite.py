from __future__ import annotations

import sqlite3
from datetime import date
from decimal import Decimal
from pathlib import Path

from smartbudget.models import Transaction, TransactionType


class TransactionRepository:
    def __init__(self, db_path: str = "data/smartbudget.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    def init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount TEXT NOT NULL,
                    description TEXT NOT NULL,
                    date TEXT NOT NULL,
                    category TEXT NOT NULL,
                    type TEXT NOT NULL
                )
                """
            )

    def insert_transaction(self, txn: Transaction) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO transactions (amount, description, date, category, type)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    str(txn.amount),
                    txn.description,
                    txn.date.isoformat(),
                    txn.category,
                    txn.type.value,
                ),
            )

    def list_transactions(self) -> list[Transaction]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT amount, description, date, category, type FROM transactions ORDER BY id ASC"
            ).fetchall()

        return [
            Transaction(
                amount=Decimal(amount),
                description=description,
                date=date.fromisoformat(txn_date),
                category=category,
                type=TransactionType(txn_type),
            )
            for amount, description, txn_date, category, txn_type in rows
        ]

    def clear_transactions(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM transactions")
