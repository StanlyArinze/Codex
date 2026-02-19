# IA Finance Mobile - Repositório separado iniciado

Conforme solicitado, a versão mobile foi iniciada em um repositório separado local:

- Caminho: `/workspace/IAFinanceMobile`
- Repositório Git: inicializado em `main`
- Commit inicial: `chore: bootstrap IA Finance mobile repo with Expo starter`

## O que já foi criado
- Base Expo + React Native + TypeScript
- Estrutura inicial com Expo Router (`app/_layout.tsx`, `app/index.tsx`)
- Tela inicial com cards de **Saldo** e **Gastos**
- Arquivos de configuração (`package.json`, `app.json`, `babel.config.js`, `tsconfig.json`)

## Como publicar no GitHub (exemplo)
```bash
cd /workspace/IAFinanceMobile
git remote add origin <URL_DO_REPO_MOBILE>
git push -u origin main
```

## Próximos passos sugeridos
1. Conectar login/cadastro com o backend atual.
2. Persistir sessão no app (secure storage).
3. Consumir endpoint de dashboard com filtros.
4. Preparar build `.aab` para Play Store.
