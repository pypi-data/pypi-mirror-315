# Getting started

The metadata is always used in conjunction with a view/viewset. Those views are a modified version of the ones from [Django Rest Framework](https://www.django-rest-framework.org/). Without modifying anything, they look almost identical:

``` py title="viewsets.py"
from wbcore import viewsets  # (1)


class MyModelViewSet(viewsets.ModelViewSet):
    display_config_class = MyDisplayViewConfig  # (2)

```

1.  Make sure you have import `viewset` from `wbcore` and not from `rest_framework`
2.  Setting a config class always follows the same pattern: `<name>_config_class`, where `<name>` is one of the config classes.
    `MyDisplayViewConfig` is a subclass from `wbcore.metadata.configs.display.DisplayViewConfig`, which inherits from
    `wbcore.metadata.configs.bases.WBCoreViewConfig`. In fact, all config classes have to inherit from `WBCoreViewConfig`.
