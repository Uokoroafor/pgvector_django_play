import openai
from decouple import config


OPENAI_API_KEY = config("OPENAI_API_KEY")

EMBEDDING_MODEL = config("EMBEDDING_MODEL", default="text-embedding-ada-002")


def get_embedding(text: str):
    text = text.replace("\n", " ")
    response = openai.embeddings.create(input=[text], model=EMBEDDING_MODEL)
    # print(response)
    return response.data[0].embedding
