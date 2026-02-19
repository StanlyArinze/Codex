from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation
from html import escape
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from smartbudget.ledger import Ledger
from smartbudget.repositories import TransactionRepository

ledger = Ledger()
repository = TransactionRepository()


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


def load_transactions_from_db() -> None:
    ledger.clear()
    for txn in repository.list_transactions():
        ledger.record_transaction(txn)


def render_dashboard(error: str | None = None, period: str | None = None) -> str:
    load_transactions_from_db()
    year, month = _parse_period(period)
    period_value = f"{year:04d}-{month:02d}"

    summary = ledger.monthly_summary(year, month)
    top_category = ledger.top_expense_category(year, month)
    insight = ledger.monthly_insight(year, month)

    expense_ratio = Decimal("0")
    if summary.total_income > 0:
        expense_ratio = ((summary.total_expense / summary.total_income) * Decimal("100")).quantize(Decimal("0.1"))

    rows = "".join(
        f"<tr><td>{txn.date}</td><td>{txn.type.value}</td><td>{escape(txn.category)}</td>"
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
  <title>SmartBudget AI SaaS</title>
  <link rel='stylesheet' href='/static/styles.css'>
</head>
<body>
  <main class='container'>
    <h1>SmartBudget AI SaaS</h1>
    <p class='subtitle'>Filtro mensal + indicadores de gastos para análise rápida.</p>

    <section class='card'>
      <form method='get' action='/' class='filter-form'>
        <label>Período
          <input type='month' name='period' value='{period_value}'>
        </label>
        <button type='submit'>Aplicar filtro</button>
      </form>
    </section>

    <section class='grid metrics'>
      <article class='card'>
        <h2>Resumo {summary.month}</h2>
        <ul>
          <li><strong>Receita:</strong> {_money(summary.total_income)}</li>
          <li><strong>Gastos:</strong> {_money(summary.total_expense)}</li>
          <li><strong>Saldo:</strong> {_money(summary.balance)}</li>
        </ul>
      </article>

      <article class='card'>
        <h2>Indicadores</h2>
        <ul>
          <li><strong>Top categoria:</strong> {escape(top_category)}</li>
          <li><strong>% da receita comprometida:</strong> {expense_ratio}%</li>
        </ul>
        <p class='insight'>{escape(insight)}</p>
      </article>

      <article class='card'>
        <h2>Nova transação</h2>
        {error_html}
        <form method='post' action='/transactions' class='form'>
          <label>Tipo
            <select name='transaction_type'>
              <option value='expense'>Despesa</option>
              <option value='income'>Receita</option>
            </select>
          </label>
          <label>Valor
            <input type='number' step='0.01' min='0' name='amount' required>
          </label>
          <label>Descrição
            <input type='text' name='description' placeholder='Ex: Uber centro' required>
          </label>
          <label>Data
            <input type='date' name='txn_date' value='{date.today().isoformat()}' required>
          </label>
          <button type='submit'>Salvar</button>
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


def save_transaction(form_data: dict[str, list[str]]) -> str | None:
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

    repository.insert_transaction(txn)
    return None


class SmartBudgetHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/":
            query = parse_qs(parsed.query)
            period = query.get("period", [None])[0]
            self._send_html(render_dashboard(period=period))
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
        if self.path != "/transactions":
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        data = self.rfile.read(content_length).decode("utf-8")
        form_data = parse_qs(data)
        error = save_transaction(form_data)

        if error:
            self._send_html(render_dashboard(error), status=HTTPStatus.BAD_REQUEST)
            return

        self.send_response(HTTPStatus.SEE_OTHER)
        self.send_header("Location", "/")
        self.end_headers()

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
    print(f"SmartBudget rodando em http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
