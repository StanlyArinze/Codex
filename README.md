# My Finance

Aplicativo de finanças pessoais com foco em uso local (offline-first) no mobile.

## O que está no projeto

- App mobile Expo em `mobile/`.
- Núcleo de domínio em Python (`Ledger`, modelos e categorização simples).
- Persistência local em SQLite (`TransactionRepository`).
- Testes automatizados de domínio e persistência.

## Estrutura principal

- `mobile/`: aplicativo React Native (Expo Router).
- `src/smartbudget/models.py`: modelos de domínio.
- `src/smartbudget/ai.py`: categorização por palavras-chave.
- `src/smartbudget/ledger.py`: regras de negócio.
- `src/smartbudget/repositories/transactions_sqlite.py`: persistência SQLite.
- `tests/test_ledger.py`: testes de domínio.
- `tests/test_persistence.py`: testes de persistência/autenticação.

## Rodar mobile

```bash
cd mobile
npm install
npx expo install --fix
npm run start -- --clear
```

## Rodar testes Python

```bash
PYTHONPATH=src pytest -q
```
