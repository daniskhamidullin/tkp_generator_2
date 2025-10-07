"""FastAPI application for TKP Generator."""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict

from fastapi import FastAPI
from pydantic import ValidationError

from .models import (
    CollectRequest,
    CollectResponse,
    CollectResponseNeedMoreInfo,
    CollectResponseReady,
    TKPData,
    pretty_validation_errors,
)
from .openai_client import openai_client
from .services.tkp_renderer import render_tkp
from .services.totals import compute_grand_total, total_before_discount
from .settings import settings

app = FastAPI(title=settings.project_name)


def _deep_update(target: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            target[key] = _deep_update(target[key], value)
        else:
            target[key] = value
    return target


@app.post("/tkp/collect", response_model=CollectResponse)
def collect_tkp(request: CollectRequest) -> CollectResponse:
    """Collect TKP data iteratively using OpenAI structured outputs."""

    state: Dict[str, Any] = deepcopy(request.state) if request.state else {}
    structured = openai_client.collect_structured_data(request.message, state)
    if structured:
        state = _deep_update(state, structured)

    try:
        data = TKPData.parse_obj(state)
    except ValidationError as exc:
        question = (
            "Пожалуйста, уточните данные: "
            f"{pretty_validation_errors(exc)}"
        )
        return CollectResponseNeedMoreInfo(
            need_more_info=True,
            question=question,
            state=state,
        )

    markdown = render_tkp(data)
    return CollectResponseReady(need_more_info=False, markdown=markdown, state=data.dict())


@app.post("/tkp/render")
def render_tkp_endpoint(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Render TKP directly from provided JSON payload."""

    data = TKPData.parse_obj(payload)
    markdown = render_tkp(data)
    totals = {
        "total_before_discount": total_before_discount(data.scope),
        "discount_percent": data.commercial.discount_percent or 0,
        "grand_total": compute_grand_total(data.scope, data.commercial.discount_percent),
        "currency": data.commercial.currency,
    }

    return {"markdown": markdown, "state": data.dict(), "totals": totals}


@app.get("/healthz")
def healthcheck() -> Dict[str, bool]:
    return {"ok": True}
