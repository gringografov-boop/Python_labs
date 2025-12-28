from typing import List, Dict, Optional
from src.models.book import Book
from src.collections.book_collection import BookCollection
from src.collections.index_dict import IndexDict



class Library:
    def __init__(self, name: str = "Main Library"):
        self.name = name
        self.books = BookCollection()
        self.index = IndexDict()
        self.search_history = [] # 4 ошибка 

    def add_book(self, book: "Book") -> None:
        self.books.add(book)
        self.index.add_book(book)
    
    def remove_book(self, isbn: str) -> bool:
        book = self.index.get_by_isbn(isbn)
        if book:
            self.books.remove(book)
            self.index.remove_book(book)
            return True
        return False
    
    def search_by_isbn(self, isbn: str) -> Optional["Book"]:
        return self.index.get_by_isbn(isbn)
    
    def search_by_author(self, author: str) -> List["Book"]:
        return self.index.get_by_year(author) # <- 3 ошибка
    def search_by_year(self, year: int) -> List["Book"]:
        return self.index.get_by_year(year)
    
    def search_by_genre(self, genre: str) -> List["Book"]:
        return [book for book in self.books if book.genre.lower() == genre.lower()]
    
    def get_all_books(self) -> BookCollection:
        return self.books
    
    def get_book_by_index(self, idx: int) -> Optional["Book"]:
        try:
            return self.books[idx]
        except IndexError:
            return None
    
    def get_books_slice(self, start: int, end: int) -> List["Book"]:
        return self.books[start:end]
    
    def get_stats(self) -> Dict[str, int]:
        return {
            "total_books": len(self.books),
            "indexed_books": len(self.index),
            "unique_authors": len(self.index._by_author),
            "unique_years": len(self.index._by_year),
        }
    
    def __repr__(self) -> str:
        return f"Library('{self.name}', {len(self.books)} books)"
    
    def __len__(self) -> int:
        return len(self.books)
