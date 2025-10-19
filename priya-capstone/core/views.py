from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json
import numpy as np
from .models import Embedding

def health(request):
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT 1;")
            cur.fetchone()
        db_ok = True
    except Exception:
        db_ok = False
    return JsonResponse({"status": "ok", "db_connected": db_ok})

@csrf_exempt
def test_retrieval(request):
    body = json.loads(request.body.decode()) if request.body else {}
    query_text = body.get("query", "sample query")

    def text_to_vector(text, dim=16):
        h = abs(hash(text))
        rng = np.random.default_rng(h % (2**32))
        return rng.random(dim).tolist()

    qv = np.array(text_to_vector(query_text))

    rows = Embedding.objects.all().select_related("document__metadata")
    results = []
    for e in rows:
        ev = np.array(e.vector)
        sim = float(np.dot(qv, ev) / (np.linalg.norm(qv) * np.linalg.norm(ev) + 1e-9))
        results.append({"metadataid": e.document.metadata.metadataid, "sim": sim})

    results = sorted(results, key=lambda r: r["sim"], reverse=True)[:3]
    return JsonResponse({"query": query_text, "results": results})
