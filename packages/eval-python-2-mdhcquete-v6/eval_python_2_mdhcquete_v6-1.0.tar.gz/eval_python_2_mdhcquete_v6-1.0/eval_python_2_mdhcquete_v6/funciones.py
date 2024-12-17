# Importar modulos.
import os
import platform
import time
import subprocess
import platform
import re
from PIL import Image, ImageDraw, ImageFont
import requests
import time
import matplotlib.pyplot as plt

#######################################################################
#######################################################################

# Declarar directorio.
directorio = "Examen Marcos Daniel Herrera Cervantes"

# Detectar tipo de sistema operativo (Windows vs Linux).
tipo_os = platform.system()
if tipo_os == "Windows":
    ruta = f"C:\\{directorio}"
else:  # Para MacOS y otros sistemas
    ruta = os.path.join(os.path.expanduser("~"), directorio)

#######################################################################
#######################################################################

def continuar():
    """
    La funcion 'continuar' se usa para que el usuaro explicitamente
    tenga que presonar Enter (o cualquier tecla, de hecho) para
    continuar con el programa.
    """
    input("\nPresiona Enter para continuar.")

#######################################################################
#######################################################################

def punto_1():
    """
    #
    # 1. Realizar un programa que cree un directorio con el nombre2
    # Examen + Nombre Estudiante, el cual se debe de crear en la 
    # unidad C, es decir, en la raíz. A su vez el programa al crear 
    # el directorio debe de desplegar el mensaje “Directorio + nombre 
    # directorio creado exitosamente y en caso de error o que no se 
    # pudo crear desplegará el mensaje “Directorio + nombre estudiante 
    # no se pudo crear”. Valor 5 pts.
    #
    """
    # Crear directorio tipo de sistema operativo (Windows vs Linux).
    try:
        os.makedirs(ruta)
        print()
        print(f"El directorio '{directorio}' ha sido creado exitosamente.")
        return ruta
    except Exception as error:
        print()
        print(f"ERROR: El directorio {directorio} no se pudo crear: {error}.")
        return ruta

#######################################################################
#######################################################################

def punto_2():
    """
    #
    # 2. Obtener la úl�ma hora del acceso a la ruta de la Carpeta 
    # creada en el punto anterior. # Valor 5 pts.
    #
    """

    #
    # Mostrar hora de ulimo acceso de directorio creado.
    #
    try:
        ultima_acceso = os.path.getatime(ruta)
        print()
        print(f"Última hora de acceso de '{ruta}':", time.ctime(ultima_acceso))
    except FileNotFoundError:
        print()
        print("ERROR: El directorio no existe.")

#######################################################################
#######################################################################

def punto_3():
    """
    #
    # 3. Un programa que mediante el uso del subprocess permita mediante
    # la opción de un menú abrir: el Notepad, la calculadora, Word, Excel
    # y Paint. Valor 15 pts.
    #
    """

    #
    # Comandos a correr para Windows.
    #
    aplicaciones_windows = {
        "1": "notepad",
        "2": "calc",
        "3": "winword",
        "4": "excel",
        "5": "mspaint",
        "6": "code"
    }

    #
    # Comandos a correr para macOS.
    #
    aplicaciones_macos = {
        "1": "open -a 'TextEdit'",
        "2": "open -a 'Calculator'",
        "3": "open -a 'Microsoft Word'",
        "4": "open -a 'Microsoft Excel'",
        "5": "open -a 'Preview'",
        "6": "open -a 'Visual Studio Code'"
    }

    #
    # Selección de comandos a correr según el sistema operativo.
    #
    aplicaciones = aplicaciones_windows if tipo_os == "Windows" else aplicaciones_macos

    #
    # Menú interactivo mostrado al usuario para escoger aplicacion para abrir.
    #
    menu = """
    Selecciona una aplicación para abrir:
    1. Editor de texto (Notepad o TextEdit)
    2. Calculadora
    3. Microsoft Word
    4. Microsoft Excel
    5. Paint (o Vista previa en MacOS)
    6. Visual Studio Code
    """

    #
    # Abrir applicacion escogida por el usuario.
    #
    while True:
        print(menu)
        opcion = input("Aplicación escogida (1-7): ")

        if opcion not in aplicaciones:
            print("\nLa opcion escogida es invalida. Por favor escoger "
                    "alguna de las opciones validas del menu. \n.")
            continue
        try:
            if tipo_os == "Windows":
                subprocess.run(aplicaciones[opcion], check=True)
            else:
                subprocess.run(aplicaciones[opcion], shell=True, 
                                check=True)
            break
        except Exception as error:
            print(f"Error al intentar abrir la aplicación: {error}")

#######################################################################
#######################################################################

def punto_4(ruta):
    while True:
        nombre = input("Nombre: ")
        apellidos = input("Apellidos: ")
        telefono = input("Teléfono (8 dígitos): ").replace(" ", "")
        email = input("Email: ")

        # Validación simple de los datos
        if not re.match(r"^[a-zA-ZÀ-ÿ' -]+$", nombre) or not re.match(r"^[a-zA-ZÀ-ÿ' -]+$", apellidos):
            print("Nombre o apellidos inválidos.")
            continue
        if not re.match(r'^\d{8}$', telefono):
            print("Teléfono inválido.")
            continue
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            print("Email inválido.")
            continue

        # Si todos los datos son válidos, guardamos en el archivo
        with open(os.path.join(ruta, "Datos Persona.txt"), "w") as archivo:
            archivo.write(f"Nombre: {nombre}\n")
            archivo.write(f"Apellidos: {apellidos}\n")
            archivo.write(f"Teléfono: {telefono}\n")
            archivo.write(f"Email: {email}\n")
        print(f"\n El archivo con tu infomacion personal ha sido creado exitosamente en {ruta}.")
        break

#######################################################################
#######################################################################

def punto_5():

    ruta_entorno = os.path.join(ruta, "Entorno")

    # Crear carpeta y entorno virtual
    os.makedirs(ruta_entorno, exist_ok=True)

    if tipo_os == "Windows":
        subprocess.run(["python", "-m", "venv", os.path.join(ruta_entorno, "venv")])
    else:
        subprocess.run(["python3", "-m", "venv", os.path.join(ruta_entorno, "venv")])

    print(f"El entorno virtual ha sido creado exitosamente en {ruta_entorno}\n")

    url_imagen_descargar = "https://es.wikipedia.org/w/api.php?action=opensearch&search=Python&limit=5&namespace=0&format=json"

    response = requests.get(url_imagen_descargar)

    print(response.json())

#######################################################################
#######################################################################

def punto_6():
    """
    #######################################################################
    # 6. Crear una carpeta con el nombre “asset” dentro de la carpeta     #
    # creada en el punto uno, dentro de la carpeta guardar una imagen     #
    # con el formato jpg. Luego crear un programa que en la imagen        #
    # escriba o dibuje su nombre completo con la fecha de creación y      #
    # luego que lo muestre. El tipo de fuente y tamaño de la letra la     #
    # que guste. Valor 15 pts.                                            #
    #######################################################################
    """
    #
    # crear directorio asset
    #
    ruta_directorio_asset = os.path.join(ruta, "asset")
    os.makedirs(ruta_directorio_asset, exist_ok=True)

    #
    # descargar imagen desde internet 
    #
    url_imagen_descargar = "https://upload.wikimedia.org/wikipedia/commons/b/bf/Holly_the_Yorkshire_Terrier.jpg"
    imagen_respuesta = requests.get(url_imagen_descargar)
    imagen_ruta = os.path.join(ruta_directorio_asset, "imagen.jpg")
    with open(imagen_ruta, "wb") as file:
        file.write(imagen_respuesta.content)

    #
    # modificar imagen descargada y salvar/mostrar modificacion
    #
    imagen = Image.open(imagen_ruta)

    draw = ImageDraw.Draw(imagen)
    font = ImageFont.load_default(size=48)
    fecha = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    texto = f"Marcos Daniel \n Herrera Cervantes \n {fecha}" 
    draw.text((50, 50), texto, fill="white", font=font)

    imagen.save(os.path.join(ruta_directorio_asset, "imagen_modificada.jpg"))
    imagen.show()

    print(f"Imagen original y modificada salvadas en {imagen_ruta}.")

#######################################################################
#######################################################################

def punto_7(ruta):
    """
    #######################################################################
    # 7. Realizar un scrapy. Valor 10 pts.                                #
    #######################################################################
    """

    #
    # Cambiar directorio al directorio inicial.
    #
    os.chdir(ruta)

    #
    # Crear el proyecto de scrapy.
    #
    if not os.path.exists("scraper_citas_famosas"):
        subprocess.run(["scrapy", "startproject", "scraper_citas_famosas"], 
                       check=True)

    #
    # Crear el código del spider.
    #
    spider_code = '''
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("span small::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
'''

    # Guardar el código del spider en la ubicación correcta.
    ruta_spider = os.path.join("scraper_citas_famosas", 
                               "scraper_citas_famosas", "spiders", 
                               "spider_citas_famosas.py")
    with open(ruta_spider, "w") as f:
        f.write(spider_code)

    #  Cambiar el directorio de trabajo al directorio del 
    # proyecto Scrapy
    os.chdir('scraper_citas_famosas')

    # Ejecutar el spider y guardar el archivo JSON en la ruta 
    # proporcionada
    subprocess.run(["scrapy", "crawl", "quotes", "-o", 
                    os.path.join(ruta, "citas_famosas.json")], check=True)

    print(f"\nEl spider ha sido ejecutado exitosamente y los datos recogidos "
        f"han sido guardados en {os.path.join(ruta, 'citas_famosas.json')}")
        
#######################################################################
#######################################################################

def punto_9():
    """     
    ########################################################################
    # 9. Graficar los datos de la tasa de mortalidad infantil, publicada   #
    # # en la página oficial del INEC, cuya información la puede obtener   #
    # del siguiente link: htps://inec.cr/indicadores/                      #
    # tasa-mortalidad-infan�l Valor 10 pts.                                #
    ########################################################################
    """

    años = [2018, 2019, 2020, 2021, 2022, 2023]
    tasa = [8.37, 8.25, 7.86, 8.68, 9.51, 9.06]

    plt.plot(años, tasa, marker='o')
    plt.title("Tasa de mortalidad infantil INEC")
    plt.xlabel("Año")
    plt.ylabel("Tasa")
    plt.grid()

    # Guardar gráfica dependiendo del sistema operativo
    ruta_repositorio = os.path.join(ruta, "grafica.png")
    print("IMPORTANTE: Por favor cierra la grafica para continuar "
            "con el programa. Gracias! \n")
    plt.savefig(ruta_repositorio)
    plt.show()

#######################################################################
#######################################################################