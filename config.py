import os
from dotenv import load_dotenv

# Завантажуємо змінні середовища з файлу .env
load_dotenv()

class Config:
    # 1. Секретні ключі
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    # 2. Системні налаштування
    MODEL_NAME = "qwen/qwen3.8-27b"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    QDRANT_PATH = "./qdrant_local_db"
    COLLECTION_NAME = "company_knowledge_base"
    RETRIEVER_K = 1

    # Сувора перевірка, щоб сервер не запускався без ключа
    if not GROQ_API_KEY:
        raise ValueError("API ключ не знайдено! Перевірте файл .env у корені проєкту.")