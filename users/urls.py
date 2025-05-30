from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

# API URL patterns
api_urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", views.RegisterView.as_view(), name="api_register"),
    path("profile/", views.UserProfileView.as_view(), name="api_profile"),
    path(
        "regenerate-token/",
        views.RegenerateRequestTokenView.as_view(),
        name="api_regenerate_token",
    ),
    path(
        "token-history/", views.TokenHistoryView.as_view(), name="api_token_history"
    ),
    path("plans/", views.PlansListView.as_view(), name="api_plans"),
    path("subscription/", views.user_subscription, name="user-subscription"),
    path("create-checkout-session/", views.create_checkout_session_api, name="api_create_checkout_session"),
]

urlpatterns = [
    path("", views.home, name="home"),
    path("profile/", views.profile, name="profile"),
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("register/", views.register_user, name="register"),
    path("regenerate-token/", views.regenerate_token, name="regenerate_token"),
    
    # API endpoints (standalone for backward compatibility)
    path("api/plans/", views.PlansListView.as_view(), name="api_plans"),
    
    # Subscription URLs - Fixed to match test expectations
    path("plans/", views.plans_view, name="plans"),
    path("create-checkout-session/", views.create_checkout_session, name="create-checkout-session"),
    path("subscription/success/", views.subscription_success, name="subscription-success"),
    path("cancel-subscription/", views.cancel_subscription, name="cancel-subscription"),
    path("reactivate-subscription/", views.reactivate_subscription, name="reactivate-subscription"),
    path("stripe/webhook/", views.stripe_webhook, name="stripe_webhook"),
    
    # Include API URLs with namespace
    path("api/", include((api_urlpatterns, 'api'), namespace='api')),
]
