from typing import Any, Literal, Optional, Union

from pydantic import BaseModel, Field

GenerativeResponseType = Literal["text", "object", "meta", "citations", "status"]


class TextGenerativeResponse(BaseModel):
    type: Literal["text"] = "text"
    text: str


class JSONGenerativeResponse(BaseModel):
    type: Literal["object"] = "object"
    object: dict[str, Any]


class MetaGenerativeResponse(BaseModel):
    type: Literal["meta"] = "meta"
    input_tokens: float
    output_tokens: float
    timings: dict[str, float]


class CitationsGenerativeResponse(BaseModel):
    type: Literal["citations"] = "citations"
    citations: dict[str, Any]


class RerankGenerativeResponse(BaseModel):
    type: Literal["rerank"] = "rerank"
    context_scores: dict[str, float]


class StatusGenerativeResponse(BaseModel):
    type: Literal["status"] = "status"
    code: str
    details: Optional[str] = None


GenerativeResponse = Union[
    TextGenerativeResponse,
    JSONGenerativeResponse,
    MetaGenerativeResponse,
    CitationsGenerativeResponse,
    StatusGenerativeResponse,
    RerankGenerativeResponse,
]


class GenerativeChunk(BaseModel):
    chunk: GenerativeResponse = Field(..., discriminator="type")
