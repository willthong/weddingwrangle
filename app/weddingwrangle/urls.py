"""weddingwrangle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, reverse_lazy
from . import views
from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

app_name = "weddingwrangle"
urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "", 
        TemplateView.as_view(template_name="weddingwrangle/wedding_details.html"),
        name="details",
    ),
    path("home/", views.HomePage.as_view(), name="home"),
    path("guests/", views.GuestList.as_view(), name="guest_list"),
    path("guests/create/", views.GuestCreate.as_view(), name="guest_create"),
    path("guests/export/csv/", views.export_csv, name="guest_export_csv"),
    path("guests/export/qr/", views.export_qr, name="guest_export_qr"),
    path("guests/upload/", views.GuestUpload.as_view(), name="guest_upload"),
    path(
        "guests/<int:pk>/update/",
        views.GuestUpdate.as_view(success_url=reverse_lazy("guest_list")),
        name="guest_update",
    ),
    path("guests/<int:pk>/delete/", views.GuestDelete.as_view(), name="guest_delete"),
    path("email/", views.EmailList.as_view(), name="email_create"),
    path(
        "email/rsvp_template/",
        views.RSVPEmailTemplate.as_view(
            success_url=reverse_lazy("email_create"),
        ),
        name="rsvp_email_template",
    ),
    path(
        "email/<int:pk>/email_confirm/",
        views.EmailConfirm.as_view(
            success_url=reverse_lazy("email_create"),
        ),
        name="email_confirm",
    ),
    path("email/<int:pk>/detail/", views.EmailDetail.as_view(), name="email_detail"),
    path("qr_code/", include("qr_code.urls", namespace="qr_code"), name="qr_urls"),
    path(
        "rsvp/thankyou/",
        TemplateView.as_view(template_name="weddingwrangle/rsvp_thank_partner.html"),
        name="rsvp_thank_partner",
    ),
    path(
        "rsvp/<str:rsvp_link>/",
        views.RSVPView.as_view(success_url=reverse_lazy("rsvp_thank")),
        name="rsvp",
    ),
    path(
        "rsvp/<str:rsvp_link>/thanks/",
        views.RSVPThank.as_view(),
        name="rsvp_thank",
    ),
    path(
        "rsvp/<str:rsvp_link>/partner/",
        views.RSVPPartner.as_view(),
        name="rsvp_partner",
    ),
    path("invites", views.Invites.as_view(), name="invites"),
    path("accounts/", include("django.contrib.auth.urls")),
    # https://stackoverflow.com/a/63445257/3161714
    path(
        "logout/",
        LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL),
        name="logout",
    ),
]
