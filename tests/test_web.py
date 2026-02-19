from urllib.parse import parse_qs

from smartbudget.web.app import ledger, render_dashboard, repository, save_transaction


def setup_function() -> None:
    ledger.clear()
    repository.clear_transactions()


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


def test_data_survives_memory_reset():
    save_transaction(
        parse_qs("transaction_type=income&amount=5000&description=Salario&txn_date=2026-02-19")
    )

    ledger.clear()
    html = render_dashboard()

    assert "Salario" in html
    assert "R$ 5000.00" in html
