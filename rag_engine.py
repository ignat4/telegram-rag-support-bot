from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from config import Config
from database import VectorDBManager

class RAGEngine:
    def __init__(self, db_manager: VectorDBManager):
        self.llm = ChatGroq(
            api_key=Config.GROQ_API_KEY,
            model=Config.MODEL_NAME,
            temperature=0
        )
        self.retriever = db_manager.get_retriever()
        self.prompt = self._create_prompt()
        self.chain = self._build_chain()

    def _create_prompt(self):
        prompt_template = """
        Ти ввічливий помічник підтримки. 
        Використовуй ЛИШЕ наступний контекст, щоб відповісти на запитання користувача.
        Якщо контекст не містить необхідної інформації, не вигадуй її. Просто поверни точне слово: "ESCALATE".

        ВАЖЛИВЕ ПРАВИЛО ФОРМАТУВАННЯ: НЕ використовуй зірочки markdown (* або **) у своїй відповіді. Використовуй звичайний текст та стандартні тире (-) для маркованих списків.

        Контекст бази знань:
        {context}

        Запитання користувача: {question}
        uvicorn main:app --reload"""
        return ChatPromptTemplate.from_template(prompt_template)

    @staticmethod
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def _build_chain(self):
        return (
            {"context": self.retriever | self.format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def ask(self, question: str) -> str:
        return self.chain.invoke(question)