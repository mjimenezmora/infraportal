from django.urls import path
from . import views
from . import views_auth

urlpatterns = [

    # Dashboard
    path("", views.dashboard, name="dashboard"),
    # Vistas de Login
    path("login/", views_auth.login_view, name="login"),
    path("logout/", views_auth.logout_view, name="logout"),
    # rutas
    path("virtuales/", views.lista_virtuales, name="lista_virtuales"),
    path("fisicos/", views.lista_fisicos, name="lista_fisicos"),
    path("password-gen/", views.generar_password, name="generar_password"),
    path("ips/", views.lista_ip, name="lista_ip"),
    # CRUD
    path("virtuales/agregar/", views.agregar_virtual, name="agregar_virtual"),
    path("virtuales/editar/<int:id>/", views.editar_virtual, name="editar_virtual"),
    path("virtuales/eliminar/<int:id>/", views.eliminar_virtual, name="eliminar_virtual"),
    path("subir-csv/", views.subir_csv, name="subir_csv"),
]
