"""
FastAPI application for the Fairness-Aware Academic Search Engine.
Provides endpoints for searching academic papers with fairness-aware ranking.
"""
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db, Paper, Author, AuthorTag, init_db
from schemas import (
    PaperSchema,
    PaperSummarySchema,
    SearchResponseSchema,
    SearchQuerySchema
)
from config import settings

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="API for searching academic papers with fairness-aware re-ranking"
)

# CORS middleware (needed for frontend to call backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "Fairness-Aware Academic Search Engine API",
        "version": settings.API_VERSION,
        "status": "running"
    }


@app.get("/search", response_model=SearchResponseSchema)
async def search_papers(
    q: str = Query(..., description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Results per page"),
    boosted_only: bool = Query(False, description="Show only boosted results"),
    db: Session = Depends(get_db)
):
    """
    Search for academic papers.
    
    Currently returns mock data. In production, this will:
    1. Query PostgreSQL/Elasticsearch for matching papers
    2. Extract contribution sentences
    3. Apply fairness-aware re-ranking algorithm
    4. Return sorted results with provenance information
    """
    # TODO: Implement actual search logic
    # For now, return mock data to demonstrate API structure
    
    # Check if database has any papers
    paper_count = db.query(Paper).count()
    
    if paper_count == 0:
        # Return empty results with helpful message
        return SearchResponseSchema(
            query=q,
            results=[],
            total_results=0,
            page=page,
            page_size=page_size
        )
    
    # Basic keyword search in title and abstract (simple implementation)
    search_term = f"%{q.lower()}%"
    papers = db.query(Paper).filter(
        (Paper.title.ilike(search_term)) | 
        (Paper.abstract.ilike(search_term))
    ).limit(page_size).offset((page - 1) * page_size).all()
    
    # Convert to response format
    results = []
    for paper in papers:
        # Get authors
        authors = [author.name for author in paper.authors]
        
        # Check if paper has boost tags
        has_boost = len(paper.tags) > 0
        
        # Get first contribution sentence if available
        contribution_snippet = None
        if paper.contribution_sentences:
            # In production, parse JSON and get first sentence
            contribution_snippet = paper.contribution_sentences[:200] + "..." if len(paper.contribution_sentences) > 200 else paper.contribution_sentences
        
        results.append(PaperSummarySchema(
            id=paper.id,
            title=paper.title,
            abstract=paper.abstract[:300] + "..." if paper.abstract and len(paper.abstract) > 300 else paper.abstract,
            authors=authors,
            citation_count=paper.citation_count,
            published_date=paper.published_date,
            relevance_score=None,  # TODO: Calculate from search engine
            contribution_snippet=contribution_snippet,
            has_boost=has_boost
        ))
    
    total_count = db.query(Paper).filter(
        (Paper.title.ilike(search_term)) | 
        (Paper.abstract.ilike(search_term))
    ).count()
    
    return SearchResponseSchema(
        query=q,
        results=results,
        total_results=total_count,
        page=page,
        page_size=page_size
    )


@app.get("/paper/{paper_id}", response_model=PaperSchema)
async def get_paper(
    paper_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific paper."""
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    return paper


@app.post("/init-db")
async def initialize_database():
    """
    Initialize database tables.
    WARNING: This will create tables if they don't exist.
    Run this once when setting up the project.
    """
    try:
        init_db()
        return {"message": "Database initialized successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database initialization failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)