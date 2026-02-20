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
- Dashboard mobile com dados reais (saldo, gastos, insight e transações)
- Filtro por período (`YYYY-MM`) no app
- Cadastro de transações direto no app (entrada/saída)

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
1. Melhorar UX do filtro por período (seletor de mês nativo).
2. Incluir gráfico de categorias no app mobile.
3. Padronizar mensagens de erro por endpoint.
4. Build Android `.aab` para Play Store.


## Erro comum: `expo-asset` cannot be found
Se aparecer esse erro ao rodar `npm run start`, execute:

```bash
cd mobile
npm install
npx expo install expo-asset
```

No **PowerShell**, para subir com variável de ambiente:

```powershell
$env:EXPO_PUBLIC_API_URL="http://SEU_IP_LOCAL:8000"; npm run start
```


## Compatibilidade com Expo Go (Windows)
Este projeto foi atualizado para **Expo SDK 54**.

Se você estava com dependências antigas, rode no **PowerShell**:

```powershell
cd .\mobile
if (Test-Path .\node_modules) { Remove-Item -Recurse -Force .\node_modules }
if (Test-Path .\package-lock.json) { Remove-Item -Force .\package-lock.json }
npm install
npx expo install --fix
```

Depois inicie:

```powershell
$env:EXPO_PUBLIC_API_URL="http://SEU_IP_LOCAL:8000"; npm run start
```


## Erro de `ERESOLVE` com `@types/react` no Windows
Se o `npm install` falhar com conflito entre `react-native@0.81.x` e `@types/react`, rode no PowerShell:

```powershell
cd .\mobile
if (Test-Path .\node_modules) { Remove-Item -Recurse -Force .\node_modules }
if (Test-Path .\package-lock.json) { Remove-Item -Force .\package-lock.json }
npm install
npx expo install --fix
```

Se ainda houver conflito de resolução no seu npm, use temporariamente:

```powershell
npm install --legacy-peer-deps
```


## Erro `Cannot find module babel-preset-expo` (tela branca / code 500)
Se aparecer esse erro no terminal do Expo, instale o preset e sincronize dependências:

```powershell
cd .\mobile
npm install
npx expo install babel-preset-expo
npx expo install --fix
```

Depois reinicie o Metro limpando cache:

```powershell
npm run start -- --clear
```
