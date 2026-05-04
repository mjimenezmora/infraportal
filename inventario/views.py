from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from .utils import encriptar_password
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import csv
# Create your views here.


# las rutas del dashboard
@login_required
def dashboard(request):
    return render(request, 'inventario/dashboard.html')


def generar_password(request):
    import secrets
    import string

    lista_passwords = []
    form = PasswordGen()

    if request.method == 'POST':
        form = PasswordGen(request.POST)
        if form.is_valid():
            no_contra = form.cleaned_data['numero']
            lon_contra = form.cleaned_data['longitud']
            out_caracter = form.cleaned_data['caracter'] or ""

            # Definimos el set de caracteres (letras + números + puntuación común)
            # Evitamos usar todo string.printable porque incluye espacios y saltos de línea
            caracteres_base = string.ascii_letters + string.digits + string.punctuation
            full_caracter = "".join([c for c in caracteres_base if c not in out_caracter])

            for _ in range(no_contra):
                # Generamos una contraseña usando secrets para alta seguridad
                passw = "".join(secrets.choice(full_caracter) for _ in range(lon_contra))
                lista_passwords.append(passw)

    return render(request, 'inventario/passwgen/password_gen.html', {
        'form': form,
        'passwords': lista_passwords
    })

@login_required
def lista_ip(request):
    # Definimos el rango del segmento.
    segmentos_validos = ["10.1.238.", "10.1.239.", "10.1.240.", "10.1.241."] # nuestros segmentos validos de IPs

    # 2. Obtenemos el segmento seleccionado (por defecto el primero de la lista)

    prefijo = request.GET.get('segmento')
    if prefijo not in segmentos_validos:
        prefijo = segmentos_validos[0]

    # El rago de las IPs van de .1 a .254        
    rango_ips = range(1,255)
    

    # 3. Traemos datos NOTA: Filtramos en la BD por el prefijo para no traer miles de registros 
    ips_fisicas=ServidorFisico.objects.filter(ip_int__startswith=prefijo).values('ip_int', 'nombre', 'descripcion')
    ips_virtuales=ServidorVirtual.objects.filter(ip_int__startswith=prefijo).values('ip_int', 'nombre', 'descripcion')

    ocupadas={}
    for s in ips_fisicas:
        ocupadas[s['ip_int']]={'nombre':s['nombre'], 'tipo':'Fisico', 'desc': s['descripcion']}
    for s in ips_virtuales:
        ocupadas[s['ip_int']]={'nombre':s['nombre'], 'tipo':'Fisico', 'desc': s['descripcion']}

    # 4. Construimos la lista final para el template

    mapa_red = []
    for i in rango_ips:
        ip_completa = f"{prefijo}{i}"
        info = ocupadas.get(ip_completa)
        mapa_red.append({
            'ip':ip_completa,
            'estado': 'ocupado' if info else 'libre',
            'detalle': info
        })

    return render(request, 'inventario/ip/ips.html', {
        'mapa_red': mapa_red,
        'segmentos':segmentos_validos,
        "segmentos_activo":prefijo
        })

# Servidores Virtuales

@login_required
def lista_virtuales(request):

    servidores = ServidorVirtual.objects.all()
    es_admin = ServidorVirtual.objects.all()

    es_admin = request.user.groups.filter(name="Administradores").exists()

    context = {
        "servidores": servidores,
        "es_admin": es_admin
    }


    sede = request.GET.get("sede")
    hipervisor = request.GET.get("hipervisor")
    os = request.GET.get("os")

    if sede:
        servidores = servidores.filter(Sede=sede)

    if hipervisor:
        servidores = servidores.filter(Hipervizor=hipervisor)

    if os:
        servidores = servidores.filter(O_S=os)

    return render(request, "inventario/lista_virtuales.html", {
        "servidores": servidores
    })

@login_required
def agregar_virtual(request):
    if request.method == "POST":
        form = ServidorVirtualForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_virtuales")
    else:
        form = ServidorVirtualForm()
    return render(request, "inventario/form_virtual.html", {"form": form})

@login_required
def editar_virtual(request, id):
    servidor = get_object_or_404(ServidorVirtual, id=id)
    if request.method == "POST":
        form = ServidorVirtualForm(request.POST, instance=servidor)
        if form.is_valid():
            form.save()
            return redirect("lista_virtuales")
    else:
        form = ServidorVirtualForm(instance=servidor)
    return render(request, "inventario/form_virtual.html", {"form": form})

@login_required
def eliminar_virtual(request, id):

    if not request.user.groups.filter(name="Administradores").exists():
        return redirect("lista_virtuales")

    servidor = ServidorVirtual.objects.get(id=id)

    servidor.delete()

    return redirect("lista_virtuales")

# Servidores Fisicos

@login_required
def lista_fisicos(request):
    return render(request, 'lista_fisicos.html')

# Para subir el CSV

def subir_csv(request):
    if request.method == "POST":
        archivo = request.FILES.get('archivo')

        if not archivo:
            return render(request, 'inventario/upload_csv.html', {
                'mensaje': 'No se seleccionó archivo'
            })

        try:
            decoded_file = archivo.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:

                # Obtener relaciones
                sede = Sede.objects.get(nombre=row['sede'])
                hipervisor = Hipervisor.objects.get(nombre=row['hipervisor'])
                sistema = SistemaOperativo.objects.get(nombre=row['sistema_operativo'])

                # Crear servidor
                ServidorVirtual.objects.create(
                    nombre=row['nombre'],
                    ip_int=row['ip_int'],
                    cpu=row['cpu'],
                    memoria_ram=row['memoria_ram'],
                    almacenamiento=row.get('almacenamiento', 0),
                    sede=sede,
                    hipervisor=hipervisor,
                    sistema_operativo=sistema
                )

            return render(request, 'inventario/upload_csv.html', {
                'mensaje': 'Archivo cargado correctamente'
            })

        except Exception as e:
            return render(request, 'inventario/upload_csv.html', {
                'mensaje': f'Error: {str(e)}'
            })

    return render(request, 'inventario/upload_csv.html')
    #equipos = Servidores_Virtuales.objects.all()
    #context = {
    #    "Servidores Vituales": Servidores_Virtuales
    #}
    #return render(request, "inventario/lista_equipos.html", context) #por que funciono?