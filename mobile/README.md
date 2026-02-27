# IA Finance Mobile

Versão mobile iniciada dentro do repositório principal em `mobile/`.

## Stack inicial
- Expo + React Native + TypeScript
- Expo Router
- SecureStore (sessão local)

## Funcionalidades já iniciadas
- Sem login (dados locais no dispositivo)
- Cache local de transações com AsyncStorage
- Dashboard com saldo/gastos e lista de transações (mais recentes primeiro)
- Filtro por período (`YYYY-MM`)
- Tema claro / escuro / sistema
- Tela de configurações com versão do app

## Como rodar
```powershell
cd .\mobile
npm install
npx expo install --fix
npm run start -- --clear
```

## Testar no celular (Expo Go)
1. No **PowerShell** na raiz do projeto (`Codex`), suba o backend:
   ```powershell
   $env:PYTHONPATH="src"
   python -m smartbudget.web.app
   ```
2. Em outro terminal PowerShell, suba o mobile:
   ```powershell
   cd .\mobile
   $env:EXPO_PUBLIC_API_URL="http://SEU_IP_LOCAL:8000"
   npm run start -- --clear
   ```
3. Abra o Expo Go no celular e escaneie o QR code.
4. Confirme que celular e PC estão na mesma rede Wi‑Fi.

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


## Preparação para Play Store
Status atual: base pronta ✅

Concluído nesta etapa:
1. `android.package` final definido (`com.myfinance.app`).
2. Ícone/splash finais serão versionados fora do repositório (evitar binários neste PR).
3. EAS Build configurado para preview (APK) e produção (AAB).
4. Permissões Android mínimas revisadas (`INTERNET`).
5. Política de privacidade criada em `mobile/PRIVACY_POLICY.md`.
6. Ficha inicial da loja criada em `mobile/PLAYSTORE_LISTING_PTBR.md`.
7. Bateria de testes em aparelhos reais definida em `mobile/REAL_DEVICE_TEST_PLAN.md`.

Próximos comandos (mantenedor):
```powershell
cd .\mobile
npx eas-cli@latest login
npx eas-cli@latest build -p android --profile production
npx eas-cli@latest submit -p android --profile production
```

Observação: geração do `.aab` assinado depende da autenticação da conta Expo/Google Play do mantenedor.

## Erro `Unable to resolve react-native-svg`
Se o bundle falhar com erro em `import Svg ... from "react-native-svg"`, instale a dependência compatível com o Expo SDK:

```powershell
cd .\mobile
npx expo install react-native-svg
npm install
npm run start -- --clear
```
