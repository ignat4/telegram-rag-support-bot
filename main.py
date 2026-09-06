import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import VectorDBManager
from rag_engine import RAGEngine
from telegram_listener import start_telegram_listener

app = FastAPI(
    title="Enterprise RAG API",
    description="Microservice using Qdrant, Groq and FastAPI"
)

print("Initializing System...")
db_manager = VectorDBManager()

if os.path.exists("company_policy.txt"):
    db_manager.ingest_document("company_policy.txt")
else:
    print("Warning: company_policy.txt not found. Database might be empty.")

rag_service = RAGEngine(db_manager=db_manager)
print("System is ready to receive requests!")

@app.on_event("startup")
async def startup_event():
    start_telegram_listener()

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

class OperatorRequest(BaseModel):
    user_id: int
    username: str = "Unknown"
    message: str = ""

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    try:
        answer = rag_service.ask(request.question)
        return AnswerResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/operator")
async def notify_operator(data: OperatorRequest):
    print(f"\n🚨 [ALARM] УВАГА! Користувач @{data.username} (ID: {data.user_id}) запросив зв'язок з оператором!")
    print(f"💬 Останнє повідомлення: {data.message}\n")
    return {"status": "notification_received"}