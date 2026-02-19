from urllib.parse import parse_qs

from smartbudget.web.app import ledger, render_dashboard, save_transaction


def setup_function() -> None:
    ledger.clear()


def test_dashboard_loads():
    html = render_dashboard()
    assert "SmartBudget AI SaaS" in html
    assert "Nenhuma transação cadastrada ainda" in html


def test_save_transaction_and_render():
    error = save_transaction(
        parse_qs("transaction_type=expense&amount=120&description=Uber+centro&txn_date=2026-02-19")
    )
    assert error is None

    html = render_dashboard()
    assert "Uber centro" in html
    assert "Transporte" in html
