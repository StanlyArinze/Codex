from __future__ import annotations

import secrets
from datetime import date
from decimal import Decimal, InvalidOperation
from html import escape
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from smartbudget.ledger import Ledger
from smartbudget.repositories import TransactionRepository

ledger = Ledger()
repository = TransactionRepository()
sessions: dict[str, int] = {}

TYPE_LABELS = {
    "income": "Entrada",
    "expense": "Saída",
}


def _money(value: Decimal) -> str:
    return f"R$ {value:.2f}"


def _parse_period(period: str | None) -> tuple[int, int]:
    today = date.today()
    if not period:
        return today.year, today.month

    try:
        year_str, month_str = period.split("-", maxsplit=1)
        year = int(year_str)
        month = int(month_str)
        if 1 <= month <= 12:
            return year, month
    except ValueError:
        pass

    return today.year, today.month


def _get_session_token(handler: BaseHTTPRequestHandler) -> str | None:
    raw = handler.headers.get("Cookie")
    if not raw:
        return None
    cookie = SimpleCookie()
    cookie.load(raw)
    morsel = cookie.get("iafinance_session")
    return morsel.value if morsel else None


def _get_user(handler: BaseHTTPRequestHandler) -> tuple[int, str] | None:
    token = _get_session_token(handler)
    if not token:
        return None
    user_id = sessions.get(token)
    if not user_id:
        return None
    return repository.get_user(user_id)


def load_transactions_from_db(user_id: int) -> None:
    ledger.clear()
    for txn in repository.list_transactions(user_id):
        ledger.record_transaction(txn)


def _expense_chart(year: int, month: int) -> tuple[str, str]:
    palette = ["#ff6b6b", "#4ecdc4", "#ffe66d", "#5f6caf", "#f7a072", "#5aa9e6", "#c77dff"]
    totals: dict[str, Decimal] = {}

    for txn in ledger.transactions:
        if txn.date.year == year and txn.date.month == month and txn.type.value == "expense":
            totals[txn.category] = totals.get(txn.category, Decimal("0")) + txn.amount

    total_expense = sum(totals.values(), Decimal("0"))
    if total_expense <= 0:
        return "conic-gradient(#dbeafe 0deg 360deg)", "<li>Sem gastos no período.</li>"

    current_angle = Decimal("0")
    gradient_parts: list[str] = []
    legend_items: list[str] = []

    for idx, (category, amount) in enumerate(sorted(totals.items(), key=lambda item: item[1], reverse=True)):
        color = palette[idx % len(palette)]
        pct = (amount / total_expense) * Decimal("100")
        angle = (pct / Decimal("100")) * Decimal("360")
        start = current_angle
        end = start + angle
        gradient_parts.append(f"{color} {start:.2f}deg {end:.2f}deg")
        legend_items.append(
            "<li>"
            f"<span class='dot' style='background:{color}'></span>"
            f"<span>{escape(category)} — {pct.quantize(Decimal('0.1'))}% ({_money(amount)})</span>"
            "</li>"
        )
        current_angle = end

    gradient = "conic-gradient(" + ", ".join(gradient_parts) + ")"
    return gradient, "".join(legend_items)


def render_auth_page(message: str | None = None) -> str:
    message_html = f"<p class='error'>{escape(message)}</p>" if message else ""
    return f"""<!doctype html>
<html lang='pt-BR'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>IA Finance</title>
  <link rel='stylesheet' href='/static/styles.css'>
</head>
<body>
  <main class='container'>
    <header class='hero'>
      <h1>IA Finance</h1>
      <p class='auth-subtitle'>Faça login para acessar seu dashboard financeiro.</p>
    </header>

    <section class='grid'>
      <article class='card'>
        <h2>Entrar</h2>
        {message_html}
        <form method='post' action='/login' class='form'>
          <label>E-mail
            <input type='email' name='email' required>
          </label>
          <label>Senha
            <input type='password' name='password' required>
          </label>
          <button type='submit'>Entrar</button>
        </form>
      </article>

      <article class='card'>
        <h2>Criar conta</h2>
        <form method='post' action='/register' class='form'>
          <label>Nome
            <input type='text' name='name' required>
          </label>
          <label>E-mail
            <input type='email' name='email' required>
          </label>
          <label>Senha
            <input type='password' name='password' minlength='4' required>
          </label>
          <button type='submit'>Criar conta</button>
        </form>
      </article>
    </section>
  </main>
</body>
</html>"""


def render_dashboard(user_name: str, user_id: int, error: str | None = None, period: str | None = None) -> str:
    load_transactions_from_db(user_id)
    year, month = _parse_period(period)
    period_value = f"{year:04d}-{month:02d}"

    summary = ledger.monthly_summary(year, month)
    top_category = ledger.top_expense_category(year, month)
    insight = ledger.monthly_insight(year, month)

    expense_ratio = Decimal("0")
    if summary.total_income > 0:
        expense_ratio = ((summary.total_expense / summary.total_income) * Decimal("100")).quantize(Decimal("0.1"))

    pie_gradient, pie_legend = _expense_chart(year, month)

    rows = "".join(
        f"<tr><td>{txn.date}</td><td>{TYPE_LABELS[txn.type.value]}</td><td>{escape(txn.category)}</td>"
        f"<td>{escape(txn.description)}</td><td>{_money(txn.amount)}</td></tr>"
        for txn in reversed(ledger.transactions)
        if txn.date.year == year and txn.date.month == month
    )
    if not rows:
        rows = '<tr><td colspan="5">Nenhuma transação cadastrada para o período selecionado.</td></tr>'

    error_html = f'<p class="error">{escape(error)}</p>' if error else ""

    return f"""<!doctype html>
<html lang='pt-BR'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>IA Finance</title>
  <link rel='stylesheet' href='/static/styles.css'>
</head>
<body>
  <main class='container'>
    <header class='hero header-row'>
      <h1>IA Finance</h1>
      <div class='user-area'>
        <span>Olá, {escape(user_name)}</span>
        <form method='post' action='/logout'><button type='submit' class='ghost-btn'>Sair</button></form>
      </div>
    </header>

    <section class='card filter-card'>
      <form method='get' action='/' class='filter-form'>
        <label>Filtrar período
          <input type='month' name='period' value='{period_value}'>
        </label>
        <button type='submit'>Filtrar</button>
      </form>
    </section>

    <section class='grid metrics'>
      <article class='card destaque saldo-card'>
        <h2>Saldo do mês</h2>
        <p class='big-value'>{_money(summary.balance)}</p>
        <p class='muted'>Entrada total: {_money(summary.total_income)}</p>
      </article>

      <article class='card destaque gasto-card'>
        <h2>Gasto do mês</h2>
        <p class='big-value'>{_money(summary.total_expense)}</p>
        <p class='muted'>Comprometido da entrada: {expense_ratio}%</p>
      </article>

      <article class='card'>
        <h2>Indicadores</h2>
        <ul>
          <li><strong>Categoria com maior gasto:</strong> {escape(top_category)}</li>
          <li><strong>Status financeiro:</strong> {'Atenção' if expense_ratio >= 70 else 'Saudável'}</li>
        </ul>
        <p class='insight'>{escape(insight)}</p>
      </article>
    </section>

    <section class='grid'>
      <article class='card'>
        <h2>Gastos</h2>
        <div class='chart-wrap'>
          <div class='pie-chart' style='background:{pie_gradient}' aria-label='Gastos por categoria'></div>
          <ul class='legend'>{pie_legend}</ul>
        </div>
      </article>

      <article class='card'>
        <h2>Nova transação</h2>
        {error_html}
        <form method='post' action='/transactions' class='form'>
          <label>Valor
            <input type='number' step='0.01' min='0' name='amount' required>
          </label>
          <label>Descrição
            <input type='text' name='description' placeholder='Ex: Mercado, aluguel, salário...' required>
          </label>
          <label>Data
            <input type='date' name='txn_date' value='{date.today().isoformat()}' required>
          </label>
          <div class='type-buttons'>
            <button type='submit' name='transaction_type' value='expense' class='btn-expense'>Salvar saída</button>
            <button type='submit' name='transaction_type' value='income' class='btn-income'>Salvar entrada</button>
          </div>
        </form>
      </article>
    </section>

    <section class='card'>
      <h2>Transações do período</h2>
      <table>
        <thead>
          <tr><th>Data</th><th>Tipo</th><th>Categoria</th><th>Descrição</th><th>Valor</th></tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>
    </section>
  </main>
</body>
</html>"""


def save_transaction(user_id: int, form_data: dict[str, list[str]]) -> str | None:
    try:
        txn_type = form_data.get("transaction_type", [""])[0]
        amount = Decimal(form_data.get("amount", [""])[0])
        description = form_data.get("description", [""])[0].strip()
        txn_date = date.fromisoformat(form_data.get("txn_date", [""])[0])
    except (InvalidOperation, ValueError):
        return "Verifique valor e data antes de salvar."

    if not description:
        return "A descrição é obrigatória."

    if txn_type == "income":
        txn = ledger.add_income(amount, description, txn_date)
    else:
        txn = ledger.add_expense(amount, description, txn_date)

    repository.insert_transaction(user_id, txn)
    return None


def _set_session_cookie(handler: BaseHTTPRequestHandler, token: str) -> None:
    handler.send_header("Set-Cookie", f"iafinance_session={token}; HttpOnly; Path=/; SameSite=Lax")


def _clear_session_cookie(handler: BaseHTTPRequestHandler) -> None:
    handler.send_header("Set-Cookie", "iafinance_session=; HttpOnly; Path=/; Max-Age=0; SameSite=Lax")


class SmartBudgetHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/":
            query = parse_qs(parsed.query)
            period = query.get("period", [None])[0]
            user = _get_user(self)
            if not user:
                self._send_html(render_auth_page())
                return
            user_id, user_name = user
            self._send_html(render_dashboard(user_name=user_name, user_id=user_id, period=period))
            return

        if parsed.path == "/static/styles.css":
            with open("src/smartbudget/web/static/styles.css", "rb") as file:
                css = file.read()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/css; charset=utf-8")
            self.end_headers()
            self.wfile.write(css)
            return

        self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802
        content_length = int(self.headers.get("Content-Length", "0"))
        data = self.rfile.read(content_length).decode("utf-8")
        form_data = parse_qs(data)

        if self.path == "/register":
            name = form_data.get("name", [""])[0]
            email = form_data.get("email", [""])[0]
            password = form_data.get("password", [""])[0]
            ok, payload = repository.create_user(name, email, password)
            if not ok:
                self._send_html(render_auth_page(str(payload)), status=HTTPStatus.BAD_REQUEST)
                return

            token = secrets.token_urlsafe(32)
            sessions[token] = int(payload)
            self.send_response(HTTPStatus.SEE_OTHER)
            _set_session_cookie(self, token)
            self.send_header("Location", "/")
            self.end_headers()
            return

        if self.path == "/login":
            email = form_data.get("email", [""])[0]
            password = form_data.get("password", [""])[0]
            ok, payload = repository.authenticate_user(email, password)
            if not ok:
                self._send_html(render_auth_page(str(payload)), status=HTTPStatus.UNAUTHORIZED)
                return

            user_id, _ = payload
            token = secrets.token_urlsafe(32)
            sessions[token] = user_id
            self.send_response(HTTPStatus.SEE_OTHER)
            _set_session_cookie(self, token)
            self.send_header("Location", "/")
            self.end_headers()
            return

        if self.path == "/logout":
            token = _get_session_token(self)
            if token:
                sessions.pop(token, None)
            self.send_response(HTTPStatus.SEE_OTHER)
            _clear_session_cookie(self)
            self.send_header("Location", "/")
            self.end_headers()
            return

        if self.path == "/transactions":
            user = _get_user(self)
            if not user:
                self.send_response(HTTPStatus.SEE_OTHER)
                self.send_header("Location", "/")
                self.end_headers()
                return

            user_id, user_name = user
            error = save_transaction(user_id, form_data)
            if error:
                self._send_html(render_dashboard(user_name=user_name, user_id=user_id, error=error), status=HTTPStatus.BAD_REQUEST)
                return

            self.send_response(HTTPStatus.SEE_OTHER)
            self.send_header("Location", "/")
            self.end_headers()
            return

        self.send_error(HTTPStatus.NOT_FOUND)

    def log_message(self, format: str, *args: object) -> None:
        return

    def _send_html(self, body: str, status: HTTPStatus = HTTPStatus.OK) -> None:
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def run(host: str = "0.0.0.0", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), SmartBudgetHandler)
    print(f"IA Finance rodando em http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
