import pandas as pd
from langchain_core.documents import Document

from utils.custom_exception import CustomException
from utils.logger import get_logger

logger = get_logger(__name__)


class DataConverter:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def convert(self):
        try:
            logger.info(f"Loading CSV: {self.file_path}")
            df = pd.read_csv(self.file_path)[["product_title", "review"]]

            docs = [
                Document(page_content=row['review'], metadata={"product_name": row["product_title"]})
                for _, row in df.iterrows()
            ]

            logger.info(f"Converted {len(docs)} rows to documents")
            return docs
        except Exception as e:
            logger.error(f"Failed to convert CSV: {e}")
            raise CustomException("Failed to convert CSV", e)
