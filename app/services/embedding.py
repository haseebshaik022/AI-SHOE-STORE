from huggingface_hub import AsyncInferenceClient
from app.core.config import settings

client = AsyncInferenceClient(provider="hf-inference", api_key=settings.hf_token)

async def get_embeddings(texts: list[str]):
    result = await client.feature_extraction(text=texts, model=settings.hf_embedding_model)
    if hasattr(result, "tolist"):
        result = result.tolist()
    return [list(map(float, vector)) for vector in result]
