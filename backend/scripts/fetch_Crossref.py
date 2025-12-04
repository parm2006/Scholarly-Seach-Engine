import requests
import time
from datetime import datetime

import sys
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from database import get_database_url, Author, Paper 


def fetch_Crossref(query, fetchcount) -> dict:
    # get the paper
    url = "https://api.crossref.org/works"
    params = {
        "query": query, 
        "rows": fetchcount
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json() 


def parse_Crossref_item(item):
    
    title = item.get("title", ["No Title"])[0]
    abstract = item.get("abstract", None)
    if abstract:
        abstract = abstract.replace("<jats:p>", "").replace("</jats:p>", "").strip()

    published_date = None
    if "published-print" in item and "date-parts" in item["published-print"]:
        parts = item["published-print"]["date-parts"][0]
        # Handle missing dates with padding
        parts += [1] * (3 - len(parts)) 
        published_date = datetime(*parts)
        
    # Using container-title as ArXiv's journal_ref
    where_published = item.get("container-title", ["Unknown"])[0]

    authors = {f"{a.get('given', '')} {a.get('family', '')}".strip() 
               for a in item.get("author", [])}

    doi_url = f"https://doi.org/{item.get('DOI')}" if item.get('DOI') else None

    return {
        "title": title,
        "abstract": abstract or "No abstract available",
        "published_date": published_date,
        "abs_url": doi_url,
        "pdf_url": None, 
        "where_published": where_published,
        "authors": authors,
    }

def parse_Crossref(jsondata):
    return [parse_Crossref_item(item) for item in jsondata["message"]["items"]]


def save_Crossref(papers: list[dict], engine):
    with Session(engine) as session:
        try:
            for paper in papers:
                # authors first cuz add to Author
                author_objs = []
                for auth_name in paper["authors"]:
                    author = session.query(Author).filter_by(name=auth_name).first()
                    if not author:
                        author = Author(name=auth_name)
                        session.add(author)
                        session.flush()
                    author_objs.append(author)

                paper_obj = Paper(
                    title=paper["title"],
                    abstract=paper["abstract"],
                    published_date=paper["published_date"],
                    abs_url=paper.get("abs_url") or "No URL available",
                    pdf_url=paper.get("pdf_url") or "No URL available",
                    where_published=paper.get("where_published") or "No Source available",
                    authors=author_objs
                )
                session.add(paper_obj)
            session.commit()
        except:
            session.rollback()
            raise


def fetchCrossref(query, amount):
    # fetch, extract, save control
    engine = create_engine(get_database_url())
    jsondata = fetch_Crossref(query, amount)
    paperdicts = parse_Crossref(jsondata)
    save_Crossref(paperdicts, engine)


def main():
    if len(sys.argv) < 3:
        print("Usage: python script_name.py <query> <amount>")
        sys.exit(1)
        
    query = sys.argv[1]
    amount = int(sys.argv[2])
    
    fetchCrossref(query, amount)
    time.sleep(2)


if __name__ == "__main__":
    main()