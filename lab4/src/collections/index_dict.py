from typing import Dict, List, Iterator, Union
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.book import Book


class IndexDict:
    
    def __init__(self):
        self._by_isbn: Dict[str, "Book"] = {}          # ISBN -> Book (1:1)
        self._by_author: Dict[str, List["Book"]] = {}  # Author -> [Books]
        self._by_year: Dict[int, List["Book"]] = {}    # Year -> [Books]
    
    def add_book(self, book: "Book") -> None:
        self._by_isbn[book.isbn] = book
        
        if book.author not in self._by_author:
            self._by_author[book.author] = []
        if book not in self._by_author[book.author]:
            self._by_author[book.author].append(book)
        
        if book.year not in self._by_year:
            self._by_year[book.year] = []
        if book not in self._by_year[book.year]:
            self._by_year[book.year].append(book)
    
    def remove_book(self, book: "Book") -> None:
        if book.isbn in self._by_isbn:
            del self._by_isbn[book.isbn]
        
        if book.author in self._by_author:
            if book in self._by_author[book.author]:
                self._by_author[book.author].remove(book)
            if len(self._by_author[book.author]) == 0:
                del self._by_author[book.author]
        
        if book.year in self._by_year:
            if book in self._by_year[book.year]:
                self._by_year[book.year].remove(book)
            if len(self._by_year[book.year]) == 0:
                del self._by_year[book.year]

    def get_by_isbn(self, isbn: str) -> "Book | None":
        return self._by_isbn.get(isbn)

    def get_by_author(self, author: str) -> list["Book"]:
        return self._by_author.get(author, [])

    def get_by_year(self, year: int) -> list["Book"]:
        return self._by_year.get(year, [])
    
    def __getitem__(self, key: str) -> Union["Book", List["Book"], None]:
        if key.startswith("isbn:"):
            isbn = key[5:]
            return self._by_isbn.get(isbn)
        elif key.startswith("author:"):
            author = key[7:]
            return self._by_author.get(author, [])
        elif key.startswith("year:"):
            year = int(key[5:])
            return self._by_year.get(year, [])
        else:
            raise KeyError(
                f"Unknown index format: {key}. Use 'isbn:', 'author:' or 'year:' prefix"
            )
    
    def __setitem__(self, key: str, value: "Book") -> None:
        if key.startswith("add:"):
            self.add_book(value)
        else:
            raise KeyError(f"Unsupported operation: {key}. Use 'add:' prefix")
    
    def __delitem__(self, key: str) -> None:
        if key.startswith("remove:"):
            isbn = key[7:]
            book = self.get_by_isbn(isbn)
            if book:
                self.remove_book(book)
        else:
            raise KeyError(f"Unknown delete format: {key}. Use 'remove:' prefix")
    
    def __len__(self) -> int:
        return len(self._by_isbn)
    
    def __iter__(self) -> Iterator[str]:
        yield f"by_isbn: {len(self._by_isbn)}"
        yield f"by_author: {len(self._by_author)}"
        yield f"by_year: {len(self._by_year)}"
    
    def __contains__(self, item: Union["Book", str]) -> bool:
        if hasattr(item, 'isbn'):
            return item.isbn in self._by_isbn
        elif isinstance(item, str):
            if item.startswith("isbn:"):
                return item[5:] in self._by_isbn
            elif item.startswith("author:"):
                return item[7:] in self._by_author
            elif item.startswith("year:"):
                try:
                    return int(item[5:]) in self._by_year
                except ValueError:
                    return False
        return False
    
    def __repr__(self) -> str:#индекс в строку
        return f"IndexDict({len(self._by_isbn)} books indexed)"
    
    def clear(self) -> None:
        self._by_isbn.clear()
        self._by_author.clear()
        self._by_year.clear()
