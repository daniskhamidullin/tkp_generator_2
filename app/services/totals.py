"""Utilities to calculate TKP totals."""
from __future__ import annotations

from typing import Iterable

from ..models import ScopeItem


def total_before_discount(scope: Iterable[ScopeItem]) -> float:
    """Sum of scope line totals before discount."""

    return round(sum(item.qty * item.price for item in scope), 2)


def total_after_discount(total: float, discount_percent: float | None) -> float:
    """Apply discount percentage to total."""

    discount = (discount_percent or 0) / 100
    return round(total * (1 - discount), 2)


def compute_grand_total(scope: Iterable[ScopeItem], discount_percent: float | None) -> float:
    """Helper to compute grand total from scope and discount."""

    return total_after_discount(total_before_discount(scope), discount_percent)
