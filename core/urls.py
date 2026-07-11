from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
    path("projects/", views.projects, name="projects"),
    path("blog/", views.blog, name="blog"),
    path("blog/<slug:slug>/", views.article_detail, name="article_detail"),
    path("careers/", views.careers, name="careers"),
    path("faq/", views.faq, name="faq"),
    path("contact/", views.contact, name="contact"),
    path("newsletter/", views.newsletter_subscribe, name="newsletter_subscribe"),
    # Comptes & espace membre
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("account/", views.account, name="account"),
]
