import os
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Загружаем переменные окружения из .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if not OPENAI_API_KEY:
    logger.warning("OPENAI_API_KEY не найден в .env. Проект не сможет вызвать LLM.")

# Инициализация LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key=OPENAI_API_KEY,
    temperature=0.2,  # понижаем креативность для более стабильного поведения
)