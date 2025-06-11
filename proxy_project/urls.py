from django.conf import settings
from django.conf.urls.i18n import i18n_patterns, set_language
from django.contrib import admin
from django.urls import include, path
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from sitemaps import sitemaps
from proxy_app.views import api_documentation

def redirect_to_default_language(request):
    """Redirect root path to default language"""
    return redirect('/en/')

urlpatterns = [
    path("", redirect_to_default_language, name="root_redirect"),
    path("i18n/", include("django.conf.urls.i18n")),
    path("set_language/", set_language, name="set_language"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', lambda r: HttpResponse("User-agent: *\nAllow: /\nSitemap: https://api.financialdata.online/sitemap.xml", content_type="text/plain")),
    # API Documentation - accessible without language prefix
    path("api/docs/", api_documentation, name="api_docs_direct"),
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("users.urls")),
    # Legacy route for backward compatibility
    path("v1/", include("proxy_app.urls", namespace="proxy_app_legacy")),
    # New unified API route
    path("api/v1/", include("proxy_app.urls", namespace="proxy_app")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    prefix_default_language=True,
)

# Add debug toolbar URLs for development
if settings.DEBUG:
    try:
        import debug_toolbar

        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        # debug_toolbar not installed, skip it
        pass
