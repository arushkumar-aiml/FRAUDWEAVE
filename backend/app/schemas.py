from pydantic import BaseModel, Field
from .config import MAX_TEXT
class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=MAX_TEXT)
class ReportRequest(AnalyzeRequest):
    consent: bool
class LinkRequest(BaseModel):
    a: str = Field(min_length=1, max_length=MAX_TEXT)
    b: str = Field(min_length=1, max_length=MAX_TEXT)

from typing import Literal
class ReviewRequest(BaseModel):
    a: int
    b: int
    decision: Literal["accept", "reject"]
