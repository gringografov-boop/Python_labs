class Book:
    def __init__(
        self,
        title: str,
        author: str,
        year: int,
        genre: str,
        isbn: str
    ):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.isbn = isbn
    
    def __repr__(self) -> str:#объект в строку 
        return f"{self.__class__.__name__}('{self.title}', {self.author}, {self.year})"
    
    def __contains__(self, keyword: str) -> bool:
        keyword_lower = keyword.lower()
        return (
            keyword_lower in self.title.lower() or
            keyword_lower in self.author.lower()
        )
    
    def get_info(self) -> str:
        return (
            f"'{self.title}' ({self.author}, {self.year}) - {self.genre}"
            f"[ISBN: {self.isbn}]" 
        )
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Book):
            return False
        return self.isbn == other.isbn
    
    def __hash__(self) -> int:
        return hash(self.isbn)


class PaperBook(Book):
    def __init__(
        self,
        title: str,
        author: str,
        year: int,
        genre: str,
        isbn: str,
        pages: int
    ):
        super().__init__(title, author, year, genre, isbn)
        self.pages = pages
    
    def get_info(self) -> str:
        base_info = super().get_info()
        return f"{base_info} - {self.pages} стр."


class EBook(Book):
    def __init__(
        self,
        title: str,
        author: str,
        year: int,
        genre: str,
        isbn: str,
        file_size_mb: float
    ):
        super().__init__(title, author, year, genre, isbn)
        self.file_size_mb = file_size_mb
    
    def get_info(self) -> str:
        base_info = super().get_info()
        return f"{base_info} - {self.file_size_mb:.1f} МБ"
