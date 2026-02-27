# Bateria de Testes em Aparelhos Reais — My Finance

## Objetivo
Validar build release Android antes de enviar para produção.

## Matriz mínima
- Android 11 (API 30)
- Android 12 (API 31)
- Android 13 (API 33)
- Android 14 (API 34)

## Cenários críticos
1. Abrir app e validar splash + dashboard.
2. Criar receita, criar despesa, editar e excluir transação.
3. Trocar mês no filtro e validar totalização.
4. Fechar/abrir app e conferir persistência local.
5. Alternar tema claro/escuro.
6. Testar com internet desligada (fluxo local continua funcional).

## Critério de aceite
- Sem crash em 100% dos cenários críticos.
- Sem perda de dados locais após reinicialização do app.
