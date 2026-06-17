import os
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.repositories.embedding_repo import EmbeddingRepository
from app.rag.embeddings import embedding_service

logger = logging.getLogger(__name__)


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start = end - overlap
    return chunks


async def load_knowledge_base(session: AsyncSession) -> int:
    knowledge_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "knowledge",
        "knowledge.txt",
    )
    if not os.path.exists(knowledge_path):
        logger.warning(f"Knowledge file not found: {knowledge_path}")
        return 0

    with open(knowledge_path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip():
        logger.warning("Knowledge file is empty")
        return 0

    chunks = chunk_text(content)
    if not chunks:
        return 0

    embedding_repo = EmbeddingRepository(session)

    existing_count = await embedding_repo.count()
    if existing_count > 0:
        logger.info(
            f"Knowledge base already has {existing_count} embeddings, skipping load"
        )
        return existing_count

    embeddings = await embedding_service.embed_documents(chunks)
    for chunk, emb in zip(chunks, embeddings):
        await embedding_repo.add(content=chunk, embedding=emb)

    logger.info(f"Loaded {len(chunks)} chunks into knowledge base")
    return len(chunks)
