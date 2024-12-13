By default all endpoints make use of a default action button to share the endpoint to another user.

The default fields are:

* `user_id`: The id of the user the endpoint is shared to
* `widget_endpoint`: A field where the widget_endpoint is injected in (NOTE: It includes the base_url and needs to be seperated.)
* `message`: The message that is sent to the user.

The share functionality can be customized in three ways:

* `DEFAULT_SHARE_BUTTON`: A method that accepts a request and returns an `ActionButton` (default: `wbcore.share.buttons.share_action_button`)
* `DEFAULT_SHARE_NOTIFICATION`: A method that accepts all fields from the share button/serializer and the user and handles the creation of the notification (default: `wbcore.share.notifications.share_notification`)
* `DEFAULT_SHARE_SERIALIZER`: The serializer that is used for serializing the share functionality (default: `wbcore.share.serializers.ShareSerializer`)

Usually it should be enough to override `DEFAULT_SHARE_NOTIFICATION` and `DEFAULT_SHARE_SERIALIZER` as the `DEFAULT_SHARE_BUTTON` makes use of the above two to render a sensible button.

An example of customization can be found below:

```python
# .../serializers.py
from wbcore.serializers import Serializer, CharField, IntegerField, TextField

class ShareSerializer(Serializer):
    user_id = IntegerField(label="User ID")
    widget_endpoint = CharField(label="Widget URL") # This is a mandatory field!
    message = TextField(label="Message", default="Check out this Widget.")

    some_additional_field = IntegerField(label="Some Additional Field")
```

```python
# .../notifications.py
from wbcore.metadata.configs.buttons import WidgetButton

def share_notification(user_id, widget_endpoint, message, some_additional_field, user):
    # Make sure that all the fields that are used in the Serializer are present as parameters and the user
    _, endpoint = widget_endpoint.split("?widget_endpoint=")
    Notification.objects.create(
        recipient_id=user_id,
        title=f"{user.first_name} {user.last_name} shared a widget with you",
        message=message,
        buttons=[
            dict(WidgetButton(label="Open", icon="wb-icon-data", endpoint=endpoint))
        ],
    )
```
