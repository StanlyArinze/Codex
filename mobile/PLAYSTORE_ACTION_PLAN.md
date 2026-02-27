# My Finance — Plano de Ação para Play Store

## Objetivo
Publicar a primeira versão Android com risco baixo de rejeição.

## Fase 1 — Base técnica
- [x] Definir `android.package` final: `com.myfinance.app`.
- [ ] Definir ícone, adaptive icon e splash finais no `app.json` (fora do repositório).
- [x] Configurar `eas.json` com build preview (APK) e produção (AAB).
- [ ] Executar `eas login` no ambiente do mantenedor.
- [ ] Gerar `.aab` assinado em `production`.

## Fase 2 — Conformidade
- [x] Revisar permissões Android (mínimas: `INTERNET`).
- [x] Criar política de privacidade (`mobile/PRIVACY_POLICY.md`).
- [ ] Publicar a política em URL pública.
- [ ] Preencher formulário Data Safety no Play Console.

## Fase 3 — Qualidade e release
- [x] Preparar ficha da loja base (`mobile/PLAYSTORE_LISTING_PTBR.md`).
- [x] Definir bateria de testes em aparelhos reais (`mobile/REAL_DEVICE_TEST_PLAN.md`).
- [ ] Rodar bateria em Android 11/12/13/14.
- [ ] Subir build para `internal testing` e coletar feedback.

## Comandos sugeridos (PowerShell)
```powershell
cd .\mobile
npm install
npx expo install --fix
npx eas-cli@latest login
npx eas-cli@latest build -p android --profile preview
npx eas-cli@latest build -p android --profile production
npx eas-cli@latest submit -p android --profile production
```

## Observações
- O passo de build/submissão exige conta Expo + credenciais Google Play do mantenedor.
- O app continua offline-first; backend é opcional para uso básico.
