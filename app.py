import streamlit as st
from core import process_user_request

# Инициализация истории в сессии
if "history" not in st.session_state:
    st.session_state.history = []

st.title("Ассистент для конвертации валют")

st.write(
    "Введите запрос на русском или английском. Примеры:\n"
    "- 'Конвертируй 100 USD в EUR'\n"
    "- 'Сколько будет 2500 рублей в долларах США?'\n"
    "- 'Переведи 50 евро в йены по курсу на 2020-01-01'\n"
)

user_input = st.text_input("Ваш запрос:")

if st.button("Конвертировать"):
    if user_input.strip():
        with st.spinner("Обработка запроса..."):
            result = process_user_request(user_input)
            if "error" in result:
                st.error(result["error"])
            else:
                st.subheader("Нормализованное намерение (цепочка LLMChain)")
                st.code(result["intent"], language="text")

                st.subheader("Ответ ассистента (агент + инструмент)")
                st.write(result["answer"])

                # Добавляем в историю
                st.session_state.history.append(
                    {
                        "user_input": user_input,
                        "intent": result["intent"],
                        "answer": result["answer"],
                    }
                )
    else:
        st.warning("Пожалуйста, введите запрос.")

# Отображение истории
if st.session_state.history:
    st.subheader("История запросов")
    for idx, entry in enumerate(reversed(st.session_state.history), 1):
        with st.expander(
            f"Запрос #{len(st.session_state.history) - idx + 1}: {entry['user_input']}"
        ):
            st.markdown("**Намерение:**")
            st.code(entry["intent"], language="text")
            st.markdown("**Ответ:**")
            st.write(entry["answer"])