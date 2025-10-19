from django.core.management.base import BaseCommand
from core.models import Metadata, Document, Embedding
import numpy as np

class Command(BaseCommand):
    help = "Seed sample documents and generate demo embeddings"

    def handle(self, *args, **options):
        samples = [
            {"meta": {"metadataid": "m_perth_2021", "region": "Perth", "year": 2021}, "chunk": "Youth unemployment in Perth was 8% in 2021."},
            {"meta": {"metadataid": "m_melb_2020", "region": "Melbourne", "year": 2020}, "chunk": "High school completion in Melbourne improved in 2020."},
            {"meta": {"metadataid": "m_syd_2022", "region": "Sydney", "year": 2022}, "chunk": "Youth health initiatives in Sydney expanded in 2022."},
        ]

        for s in samples:
            md, _ = Metadata.objects.get_or_create(metadataid=s["meta"]["metadataid"],
                                                   defaults={"region": s["meta"]["region"], "year": s["meta"]["year"]})
            doc = Document.objects.create(metadata=md, chunk=s["chunk"])
            rng = np.random.default_rng(abs(hash(md.metadataid)) % (2**32))
            vec = rng.random(16).tolist()
            Embedding.objects.create(document=doc, vector=vec)

        self.stdout.write(self.style.SUCCESS("Seeded sample documents and embeddings."))
