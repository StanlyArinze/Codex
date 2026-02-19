from urllib.parse import parse_qs

from smartbudget.web.app import ledger, render_dashboard, repository, save_transaction


def setup_function() -> None:
    ledger.clear()
    repository.clear_transactions()


def test_dashboard_loads():
    html = render_dashboard()
    assert "SmartBudget AI SaaS" in html
    assert "Aplicar filtro" in html


def test_save_transaction_and_render():
    error = save_transaction(
        parse_qs("transaction_type=expense&amount=120&description=Uber+centro&txn_date=2026-02-19")
    )
    assert error is None

    html = render_dashboard(period="2026-02")
    assert "Uber centro" in html
    assert "Transporte" in html


def test_data_survives_memory_reset():
    save_transaction(
        parse_qs("transaction_type=income&amount=5000&description=Salario&txn_date=2026-02-19")
    )

    ledger.clear()
    html = render_dashboard(period="2026-02")

    assert "Salario" in html
    assert "R$ 5000.00" in html


def test_period_filter_hides_other_month_transactions():
    save_transaction(
        parse_qs("transaction_type=expense&amount=100&description=Mercado+Janeiro&txn_date=2026-01-10")
    )
    save_transaction(
        parse_qs("transaction_type=expense&amount=200&description=Mercado+Fevereiro&txn_date=2026-02-10")
    )

    january = render_dashboard(period="2026-01")
    assert "Mercado Janeiro" in january
    assert "Mercado Fevereiro" not in january

    february = render_dashboard(period="2026-02")
    assert "Mercado Fevereiro" in february
    assert "Mercado Janeiro" not in february
