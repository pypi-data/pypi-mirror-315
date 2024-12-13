from wbcore.contrib.agenda.viewsets.menu import CALENDAR_MENUITEM
from wbcore.contrib.example_app.viewsets.menu import EXAMPLE_APP_MENU
from wbcore.menus import default_registry

default_registry.register(EXAMPLE_APP_MENU)
default_registry.register(CALENDAR_MENUITEM)
