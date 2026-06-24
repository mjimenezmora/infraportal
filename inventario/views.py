from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from .utils import encriptar_password
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import csv
import io
# ==========================================
# SECCIÓN: DASHBOARD Y UTILERÍAS
# ==========================================
@login_required
def dashboard(request):
    '''
    Renderiza la página principal del panel de control.
    Protegido con @login_required para asegurar que solo usuarios autenticados entren.
    '''
    return render(request, 'inventario/dashboard.html')


def generar_password(request):
    """
    Herramienta administrativa para la generación de contraseñas seguras (Criptografía fuerte).
    Utiliza la librería 'secrets' de Python en lugar de 'random' para evitar patrones predecibles.
    """
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
# ==========================================
# SECCIÓN: GESTIÓN DE DIRECCIONES IP (MAPA DE RED)
# ==========================================
@login_required
def lista_ip(request):
    """
    Mapea dinámicamente un segmento de red clase C (.1 a .254) e identifica
    cuáles IPs están asignadas a servidores físicos o virtuales, y cuáles están libres.
    """
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
# ==========================================
# SECCIÓN: SERVIDORES VIRTUALES (CRUD)
# ==========================================

@login_required
def lista_virtuales(request):
    """
    Muestra el inventario de servidores virtuales permitiendo búsquedas cruzadas
    y filtros avanzados por Sedes, Hipervisores y Sistemas Operativos.
    """
    #  Dfinimos el Query inicial
    servidores = ServidorVirtual.objects.all()

    # Esta parte vamos a checar los permisos (A que grupo pertenecen)
    # IMPORTANTE : Debe coincidir igual que en el admin de django
    es_admin = request.user.groups.filter(name="Administradores").exists() or request.user.is_superuser

    # BARRA DE BUSQUEDA
    # Logica de filtos

    sede = request.GET.get("sede")
    hipervisor = request.GET.get("hipervisor")
    os = request.GET.get("os")

    if sede:
        servidores = servidores.filter(sede__id=sede)

    if hipervisor:
        servidores = servidores.filter(hipervisor__id=hipervisor)

    if os:
        servidores = servidores.filter(sistema_operativo__id=os)

    # Construccion del contexto unico
    
    context = {
        "servidores": servidores,
        "es_admin": es_admin,
        # pasamos los filtros actuales, para que los "select" mantengan la seleccion en el frontend
        "filtros": {
            "sede": sede,
            "hipervisor": hipervisor,
            "os": os,
        }
    }
    return render(request, "inventario/lista_virtuales.html", context)

# Detalles de virtuales

def detalle_virtual(request,pk):
    """
    Muestra la ficha técnica completa de un servidor virtual y sus credenciales de acceso.
    ¡CORREGIDO!: Se eliminó el bucle for que intentaba reescribir 'cred.password_plana'
    y causaba el AttributeError.
    """
    # Obtenemos el servidor o lanzamos un error 404 si no existe
    servidor=get_object_or_404(ServidorVirtual, pk=pk)

    # Obtenemos las credenciales relacionadas
    credenciales = servidor.credenciales.all()
    
    # Desencriptamos las contraseñas para que el admin las vea
    #for cred in credenciales:
        #try:
            # Las desencriptamos
            #cred.password_plana = desencripta_password(cred.password)
        #except:
            #cred.password_plana = "Error al desencriptar"

    # Aqui podrias cargar informacion adicional, por ejemplo, los servicios asociados
    # Servicios = servicios.servicios.all()

    context = {
        'servidor': servidor,
        'credenciales': credenciales,
        'es_admin': request.user.groups.filter(name="Administradores").exists() or request.user.is_superuser
    }
    return render(request, 'inventario/detalle_virtual.html', context)


@login_required
def agregar_credencial(request, tipo_servidor, pk):
    """
    Controlador adaptado para el esquema relacional Muchos a Muchos (ManyToManyField).
    Permite tanto reciclar una credencial existente como crear una nueva desde cero,
    enlazando de forma segura la relación sin duplicar registros.
    """
    servidor = None
    if tipo_servidor == 'virtual':
        servidor = get_object_or_404(ServidorVirtual, pk=pk)
    else:
        servidor = get_object_or_404(ServidorFisico, pk=pk)

    if request.method == 'POST':
        form = CredencialForm(request.POST)      
        if form.is_valid():
            # Ahora esto es una LISTA de credenciales seleccionadas
            credenciales_elegidas = form.cleaned_data.get('credencial_existente')
            
            # CASO A: El usuario seleccionó una o más credenciales existentes
            if credenciales_elegidas:
                for credencial in credenciales_elegidas: # Iteramos el llavero
                    if tipo_servidor == 'virtual':
                        credencial.servidor_virtual.add(servidor)
                    else:
                        credencial.servidor_fisico.add(servidor)
                
            # CASO B: El usuario decidió crear una credencial nueva desde cero
            else:
                credencial = form.save(commit=False)
                if not form.cleaned_data.get('usuario') or not form.cleaned_data.get('password'):
                    form.add_error(None, "Debe seleccionar al menos una credencial existente o rellenar los datos para una nueva.")
                    return render(request, 'inventario/form_credentials.html', {
                        'form': form, 'titulo': f"Agregar Credencial para {servidor.nombre}", 'boton_texto': "Guardar Credencial",
                        'credenciales_existentes': CredencialServidor.objects.all()
                    })
                
                credencial.save()
                if tipo_servidor == 'virtual':
                    credencial.servidor_virtual.add(servidor)
                else:
                    credencial.servidor_fisico.add(servidor)
            
            nombre_url = 'detalle_virtual' if tipo_servidor == 'virtual' else 'detalle_fisico'
            return redirect(nombre_url, pk=pk)
    else:
        form = CredencialForm()
        
    return render(request, 'inventario/form_credenciales.html', {
        'form': form,
        'titulo': f"Agregar Credencial para {servidor.nombre}",
        'boton_texto': "Guardar Credencial",
        'credenciales_existentes': CredencialServidor.objects.all(),
        'servidor': servidor,          # <--- VITAL
        'tipo_servidor': tipo_servidor,
    })

@login_required
def agregar_virtual(request):
    """
    Crea un nuevo servidor virtual en el inventario.
    """
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
    """
    Modifica la información técnica de un servidor existente.
    Implementa un middleware manual de seguridad a nivel de función para impedir accesos no autorizados.
    """
    # Verificación de seguridad a nivel de servidor
    if not request.user.groups.filter(name="Administradores").exists() and not request.user.is_superuser:
        return redirect("lista_virtuales")

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
    """
    Elimina permanentemente un servidor de la infraestructura (Solo Administradores).
    """
    if not request.user.groups.filter(name="Administradores").exists():
        return redirect("lista_virtuales")

    servidor = ServidorVirtual.objects.get(id=id)

    servidor.delete()

    return redirect("lista_virtuales")

# ==========================================================================
# SECCIÓN: SERVIDORES FÍSICOS - BARE METAL (CRUD)
# ==========================================================================

@login_required
def lista_fisicos(request):
    """
    Muestra el inventario de servidores físicos (Bare Metal) con soporte
    para búsquedas avanzadas y filtros cruzados por Sedes y Sistemas Operativos.
    """
    # Definimos el QuerySet inicial
    servidores = ServidorFisico.objects.all()

    # Validación de permisos para renderizado de botones administrativos
    es_admin = request.user.groups.filter(name="Administradores").exists() or request.user.is_superuser

    # Captura de parámetros GET para filtros desde el frontend
    sede = request.GET.get("sede")
    os = request.GET.get("os")
    q = request.GET.get("q") # Parametros de la barra de busqueda

    # Aplicacion de los filtros de catalogo
    if sede:
        servidores = servidores.filter(sede__id=sede)

    if os:
        servidores = servidores.filter(sistema_operativo__id=os)
    # Logica de bsuqeuda avanzada
    if q:
        servidores = servidores.filter(
            Q(nombre__icontains=q) |
            Q(ip_int__icontains=q) |
            Q(descripcion__icontains=q)
        )

    context = {
        "servidores": servidores,
        "es_admin": es_admin,
        "filtros": {
            "sede": sede,
            "os": os,
        }
    }
    return render(request, "inventario/lista_fisicos.html", context)


@login_required
def detalle_fisico(request, pk):
    """
    Muestra la ficha técnica detallada de un servidor físico (hardware, ubicación, red)
    así como el llavero de credenciales y accesos asociados a este equipo.
    """
    # Obtenemos la máquina física o disparamos un 404 seguro si no existe
    servidor = get_object_or_404(ServidorFisico, pk=pk)

    # Recuperamos las credenciales vinculadas mediante la relación Muchos a Muchos
    credenciales = servidor.credenciales.all()

    context = {
        'servidor': servidor,
        'credenciales': credenciales,
        'es_admin': request.user.groups.filter(name="Administradores").exists() or request.user.is_superuser
    }
    return render(request, 'inventario/detalle_fisico.html', context)


@login_required
def agregar_fisico(request):
    """
    Controlador para dar de alta un nuevo servidor físico (Bare Metal) en el inventario.
    """
    if request.method == "POST":
        form = ServidorFisicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_fisicos")
    else:
        form = ServidorFisicoForm()
    return render(request, "inventario/form_fisico.html", {"form": form})


@login_required
def editar_fisico(request, id):
    """
    Modifica la información técnica o de infraestructura de un servidor físico existente.
    Incluye protección explícita para evitar accesos no autorizados a nivel de vista.
    """
    # Middleware manual de seguridad por función
    if not request.user.groups.filter(name="Administradores").exists() and not request.user.is_superuser:
        return redirect("lista_fisicos")

    servidor = get_object_or_404(ServidorFisico, id=id)
    
    if request.method == "POST":
        form = ServidorFisicoForm(request.POST, instance=servidor)
        if form.is_valid():
            form.save()
            return redirect("lista_fisicos")
    else:
        form = ServidorFisicoForm(instance=servidor)
        
    return render(request, "inventario/form_fisico.html", {"form": form})


@login_required
def eliminar_fisico(request, id):
    """
    Elimina permanentemente una máquina física del inventario (Operación exclusiva de administradores).
    """
    if not request.user.groups.filter(name="Administradores").exists() and not request.user.is_superuser:
        return redirect("lista_fisicos")

    servidor = get_object_or_404(ServidorFisico, id=id)
    servidor.delete()

    return redirect("lista_fisicos")

# ==========================================================================
# SECCIÓN: SUBIR CSV - LLENAR LA BD MEDIANTE UN CSV
# ==========================================================================

# Para subir el CSV
@login_required
def subir_csv(request):
    """
    Procesador por lotes (BULK IMPORT) para cargar servidores masivamente desde archivos CSV.
    Ejecuta una lógica tipo UPSERT (Actualiza si existe, Crea si no existe).
    """
    if request.method == "POST":
        archivo = request.FILES.get('archivo')
        # Valdiacion de entrada, --- Muy IMPORTANTE
        if not archivo:
            return render(request, 'inventario/upload_csv.html', {
                'mensaje': 'No se seleccionó archivo, elige un archivo tipo CSV'
            })
        
        # Inicializacion de variables
        cont_creados = 0
        cont_actualizados = 0
        errores = []

        try:
            # Manejo del ENCODING (UTF-8 y latin-1 para Excel)
            data = archivo.read()
            try:
                decoded_file = data.decode('utf-8')
            except UnicodeDecodeError:
                decoded_file = data.decode('latin-1')

            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)

            # Procesamiento por fila
            # Usamos un contador manual para reporar la fila exacta, esto nos obliga a fuituro usar una plantilla

            fila_actual = 2

            for row in reader:
                try:
                    nombre_srv = row['nombre'].strip()
                    
                    # Búsqueda de relaciones (ForeignKeys)
                    sede = Sede.objects.filter(nombre=row['sede'].strip()).first()
                    hiper = Hipervisor.objects.filter(nombre=row['hipervisor'].strip()).first()
                    so = SistemaOperativo.objects.filter(nombre=row['sistema_operativo'].strip()).first()

                    # Validación de dependencias críticas, llenadas en otras tablas.
                    if not all([sede, hiper, so]):
                        faltantes = []
                        if not sede: faltantes.append(f"Sede '{row['sede']}'")
                        if not hiper: faltantes.append(f"Hipervisor '{row['hipervisor']}'")
                        if not so: faltantes.append(f"SO '{row['sistema_operativo']}'")
                        errores.append(f"Fila {fila_actual}: No se encontró {', '.join(faltantes)} en la base de datos.")
                        fila_actual += 1
                        continue

                    # LÓGICA DE ACTUALIZACIÓN O CREACIÓN (UPSERT)
                    obj, created = ServidorVirtual.objects.update_or_create(
                        nombre=nombre_srv, # Identificador único
                        defaults={
                            'ip_int': row['ip_int'].strip(),
                            'ip_ext': row.get('ip_ext', '').strip() or None,
                            'dns_int': row.get('dns_int', '').strip(),
                            'dns_ext': row.get('dns_ext', '').strip(),
                            'puertos_int': row.get('puertos_int', '').strip(),
                            'puertos_ext': row.get('puertos_ext', '').strip(),
                            'mac_addres': row.get('mac_addres', '').strip(),
                            'cpu': row['cpu'],
                            'memoria_ram': row['memoria_ram'],
                            'almacenamiento': row.get('almacenamiento', 0),
                            'descripcion': row.get('descripcion', '').strip(),
                            'sede': sede,
                            'hipervisor': hiper,
                            'sistema_operativo': so,
                        }
                    )

                    if created:
                        cont_creados += 1
                    else:
                        cont_actualizados += 1

                except KeyError as e:
                    errores.append(f"Fila {fila_actual}: Falta la columna obligatoria {str(e)}")
                except Exception as e:
                    errores.append(f"Fila {fila_actual}: Error inesperado: {str(e)}")
                
                fila_actual += 1

            # RESULTADO FINAL
            resumen = f"Proceso finalizado. Servidores creados: {cont_creados}. Servidores actualizados: {cont_actualizados}."
            if errores:
                resumen += f" Se detectaron {len(errores)} errores."

            return render(request, 'inventario/upload_csv.html', {
                'mensaje': resumen,
                'errores': errores[:10]  # Mostramos solo los primeros 10 errores para no saturar
            })

        except Exception as e:
            return render(request, 'inventario/upload_csv.html', {
                'mensaje': f'Error Crítico al procesar el archivo: {str(e)}'
            })

    # Si el método es GET, simplemente mostramos la página de carga
    return render(request, 'inventario/upload_csv.html')

# ==========================================================================
# SECCIÓN: AGREGAR SO - EN PAGINA DE SERVIDORES VIRTUALES
# ==========================================================================

@login_required
def agregar_so(request):
    """
    Permite el alta rápida de nuevos Sistemas Operativos en el catálogo.
    """
    if not request.user.groups.filter(name="Administradores").exists():
        return redirect('lista_virtuales')
    if request.method == "POST":
        form = SistemaOperativoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_virtuales')
    else:
        form = SistemaOperativoForm()
    return render(request, 'inventario/form_general.html', {'form':form, 'titulo':'Agregar Sistema Operativo'})

# ==========================================================================
# SECCIÓN: DESVINCULAR CREDENCIAL - EN PAGINA DE SERVIDORES VIRTUALES
# ==========================================================================

@login_required
def desvincular_credencial(request, tipo_servidor, servidor_pk, credencial_pk):
    """
    Rompe la relación Muchos a Muchos entre un servidor específico y una credencial,
    dejando intacta la credencial en la base de datos para otros servidores.
    """
    credencial = get_object_or_404(CredencialServidor, pk=credencial_pk)
    
    if tipo_servidor == 'virtual':
        servidor = get_object_or_404(ServidorVirtual, pk=servidor_pk)
        credencial.servidor_virtual.remove(servidor) # Rompe la unión en la tabla pívot
        return redirect('detalle_virtual', pk=servidor_pk)
    else:
        servidor = get_object_or_404(ServidorFisico, pk=servidor_pk)
        credencial.servidor_fisico.remove(servidor) # Rompe la unión en la tabla pívot
        return redirect('detalle_fisico', pk=servidor_pk)

"""
# Version vieja del codigo, borrar en futuro.
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
"""