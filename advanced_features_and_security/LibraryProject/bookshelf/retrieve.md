
---

## ✅ 2. `retrieve.md`

📄 **Path:** `LibraryProject/bookshelf/retrieve.md`

Paste this:

```markdown
```python
from bookshelf.models import Book

# Retrieve the book
book = Book.objects.get(title="1984")
book.title, book.author, book.publication_year
# ('1984', 'George Orwell', 1949)
