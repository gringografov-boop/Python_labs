# Лабораторная работа №5: Отладка кодовой базы

## Ошибка 1 — Сравнение через `is` вместо `==`

**Место:** `book.py`, класс `EBook`, метод `get_info()`

**Симптом:**
При создании EBook с `file_size_mb=0.0`, условие не срабатывает и возвращается неправильный формат вместо "(empty)".

**Как воспроизвести:**
```python
book = EBook("Title", "Author", 2024, "Genre", "ISBN-001", 0.0)
print(book.get_info())  # Выводит неправильный формат
```

**Отладка:**
Breakpoint в методе `get_info()`. В отладчике:
- `self.file_size_mb = 0.0`
- Условие `if self.file_size_mb is 0.0:` возвращает False
- Выполняется else ветка

**Причина:**
`is` сравнивает идентичность объектов в памяти, а не значения. Для float это ненадёжно.

**Исправление:**
```python
# Было:
if self.file_size_mb is 0.0:

# Стало:
if self.file_size_mb == 0.0:
```

**Проверка:**
После исправления EBook(file_size_mb=0.0) выводит "(empty)" корректно.

---

## Ошибка 2 — Изменение коллекции во время итерации

**Место:** `index_dict.py`, метод `clear()`

**Симптом:**
При вызове `library.index.clear()` выбрасывается `RuntimeError: dictionary changed size during iteration`.

**Как воспроизвести:**
```python
library = Library("Test")
library.add_book(PaperBook("1984", "Orwell", 1949, "Dystopian", "ISBN-001", 328))
library.index.clear()  # RuntimeError!
```

**Отладка:**
Breakpoint в начало цикла `for key in self._by_author.keys():`.
В отладчике видно:
- Цикл начинает итерацию
- На первой итерации выполняется `del self._by_author[key]`
- Python выбрасывает исключение

**Причина:**
Нельзя удалять элементы из словаря во время итерации по его ключам. Python отслеживает размер и выбрасывает исключение.

**Исправление:**
```python
# Было:
def clear(self) -> None:
    for key in self._by_author.keys():
        del self._by_author[key]

# Стало:
def clear(self) -> None:
    for key in list(self._by_author.keys()):
        del self._by_author[key]
```

**Проверка:**
После исправления `library.index.clear()` выполняется без ошибок.

---

## Ошибка 3 — Перепутанные аргументы

**Место:** `library.py`, метод `search_by_author()`

**Симптом:**
При вызове `library.search_by_author("George Orwell")` выбрасывается `TypeError: 'str' object cannot be interpreted as an integer`.

**Как воспроизвести:**
```python
library = Library("Test")
library.add_book(PaperBook("1984", "George Orwell", 1949, "Dystopian", "ISBN-001", 328))
results = library.search_by_author("George Orwell")  # TypeError!
```

**Отладка:**
Breakpoint в `search_by_author()`. В стеке вызовов видно:
- Вызывается `get_by_year(author)` вместо `get_by_author(author)`
- `get_by_year()` ожидает int, получает str
- TypeError выбрасывается в `get_by_year()`

**Причина:**
В методе `search_by_author()` вызывается неправильный метод индекса.

**Исправление:**
```python
# Было:
def search_by_author(self, author: str) -> List["Book"]:
    return self.index.get_by_year(author)

# Стало:
def search_by_author(self, author: str) -> List["Book"]:
    return self.index.get_by_author(author)
```

**Проверка:**
После исправления `search_by_author("George Orwell")` возвращает список книг автора.

---

## Ошибка 4 — Использование изменяемого значения по умолчанию

**Место:** `library.py`, метод `__init__()`, инициализация `self.search_history`

**Симптом:**
При создании двух экземпляров Library, добавление значения в `search_history` одного экземпляра автоматически появляется в другом.

**Как воспроизвести:**
```python
lib1 = Library("Library 1")
lib2 = Library("Library 2")
lib1.search_history.append("query1")
print(len(lib2.search_history))  # Выведет 1 вместо 0 — ошибка!
```

**Отладка:**
Breakpoints в `__init__()` обоих экземпляров. В отладчике:
- `id(lib1.search_history)` == `id(lib2.search_history)` — один и тот же объект!
- Изменение одного влияет на другой

**Причина:**
Список `[]` создаётся один раз при определении класса. Все экземпляры указывают на один объект.

**Исправление:**
Правильная инициализация в `__init__()`:
```python
# Было:
def __init__(self, name: str = "Main Library"):
    self.name = name
    self.search_history = []

# Стало:
def __init__(self, name: str = "Main Library"):
    self.name = name
    self.search_history: List[str] = []
```

**Проверка:**
После исправления каждый экземпляр имеет собственный `search_history`.

---

## Ошибка 5 — Off-by-one в цикле

**Место:** `simulation.py`, главный цикл симуляции, строка с `for step in`

**Симптом:**
При запуске с `steps=25` логи выводят шаги 0–24 вместо 1–25. Первый шаг отображается как `[ШАГ 0]`.

**Как воспроизвести:**
```bash
python main.py
# Первые логи:
# [ШАГ 0] ADD_BOOK ...
# [ШАГ 1] REMOVE_BOOK ...
# Ожидается начинать с [ШАГ 1]
```

**Отладка:**
Breakpoint на печать шага. В отладчике:
- Первая итерация: `step = 0`
- Последняя итерация: `step = 24` (при steps=25)
- Всего 25 итераций, но нумерация с 0

**Причина:**
Цикл использует `range(0, steps)`, начиная с 0. Нужно начинать с 1.

**Исправление:**
```python
# Было:
for step in range(0, steps):

# Стало:
for step in range(1, steps + 1):
```

**Проверка:**
После исправления логи выводят `[ШАГ 1]` через `[ШАГ 25]`.

---

## Итоговая таблица

| Ошибка | Файл | Метод | Тип ошибки | Статус |
|--------|------|-------|-----------|--------|
| 1 | book.py | EBook.get_info() | is вместо == | Исправлено |
| 2 | index_dict.py | clear() | Изменение коллекции при итерации | Исправлено |
| 3 | library.py | search_by_author() | Перепутанные аргументы | Исправлено |
| 4 | library.py | __init__() | Изменяемое значение по умолчанию | Исправлено |
| 5 | simulation.py | run_simulation() | Off-by-one | Исправлено |

Все 5 ошибок выявлены, отлажены и исправлены успешно.
