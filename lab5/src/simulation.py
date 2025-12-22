import random

from lab5.src.models.book import PaperBook, EBook
from src.library import Library

def run_simulation(steps: int, seed: int | None = None) -> None:
    
    if seed is not None:
        random.seed(seed)
    
    library = Library("Grafov Library")
    
    initial_books = [
        PaperBook("1984", "George Orwell", 1949, "Dystopian", "ISBN-001", 328),
        PaperBook("Brave New World", "Aldous Huxley", 1932, "Dystopian", "ISBN-002", 288),
        EBook("The Great Gatsby", "F. Scott Fitzgerald", 1925, "Classic", "ISBN-003", 4.2),
        PaperBook("To Kill a Mockingbird", "Harper Lee", 1960, "Classic", "ISBN-004", 324),
        EBook("The Catcher in the Rye", "J. D. Salinger", 1951, "Fiction", "ISBN-005", 5.1),
        PaperBook("Pride and Prejudice", "Jane Austen", 1813, "Romance", "ISBN-006", 432),
        EBook("Dune", "Frank Herbert", 1965, "Science Fiction", "ISBN-007", 8.5),
        PaperBook("The Hobbit", "J. R. R. Tolkien", 1937, "Fantasy", "ISBN-008", 310),
    ]
    
    for book in initial_books:
        library.add_book(book)
    
    additional_books = [
        PaperBook("Fahrenheit 451", "Ray Bradbury", 1953, "Dystopian", "ISBN-009", 249),
        EBook("The Odyssey", "Homer", 800, "Epic", "ISBN-010", 12.3),
        PaperBook("Crime and Punishment", "Fyodor Dostoevsky", 1866, "Psychological", "ISBN-011", 671),
        EBook("Jane Eyre", "Charlotte Brontë", 1847, "Romance", "ISBN-012", 6.8),
        PaperBook("The Lord of the Rings", "J. R. R. Tolkien", 1954, "Fantasy", "ISBN-013", 1216),
    ]
    
    EVENT_TYPES = {
        1: "ADD_BOOK",
        2: "REMOVE_BOOK",
        3: "SEARCH_BY_AUTHOR",
        4: "SEARCH_BY_YEAR",
        5: "SEARCH_BY_GENRE",
        6: "ACCESS_BY_INDEX",
        7: "ACCESS_NONEXISTENT",
        8: "VERIFY_INDEX",
    }
    
    print(f"Симуляция {library.name}")
    print(f"Изначально {len(library.books)} книг в коллекции")
    print(f"Seed: {seed}")
    print(f"Шагов симуляции: {steps}")

    added_books_idx = 0
    
    for step in range(1, steps): # 5 ошибка 
        event_type = random.randint(1, 8)
        event_name = EVENT_TYPES[event_type]
        
        print(f"[ШАГ {step:2d}] {event_name}", end=" | ")
        
        try:
            if event_type == 1:
                if added_books_idx < len(additional_books):
                    new_book = additional_books[added_books_idx]
                    library.add_book(new_book)
                    added_books_idx += 1
                    print(f"Добавлена книга: '{new_book.title}' ({new_book.author})")
                else:
                    print("Нет больше книг для добавления")
            
            elif event_type == 2:
                if len(library.books) > 0:
                    idx_to_remove = random.randint(0, len(library.books) - 1)
                    book_to_remove = library.books[idx_to_remove]
                    library.remove_book(book_to_remove.isbn)
                    print(f"Удалена книга: '{book_to_remove.title}'")
                else:
                    print("Нечего удалять, библиотека пуста")
            
            elif event_type == 3:
                authors = list(library.index._by_author.keys())
                if authors:
                    search_author = random.choice(authors)
                    results = library.search_by_author(search_author)
                    print(f"Поиск автора '{search_author}': найдено {len(results)} книг")
                else:
                    print("Нет авторов для поиска")
            
            elif event_type == 4:
                years = list(library.index._by_year.keys())
                if years:
                    search_year = random.choice(years)
                    results = library.search_by_year(search_year)
                    print(f"Поиск года {search_year}: найдено {len(results)} книг")
                else:
                    print("Нет годов для поиска")
            
            elif event_type == 5:
                genres = set(book.genre for book in library.books)
                if genres:
                    search_genre = random.choice(list(genres))
                    results = library.search_by_genre(search_genre)
                    print(f"Поиск жанра '{search_genre}': найдено {len(results)} книг")
                else:
                    print("Нет жанров для поиска")
            
            elif event_type == 6:
                if len(library.books) > 0:
                    random_idx = random.randint(0, len(library.books) - 1)
                    book = library.books[random_idx]
                    print(f"Доступ по индексу [{random_idx}]: '{book.title}'")
                else:
                    print("Коллекция пуста")
            
            elif event_type == 7:
                fake_isbn = f"ISBN-999{random.randint(0, 99)}"
                book = library.search_by_isbn(fake_isbn)
                if book is None:
                    print(f"Попытка доступа к '{fake_isbn}': не найдена (ожидаемо)")
                else:
                    print(f"Неожиданно найдена книга: {book.title}")
            
            elif event_type == 8:
                stats = library.get_stats()
                if stats["total_books"] == stats["indexed_books"]:
                    print(f"Индексы целостны: {stats['total_books']} книг")
                else:
                    print(f"Несоответствие! Книг: {stats['total_books']}, "
                          f"Индексов: {stats['indexed_books']}")
        
        except Exception as e:
            print(f"ошибка: {e}")
    print("статистика")
    stats = library.get_stats()
    for key, value in stats.items():
        print(f"{key.upper():20s}: {value}")
    
    print(f"Топ авторы:")
    for author, books in sorted(
        library.index._by_author.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )[:5]:
        print(f"  - {author:20s}: {len(books)} книг(и)")
    
    print(f"Топ годы:")
    for year, books in sorted(
        library.index._by_year.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )[:5]:
        print(f"  - {year:4d}: {len(books)} книг(и)")
    
    print(f"Жанры:")
    genres = {}
    for book in library.books:
        genres[book.genre] = genres.get(book.genre, 0) + 1
    for genre, count in sorted(genres.items()):
        print(f"  - {genre:20s}: {count} книг(и)")
    
    print("Симуляция завершена успешно")


if __name__ == "__main__":
    run_simulation(steps=25, seed=42)