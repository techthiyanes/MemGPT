from datetime import datetime
from typing import Dict, List, Optional

from pydantic import Field, field_validator

from memgpt.constants import MAX_EMBEDDING_DIM
from memgpt.schemas.embedding_config import EmbeddingConfig
from memgpt.schemas.memgpt_base import MemGPTBase
from memgpt.utils import get_utc_time


class PassageBase(MemGPTBase):
    __id_prefix__ = "passage"

    # associated user/agent
    user_id: Optional[str] = Field(None, description="The unique identifier of the user associated with the passage.")
    agent_id: Optional[str] = Field(None, description="The unique identifier of the agent associated with the passage.")

    # origin data source
    source_id: Optional[str] = Field(None, description="The data source of the passage.")

    # document association
    doc_id: Optional[str] = Field(None, description="The unique identifier of the document associated with the passage.")
    metadata_: Optional[Dict] = Field({}, description="The metadata of the passage.")


class Passage(PassageBase):
    id: str = PassageBase.generate_id_field()

    # passage text
    text: str = Field(..., description="The text of the passage.")

    # embeddings
    embedding: Optional[List[float]] = Field(..., description="The embedding of the passage.")
    embedding_config: Optional[EmbeddingConfig] = Field(..., description="The embedding configuration used by the passage.")

    created_at: datetime = Field(default_factory=get_utc_time, description="The creation date of the passage.")

    @field_validator("embedding")
    @classmethod
    def pad_embeddings(cls, embedding: List[float]) -> List[float]:
        """Pad embeddings to MAX_EMBEDDING_SIZE. This is necessary to ensure all stored embeddings are the same size."""
        import numpy as np

        if embedding and len(embedding) != MAX_EMBEDDING_DIM:
            np_embedding = np.array(embedding)
            padded_embedding = np.pad(np_embedding, (0, MAX_EMBEDDING_DIM - np_embedding.shape[0]), mode="constant")
            return padded_embedding.tolist()
        return embedding


class PassageCreate(PassageBase):
    text: str = Field(..., description="The text of the passage.")

    # optionally provide embeddings
    embedding: Optional[List[float]] = Field(None, description="The embedding of the passage.")
    embedding_config: Optional[EmbeddingConfig] = Field(None, description="The embedding configuration used by the passage.")


class PassageUpdate(PassageCreate):
    id: str = Field(..., description="The unique identifier of the passage.")
    text: Optional[str] = Field(None, description="The text of the passage.")

    # optionally provide embeddings
    embedding: Optional[List[float]] = Field(None, description="The embedding of the passage.")
    embedding_config: Optional[EmbeddingConfig] = Field(None, description="The embedding configuration used by the passage.")
