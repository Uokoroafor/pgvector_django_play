from langchain_community.vectorstores.pgvector import PGVector
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from decouple import config
import argparse
import os
import getpass


OPENAI_API_KEY = config("OPENAI_API_KEY", default="")
if OPENAI_API_KEY == "":
    try:
        OPENAI_API_KEY = getpass.getpass("Please Provide OPENAI API KEY:")
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    except Exception as e:
        raise ValueError(
            f"Please Provide OPENAI API KEY in the .env file and rerun. Encountered error {e} when trying to set the variable"
        )

db_user = config("DB_USER")
db_password = config("DB_PASSWORD")
db_name = config("DB_NAME")
db_host = config("DB_HOST")
db_port = config("DB_PORT")


def main():
    parser = argparse.ArgumentParser(
        description="Chunk, embed and load text files"
    )
    parser.add_argument(
        "--folder",
        default="/code/data",
        help="The path of the folder to load text files from. Defaults to 'data'",
    )
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
    chunk_overlap = args.overlap
    folder = args.folder
    if not folder or not os.path.isdir(folder):
        raise ValueError(
            f"Please provide a valid folder path.\n{folder} is not valid."
        )

    # Get OpenAI Embeddings
    embeddings = OpenAIEmbeddings()

    CONNECTION_STRING = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    COLLECTION_NAME = "my_documents"

    db = PGVector(
        connection_string=CONNECTION_STRING,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
    )
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder, filename)
            print(f"Processing file: {file_path}")

            loader = TextLoader(file_path, encoding="utf8")
            documents = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size, chunk_overlap=chunk_overlap
            )
            texts = text_splitter.split_documents(documents=documents)

            db.add_documents(texts)


if __name__ == "__main__":
    main()
