from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.policy import PolicyChunk
from app.services.embedding import get_embeddings

async def search_policy(ssn: AsyncSession, question: str, limit: int = 3):
    vector = (await get_embeddings([question]))[0]
    result = await ssn.execute(
        select(PolicyChunk).order_by(PolicyChunk.embedding.cosine_distance(vector)).limit(limit)
    )
    return result.scalars().all()
