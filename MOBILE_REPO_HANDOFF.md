# IA Finance Mobile - Status atual

A versão mobile agora está **dentro deste repositório principal**.

## Localização
- Pasta: `mobile/`

## O que já foi criado
- Base Expo + React Native + TypeScript
- Estrutura inicial com Expo Router (`mobile/app/_layout.tsx`, `mobile/app/index.tsx`)
- Tela inicial com cards de **Saldo** e **Gastos**
- Arquivos de configuração (`mobile/package.json`, `mobile/app.json`, `mobile/babel.config.js`, `mobile/tsconfig.json`)

## Como rodar
```bash
cd mobile
npm install
npm run start
```

## Próximos passos sugeridos
1. Conectar login/cadastro com o backend atual.
2. Persistir sessão no app (secure storage).
3. Consumir endpoint de dashboard com filtros.
4. Preparar build `.aab` para Play Store.
