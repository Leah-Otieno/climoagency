from django.contrib import admin
from django.urls import path
from Agency import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("home", views.index, name="home"),
    path("about/", views.about, name="about"),
    path("agents/", views.agents, name="agents"),
    path("contact/", views.contact, name="contact"),
    path("properties/", views.properties, name="properties"),
    path("propertysingle/", views.property_single, name="property_single"),
    path("servicedetails/", views.service_details, name="service_details"),
    path("services/", views.services, name="services"),
    path("starter/", views.starter, name="starter"),
    path("", views.register, name="register"),
    path("login/", views.login, name="login"),
    path('pay/', views.pay, name='pay'),
    path('stk/', views.stk, name='stk'),
    path('token/', views.token, name='token'),

]
