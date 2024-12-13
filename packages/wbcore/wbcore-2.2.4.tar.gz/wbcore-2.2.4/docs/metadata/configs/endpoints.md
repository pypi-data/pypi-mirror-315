# Endpoints

The endpoint config class is in charge of defining some actions on the current resource. For example an `instance_endpoint` when looking at a list will make it possible to open an item in a list.

The default behaviour is:
- `instance_endpoint`:
    - In a list: Make it possible to open/change an item
    - In a form: Make it possible to change an item
- `list_endpoint`:
    - ???
- `delete_endpoint`:
    - Make it possible to delete an item
- `create_endpoint`:
    - Make it possible to create a new item

Usually, the developer does not have to customize this class, as it auto-generates itself with the help of some parameters:

1. For each endpoint it checks if the user has the necessary permissions, e.g. `create_endpoint` -> `<app_label>.add_<model>`
2. It gets the default endpoint from the model class: `Model.get_endpoint_basename()`


## Customizing the config class

If, for some reason, the developer does not to override and customize his mechanism, it can be done by subclassing `wbcore.metadata.configs.endpoints.EndpointViewConfig` and set it as an attribute on your view `endpoint_config_class = MyEndpointViewConfig`.

=== "endpoints.py"

    ``` py
    from wbcore.metadata.configs.endpoints import EndpointViewConfig


    class MyEndpointViewConfig(EndpointViewConfig):

        # Override this method to customize the base endpoint
        # that is used by all other methods
        def get_endpoint(self, **kwargs):
            return "some-endpoint"

        # Override this method to customize only the instance
        # endpoint
        def get_instance_endpoint(self, **kwargs):
            return "some-instance-endpoint"

    ```

=== "viewsets.py"

    ``` py
    from wbcore import viewsets
    from endpoints import MyEndpointViewConfig


    class MyModelViewSet(viewsets.ModelViewSet):
        endpoint_config_class = MyEndpointViewConfig

    ```
