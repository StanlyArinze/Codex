# SmartBudget AI (MVP)

Projeto inicial de portfólio para **finanças pessoais com IA**.

## O que já está pronto

- Registro de receitas e despesas.
- Categorização automática de despesas por palavras-chave.
- Resumo mensal (receita, gasto e saldo).
- Insight mensal em linguagem natural com base no comportamento financeiro.
- Suite básica de testes.

## Estrutura

- `src/smartbudget/models.py`: modelos de domínio (`Transaction`, `MonthlySummary`).
- `src/smartbudget/ai.py`: categorização e geração de insight.
- `src/smartbudget/ledger.py`: regras de negócio.
- `src/smartbudget/cli.py`: demo local via terminal.
- `tests/test_ledger.py`: testes do MVP.

## Como rodar localmente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip pytest
PYTHONPATH=src python -m smartbudget.cli
```

## Como testar

```bash
PYTHONPATH=src pytest -q
```

## Próximos passos

1. API HTTP (FastAPI) para integração com frontend.
2. Persistência em banco (PostgreSQL/SQLite).
3. Login por usuário.
4. Integração com LLM para categorização e recomendações mais avançadas.
5. Dashboard web com gráficos e metas.
