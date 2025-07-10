
---

## ✅ 3. `update.md`

📄 **Path:** `LibraryProject/bookshelf/update.md`

Paste this:

```markdown
```python
from bookshelf.models import Book

# Update the book title
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book
# <Book: Nineteen Eighty-Four by George Orwell (1949)>
