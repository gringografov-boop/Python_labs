import pytest
from src.models.book import Book, PaperBook, EBook


class TestBook:
    def test_book_creation(self):
        """Тест создания книги."""
        book = Book("1984", "George Orwell", 1949, "Dystopian", "ISBN-001")
        assert book.title == "1984"
        assert book.author == "George Orwell"
        assert book.year == 1949
        assert book.genre == "Dystopian"
        assert book.isbn == "ISBN-001"
    
    def test_book_repr(self):
        """Тест строкового представления."""
        book = Book("1984", "George Orwell", 1949, "Dystopian", "ISBN-001")
        assert repr(book) == "Book('1984', George Orwell, 1949)"
    
    def test_book_get_info(self):
        """Тест получения полной информации."""
        book = Book("1984", "George Orwell", 1949, "Dystopian", "ISBN-001")
        info = book.get_info()
        assert "1984" in info
        assert "George Orwell" in info
        assert "1949" in info
        assert "Dystopian" in info
        assert "ISBN-001" in info
    
    def test_book_contains_title(self):
        """Тест магического метода __contains__ для названия."""
        book = Book("1984", "George Orwell", 1949, "Dystopian", "ISBN-001")
        assert "1984" in book
        assert "984" in book
        assert "1" in book
    
    def test_book_contains_author(self):
        """Тест магического метода __contains__ для автора."""
        book = Book("1984", "George Orwell", 1949, "Dystopian", "ISBN-001")
        assert "Orwell" in book
        assert "George" in book
    
    def test_book_contains_case_insensitive(self):
        """Тест case-insensitive поиска."""
        book = Book("1984", "George Orwell", 1949, "Dystopian", "ISBN-001")
        assert "ORWELL" in book
        assert "orwell" in book
        assert "1984" in book
    
    def test_book_contains_negative(self):
        """Тест отрицательного случая __contains__."""
        book = Book("1984", "George Orwell", 1949, "Dystopian", "ISBN-001")
        assert "Unknown" not in book
        assert "2023" not in book
    
    def test_book_equality(self):
        """Тест сравнения книг по ISBN."""
        book1 = Book("1984", "George Orwell", 1949, "Dystopian", "ISBN-001")
        book2 = Book("1984", "George Orwell", 1949, "Dystopian", "ISBN-001")
        book3 = Book("1984", "George Orwell", 1949, "Dystopian", "ISBN-002")
        
        assert book1 == book2
        assert book1 != book3
    
    def test_book_hash(self):
        """Тест хеширования по ISBN."""
        book1 = Book("1984", "George Orwell", 1949, "Dystopian", "ISBN-001")
        book2 = Book("1984", "George Orwell", 1949, "Dystopian", "ISBN-001")
        
        assert hash(book1) == hash(book2)


class TestPaperBook:
    """Тесты для класса PaperBook."""
    
    def test_paperbook_creation(self):
        """Тест создания бумажной книги."""
        book = PaperBook("1984", "George Orwell", 1949, "Dystopian", "ISBN-001", 328)
        assert book.title == "1984"
        assert book.pages == 328
    
    def test_paperbook_repr(self):
        """Тест строкового представления."""
        book = PaperBook("1984", "George Orwell", 1949, "Dystopian", "ISBN-001", 328)
        assert repr(book) == "PaperBook('1984', George Orwell, 1949)"
    
    def test_paperbook_get_info(self):
        """Тест получения полной информации с количеством страниц."""
        book = PaperBook("1984", "George Orwell", 1949, "Dystopian", "ISBN-001", 328)
        info = book.get_info()
        assert "328 стр." in info
    
    def test_paperbook_inheritance(self):
        """Тест наследования от Book."""
        book = PaperBook("1984", "George Orwell", 1949, "Dystopian", "ISBN-001", 328)
        assert isinstance(book, Book)
        assert "Orwell" in book


class TestEBook:
    """Тесты для класса EBook."""
    
    def test_ebook_creation(self):
        """Тест создания электронной книги."""
        book = EBook("1984", "George Orwell", 1949, "Dystopian", "ISBN-001", 4.2)
        assert book.title == "1984"
        assert book.file_size_mb == 4.2
    
    def test_ebook_repr(self):
        """Тест строкового представления."""
        book = EBook("1984", "George Orwell", 1949, "Dystopian", "ISBN-001", 4.2)
        assert repr(book) == "EBook('1984', George Orwell, 1949)"
    
    def test_ebook_get_info(self):
        """Тест получения полной информации с размером файла."""
        book = EBook("1984", "George Orwell", 1949, "Dystopian", "ISBN-001", 4.2)
        info = book.get_info()
        assert "4.2 МБ" in info
    
    def test_ebook_inheritance(self):
        """Тест наследования от Book."""
        book = EBook("1984", "George Orwell", 1949, "Dystopian", "ISBN-001", 4.2)
        assert isinstance(book, Book)
        assert "Orwell" in book
if __name__ == "__main__":
    pytest.main()