from django.shortcuts import render
from .models import LangchainPgEmbedding
from .embedding import get_embedding
from pgvector.django import CosineDistance


# Create your views here.
def index(request):
    if request.method == "POST":
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

    embeddings = LangchainPgEmbedding.objects.all()
    context = {"embeddings": embeddings}
    return render(request, "index.html", context)
