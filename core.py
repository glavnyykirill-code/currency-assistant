from config import logger
from chains import intent_chain, agent


def process_user_request(user_input: str):
    """
    Основная функция: принимает текстовый запрос пользователя,
    запускает цепочку для определения намерения и агента для конвертации.
    Возвращает словарь с полями:
      - intent: нормализованное намерение (строка)
      - answer: ответ ассистента (строка)
      - error: сообщение об ошибке (если есть)
    """
    try:
        if not user_input or not user_input.strip():
            raise ValueError("Запрос не может быть пустым.")

        # 1. Запуск цепочки для определения намерения
        logger.info("Запуск intent_chain для анализа запроса пользователя")
        chain_result = intent_chain({"user_input": user_input})
        intent = chain_result["intent"].strip()
        logger.info(f"Результат intent_chain: {intent}")

        if intent.upper() == "NON_CONVERSION":
            return {
                "error": "Запрос не похож на задачу конвертации валют. "
                         "Пожалуйста, сформулируйте запрос типа: "
                         "'Конвертируй 100 USD в EUR'."
            }

        # 2. Вызов агента с инструментом convert_currency
        agent_input = (
            "You are a helpful currency conversion assistant.\n"
            "Always use the 'convert_currency' tool to fetch real exchange rates.\n"
            "Steps:\n"
            "1. From the user request and the intent, determine amount, from_currency, to_currency and date.\n"
            "2. Call 'convert_currency' with these arguments.\n"
            "3. If the tool output contains key 'error', explain the problem in Russian.\n"
            "4. Otherwise, explain in Russian:\n"
            "   - исходную сумму и валюты\n"
            "   - использованный курс (1 FROM = X TO)\n"
            "   - итоговую сумму\n"
            "   - дату курса.\n"
            "Do not guess exchange rates yourself, always rely on tool output.\n\n"
            f"User request (in Russian): {user_input}\n"
            f"Intent (in English): {intent}\n"
        )

        logger.info("Вызов агента с инструментом convert_currency")
        # В разных версиях LangChain может быть нужен именованный аргумент input=
        agent_response = agent.run(input=agent_input)

        return {
            "intent": intent,
            "answer": agent_response,
        }

    except Exception as e:
        logger.error(f"Ошибка в process_user_request: {e}")
        msg = str(e)
        if "api key" in msg.lower() or "OPENAI_API_KEY" in msg:
            return {
                "error": "Ошибка API модели. Проверьте ключ OpenAI в файле .env."
            }
        return {"error": msg}