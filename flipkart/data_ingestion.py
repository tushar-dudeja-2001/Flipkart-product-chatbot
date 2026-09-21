from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEndpointEmbeddings

from flipkart.config import Config
from flipkart.data_converter import DataConverter
from utils.custom_exception import CustomException
from utils.logger import get_logger

logger = get_logger(__name__)


class DataIngestor:
    def __init__(self):
        try:
            self.embedding = HuggingFaceEndpointEmbeddings(model=Config.EMBEDDING_MODEL)

            self.vstore = AstraDBVectorStore(
                embedding=self.embedding,
                collection_name="flipkart_database",
                api_endpoint=Config.ASTRA_DB_API_ENDPOINT,
                token=Config.ASTRA_DB_APPLICATION_TOKEN,
                namespace=Config.ASTRA_DB_KEYSPACE
            )
            logger.info("Connected to AstraDB vector store")
        except Exception as e:
            logger.error(f"Failed to connect to AstraDB: {e}")
            raise CustomException("Failed to connect to AstraDB", e)

    # load_existing - if docs already exits just load that
    def ingest(self, load_existing=True):
        if load_existing == True:
            return self.vstore

        try:
            logger.info("Starting data ingestion")
            docs = DataConverter("data/flipkart_product_review.csv").convert()

            self.vstore.add_documents(docs)
            logger.info(f"Ingested {len(docs)} documents")

            return self.vstore
        except CustomException:
            raise
        except Exception as e:
            logger.error(f"Ingestion failed: {e}")
            raise CustomException("Failed to ingest data", e)


if __name__ == "__main__":
    ingestor = DataIngestor()
    ingestor.ingest(load_existing=False)
