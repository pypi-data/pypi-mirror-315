---
tags:
  - Metadata
  - Pagination
---
# Pagination

The workbench supports two different types of pagination, `limitoffset` and `cursor`. Both have their pros and cons, however the rule of thumb is:
Use `limitoffset` whenever you handle data for tables - use `cursor` whenever you handle repesentational data. By default, this is already set.
Therefore you most likely will never have to subclass this config class.
