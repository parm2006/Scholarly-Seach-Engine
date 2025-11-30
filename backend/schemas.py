"""
Pydantic schemas for request/response validation.
Ensures type safety and automatic API documentation.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class AuthorSchema(BaseModel):
    """Author information."""
    name: str
    orcid_id: Optional[str] = None
    affiliation: Optional[str] = None
    author_order: int = 0

    class Config:
        from_attributes = True


class AuthorTagSchema(BaseModel):
    """Author tag with provenance information."""
    author_name: str
    tag_type: str
    source: str
    source_url: Optional[str] = None
    verified: bool = False

    class Config:
        from_attributes = True


class PaperSchema(BaseModel):
    """Full paper information."""
    id: int
    arxiv_id: Optional[str] = None
    title: str
    abstract: Optional[str] = None
    published_date: Optional[datetime] = None
    arxiv_url: Optional[str] = None
    pdf_url: Optional[str] = None
    citation_count: int = 0
    contribution_sentences: Optional[str] = None
    authors: List[AuthorSchema] = []
    tags: List[AuthorTagSchema] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PaperSummarySchema(BaseModel):
    """Summary of paper for search results."""
    id: int
    title: str
    abstract: Optional[str] = None
    authors: List[str] = Field(default_factory=list, description="List of author names")
    citation_count: int = 0
    published_date: Optional[datetime] = None
    relevance_score: Optional[float] = None
    contribution_snippet: Optional[str] = None
    has_boost: bool = False  # Whether this result was boosted by fairness algorithm

    class Config:
        from_attributes = True


class SearchResponseSchema(BaseModel):
    """Response from search endpoint."""
    query: str
    results: List[PaperSummarySchema]
    total_results: int
    page: int = 1
    page_size: int = 10


class SearchQuerySchema(BaseModel):
    """Search query parameters."""
    q: str = Field(..., description="Search query string")
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(10, ge=1, le=100, description="Results per page")
    boosted_only: bool = Field(False, description="Show only boosted results")