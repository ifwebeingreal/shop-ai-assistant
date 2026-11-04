import pytest

from app.ai_agent.schemas.intent import UserIntent
from app.ai_agent.services.business_rules import process_business_rules


@pytest.mark.parametrize(
    "intent, expected",
    [
        (
            UserIntent(intent="product", topic="price"),
            "2490 рублей",
        ),
        (
            UserIntent(intent="product", topic="availability"),
            "есть в наличии",
        ),
        (
            UserIntent(intent="product", topic="specifications"),
            "нет информации",
        ),
        (
            UserIntent(intent="delivery", topic="delivery_time"),
            "на следующий день",
        ),
        (
            UserIntent(intent="delivery", topic="delivery_price"),
            "нет информации",
        ),
        (
            UserIntent(intent="order_status"),
            "нет доступа",
        ),
        (
            UserIntent(intent="discount", discount_percent=50),
            "скидки",
        ),
        (
            UserIntent(intent="refund"),
            "3 рабочих дней",
        ),
        (
            UserIntent(intent="defect", is_defective=True),
            "экспертизу",
        ),
        (
            UserIntent(intent="unknown"),
            "нет информации",
        ),
    ],
)
def test_basic_business_rules(intent: UserIntent, expected: str):
    response = process_business_rules(intent)

    assert expected in response


@pytest.mark.parametrize(
    "days, is_defective, is_opened, expected",
    [
        (5, False, True, "вскрытый товар"),
        (10, False, False, "стандартный возврат"),
        (14, False, True, "вскрытый товар"),
        (15, False, False, "только в течение 14 дней"),
        (20, True, None, "экспертизу"),
        (20, None, None, "товар исправен"),
    ],
)
def test_returns(
    days: int,
    is_defective: bool | None,
    is_opened: bool | None,
    expected: str,
):
    intent = UserIntent(
        intent="return",
        days_since_purchase=days,
        is_defective=is_defective,
        is_opened=is_opened,
    )

    response = process_business_rules(intent)

    assert expected in response


def test_return_without_purchase_date():
    intent = UserIntent(intent="return")

    response = process_business_rules(intent)

    assert "сколько дней" in response


def test_refund_does_not_promise_instant_payment():
    intent = UserIntent(intent="refund")

    response = process_business_rules(intent)

    assert "3 рабочих дней" in response
    assert "мгновенно" not in response.lower()
    assert "сразу" not in response.lower()


def test_discount_cannot_be_granted():
    intent = UserIntent(
        intent="discount",
        discount_percent=99,
    )

    response = process_business_rules(intent)

    assert "не предусмотрены" in response
    assert "99%" not in response