# Використовуємо офіційний легкий образ Python
FROM python:3.11-slim

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# Копіюємо файл із залежностями
COPY requirements.txt .

# Встановлюємо всі потрібні бібліотеки
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо всі інші файли проєкту в контейнер
COPY . .

# Команда для запуску сервера
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]