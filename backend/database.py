#Database models and connection setup using SQLAlchemy.
#Defines the schema for papers, authors, and author tags.

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from config import get_database_url

# Create database engine
engine = create_engine(
    get_database_url(),
    pool_pre_ping=True,  # Verify connections before using
    echo=False  # Set to True for SQL query logging
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


class Paper(Base):
    """Model representing an academic paper."""
    __tablename__ = "papers"
    
    id = Column(Integer, primary_key=True, index=True)
    arxiv_id = Column(String, unique=True, index=True, nullable=True)
    title = Column(String, index=True, nullable=False)
    abstract = Column(Text, nullable=True)
    published_date = Column(DateTime, nullable=True)
    arxiv_url = Column(String, nullable=True)
    pdf_url = Column(String, nullable=True)
    citation_count = Column(Integer, default=0)
    contribution_sentences = Column(Text, nullable=True)  # JSON string of extracted contributions
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    authors = relationship("Author", back_populates="paper", cascade="all, delete-orphan")
    tags = relationship("AuthorTag", back_populates="paper", cascade="all, delete-orphan")


class Author(Base):
    """Model representing a paper author."""
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, ForeignKey("papers.id"), nullable=False)
    name = Column(String, nullable=False, index=True)
    orcid_id = Column(String, nullable=True, index=True)
    affiliation = Column(String, nullable=True)
    author_order = Column(Integer, default=0)  # Order in author list
    
    # Relationships
    paper = relationship("Paper", back_populates="authors")


class AuthorTag(Base):
    """Model for tagging authors with diversity attributes (from authoritative sources)."""
    __tablename__ = "author_tags"
    
    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, ForeignKey("papers.id"), nullable=False)
    author_name = Column(String, nullable=False, index=True)
    orcid_id = Column(String, nullable=True, index=True)
    tag_type = Column(String, nullable=False)  # e.g., "underrepresented_minority", "woman_in_stem"
    source = Column(String, nullable=False)  # Provenance: "ORCID", "curated_list", "self_declared"
    source_url = Column(String, nullable=True)  # Link to source
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    paper = relationship("Paper", back_populates="tags")


def get_db():
    """Dependency for FastAPI to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all database tables. Run this once to set up the schema."""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    # Run this script to initialize the database
    init_db()