from sqlalchemy.ext.asyncio import AsyncSession
from app.database.repositories.embedding_repo import EmbeddingRepository
from app.rag.embeddings import embedding_service
import logging

logger = logging.getLogger(__name__)


class RAGRetriever:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.embedding_repo = EmbeddingRepository(session)
        self.embedding_svc = embedding_service

    async def retrieve(self, query: str, limit: int = 5) -> list[dict]:
        query_embedding = await self.embedding_svc.embed_query(query)
        results = await self.embedding_repo.search_similar(query_embedding, limit=limit)
        relevant = [r for r in results if r["distance"] < 1.5]
        return relevant

    async def retrieve_context(self, query: str, limit: int = 5) -> str:
        results = await self.retrieve(query, limit)
        if not results:
            return ""
        context_parts = []
        for i, r in enumerate(results, 1):
            context_parts.append(f"[Source {i}]: {r['content']}")
        return "\n\n".join(context_parts)
