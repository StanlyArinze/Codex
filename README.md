# SmartBudget AI (MVP SaaS)

Projeto inicial de portfólio para **finanças pessoais com IA**, agora com interface web para teste em navegador.

## O que já está pronto

- Registro de receitas e despesas.
- Categorização automática de despesas por palavras-chave.
- Resumo mensal (receita, gasto e saldo).
- Insight mensal em linguagem natural com base no comportamento financeiro.
- Dashboard web (formulário + tabela de transações + cards de resumo).
- Suite básica de testes.

## Estrutura

- `src/smartbudget/models.py`: modelos de domínio (`Transaction`, `MonthlySummary`).
- `src/smartbudget/ai.py`: categorização e geração de insight.
- `src/smartbudget/ledger.py`: regras de negócio.
- `src/smartbudget/web/app.py`: servidor HTTP e renderização do dashboard SaaS.
- `src/smartbudget/web/static/styles.css`: estilos da interface.
- `tests/test_ledger.py`: testes do domínio.
- `tests/test_web.py`: testes do dashboard.

## Como rodar localmente (navegador)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -U pip pytest
PYTHONPATH=src python -m smartbudget.web.app
```

Depois abra: `http://127.0.0.1:8000`

## Como testar

```bash
PYTHONPATH=src pytest -q
```

## Próximos passos SaaS

1. Persistência em banco (PostgreSQL).
2. Multiusuário com autenticação.
3. Integração real com LLM para categorização.
4. Metas por categoria e alertas.
5. Deploy (Render/Fly/Vercel + API).
