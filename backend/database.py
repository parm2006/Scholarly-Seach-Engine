"""
Database models and connection setup.
TODO: You'll implement this step by step.
"""

from typing import List, Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from sqlalchemy import String, Integer, Text, DateTime, create_engine, Table, Column, ForeignKey
from config import get_database_url

engine = create_engine(get_database_url())

class Base(DeclarativeBase):
    pass


paper_author_link = Table(
    "paper_author_link",
    Base.metadata,
    Column("paper_id", ForeignKey("papers.id"), primary_key=True),
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
)


class Paper(Base):
    __tablename__ = "papers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True, )
    abstract: Mapped[Optional[str]] = mapped_column(Text)
    citation_count: Mapped[int] = mapped_column(Integer, default=0)
    abs_url: Mapped[Optional[str]] = mapped_column(String(255), index=True, default = "No URL available")
    pdf_url: Mapped[Optional[str]] = mapped_column(String(255), index=True, default = "No URL available")
    where_published: Mapped[Optional[str]] = mapped_column(String(255), index=True, default = "No Source available")
    published_date: Mapped[Optional[DateTime]] = mapped_column(DateTime, default = None)
    authors: Mapped[List["Author"]] = relationship(
        secondary=paper_author_link, back_populates="papers")
    contributions: Mapped[List["Contribution"]] = relationship(
        "Contribution", back_populates="paper", cascade="all, delete-orphan")
    
    @property
    def tags(self) -> set[str]:
        return {tag.tag for author in self.authors for tag in author.tags}
    

class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    
    papers: Mapped[List[Paper]] = relationship(secondary=paper_author_link, back_populates="authors")
    tags: Mapped[List["AuthorTag"]] = relationship("AuthorTag", back_populates="author", cascade="all, delete-orphan")



class Contribution(Base):
    __tablename__ = "contributions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    paper_id: Mapped[int] = mapped_column(Integer, ForeignKey("papers.id"))
    text : Mapped[str] = mapped_column(Text)
    paper: Mapped[Paper] = relationship("Paper", back_populates="contributions")


class AuthorTag(Base):
    __tablename__ = "author_tags"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("authors.id"))
    
    tag: Mapped[str] = mapped_column(String(63), index=True)
    author: Mapped[Author] = relationship(back_populates="tags")


def get_db():
    '''Fast API dependency function'''
    with Session(engine) as session:
        yield session


def init_db():
    '''create db tables'''
    Base.metadata.create_all(engine)
    print("DB tables made")


if __name__ == "__main__":
    init_db()