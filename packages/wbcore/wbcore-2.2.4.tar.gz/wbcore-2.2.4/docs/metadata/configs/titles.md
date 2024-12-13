---
tags:
    - Metadata
    - Models
    - Title
---
# Titles

The title is visible on the top left of a window and can be set through a `title_config_class`. By default it will try to assume all titles, but it can be overriden to customize the behaviour.
Four different titles are available:

- `instance`: The title that is visible if you look at the instance of a model
    - Default: `<model.verbose_name>: <str(instance)>`
- `list`: The title that is visible if you look at a list of a model (multiple instances)
    - Default: `<model.verbose_name_plural>`
- `delete`: The title that is visible if you delete an instance
    - Default: `Delete <model.verbose_name>: <str(instance)>`
- `create`: The temporary title that is visible when you create a new instance
    - Default: `Create <model.verbose_name>`

## Customizing the config class

Overriding the config class is done by subclassing `wbcore.metadata.configs.titles.TitleViewConfig` and set it as an attribute on your view `title_config_class = MyTitleViewConfig`:

=== "titles.py"

    ``` py
    from wbcore.metadata.configs.titles import TitleViewConfig


    class MyTitleViewConfig(TitleViewConfig):
        def get_instance_title(self) -> str:
            return "my custom title"

        def get_delete_title(self) -> str:
            return "my custom title"

        def get_list_title(self) -> str:
            return "my custom title"

        def get_create_title(self) -> str:
            return "my custom title"
    ```

=== "viewsets.py"

    ``` py
    from wbcore import viewsets
    from titles import MyTitleViewConfig


    class MyModelViewSet(viewsets.ModelViewSet):
        title_config_class = MyTitleViewConfig

    ```
