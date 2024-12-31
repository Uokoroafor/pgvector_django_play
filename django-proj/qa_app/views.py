from django.shortcuts import render
from .models import LangchainPgEmbedding
from .embedding import get_embedding
from pgvector.django import CosineDistance
from uuid import uuid4


def index(request):
    if request.method == "POST":
        if "index_search" in request.POST:
            text = request.POST.get("input_text")
            # Create Embedding of text
            embedded_text = get_embedding(text)
            document = LangchainPgEmbedding.objects.order_by(
                CosineDistance("embedding", embedded_text)
            ).first()
            context = {
                "text": text,
                "most_similar": document,
            }
            return render(request, "results.html", context)
        elif "update_db" in request.POST:
            text = request.POST.get("input_text")
            # Create Embedding of text
            embedded_text = get_embedding(text)
            db_entry = LangchainPgEmbedding.objects.create(
                embedding=embedded_text,
                document=text,
                uuid=uuid4(),
            )
            context = {
                "text": text,
                "embedding": embedded_text,
                "primary_key": db_entry.pk,
            }
            return render(request, "add_entry.html", context)

    embeddings = LangchainPgEmbedding.objects.all()
    context = {"embeddings": embeddings}
    return render(request, "index.html", context)
