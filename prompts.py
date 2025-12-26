from langchain_core.prompts import PromptTemplate

# Цепочка для нормализации / определения намерения пользователя
intent_prompt = PromptTemplate(
    input_variables=["user_input"],
    template=(
        "You analyze user requests about currency conversion.\n"
        "Your task is to summarize the user's intent in ONE short English sentence.\n"
        "If the request is NOT related to currency conversion, answer exactly: NON_CONVERSION.\n\n"
        "Examples:\n"
        "Input: 'Сколько будет 100 долларов в евро?'\n"
        "Output: 'convert 100 USD to EUR using latest rate'\n\n"
        "Input: 'Переведи 2500 рублей в тенге по курсу на 1 января 2020'\n"
        "Output: 'convert 2500 RUB to KZT using rate from 2020-01-01'\n\n"
        "Now process this request:\n"
        "Input: {user_input}\n"
        "Output:"
    ),
)