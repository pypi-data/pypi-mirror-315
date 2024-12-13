---
tags:
    - Metadata
    - Fields
---
# Fields

This config class most likely never has to be subclassed as customization is not necessary here. It returns a dictionairy mapping all field names their representation dictionairies.

```json
{
    "fields": {
        "<field_name>": {/* representation of a field */}
    }
}
```

Each serializable field has to provide a method called `#!py get_representation(request: Request, field_name: str) -> dict`. This method is then called for each field specified in `#!py MySerializer.Meta.fields`.
