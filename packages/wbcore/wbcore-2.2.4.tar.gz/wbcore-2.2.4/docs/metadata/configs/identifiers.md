---
tags:
  - Metadata
  - Cache
  - Identifier
---
# Identifier

The workbench uses identifiers to uniquely identify models and cache them. (We do not consider an endpoint unique, as multiple endpoints could handle the same data)
Whenever an endpoint with an identifier changes (create/change/delete), we know that this endpoint has to be refetched. Therefore all endpoints stored under the same
identifiers invalidate themselves.

The config class for identifiers will return a sensible default as an identifier, which is a combination of the app label + model name. If you want to override an identifier, you can still do this by adding it to the view, e.g.:

``` py
class MyModelViewSet(viewsets.ModelViewSet):
    IDENTIFIER = "mycustomidentifier"

```

Sometimes when you change data, you know that other pieces of data will change as well which might be stored in a different model. In order to invalidate the cache and make sure that the frontend fetches the relevant data as well, we can also supply dependant identifiers:

``` py
class MyModelViewSet(viewsets.ModelViewSet):
    IDENTIFIER = "mycustomidentifier"
    DEPENDANT_IDENTIFIER = "mydepedandantidentifier"

```

Whenever the data behind the Viewset `MyModelViewSet` is updated by the frontend, it knows that is has to update all data cached behind

- `mycustomidentifier`
- `mydependandantidentifier`
