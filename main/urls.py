from django.urls import path, include
from . import views

app_name = "main"

urlpatterns = [
    path('', views.index, name='index'),
    path("receipt_create/", views.receipt_create, name="receipt_create"),
    path("profile/", views.profile, name="profile"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("receipts/", views.receipts, name="receipts"),
    path("rules/", views.rules, name="rules"),
]