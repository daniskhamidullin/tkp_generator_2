from app.models import ScopeItem
from app.services.totals import compute_grand_total, total_after_discount, total_before_discount


def make_scope():
    return [
        ScopeItem(item="Работа 1", qty=2, unit="шт", price=1000),
        ScopeItem(item="Работа 2", qty=1, unit="шт", price=500),
    ]


def test_total_before_discount():
    assert total_before_discount(make_scope()) == 2500.0


def test_total_after_discount():
    assert total_after_discount(2000, 10) == 1800.0
    assert total_after_discount(2000, None) == 2000.0


def test_compute_grand_total():
    assert compute_grand_total(make_scope(), 20) == 2000.0
