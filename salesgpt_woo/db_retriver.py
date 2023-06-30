from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain.vectorstores.pgvector import DistanceStrategy
import os
from dotenv import load_dotenv
load_dotenv()
def get_db():
    # db_port=int(os.environ.get("PGVECTOR_PORT", "5432"))
    # print(db_port)
    DEFAULT_DISTANCE_STRATEGY = DistanceStrategy.EUCLIDEAN
    CONNECTION_STRING = PGVector.connection_string_from_db_params(
        driver=os.environ.get("PGVECTOR_DRIVER"),
        host=os.environ.get("PGVECTOR_HOST"),
        port=int(os.environ.get("PGVECTOR_PORT", "5432")),
        database=os.environ.get("PGVECTOR_DATABASE"),
        user=os.environ.get("PGVECTOR_USER"),
        password=os.environ.get("PGVECTOR_PASSWORD"),
    )   
    embeddings = OpenAIEmbeddings(deployment="chatbot-embedding-ada-dev")
    return PGVector.from_existing_index(
    embedding=embeddings,
    collection_name="test",
    distance_strategy=DEFAULT_DISTANCE_STRATEGY,
    pre_delete_collection=False,
    connection_string=CONNECTION_STRING,
)

def get_documents(db, query):
    result = db.similarity_search_with_score(query)
    return result

def documents_to_string(docs):
    result = []
    for doc, score in docs:
        print(doc)
        result.append(doc.page_content)
    return "\n".join(result)