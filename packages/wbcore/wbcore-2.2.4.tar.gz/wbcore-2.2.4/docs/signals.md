Since one app can impose indirect dependencies to other apps by adding buttons to their views, django wbcore defines two signals to remedy this and to provide means to define buttons and resources outside of an app:

### add_instance_buttons

To add an instance button into a remote app, simply create a receiver which listens to the `wbcore.signals.instance_buttons.add_instance_button` signal and which accepts the following arguments:

* sender: The Viewset class that is sending the signal
* many: Boolean, indicates whether it is a list or an instance

Example:

```python
@receiver(add_instance_button, sender=<ModelViewSet>)
def add_instance_buttons_receiver(sender, many, *args, **kwargs):
    return bt.HyperlinkButton(icon="<icon>", label="<label>", endpoint="<url>")
```

Sometimes you wan to create a button with a key instead of an endpoint, where the key is an additional resource.

### add_additional_resources

To add an additional resource to a remote app, create a receiver which listens to the `wbcore.signals.instance_buttons.add_additional_resouce` and which accepts the following arguments:

* sender: The Serializer Class that is sending the signal
* serializer: The Serializer instance that is sending the signal
* request: The current request
* user: The current user

Example:

```python
@receiver(add_additional_resource, sender=<ModelSerializer>)
def test_adding_additional_resource(sender, serializer, instance, request, user, **kwargs):
    return {"<key>": "<url>"}
```

### add_filters

To add an remote filters to a remote app, create a receiver which listens to the `wbcore.signals.filters.add_filters` and which accepts the following arguments:

* sender: The Serializer Class that is sending the signal
* request: The current request
* queryset: The filtered queryset

Example:
```python
@receiver(add_filters, sender=<ModelSerializer)
def test_adding_remote_filter(sender, **kwargs):
    return {"filter_label": wb_filters.BooleanFilter(
            field_name="filter_name", # important!
            label="Filter Label",
            method=method_x
        )}
```
