import csv
from django.shortcuts import render, redirect
from django.contrib import admin, messages
from django.urls import path
from .models import *
from django import forms

# Formulario CSV
###################

class CSVUploadForm(forms.Form):
    file=forms.FileField()

# Credenciales INLINE
#####################

class CredencialInline(admin.TabularInline):
    model= CredencialServidor
    extra=1
    fk_name = "servidor_virtual"


# Admin de Servidor Virtual
#########################

@admin.register(ServidorVirtual)
class ServidoresVirtualesAdmin(admin.ModelAdmin):

    list_display = (
        'nombre',
        'hipervisor',
        'sistema_operativo',
        'sede',
        'ip_int',
        'cpu',
        'memoria_ram'
    )

    search_fields = (
        'nombre',
        'ip_int'
    )

    list_filter = (
        'hipervisor',
        'sede',
        'sistema_operativo'
    )

    ordering = ('nombre',)

    list_per_page = 40

    inlines=[CredencialInline]

    # Template
    change_list_template = "admin/csv_upload.html"

    # URL
    def get_urls(self):
        urls=super().get_urls()
        custom_urls = [
            path('upload-csv/', self.upload_csv),
        ]
        return custom_urls + urls
    
    # Funcion de carga
    
    def  upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["files"]
            decoded_files = csv_file.read().decode('utf-8').splitlines()
            reader=csv.DictReader(decoded_files)

            for row in reader:
                sede=Sede.objects.get(nombre=row['sede'])
                hipervisor=Hipervisor.objects.get(nombre=row['hipervizor'])
                os=SistemaOperativo.objects.get(nombre=row['sistema_operativo'])

                ServidorVirtual.objects.create(
                    nombre=row["nombre"],
                    ip_int=row["ip_int"],
                    cpu=row["cpu"],
                    memoria=row["memoria_ram"],
                    sede=sede,
                    hipervisor=hipervisor,
                    sistema_operativo=os
                )
            self.message_user(request, "Datos cargados correctamente")
            return redirect("..")
        form=CSVUploadForm()
        return render(request, "admin/upload_csv.html", {"form":form})
    
    #def ver_documento(self, obj):
    #    if obj.documento:
    #        return format_html(
    #            '<a href="{}" target="_blank">Ver archivo</a>',
    #            obj.documento.url
    #        )
    #    return "Sin archivo"


    #def save_model(self, request, obj, form, change):
    #    obj.save()
        

@admin.register(ServidorFisico)
class ServidoresFisicosAdmin(admin.ModelAdmin):

    list_display = (
        'service_tag',
        'nombre',
        'sistema_operativo',
        'sede',
        'ip_int',
        'cpu',
        'memoria_ram'
    )

    search_fields = (
        'nombre',
        'service_tag',
        'ip_int'
    )

    list_filter = (
        'sede',
        'sistema_operativo'
    )

    ordering = ('service_tag',)  # ✔ aquí sí existe

    list_per_page = 20

@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):
    search_fields=('nombre',)

@admin.register(Hipervisor)
class HipervisorAdmin(admin.ModelAdmin):
    search_fields=('nombre',)

@admin.register(SistemaOperativo)
class SistemaOperativoAdmin(admin.ModelAdmin):
    search_fields=('nombre',)

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    search_fields=('nombre',)



"""
@admin.register(usuariointerno)
class UsuarioInternoAdmin(admin.ModelAdmin):

    list_display = (
        'nombre_usuario',
        'nombre_interno',
        'rol'
    )

    search_fields = (
        'nombre_usuario',
        'nombre_interno'
    )

    list_filter = (
        'rol',
    )



@admin.register(contacto)
class ContactoAdmin(admin.ModelAdmin):

    list_display = (
        'nombre',
        'correo',
        'tipos_consulta'
    )

    search_fields = (
        'nombre',
        'correo'
    )

    list_filter = (
        'tipos_consulta',
    )
"""