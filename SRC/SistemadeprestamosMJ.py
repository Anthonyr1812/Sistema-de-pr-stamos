# Sistema de Gestión de Préstamos en Python


## main.py

import os
import csv
import re
from datetime import datetime, timedelta

# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================

USUARIOS_FILE = "usuarios.txt"
ARTICULOS_FILE = "articulos.txt"
PRESTAMOS_FILE = "prestamos.txt"
DEVOLUCIONES_FILE = "devoluciones.txt"
VENTAS_FILE = "ventas.txt"

ADMIN_USER = "admin"
ADMIN_PASS = "1234"

CATEGORIAS = [
    "videojuego",
    "libro",
    "musica y video",
    "herramientas",
    "dinero",
    "miscelaneo",
    "varios"
]

# ==========================================
# CREAR ARCHIVOS SI NO EXISTEN
# ==========================================

archivos = [
    USUARIOS_FILE,
    ARTICULOS_FILE,
    PRESTAMOS_FILE,
    DEVOLUCIONES_FILE,
    VENTAS_FILE
]

for archivo in archivos:
    if not os.path.exists(archivo):
        open(archivo, "w", encoding="utf-8").close()

if not os.path.exists("certificados"):
    os.mkdir("certificados")

if not os.path.exists("facturas"):
    os.mkdir("facturas")

if not os.path.exists("exportaciones"):
    os.mkdir("exportaciones")

# ==========================================
# VALIDACIONES
# ==========================================


def validar_nombre(nombre):
    return nombre.isalpha() and len(nombre) >= 3



def validar_documento(doc):
    return doc.isdigit() and 3 <= len(doc) <= 15



def validar_correo(correo):
    patron = r'^[\w\.-]+@[\w\.-]+\.com$'
    return re.match(patron, correo)



def validar_categoria(categoria):
    return categoria.lower() in CATEGORIAS



def generar_id_articulo(categoria, numero):
    prefijo = categoria[:3].upper()
    return f"{prefijo}{numero}"


# ==========================================
# FUNCIONES DE ARCHIVOS
# ==========================================


def leer_archivo(nombre_archivo):
    datos = []

    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            datos.append(linea.strip().split("|"))

    return datos



def escribir_archivo(nombre_archivo, datos):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        for dato in datos:
            archivo.write("|".join(dato) + "\n")


# ==========================================
# REGISTRAR USUARIO
# ==========================================


def registrar_usuario():
    print("\n=== REGISTRO DE USUARIO ===")

    nombre = input("Nombre: ")
    while not validar_nombre(nombre):
        print("Nombre inválido")
        nombre = input("Nombre: ")

    apellido = input("Apellido: ")
    while not validar_nombre(apellido):
        print("Apellido inválido")
        apellido = input("Apellido: ")

    documento = input("Documento: ")
    while not validar_documento(documento):
        print("Documento inválido")
        documento = input("Documento: ")

    correo = input("Correo: ")
    while not validar_correo(correo):
        print("Correo inválido")
        correo = input("Correo: ")

    print("\nTiempo préstamo")
    print("1. 5 días")
    print("2. 10 días")
    print("3. 15 días")
    print("4. 30 días")

    opcion = input("Seleccione: ")

    tiempos = {
        "1": "5",
        "2": "10",
        "3": "15",
        "4": "30"
    }

    tiempo = tiempos.get(opcion)

    if not tiempo:
        print("Opción inválida")
        return

    fecha = datetime.now().strftime("%Y-%m-%d")

    with open(USUARIOS_FILE, "a", encoding="utf-8") as archivo:
        archivo.write(f"{nombre}|{apellido}|{documento}|{correo}|{tiempo}|{fecha}\n")

    print("Usuario registrado correctamente")


# ==========================================
# REGISTRAR ARTÍCULO
# ==========================================


def registrar_articulo():
    print("\n=== REGISTRO DE ARTÍCULO ===")

    nombre = input("Nombre artículo: ")

    while len(nombre) < 3:
        print("Nombre inválido")
        nombre = input("Nombre artículo: ")

    print("\nCategorías disponibles:")

    for categoria in CATEGORIAS:
        print("-", categoria)

    categoria = input("Categoría: ").lower()

    while not validar_categoria(categoria):
        print("Categoría inválida")
        categoria = input("Categoría: ").lower()

    precio = input("Precio compra: ")

    while not precio.isdigit():
        print("Precio inválido")
        precio = input("Precio compra: ")

    articulos = leer_archivo(ARTICULOS_FILE)

    numero = len(articulos) + 1

    articulo_id = generar_id_articulo(categoria, numero)

    estado = "1"

    with open(ARTICULOS_FILE, "a", encoding="utf-8") as archivo:
        archivo.write(
            f"{articulo_id}|{nombre}|{categoria}|{precio}|{estado}\n"
        )

    print("Artículo registrado correctamente")
    print("ID:", articulo_id)


# ==========================================
# BUSCAR USUARIO
# ==========================================


def buscar_usuario(documento):
    usuarios = leer_archivo(USUARIOS_FILE)

    for usuario in usuarios:
        if usuario[2] == documento:
            return usuario

    return None


# ==========================================
# BUSCAR ARTÍCULO
# ==========================================


def buscar_articulo(articulo_id):
    articulos = leer_archivo(ARTICULOS_FILE)

    for articulo in articulos:
        if articulo[0] == articulo_id:
            return articulo

    return None


# ==========================================
# REGISTRAR PRÉSTAMO
# ==========================================


def registrar_prestamo():
    print("\n=== REGISTRAR PRÉSTAMO ===")

    documento = input("Documento usuario: ")

    usuario = buscar_usuario(documento)

    if not usuario:
        print("Usuario no existe")
        print("MJ debe registrar el usuario")
        return

    articulo_id = input("ID artículo: ")

    articulo = buscar_articulo(articulo_id)

    if not articulo:
        print("Artículo no existe")
        return

    if articulo[4] == "0":
        print("Artículo no disponible")
        return

    fecha_prestamo = datetime.now()

    dias = int(usuario[4])

    fecha_limite = fecha_prestamo + timedelta(days=dias)

    with open(PRESTAMOS_FILE, "a", encoding="utf-8") as archivo:
        archivo.write(
            f"{documento}|{articulo_id}|{fecha_prestamo.strftime('%Y-%m-%d')}|{fecha_limite.strftime('%Y-%m-%d')}|activo\n"
        )

    articulos = leer_archivo(ARTICULOS_FILE)

    for articulo_lista in articulos:
        if articulo_lista[0] == articulo_id:
            articulo_lista[4] = "0"

    escribir_archivo(ARTICULOS_FILE, articulos)

    print("Préstamo registrado correctamente")


# ==========================================
# REGISTRAR DEVOLUCIÓN
# ==========================================


def registrar_devolucion():
    print("\n=== DEVOLUCIÓN ===")

    documento = input("Documento usuario: ")

    prestamos = leer_archivo(PRESTAMOS_FILE)

    activos = []

    for prestamo in prestamos:
        if prestamo[0] == documento and prestamo[4] == "activo":
            activos.append(prestamo)

    if len(activos) == 0:
        print("No tiene préstamos activos")
        return

    for i, prestamo in enumerate(activos):
        print(i + 1, prestamo)

    opcion = int(input("Seleccione préstamo: ")) - 1

    prestamo = activos[opcion]

    fecha_actual = datetime.now()
    fecha_limite = datetime.strptime(prestamo[3], "%Y-%m-%d")

    if fecha_actual > fecha_limite:
        generar_venta(prestamo)
        return

    for p in prestamos:
        if p == prestamo:
            p[4] = "devuelto"

    escribir_archivo(PRESTAMOS_FILE, prestamos)

    articulos = leer_archivo(ARTICULOS_FILE)

    for articulo in articulos:
        if articulo[0] == prestamo[1]:
            articulo[4] = "1"

    escribir_archivo(ARTICULOS_FILE, articulos)

    with open(DEVOLUCIONES_FILE, "a", encoding="utf-8") as archivo:
        archivo.write(
            f"{prestamo[0]}|{prestamo[1]}|{fecha_actual.strftime('%Y-%m-%d')}\n"
        )

    generar_certificado(prestamo)

    print("Devolución registrada")


# ==========================================
# CERTIFICADO
# ==========================================


def generar_certificado(prestamo):
    nombre_archivo = (
        f"certificados/{prestamo[0]}_{prestamo[1]}.txt"
    )

    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("CERTIFICADO DE DEVOLUCIÓN\n")
        archivo.write("============================\n")
        archivo.write(f"Usuario: {prestamo[0]}\n")
        archivo.write(f"Artículo: {prestamo[1]}\n")
        archivo.write(
            f"Fecha devolución: {datetime.now().strftime('%Y-%m-%d')}\n"
        )


# ==========================================
# GENERAR VENTA
# ==========================================


def generar_venta(prestamo):
    articulo = buscar_articulo(prestamo[1])

    precio = float(articulo[3])

    impuesto = precio * 0.23

    total = precio + impuesto

    with open(VENTAS_FILE, "a", encoding="utf-8") as archivo:
        archivo.write(
            f"{prestamo[0]}|{prestamo[1]}|{precio}|{impuesto}|{total}\n"
        )

    nombre_archivo = (
        f"facturas/{prestamo[0]}_{prestamo[1]}.txt"
    )

    with open(nombre_archivo, "w", encoding="utf-8") as factura:
        factura.write("FACTURA DE VENTA\n")
        factura.write("=========================\n")
        factura.write("Motivo: Incumplimiento devolución\n")
        factura.write(f"Usuario: {prestamo[0]}\n")
        factura.write(f"Artículo: {prestamo[1]}\n")
        factura.write(f"Subtotal: {precio}\n")
        factura.write(f"Impuesto 23%: {impuesto}\n")
        factura.write(f"TOTAL: {total}\n")

    print("Artículo vendido automáticamente")


# ==========================================
# CONSULTAR MÁS DE 30 DÍAS
# ==========================================


def consultar_mas_30_dias():
    prestamos = leer_archivo(PRESTAMOS_FILE)

    print("\n=== MÁS DE 30 DÍAS ===")

    for prestamo in prestamos:
        fecha = datetime.strptime(prestamo[2], "%Y-%m-%d")

        diferencia = (datetime.now() - fecha).days

        if diferencia > 30 and prestamo[4] == "activo":
            print(prestamo)


# ==========================================
# ESTADO GENERAL
# ==========================================


def estado_general():
    prestamos = leer_archivo(PRESTAMOS_FILE)

    lista = []

    for prestamo in prestamos:
        fecha = datetime.strptime(prestamo[2], "%Y-%m-%d")

        dias = (datetime.now() - fecha).days

        lista.append((dias, prestamo))

    lista.sort(reverse=True)

    print("\n=== ESTADO GENERAL ===")

    for item in lista:
        print(f"Días: {item[0]} -> {item[1]}")


# ==========================================
# EXPORTAR CSV
# ==========================================


def exportar_csv(nombre_txt, nombre_csv):
    datos = leer_archivo(nombre_txt)

    with open(nombre_csv, "w", newline="", encoding="utf-8") as archivo_csv:
        writer = csv.writer(archivo_csv)

        for fila in datos:
            writer.writerow(fila)

    print("Exportación completada")


# ==========================================
# ADMINISTRADOR
# ==========================================


def administrador():
    print("\n=== LOGIN ADMIN ===")

    usuario = input("Usuario: ")
    clave = input("Contraseña: ")

    if usuario != ADMIN_USER or clave != ADMIN_PASS:
        print("Acceso denegado")
        return

    prestamos = leer_archivo(PRESTAMOS_FILE)
    devoluciones = leer_archivo(DEVOLUCIONES_FILE)
    ventas = leer_archivo(VENTAS_FILE)
    usuarios = leer_archivo(USUARIOS_FILE)

    total_pago = 0

    for venta in ventas:
        total_pago += float(venta[4])

    contador = {}

    for prestamo in prestamos:
        documento = prestamo[0]

        if documento not in contador:
            contador[documento] = 0

        contador[documento] += 1

    mayor = max(contador, key=contador.get) if contador else "N/A"
    menor = min(contador, key=contador.get) if contador else "N/A"

    print("\n=== REPORTE ADMIN ===")
    print("Total préstamos:", len(prestamos))
    print("Total devoluciones:", len(devoluciones))
    print("Total ventas:", len(ventas))
    print("Total pagos:", total_pago)
    print("Usuarios registrados:", len(usuarios))
    print("Mayor préstamos:", mayor)
    print("Menor préstamos:", menor)


# ==========================================
# MENÚ PRINCIPAL
# ==========================================


def menu():
    while True:
        print("\n================================")
        print(" SISTEMA DE PRÉSTAMOS MJ ")
        print("================================")
        print("1. Registrar usuario")
        print("2. Registrar artículo")
        print("3. Registrar préstamo")
        print("4. Registrar devolución")
        print("5. Consultar más de 30 días")
        print("6. Estado general")
        print("7. Exportar CSV")
        print("8. Administrador")
        print("9. Salir")

        opcion = input("Seleccione: ")

        if opcion == "1":
            registrar_usuario()

        elif opcion == "2":
            registrar_articulo()

        elif opcion == "3":
            registrar_prestamo()

        elif opcion == "4":
            registrar_devolucion()

        elif opcion == "5":
            consultar_mas_30_dias()

        elif opcion == "6":
            estado_general()

        elif opcion == "7":
            exportar_csv(PRESTAMOS_FILE, "exportaciones/prestamos.csv")

        elif opcion == "8":
            administrador()

        elif opcion == "9":
            print("Gracias por usar el sistema")
            break

        else:
            print("Opción inválida")


# ==========================================
# INICIO DEL SISTEMA
# ==========================================

menu()