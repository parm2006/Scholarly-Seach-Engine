"""
Script to fetch academic papers from ArXiv API and store them in the database.
This is a placeholder structure showing the ingestion pipeline.
"""
import requests
import time
from sqlalchemy.orm import Session
from database import SessionLocal, Paper, Author, init_db
from datetime import datetime
import xml.etree.ElementTree as ET


def fetch_arxiv_papers(categories: list = ["cs.CL", "cs.IR"], max_results: int = 50):
    """
    Fetch papers from ArXiv API.
    
    Args:
        categories: List of ArXiv categories (e.g., ["cs.CL", "cs.IR"])
        max_results: Maximum number of papers to fetch
    
    Returns:
        List of paper dictionaries
    """
    base_url = "http://export.arxiv.org/api/query"
    papers = []
    
    for category in categories:
        params = {
            "search_query": f"cat:{category}",
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending"
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            
            # Parse XML response
            root = ET.fromstring(response.content)
            
            # ArXiv uses Atom feed format
            entries = root.findall("{http://www.w3.org/2005/Atom}entry")
            
            for entry in entries:
                paper_data = {
                    "arxiv_id": entry.find("{http://www.w3.org/2005/Atom}id").text.split("/")[-1],
                    "title": entry.find("{http://www.w3.org/2005/Atom}title").text.strip(),
                    "abstract": entry.find("{http://www.w3.org/2005/Atom}summary").text.strip(),
                    "published_date": datetime.fromisoformat(
                        entry.find("{http://www.w3.org/2005/Atom}published").text.replace("Z", "+00:00")
                    ),
                    "arxiv_url": entry.find("{http://www.w3.org/2005/Atom}id").text,
                    "pdf_url": entry.find("{http://www.w3.org/2005/Atom}id").text.replace("/abs/", "/pdf/") + ".pdf",
                    "authors": [
                        author.find("{http://www.w3.org/2005/Atom}name").text
                        for author in entry.findall("{http://www.w3.org/2005/Atom}author")
                    ]
                }
                papers.append(paper_data)
            
            # Be respectful to ArXiv API
            time.sleep(3)
            
        except Exception as e:
            print(f"Error fetching papers from {category}: {e}")
            continue
    
    return papers


def store_papers_in_db(papers: list, db: Session):
    """Store fetched papers in the database."""
    stored_count = 0
    
    for paper_data in papers:
        # Check if paper already exists
        existing = db.query(Paper).filter(Paper.arxiv_id == paper_data["arxiv_id"]).first()
        if existing:
            continue
        
        # Create paper
        paper = Paper(
            arxiv_id=paper_data["arxiv_id"],
            title=paper_data["title"],
            abstract=paper_data["abstract"],
            published_date=paper_data["published_date"],
            arxiv_url=paper_data["arxiv_url"],
            pdf_url=paper_data["pdf_url"],
            citation_count=0  # Would fetch from Crossref/Semantic Scholar
        )
        
        db.add(paper)
        db.flush()  # Get paper ID
        
        # Add authors
        for idx, author_name in enumerate(paper_data["authors"]):
            author = Author(
                paper_id=paper.id,
                name=author_name,
                author_order=idx
            )
            db.add(author)
        
        stored_count += 1
    
    db.commit()
    return stored_count


def main():
    """Main function to run the ingestion pipeline."""
    print("Initializing database...")
    init_db()
    
    print("Fetching papers from ArXiv...")
    papers = fetch_arxiv_papers(categories=["cs.CL", "cs.IR"], max_results=20)
    print(f"Fetched {len(papers)} papers")
    
    print("Storing papers in database...")
    db = SessionLocal()
    try:
        stored = store_papers_in_db(papers, db)
        print(f"Successfully stored {stored} new papers")
    except Exception as e:
        print(f"Error storing papers: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()