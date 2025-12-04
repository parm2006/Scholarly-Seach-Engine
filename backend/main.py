"""
FastAPI application for the Fairness-Aware Academic Search Engine.
"""
from fastapi import FastAPI, Depends, Query
from database import get_db, Paper
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

# Create FastAPI app
app = FastAPI(
    title="Fairness-Aware Academic Search Engine API",
    version="0.1.0"
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "API is running"}



@app.get("/search")
async def search_papers(q: str = Query(...), db: Session = Depends(get_db)):
    '''/search?q=<search>+<keywords>'''
    keyword = f"%{q}%"
    papers = db.query(Paper).filter(or_(Paper.title.ilike(keyword),Paper.abstract.ilike(keyword))
    ).all()


    results = []
    for paper in papers:
        results.append({
            "id": paper.id,
            "title": paper.title,
            "abstract": paper.abstract,
            "citation_count":paper.citation_count,
            "tags":paper.tags
        })

    return {"query": q, "Papers": results, "Count": len(results)}


    
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
