from typing import Annotated, Literal
from pydantic import BaseModel, Field


class UserIntent(BaseModel):
    intent: Literal[
        "product",
        "delivery",
        "order_status",
        "return",
        "refund",
        "defect",
        "discount",
        "unknown",
    ]
    topic: Literal[
        "price",
        "availability",
        "specifications",
        "delivery_time",
        "delivery_price",
        "unknown",
    ] = "unknown"

    days_since_purchase: Annotated[int | None, Field(default=None, ge=0)]
    is_defective: Annotated[bool | None, Field(default=None)]
    is_opened: Annotated[bool | None, Field(default=None)]
    order_id: Annotated[int | None, Field(default=None)]
    discount_percent: Annotated[int | None, Field(default=None, ge=0, le=100)]


class UserIntents(BaseModel):
    intents: list[UserIntent] = Field(min_length=1, max_length=5)
