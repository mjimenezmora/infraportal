from django.db import models
from django.contrib.auth.models import User
from .utils import encriptar_password

# Create your models here.

### Normalizacion de tablas
##########################################

class Sede(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre
    
class Hipervisor(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre
    
class SistemaOperativo(models.Model):
    nombre = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

## Servidores Fisicos
######################################

class ServidorFisico(models.Model):

    service_tag=models.CharField(max_length=20, unique=True)
    nombre=models.CharField(max_length=120, unique=True)

    sistema_operativo=models.ForeignKey(
        SistemaOperativo,on_delete=models.SET_NULL,null=True
    )

    sede=models.ForeignKey(
        Sede,on_delete=models.SET_NULL, null=True
    )
    # Redes
    ip_int=models.GenericIPAddressField(null=True, blank=True)
    ip_ext=models.GenericIPAddressField(null=True, blank=True)
    # Caracteristicas tecnicas
    cpu=models.IntegerField(null=True, blank=True)
    memoria_ram=models.IntegerField(null=True, blank=True)
    almacenamiento=models.IntegerField(null=True, blank=True)
    # Campo de descripcion
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['service_tag']
    def __str__(self):
        return f"{self.nombre} ({self.service_tag})"

## Servidores virtuales
############################################

class ServidorVirtual(models.Model):
    
    nombre=models.CharField(max_length=120, unique=True)

    hipervisor = models.ForeignKey(
        Hipervisor, on_delete=models.SET_NULL, null=True
    )
    sistema_operativo = models.ForeignKey(
        SistemaOperativo, on_delete=models.SET_NULL, null=True
    )
    sede = models.ForeignKey(
        Sede, on_delete=models.SET_NULL, null=True
    )
    
    servidor_fisico=models.ForeignKey(
        ServidorFisico, on_delete=models.CASCADE, related_name="virtuales", null=True, blank=True
    )

    servicio = models.ForeignKey(
        Servicio, on_delete=models.SET_NULL, null=True, blank=True
    )
    # Area acargo del servidor
    a_cargo = models.CharField(max_length=50, blank=True)
    # Redes
    ip_int=models.GenericIPAddressField(null=True, blank=True)
    ip_ext=models.GenericIPAddressField(null=True, blank=True)
    dns_int=models.CharField(max_length=300, blank=True)
    dns_ext=models.CharField(max_length=300, blank=True)
    puertos_int=models.CharField(max_length=100, blank=True)
    puertos_ext=models.CharField(max_length=100, blank=True)
    mac_addres=models.CharField(max_length=20, blank=True)
    # Caracteristicas Tecnicas
    cpu = models.FloatField(null=True, blank=True)
    memoria_ram = models.FloatField(null=True, blank=True)
    almacenamiento = models.FloatField(null=True, blank=True)
    # Campo de Descripcion
    descripcion=models.TextField(blank=True)
    # Documento de resguardo del servidor
    documento=models.FileField(
        upload_to='documentos_servidores',
        null=True,
        blank=True
    )

    class Meta:
        ordering=['nombre']

    def __str__(self):
        return self.nombre
    
class TipoAcceso(models.Model):

    TIPOS=(
        ('SSH', 'SSH'),
        ('RDP', 'RDP'),
        ('BD', 'Base de datos'),
    )
    nombre=models.CharField(max_length=10, choices=TIPOS, unique=True)

    def __str__(self):
        return self.nombre
    
class UsuarioSistema(models.Model):
    nombre=models.CharField(max_length=50)
    password=models.TextField()

    def __str__(self):
        return self.nombre
       
    
class CredencialServidor(models.Model):
    
    # Relaciones (Una a una)
    servidor_virtual=models.ForeignKey(
        ServidorVirtual,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="credenciales"
    )

    servidor_fisico=models.ForeignKey(
        ServidorFisico,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="credenciales"
    )

    tipo_acceso=models.ForeignKey(
        TipoAcceso,
        on_delete=models.CASCADE,
        null=True,
        blank=True                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
    )
    def clean(self):
        from django.core.exceptions import ValidationError

        if not self.servidor_virtual and not self.servidor_fisico:
            raise ValidationError("Debe asignar un servidor")
        if self.servidor_virtual and self.servidor_fisico:
            raise ValidationError("Solo se puede asignar un tipo de servidor")
    usuario=models.CharField(max_length=50)
    password=models.TextField() #Se encripta el password
    puerto=models.IntegerField(null=True, blank=True)
    descripcion=models.CharField(max_length=100, blank=True)
    def save(self, *args, **kwargs):
        if not self.password.startswith("gAAAA"):
            self.password = encriptar_password(self.password)
        super().save(*args, **kwargs)
    def __str__(self):
        if self.servidor_virtual:
            return f"{self.usuario} ({self.tipo_acceso}) - {self.servidor_virtual.nombre}"
        elif self.servidor_fisico:
            return f"{self.usuario} ({self.tipo_acceso}) - {self.servidor_fisico.nombre}"
        return self.usuario




