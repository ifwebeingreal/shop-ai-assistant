from app.ai_agent.schemas.intent import UserIntent
from app.ai_agent.services.knowledge import load_regulations


def process_business_rules(user_intent: UserIntent) -> str:
    regulations = load_regulations()

    match user_intent.intent:
        case "product":
            product = regulations["product"]

            name = product["name"]
            price = product["price"]
            in_stock = product["in_stock"]

            match user_intent.topic:

                case "price":
                    return f"{name} стоят {price} рублей."

                case "availability":
                    if in_stock:
                        return f"{name} есть в наличии."

                    return f"К сожалению, {name} сейчас нет в наличии."

                case "specifications":
                    return (
                        "К сожалению, у меня нет информации "
                        "о характеристиках, цветах и комплектации товара."
                    )

                case _:
                    return (
                        "Уточните, пожалуйста, что именно "
                        "вы хотите узнать о товаре: "
                        "цену, наличие или характеристики?"
                    )

        case "discount":
            discounts = regulations["discounts"]

            if not discounts["allowed"]:
                return (
                    "К сожалению, скидки в нашем "
                    "магазине не предусмотрены."
                )

            return "Информация о доступных скидках отсутствует."

        case "order_status":
            orders = regulations["orders"]

            if not orders["individual_order_tracking_available"]:
                return (
                    "К сожалению, у меня нет доступа "
                    "к информации о статусе конкретного заказа."
                )

            return (
                "К сожалению, сейчас я не могу "
                "определить статус вашего заказа."
            )

        case "delivery":
            delivery = regulations["delivery"]

            days = delivery["estimated_days"]
            time_from = delivery["time_slot"]["from"]
            time_to = delivery["time_slot"]["to"]

            match user_intent.topic:

                case "delivery_time":
                    if days == 1:
                        delivery_text = "на следующий день"
                    else:
                        delivery_text = f"через {days} дн."

                    return (
                        f"Доставка курьером осуществляется "
                        f"{delivery_text} "
                        f"с {time_from} до {time_to}."
                    )

                case "delivery_price":
                    return (
                        "К сожалению, у меня нет информации "
                        "о стоимости доставки."
                    )

                case _:
                    return (
                        "Доставка осуществляется курьером. "
                        "Уточните, пожалуйста, вас интересуют "
                        "сроки или стоимость доставки?"
                    )

        case "return":
            returns = regulations["returns"]
            period = returns["period_days"]

            if user_intent.is_defective is True:
                defective = regulations["defective_product"]

                if defective["inspection_required"]:
                    return (
                        "Если товар неисправен, он принимается "
                        "на экспертизу. Немедленный возврат "
                        "денежных средств не гарантируется."
                    )

                return (
                    "К сожалению, у меня недостаточно информации "
                    "об условиях возврата неисправного товара."
                )

            days = user_intent.days_since_purchase

            if days is None:
                return (
                    "Уточните, пожалуйста, сколько дней "
                    "прошло с момента покупки."
                )

            if days <= period:
                if user_intent.is_opened is True:
                    if returns["opened_without_defect"]["allowed"]:
                        return (
                            f"Да, вскрытый товар без брака можно "
                            f"вернуть в течение {period} дней "
                            "с момента покупки."
                        )

                    return (
                        "К сожалению, возврат вскрытого товара "
                        "без брака не предусмотрен."
                    )

                return (
                    f"Да, стандартный возврат товара возможен "
                    f"в течение {period} дней с момента покупки."
                )

            if user_intent.is_defective is None:
                return (
                    f"Стандартный возврат предусмотрен в течение "
                    f"{period} дней. Уточните, пожалуйста, "
                    "товар исправен или имеет неисправность?"
                )

            return (
                f"К сожалению, стандартный возврат исправного "
                f"товара возможен только в течение {period} дней."
            )

        case "defect":
            defective = regulations["defective_product"]

            if defective["inspection_required"]:
                return (
                    "Если товар неисправен, он принимается "
                    "на экспертизу. Немедленный возврат "
                    "денежных средств не гарантируется."
                )

            return (
                "К сожалению, у меня недостаточно информации "
                "об условиях возврата неисправного товара."
            )

        case "refund":
            refund = regulations["refund"]

            method = refund["method"]
            days = refund["processing_days"]
            days_type = refund["days_type"]

            if method == "original_card":
                method_text = "на ту же карту"
            else:
                return (
                    "К сожалению, у меня нет подтверждённой "
                    "информации о способе возврата денег."
                )

            if days_type == "business":
                days_text = f"{days} рабочих дней"
            else:
                days_text = f"{days} дней"

            return (
                f"Денежные средства возвращаются {method_text} "
                f"в течение {days_text}."
            )

        case "unknown":
            return (
                "К сожалению, у меня нет информации "
                "по вашему вопросу. Я могу помочь "
                "с вопросами о товарах, доставке, "
                "возвратах и скидках."
            )