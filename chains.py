from langchain_classic.chains import LLMChain
from langchain_classic.agents import initialize_agent, AgentType

from config import llm
from prompts import intent_prompt
from tools import convert_currency

# LLMChain — определение намерения пользователя (интерпретация запроса)
intent_chain = LLMChain(
    llm=llm,
    prompt=intent_prompt,
    output_key="intent",
    verbose=True,
)

# Набор инструментов для агента (в нашем случае один — convert_currency)
tools = [convert_currency]

# Агент с инструментом
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)