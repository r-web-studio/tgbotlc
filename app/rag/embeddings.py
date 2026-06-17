import hashlib
import struct
import httpx
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    DIMENSION = 1536

    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"

    async def embed_query(self, text: str) -> list[float]:
        try:
            result = await self._api_embed(text)
            return result
        except Exception as e:
            logger.warning(f"API embedding failed, using fallback: {e}")
            return self._hash_embed(text)

    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        results = []
        for text in texts:
            try:
                result = await self._api_embed(text)
                results.append(result)
            except Exception:
                results.append(self._hash_embed(text))
        return results

    async def _api_embed(self, text: str) -> list[float]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/embeddings",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"input": text, "model": "openai/text-embedding-3-small"},
            )
            response.raise_for_status()
            data = response.json()
            embedding = data["data"][0]["embedding"]
            # Validate: reject vectors with NaN or inf
            if any(not (-1e30 < v < 1e30) for v in embedding):
                logger.warning("API returned invalid embedding (NaN/inf), using fallback")
                return self._hash_embed(text)
            return embedding

    def _hash_embed(self, text: str) -> list[float]:
        h = hashlib.sha512(text.encode("utf-8")).digest()
        values = list(struct.unpack(f"{len(h) // 4}f", h[: len(h) // 4 * 4]))
        while len(values) < self.DIMENSION:
            values.extend(values[: min(len(values), self.DIMENSION - len(values))])
        values = values[: self.DIMENSION]
        norm = sum(v * v for v in values) ** 0.5
        if norm > 0:
            values = [v / norm for v in values]
        return values


embedding_service = EmbeddingService()
