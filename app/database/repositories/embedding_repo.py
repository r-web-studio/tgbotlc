from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database.models.embedding import Embedding


class EmbeddingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, content: str, embedding: list[float], metadata_info: str = None) -> Embedding:
        emb = Embedding(content=content, embedding=embedding, metadata_info=metadata_info)
        self.session.add(emb)
        await self.session.commit()
        await self.session.refresh(emb)
        return emb

    async def search_similar(self, query_embedding: list[float], limit: int = 5) -> list[dict]:
        result = await self.session.execute(
            select(Embedding, Embedding.embedding.cosine_distance(query_embedding).label("distance"))
            .order_by("distance")
            .limit(limit)
        )
        rows = result.all()
        return [{"content": row[0].content, "metadata": row[0].metadata_info, "distance": row[1]} for row in rows]

    async def count(self) -> int:
        result = await self.session.execute(select(func.count(Embedding.id)))
        return result.scalar()

    async def delete_all(self) -> int:
        result = await self.session.execute(select(Embedding))
        embeddings = result.scalars().all()
        count = len(embeddings)
        for emb in embeddings:
            await self.session.delete(emb)
        await self.session.commit()
        return count
