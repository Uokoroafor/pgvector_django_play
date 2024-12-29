from langchain_community.vectorstores.pgvector import PGVector
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from decouple import config
import argparse


OPENAI_API_KEY = config("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    OPENAI_API_KEY = input("Please Provide OPENAI API KEY:").strip()
    if not OPENAI_API_KEY:
        raise ValueError("Must Provide OPENAI API KEY")

db_user = config("DB_USER")
db_password = config("DB_PASSWORD")
db_name = config("DB_NAME")
db_host = config("DB_HOST")
db_port = config("DB_PORT")


def main():
    parser = argparse.ArgumentParser(
        description="Chunk, embed and load text files"
    )
    parser.add_argument("--path", help="The path of the text file to load")
    parser.add_argument(
        "--chunk-size", default=1000, help="The size of the chunks"
    )
    parser.add_argument(
        "--overlap",
        default=80,
        help="The number of characters of chunks that overlap",
    )
    args = parser.parse_args()

    chunk_size = args.chunk_size
    chunk_overlap = args.chunk_overlap
    data_path = args.path

    loader = TextLoader(data_path, encoding="utf8")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    texts = text_splitter.split_documents(documents=documents)

    # Get OpenAI Embeddings
    embeddings = OpenAIEmbeddings()

    CONNECTION_STRING = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    COLLECTION_NAME = "my_documents"

    db = PGVector(
        connection_string=CONNECTION_STRING,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
    )

    db.add_documents(texts)

    # db = PGVector.from_documents(
    #     embedding=embeddings,
    #     documents=texts,
    #     collection_name=COLLECTION_NAME,
    #     connection_string=CONNECTION_STRING,
    # )
