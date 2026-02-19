from __future__ import annotations

from collections.abc import Callable
from decimal import Decimal

DEFAULT_CATEGORY = "Outros"

CATEGORY_KEYWORDS: dict[str, tuple[str, ...]] = {
    "Alimentação": ("mercado", "restaurante", "ifood", "padaria", "lanche", "delivery"),
    "Transporte": ("uber", "99", "ônibus", "combustível", "gasolina", "metrô", "pedágio"),
    "Moradia": ("aluguel", "condomínio", "energia", "água", "internet", "gás"),
    "Saúde": ("farmácia", "médico", "consulta", "plano de saúde", "exame"),
    "Educação": ("curso", "faculdade", "livro", "escola", "bootcamp"),
    "Lazer": ("cinema", "show", "viagem", "jogo", "netflix", "spotify"),
    "Assinaturas": ("assinatura", "saas", "mensalidade", "anuidade"),
}


AIProvider = Callable[[str], str]


def categorize_transaction(description: str, ai_provider: AIProvider | None = None) -> str:
    """Return a category for transaction text.

    If an AI provider is available it is used first; if it fails or returns an
    empty string, fallback keyword classification is applied.
    """

    normalized = description.lower().strip()

    if ai_provider:
        try:
            suggestion = ai_provider(description).strip()
            if suggestion:
                return suggestion
        except Exception:
            # Intentionally silent: the app should keep working even when AI fails.
            pass

    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            return category

    return DEFAULT_CATEGORY


def generate_monthly_insight(total_income: Decimal, total_expense: Decimal, top_category: str) -> str:
    if total_income <= 0:
        return "Adicione receitas para receber recomendações financeiras mais úteis."

    expense_ratio = (total_expense / total_income) * Decimal("100")

    if expense_ratio >= 90:
        status = "atenção máxima"
    elif expense_ratio >= 70:
        status = "zona de cautela"
    else:
        status = "situação saudável"

    return (
        f"Você está em {status}: gastos em {expense_ratio.quantize(Decimal('0.1'))}% "
        f"da sua receita no mês. A categoria com maior impacto foi {top_category}."
    )
