# IA Finance Mobile

Versão mobile iniciada dentro do repositório principal em `mobile/`.

## Stack inicial
- Expo + React Native + TypeScript
- Expo Router
- SecureStore (sessão local)

## Funcionalidades já iniciadas
- Login
- Cadastro
- Sessão persistente local
- Dashboard mobile com teste de conexão ao backend

## Como rodar
```bash
cd mobile
npm install
npm run start
```

## Testar no celular (Expo Go)
1. Garanta o backend rodando no repositório principal:
   ```bash
   cd ..
   PYTHONPATH=src python -m smartbudget.web.app
   ```
2. Em outro terminal, suba o app mobile:
   ```bash
   cd mobile
   npm run start
   ```
3. Abra o app Expo Go no celular e escaneie o QR code.
4. Defina a URL da API antes de abrir o app (ajuste conforme seu IP local):
   ```bash
   EXPO_PUBLIC_API_URL=http://SEU_IP_LOCAL:8000 npm run start
   ```
   Exemplo: `http://192.168.0.10:8000`

## Próximas tarefas
1. Dashboard com dados estruturados via API JSON (não só leitura de HTML).
2. Cadastro de transações direto no app mobile.
3. Filtro por período no app.
4. Build Android `.aab` para Play Store.
