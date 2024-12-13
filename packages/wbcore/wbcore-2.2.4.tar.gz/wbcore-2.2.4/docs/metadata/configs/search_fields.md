---
tags:
  - Metadata
  - Search
---
# Search Fields

This config class most likely never has to be subclassed as customization is not necessary here. It returns a list of all fields used for searching.

```json
{
    "search_fields": ["<field_a>", "<field_b>"]
}
```

The `search_fields` is populated by using all fields set in a View, for example:

```python
class MyModelViewSet(viewsets.ModelViewSet):
    search_fields = ["<field_a>", "<field_b>"]

```
