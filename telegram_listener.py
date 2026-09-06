import os
import asyncio
import httpx

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://n8n:5678/webhook/telegram-webhook")


async def telegram_listener_loop():
    if not TELEGRAM_TOKEN:
        print("Warning: TELEGRAM_BOT_TOKEN is not set in .env. Background listener disabled.")
        return

    print(f"▶️ Слухач Telegram запущено! Очікуємо повідомлення...")
    offset = 0
    async with httpx.AsyncClient() as client:
        while True:
            try:
                url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?offset={offset}&timeout=30"
                response = await client.get(url, timeout=35.0)
                data = response.json()

                if data.get("ok"):
                    if data.get("result"):
                        for update in data["result"]:
                            offset = update["update_id"] + 1
                            print(f"📩 Отримано повідомлення з Telegram: {update}")

                            # Відправляємо в n8n
                            n8n_response = await client.post(N8N_WEBHOOK_URL, json=update)
                            print(f"✅ Успішно переслано в n8n! Статус: {n8n_response.status_code}")
                else:
                    print(f"⚠️ Помилка від API Telegram: {data}")
                    await asyncio.sleep(3)

            except Exception as e:
                print(f"❌ Системна помилка слухача: {e}")
                await asyncio.sleep(3)


def start_telegram_listener():
    asyncio.create_task(telegram_listener_loop())