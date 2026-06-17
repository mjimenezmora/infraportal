from django.db import models
from django.contrib.auth.models import User
from .utils import encriptar_password, desencriptar_password
from django.core.exceptions import ValidationError

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
    mac_addres=models.CharField(max_length=20, blank=True)
    ip_serv=models.GenericIPAddressField(null=True, blank=True)
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
"""    
class TipoAcceso(models.Model):

    TIPOS=(
        ('SSH', 'SSH'),
        ('RDP', 'RDP'),
        ('LOCAL', 'Local'),
        ('IMora', 'Dominio'),
        ('BD', 'Base de datos'),
    )
    nombre=models.CharField(max_length=10, choices=TIPOS, unique=True)

    def __str__(self):
        return self.nombre
"""    
class UsuarioSistema(models.Model):
    nombre=models.CharField(max_length=50)
    password=models.TextField()

    def __str__(self):
        return self.nombre
       
    
class CredencialServidor(models.Model):

    # La tupla de opciones, a manera estatica
    TIPOS_ACCESO = (
        ('SSH', 'SSH'),
        ('RDP', 'RDP'),
        ('LOCAL', 'Local'),
        ('IMORA', 'Dominio'),
        ('BD', 'Base de Datos'),
        ('PHPMYADMIN', 'phpMyAdmin'),
    )
    
    # Relaciones (muchas a muchas)
    servidor_virtual=models.ManyToManyField(
        ServidorVirtual,
        #on_delete=models.CASCADE,
        #null=True,
        blank=True,
        related_name="credenciales"
    )

    # Relaciones (muchas a muchas)
    servidor_fisico=models.ManyToManyField(
        ServidorFisico,
        #on_delete=models.CASCADE,
        #null=True,
        blank=True,
        related_name="credenciales"
    )

    tipo_acceso=models.CharField(
        max_length=30,
        choices=TIPOS_ACCESO,
        null=True,
        blank=True                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
    )
    # Parametros de la tabla
    usuario=models.CharField(max_length=50)
    password=models.TextField() #Se encripta el password
    puerto=models.IntegerField(null=True, blank=True)
    descripcion=models.CharField(max_length=100, blank=True)
    # Funciones para guardar y limpiar
    """
    # Funcion ya no requerida y necesaria para asignar servidor a fuerza
    def clean(self):
        if not self.servidor_virtual and not self.servidor_fisico:
            raise ValidationError("Debe asignar un servidor")
        if self.servidor_virtual and self.servidor_fisico:
            raise ValidationError("Solo se puede asignar un tipo de servidor")
    """    
    def save(self, *args, **kwargs):
        # Aseguramos que sea string antes de validar el prefijo gAAAA
        if self.password:
            password_str = str(self.password)
            if not password_str.startswith("gAAAA"):
                self.password = encriptar_password(password_str)
        super().save(*args, **kwargs)

    @property
    def password_plana(self):
        try:
            if self.password:
                password_str = str(self.password)
                if password_str.startswith("gAAAA"):
                    return desencriptar_password(password_str) # Ahora sí funcionará
                return password_str
            return self.password
        except Exception as e:
            # Puedes cambiar temporalmente esto por: return str(e) si quieres debuguear en pantalla
            return "Error al desencriptar"

    
    #Método __str__ adaptado para contar las relaciones
    def __str__(self):
        cant_virtuales = self.servidor_virtual.count()
        cant_fisicos = self.servidor_fisico.count()
        total_servidores = cant_virtuales + cant_fisicos
        
        return f"{self.usuario} ({self.get_tipo_acceso_display()}) - Asignado a {total_servidores} servidor(es)"
        
        """
        if self.servidor_virtual:
            return f"{self.usuario} ({self.tipo_acceso}) - {self.servidor_virtual.nombre}"
        elif self.servidor_fisico:
            return f"{self.usuario} ({self.tipo_acceso}) - {self.servidor_fisico.nombre}"
        return self.usuario
        """




