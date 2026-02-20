import json
from urllib.parse import parse_qs

from smartbudget.web.app import (
    ledger,
    render_auth_page,
    render_dashboard,
    render_dashboard_payload,
    render_health_payload,
    render_session_payload,
    repository,
    save_transaction,
)


def setup_function() -> None:
    ledger.clear()
    repository.clear_transactions()
    repository.clear_users()


def test_auth_page_loads():
    html = render_auth_page()
    assert "IA Finance" in html
    assert "Entrar" in html
    assert "Criar conta" in html


def test_save_transaction_and_render_for_user():
    ok, created = repository.create_user("Ana", "ana@example.com", "1234")
    assert ok is True
    user_id = int(created)

    error = save_transaction(
        user_id,
        parse_qs("transaction_type=expense&amount=120&description=Uber+centro&txn_date=2026-02-19"),
    )
    assert error is None

    html = render_dashboard(user_name="Ana", user_id=user_id, period="2026-02")
    assert "Uber centro" in html
    assert "Transporte" in html
    assert "Saída" in html
    assert "tipo-expense" in html


def test_data_isolated_by_user():
    ok_1, user_1 = repository.create_user("Ana", "ana@teste.com", "1234")
    ok_2, user_2 = repository.create_user("Bruno", "bruno@teste.com", "1234")
    assert ok_1 and ok_2

    save_transaction(int(user_1), parse_qs("transaction_type=income&amount=5000&description=Salario&txn_date=2026-02-19"))
    save_transaction(int(user_2), parse_qs("transaction_type=expense&amount=200&description=Mercado&txn_date=2026-02-19"))

    html_ana = render_dashboard(user_name="Ana", user_id=int(user_1), period="2026-02")
    html_bruno = render_dashboard(user_name="Bruno", user_id=int(user_2), period="2026-02")

    assert "Salario" in html_ana
    assert "<td>Mercado</td>" not in html_ana
    assert "<td>Mercado</td>" in html_bruno
    assert "<td>Salario</td>" not in html_bruno


def test_period_filter_hides_other_month_transactions():
    ok, user = repository.create_user("Ana", "ana2@teste.com", "1234")
    assert ok

    save_transaction(
        int(user), parse_qs("transaction_type=expense&amount=100&description=Mercado+Janeiro&txn_date=2026-01-10")
    )
    save_transaction(
        int(user), parse_qs("transaction_type=expense&amount=200&description=Mercado+Fevereiro&txn_date=2026-02-10")
    )

    january = render_dashboard(user_name="Ana", user_id=int(user), period="2026-01")
    assert "Mercado Janeiro" in january
    assert "Mercado Fevereiro" not in january

    february = render_dashboard(user_name="Ana", user_id=int(user), period="2026-02")
    assert "Mercado Fevereiro" in february
    assert "Mercado Janeiro" not in february


def test_status_financeiro_destacado():
    ok, user = repository.create_user("Carla", "carla@teste.com", "1234")
    assert ok
    save_transaction(int(user), parse_qs("transaction_type=income&amount=1000&description=Salario&txn_date=2026-02-10"))
    save_transaction(int(user), parse_qs("transaction_type=expense&amount=200&description=mercado&txn_date=2026-02-10"))
    html = render_dashboard(user_name="Carla", user_id=int(user), period="2026-02")
    assert "status-bom" in html


def test_render_health_payload_json():
    payload = json.loads(render_health_payload().decode("utf-8"))
    assert payload == {"status": "ok", "service": "ia-finance"}


def test_render_session_payload_json():
    anonymous = json.loads(render_session_payload(None).decode("utf-8"))
    assert anonymous == {"authenticated": False}

    authenticated = json.loads(render_session_payload((7, "Lia")).decode("utf-8"))
    assert authenticated == {"authenticated": True, "user": {"id": 7, "name": "Lia"}}


def test_render_dashboard_payload_json():
    ok, user = repository.create_user("Dani", "dani@teste.com", "1234")
    assert ok

    save_transaction(int(user), parse_qs("transaction_type=income&amount=2500&description=Freela&txn_date=2026-03-05"))
    save_transaction(int(user), parse_qs("transaction_type=expense&amount=500&description=Aluguel&txn_date=2026-03-08"))

    payload = json.loads(render_dashboard_payload(user_id=int(user), period="2026-03").decode("utf-8"))

    assert payload["period"] == "2026-03"
    assert payload["summary"] == {"income": "2500", "expense": "500", "balance": "2000"}
    assert payload["top_category"]
    assert payload["insight"]
    assert len(payload["transactions"]) == 2
