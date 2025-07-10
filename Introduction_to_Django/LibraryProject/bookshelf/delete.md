
---

## ✅ 4. `delete.md`

📄 **Path:** `LibraryProject/bookshelf/delete.md`

Paste this:

```markdown
```python
from bookshelf.models import Book

# Delete the book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Confirm deletion
Book.objects.all()
# <QuerySet []>
