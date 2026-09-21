import re

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from flipkart.config import Config
from flipkart.data_ingestion import DataIngestor
from utils.custom_exception import CustomException
from utils.logger import get_logger

logger = get_logger(__name__)

PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a friendly Flipkart shopping assistant. Answer using only the product "
     "reviews in the context. If the context does not contain the answer, say you "
     "don't have that information and suggest contacting customer care. "
     "Keep answers concise and use markdown.\n\nContext:\n{context}"),
    ("human", "{question}"),
])


class RAGAgent:
    def __init__(self):
        try:
            self.retriever = DataIngestor().ingest(load_existing=True).as_retriever(
                search_kwargs={"k": 4}
            )
            model_name = Config.RAG_MODEL.split(":", 1)[-1]
            self.llm = ChatGroq(model=model_name, api_key=Config.GROQ_API_KEY, temperature=0.3)
            self.chain = PROMPT | self.llm
            logger.info(f"RAG agent ready (model: {model_name})")
        except CustomException:
            raise
        except Exception as e:
            logger.error(f"Failed to initialise RAG agent: {e}")
            raise CustomException("Failed to initialise RAG agent", e)

    def ask(self, question: str) -> str:
        try:
            logger.info(f"Question received: {question}")
            docs = self.retriever.invoke(question)
            context = "\n\n".join(
                f"Product: {d.metadata.get('product_name')}\nReview: {d.page_content}"
                for d in docs
            )
            answer = self.chain.invoke({"context": context, "question": question}).content
            return re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()
        except Exception as e:
            logger.error(f"Failed to answer question: {e}")
            raise CustomException("Failed to answer question", e)
