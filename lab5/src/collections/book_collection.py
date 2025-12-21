from typing import List, Iterator, Union
from src.models.book_buggy import Book


class BookCollection:
    def __init__(self):
        self._books: List = []
    
    def add(self, book: "Book") -> None:
        self._books.append(book)
    
    def remove(self, book: "Book") -> bool:
        try:
            self._books.remove(book)
            return True
        except ValueError:
            return False
    
    def remove_by_isbn(self, isbn: str) -> bool:
        for book in self._books:
            if book.isbn == isbn:
                self._books.remove(book)
                return True
        return False
    
    def __getitem__(self, index: Union[int, slice]) -> Union["Book", List["Book"]]:
        return self._books[index]
    
    def __iter__(self) -> Iterator["Book"]:
        return iter(self._books)
    
    def __len__(self) -> int:
        return len(self._books)
    
    def __contains__(self, item: "Book") -> bool:
        return item in self._books
    
    def __repr__(self) -> str:
        return f"BookCollection({len(self._books)} books)"
    
    def clear(self) -> None:
        self._books.clear()
    
    def get_all(self) -> List["Book"]:
        return self._books.copy()
