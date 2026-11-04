import logging

from app.ai_agent.services.intent_classifier import classify_intent
from app.ai_agent.services.intent_validator import validate_intent
from app.ai_agent.services.business_rules import process_business_rules


logger = logging.getLogger(__name__)

AI_ERROR_MESSAGE = (
    "Извините, сейчас не получается обработать ваш вопрос. "
    "Попробуйте ещё раз немного позже."
)


async def get_ai_response(question: str) -> str:
    try:
        result = await classify_intent(question)

    except Exception:
        logger.exception("Ошибка при классификации вопроса")
        return AI_ERROR_MESSAGE

    logger.info(
        "CLASSIFIED INTENTS: %s",
        result.model_dump(),
    )

    responses = []

    for user_intent in result.intents:
        validated_intent = validate_intent(question, user_intent)

        logger.info(
            "VALIDATED INTENT: %s",
            validated_intent.model_dump(),
        )

        response = process_business_rules(validated_intent)

        if response not in responses:
            responses.append(response)

    return "\n\n".join(responses)