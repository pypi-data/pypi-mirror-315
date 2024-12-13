from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views
from wbcore.frontend import FrontendView

urlpatterns = [
    FrontendView.bundled_view(""),
    path("admin/", admin.site.urls),
    path("wbcore/", include(("wbcore.urls", "wbcore"), namespace="wbcore")),
    path("gleap/", include(("wbcore.contrib.gleap.urls", "gleap"), namespace="gleap")),
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", jwt_views.TokenVerifyView.as_view(), name="token_verify"),
    path(
        "example_app/",
        include(("wbcore.contrib.example_app.urls", "wbcore.contrib.example_app"), namespace="example_app"),
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
