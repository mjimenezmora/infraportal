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
    # CRUD Virtuales
    path("virtuales/agregar/", views.agregar_virtual, name="agregar_virtual"),
    path("virtuales/editar/<int:id>/", views.editar_virtual, name="editar_virtual"),
    path("virtuales/eliminar/<int:id>/", views.eliminar_virtual, name="eliminar_virtual"),
    path("subir-csv/", views.subir_csv, name="subir_csv"),
    # CRUD Fisicos
    path("fisicos/agregar/", views.agregar_fisico, name="agregar_fisico"),
    path("fisicos/editar/<int:id>/", views.editar_fisico, name="editar_fisico"),
    path("fisicos/eliminar/<int:id>/", views.eliminar_fisico, name="eliminar_fisico"),
    # Agregar OS, servicio
    path('so/agregar', views.agregar_so, name='agregar_so'),
    #path('servicio/agregar', views.agregar_servicio, name='agregar_servicio'),
    # Detalles de tabla
    path('virtual/<int:pk>/detalle/', views.detalle_virtual, name='detalle_virtual'),
    path('fisico/<int:pk>/detalle/', views.detalle_fisico, name='detalle_fisico'),
    # Agregar credenciales
    path('credencial/agregar/<str:tipo_servidor>/<int:pk>/', views.agregar_credencial, name='agregar_credencial'),
    # Desvincular credencial
    path('credencial/desvincular/<str:tipo_servidor>/<int:servidor_pk>/<int:credencial_pk>/', views.desvincular_credencial, name='desvincular_credencial'),
]
