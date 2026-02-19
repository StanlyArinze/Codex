# IA Finance (MVP SaaS)

Projeto inicial de portfólio para **finanças pessoais com IA**, com interface web para teste em navegador.

## O que já está pronto

- Registro de entradas e saídas.
- Categorização automática de despesas por palavras-chave.
- Resumo mensal (entrada, gasto e saldo).
- Insight mensal em linguagem natural com base no comportamento financeiro.
- Dashboard web com:
  - filtro por período (mês/ano),
  - indicador de categoria com maior gasto,
  - percentual da entrada comprometida,
  - tabela de transações por período,
  - visual renovado com tema colorido,
  - gráfico de gastos por categoria com animação.
- **Multiusuário com autenticação** (cadastro, login e logout).
- Persistência local em SQLite (dados não somem ao reiniciar o servidor).
- Suite de testes para domínio, web e persistência.

## Estrutura

- `src/smartbudget/models.py`: modelos de domínio (`Transaction`, `MonthlySummary`).
- `src/smartbudget/ai.py`: categorização e geração de insight.
- `src/smartbudget/ledger.py`: regras de negócio.
- `src/smartbudget/repositories/transactions_sqlite.py`: repositório SQLite + usuários/auth.
- `src/smartbudget/web/app.py`: servidor HTTP, autenticação e dashboard SaaS.
- `src/smartbudget/web/static/styles.css`: estilos da interface.
- `tests/test_ledger.py`: testes do domínio.
- `tests/test_web.py`: testes do dashboard.
- `tests/test_persistence.py`: testes de persistência e autenticação.

## Como rodar localmente (navegador)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -U pip pytest
PYTHONPATH=src python -m smartbudget.web.app
```

Depois abra: `http://127.0.0.1:8000`

## Banco de dados

- O banco é criado automaticamente em: `data/smartbudget.db`.
- Para resetar os dados, apague este arquivo.

## Como testar

```bash
PYTHONPATH=src pytest -q
```

## Próximos passos SaaS

1. Integração real com LLM para categorização.
2. Metas por categoria e alertas.
3. Deploy (Render/Fly/Vercel + API).
