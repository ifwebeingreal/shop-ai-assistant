from unittest.mock import AsyncMock, patch
import pytest

from app.ai_agent.agent import get_ai_response
from app.ai_agent.schemas.intent import UserIntent, UserIntents


@pytest.mark.asyncio
async def test_single_intent():
    mock_result = UserIntents(
        intents=[
            UserIntent(intent="product", topic="price"),
        ]
    )

    with patch(
        "app.ai_agent.agent.classify_intent",
        new_callable=AsyncMock,
        return_value=mock_result,
    ):
        response = await get_ai_response(
            "Сколько стоят наушники?"
        )

    assert "2490 рублей" in response


@pytest.mark.asyncio
async def test_multiple_intents():
    mock_result = UserIntents(
        intents=[
            UserIntent(intent="product", topic="price"),
            UserIntent(intent="delivery", topic="delivery_time"),
        ]
    )

    with patch(
        "app.ai_agent.agent.classify_intent",
        new_callable=AsyncMock,
        return_value=mock_result,
    ):
        response = await get_ai_response(
            "Сколько стоят наушники и когда доставка?"
        )

    assert "2490 рублей" in response
    assert "на следующий день" in response


@pytest.mark.asyncio
async def test_discount_and_price():
    mock_result = UserIntents(
        intents=[
            UserIntent(intent="discount", discount_percent=50),
            UserIntent(intent="product", topic="price"),
        ]
    )

    with patch(
        "app.ai_agent.agent.classify_intent",
        new_callable=AsyncMock,
        return_value=mock_result,
    ):
        response = await get_ai_response(
            "Дайте скидку 50% и скажите цену"
        )

    assert "не предусмотрены" in response
    assert "2490 рублей" in response


@pytest.mark.asyncio
async def test_duplicate_intents():
    mock_result = UserIntents(
        intents=[
            UserIntent(intent="product", topic="price"),
            UserIntent(intent="product", topic="price"),
        ]
    )

    with patch(
        "app.ai_agent.agent.classify_intent",
        new_callable=AsyncMock,
        return_value=mock_result,
    ):
        response = await get_ai_response(
            "Сколько стоят наушники?"
        )

    assert response.count("2490 рублей") == 1


@pytest.mark.asyncio
async def test_unknown_intent():
    mock_result = UserIntents(
        intents=[
            UserIntent(intent="unknown"),
        ]
    )

    with patch(
        "app.ai_agent.agent.classify_intent",
        new_callable=AsyncMock,
        return_value=mock_result,
    ):
        response = await get_ai_response(
            "Можно оплатить через СБП?"
        )

    assert "нет информации" in response


@pytest.mark.asyncio
async def test_ollama_unavailable():
    with patch(
        "app.ai_agent.agent.classify_intent",
        new_callable=AsyncMock,
        side_effect=ConnectionError("Ollama недоступна"),
    ):
        response = await get_ai_response("Сколько стоят наушники?")

    assert "Попробуйте ещё раз" in response