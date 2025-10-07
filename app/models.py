"""Pydantic models for TKP API."""
from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, EmailStr, Field, ValidationError


class ClientInfo(BaseModel):
    name: str
    inn: Optional[str] = None
    kpp: Optional[str] = None
    contact_name: str
    email: EmailStr
    phone: Optional[str] = None


class ProjectInfo(BaseModel):
    title: str
    summary: str
    deadline: str


class ScopeItem(BaseModel):
    item: str
    desc: Optional[str] = None
    qty: float
    unit: str
    price: float


class CommercialInfo(BaseModel):
    currency: Literal["RUB", "USD", "EUR"]
    vat_included: bool
    discount_percent: Optional[float] = Field(default=0, ge=0, le=100)
    payment_terms: str


class LegalInfo(BaseModel):
    valid_until: str
    warranty: str
    liability: Optional[str] = None


class SignaturesInfo(BaseModel):
    supplier_sign: Optional[str] = None
    client_sign: Optional[str] = None


class TKPData(BaseModel):
    client: ClientInfo
    project: ProjectInfo
    scope: List[ScopeItem]
    commercial: CommercialInfo
    legal: LegalInfo
    signatures: SignaturesInfo = SignaturesInfo()


class CollectRequest(BaseModel):
    message: str
    state: Dict[str, Any] = Field(default_factory=dict)


class CollectResponseNeedMoreInfo(BaseModel):
    need_more_info: Literal[True]
    question: str
    state: Dict[str, Any]


class CollectResponseReady(BaseModel):
    need_more_info: Literal[False]
    markdown: str
    state: Dict[str, Any]


CollectResponse = Union[CollectResponseNeedMoreInfo, CollectResponseReady]


def pretty_validation_errors(error: ValidationError) -> str:
    """Format validation errors for human readable prompts."""

    fragments = []
    for err in error.errors():
        loc = ".".join(str(part) for part in err["loc"])
        msg = err["msg"]
        fragments.append(f"{loc}: {msg}")
    return "; ".join(fragments)
