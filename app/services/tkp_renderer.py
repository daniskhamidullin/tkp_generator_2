"""Render TKP Markdown from structured data."""
from __future__ import annotations

from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader, select_autoescape

from ..models import TKPData
from ..settings import settings
from .totals import compute_grand_total, total_before_discount


def render_tkp(data: TKPData) -> str:
    """Render TKP Markdown string using Jinja2 template."""

    environment = Environment(
        loader=FileSystemLoader(str(settings.templates_path)),
        autoescape=select_autoescape(enabled_extensions=(".j2",)),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = environment.get_template("tkp.md.j2")

    context: Dict[str, Any] = data.dict()
    scope_items = data.scope
    context["total_before_discount"] = total_before_discount(scope_items)
    context["grand_total"] = compute_grand_total(scope_items, data.commercial.discount_percent)

    return template.render(**context)
