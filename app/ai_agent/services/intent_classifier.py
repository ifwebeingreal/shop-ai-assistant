from langchain_core.messages import HumanMessage, SystemMessage

from app.ai_agent.llm import get_llm
from app.ai_agent.prompts import CLASSIFIER_PROMPT
from app.ai_agent.schemas.intent import UserIntents


async def classify_intent(question: str) -> UserIntents:
    model = get_llm()

    structured_model = model.with_structured_output(
        UserIntents,
        method="json_schema",
    )

    messages = [
        SystemMessage(content=CLASSIFIER_PROMPT),
        HumanMessage(content=question),
    ]

    response = await structured_model.ainvoke(messages)

    if not isinstance(response, UserIntents):
        raise ValueError("Некорректный результат классификации")

    return response