---
tags:
  - Metadata
  - Ordering
---
# Search Fields

This config class most likely never has to be subclassed as customization is not necessary here. It returns a list of all orderable fields.

```json
{
    "ordering_fields": ["<field_a>", "<field_b>"]
}
```

The `ordering_fields` is populated by using all fields set in a View, for example:

```python
class MyModelViewSet(viewsets.ModelViewSet):
    ordering_fields = ["<field_a>", "<field_b>"]

```

In particular cases, we would like to order a field behind a foreign key, or specify that we want to disregard `null` values from ordering:
```python
class MyModelViewSet(viewsets.ModelViewSet):
    ordering_fields = ["<remote_field>__<field>", "<field>__nulls_last"]

```
The config class in the background makes sure that the appropriate fields are returned, in order to let the frontend know on what columns to append the ordering mechanism.
