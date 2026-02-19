from __future__ import annotations

import hashlib
import hmac
import os
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
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    amount TEXT NOT NULL,
                    description TEXT NOT NULL,
                    date TEXT NOT NULL,
                    category TEXT NOT NULL,
                    type TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
                """
            )

            columns = [row[1] for row in conn.execute("PRAGMA table_info(transactions)").fetchall()]
            if "user_id" not in columns:
                conn.execute("ALTER TABLE transactions ADD COLUMN user_id INTEGER")

    def _hash_password(self, password: str) -> str:
        salt = os.urandom(16).hex()
        hashed = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
        return f"{salt}${hashed}"

    def _verify_password(self, password: str, password_hash: str) -> bool:
        try:
            salt, known_hash = password_hash.split("$", maxsplit=1)
        except ValueError:
            return False
        candidate = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
        return hmac.compare_digest(candidate, known_hash)

    def create_user(self, name: str, email: str, password: str) -> tuple[bool, str | int]:
        if not name.strip() or not email.strip() or len(password) < 4:
            return False, "Preencha nome, e-mail e senha (mínimo 4 caracteres)."

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                    (name.strip(), email.strip().lower(), self._hash_password(password)),
                )
                return True, cursor.lastrowid
        except sqlite3.IntegrityError:
            return False, "Este e-mail já está cadastrado."

    def authenticate_user(self, email: str, password: str) -> tuple[bool, str | tuple[int, str]]:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT id, name, password_hash FROM users WHERE email = ?",
                (email.strip().lower(),),
            ).fetchone()

        if not row:
            return False, "Usuário não encontrado."

        user_id, name, password_hash = row
        if not self._verify_password(password, password_hash):
            return False, "Senha inválida."

        return True, (user_id, name)

    def get_user(self, user_id: int) -> tuple[int, str] | None:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("SELECT id, name FROM users WHERE id = ?", (user_id,)).fetchone()
        return row if row else None

    def insert_transaction(self, user_id: int, txn: Transaction) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO transactions (user_id, amount, description, date, category, type)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    str(txn.amount),
                    txn.description,
                    txn.date.isoformat(),
                    txn.category,
                    txn.type.value,
                ),
            )

    def list_transactions(self, user_id: int) -> list[Transaction]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                """
                SELECT amount, description, date, category, type
                FROM transactions
                WHERE user_id = ?
                ORDER BY id ASC
                """,
                (user_id,),
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

    def clear_users(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM users")
