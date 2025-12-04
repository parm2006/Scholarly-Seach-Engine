import requests
import time
from datetime import datetime
import xml.etree.ElementTree as ET
import sys
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from database import get_database_url, Author, Paper
from arxiv_categories import arXivcats as CATS


def fetch_ArXiv(category, fetchcount) ->str:
    #get the paper
    if category not in CATS:
        raise ValueError(f"Category '{category}' is not a valid arXiv category.")

    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"cat:{category}",
        "start": 0,
        "max_results": fetchcount,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.text  # XML string

ns = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
    "open": "http://a9.com/-/spec/opensearch/1.1/"
}


def parse_ArXiv_entry(entry):

    title = entry.find("atom:title", ns).text.strip()
    summary_el = entry.find("atom:summary", ns)
    summary = summary_el.text.strip() if summary_el is not None else "No Abstract Available"
    


    published_date = None
    published_el = entry.find("atom:published", ns)
    if published_el is not None and published_el.text:
        published_date = datetime.fromisoformat(published_el.text.rstrip("Z"))
  
    abs_url = None
    pdf_url = None

    for link in entry.findall("atom:link", ns):
        rel = link.attrib.get("rel", "")
        typ = link.attrib.get("type", "")

        if rel == "alternate" and typ == "text/html":
            abs_url = link.attrib["href"]
        if rel == "related" and typ == "application/pdf":
            pdf_url = link.attrib["href"]

    journal_el = entry.find("arxiv:journal_ref", ns)
    journal_ref = journal_el.text.strip() if journal_el is not None else None

    authors = {author.find("atom:name", ns).text.strip() for author in entry.findall("atom:author", ns)}

    return {
        "title": title,
        "abstract": summary,
        "published_date": published_date,
        "abs_url": abs_url,
        "pdf_url": pdf_url,
        "where_published": journal_ref,
        "authors": authors,
    }

def parse_ArXiv(xmlstring):
    #extract paper info
    root = ET.fromstring(xmlstring)
    return [parse_ArXiv_entry(entry) for entry in root.findall("atom:entry", ns)]


def save_ArXiv(papers: list[dict], engine):
    #save to database
    with Session(engine) as session:
        try:
            for paper in papers:
            #authors first cuz add to Author
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

def fetchAcategory(cat,amount):
    #fetch, extract, save control
    engine = create_engine(get_database_url())

    xmlpapers = fetch_ArXiv(cat,amount)
    paperdicts = parse_ArXiv(xmlpapers)
    save_ArXiv(paperdicts, engine)
    
def main():
    amount = int(sys.argv[1])
    for cat in CATS:
        fetchAcategory(cat,amount)
        time.sleep(2)
    return 0


if __name__ == "__main__":
    main()