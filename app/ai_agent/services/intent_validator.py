from app.ai_agent.schemas.intent import UserIntent


def validate_intent(question: str, intent: UserIntent) -> UserIntent:
    product_topics = {
        "price",
        "availability",
        "specifications",
    }

    delivery_topics = {
        "delivery_time",
        "delivery_price",
    }

    if intent.topic in product_topics:
        intent.intent = "product"

    elif intent.topic in delivery_topics:
        intent.intent = "delivery"

    return intent