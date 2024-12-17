# Importar modulos.
import os
import platform
import platform
from funciones import punto_1, punto_2, punto_3, punto_4, punto_5, punto_6, punto_7, punto_9, continuar

#######################################################################
#######################################################################

def main():
    """
    Academia de Tecnología – Universidad de Costa Rica
    Programación con Python Nivel 2 Inst. Larry Mayorga (XII-2024)

    Proyecto - Evaluación. Valor total 100 pts 30%.
    Nota: enviar en una carpeta comprimida con nombre y apellidos, 
    los códigos fuentes que se solicitan a continuación:

    Objetvo: Evaluar los conocimientos adquiridos en el curso en la
    realizar de los siguientes códigos:

    1. Realizar un programa que cree un directorio con el nombre Examen 
    + Nombre Estudiante, el cual se debe de crear en la unidad C, 
    es decir, en la raíz. A su vez el programa al crear el directorio 
    debe de desplegar el mensaje “Directorio + nombre directorio creado
    exitosamente y en caso de error o que no se pudo crear desplegará el
    mensaje “Directorio + nombre estudiante no se pudo crear”. Valor 5 pts.

    2. Obtener la última hora del acceso a la ruta de la Carpeta creada en 
    el punto anterior. Valor 5 pts.

    3. Un programa que mediante el uso del subprocess permita mediante la 
    opción de un menú abrir: el Notepad, la calculadora, Word, Excel y 
    Paint. Valor 15 pts.

    4. Un programa que valide el ingreso de un nombre y apellidos, número 
    telefónico y de email, si todos están correctos crear un archivo con 
    el nombre “Datos Persona.txt”, este archivo se guardará en la carpeta 
    creada en el punto número uno. Valor 15 pts.

    5. En la carpeta creada en el punto uno, crear otra carpeta con el 
    nombre Entorno y dentro de esta realizar un entorno virtual que 
    efectué una petición GET a la url_imagen_descargar = htps://es.wikipedia.org/w/
    api.php?ac�on=opensearch&search=Python&limit=5&namespace=0&format=json. 
    Valor 15 pts.

    6. Crear una carpeta con el nombre “asset” dentro de la carpeta creada 
    en el punto uno, dentro de la carpeta guardar una imagen con el formato 
    jpg. Luego crear un programa que en la imagen escriba o dibuje su nombre 
    completo con la fecha de creación y luego que lo muestre. El �po de fuente 
    y tamaño de la letra la que guste. Valor 15 pts.

    7. Realizar un scrapy de la Tenda Universal del apartado 
    “juegos de mesas.” Valor 10 pts.

    8. De los programas creados anteriormente escoger uno y aplicar 
    el “Docstring” y posterior crear un paquete instalable y portable. 
    Valor 10 pts.

    9. Graficar los datos de la tasa de mortalidad infan�l, publicada en 
    la página oficial del INEC, cuya información la puede obtener del 
    siguiente link: htps://inec.cr/indicadores/tasa-mortalidad-infantil. 
    Valor 10 pts.
    """

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

print( """
#######################################################################
# 1. Realizar un programa que cree un directorio con el nombre        #
# Examen + Nombre Estudiante, el cual se debe de crear en la          #
# unidad C, es decir, en la raíz. A su vez el programa al crear       #
# el directorio debe de desplegar el mensaje “Directorio + nombre     #
# directorio creado exitosamente y en caso de error o que no se       #
# pudo crear desplegará el mensaje “Directorio + nombre estudiante    #
# no se pudo crear”. Valor 5 pts.                                     #
#######################################################################
""")

punto_1()

continuar()

#######################################################################
#######################################################################

print("""
#######################################################################
# 2. Obtener la última hora del acceso a la ruta de la Carpeta        #
# creada en el punto anterior. # Valor 5 pts.                         #
#######################################################################
""")

punto_2()

continuar()

#######################################################################
#######################################################################

print("""
#######################################################################
# 3. Un programa que mediante el uso del subprocess permita mediante  #
# la opción de un menú abrir: el Notepad, la calculadora, Word, Excel #
# y Paint. Valor 15 pts.                                              #
#######################################################################
""")
    
punto_3()

continuar()

#######################################################################
#######################################################################

print("""
#######################################################################
# 4. Un programa que valide el ingreso de un nombre y apellido,       #
# número telefónico y de correo, si todos están correctos crear un    #
# archivo con el nombre “Datos Persona.txt”, este archivo se guardará #
# en la carpeta creada en el punto número uno. Valor 15 pts.          #
#######################################################################
""")

punto_4(ruta)

continuar()

#######################################################################
#######################################################################

print("""
#######################################################################
# 5. En la carpeta creada en el punto uno, crear otra carpeta con el  #
# nombre Entorno y dentro de esta realizar un entorno virtual que     #
# efectué una petición GET a la url_imagen_descargar =                #
# htps://es.wikipedia.org/w/api.php?ac�on=opensearch&search=          #
# ython&limit=5&namespace= 0&format=json                              #
# Valor 15 pts.                                                       #
#######################################################################
""")
    
punto_5()

continuar()

#######################################################################
#######################################################################

print("""
#######################################################################
# 6. Crear una carpeta con el nombre “asset” dentro de la carpeta     #
# creada en el punto uno, dentro de la carpeta guardar una imagen     #
# con el formato jpg. Luego crear un programa que en la imagen        #
# escriba o dibuje su nombre completo con la fecha de creación y      #
# luego que lo muestre. El tipo de fuente y tamaño de la letra la     #
# que guste. Valor 15 pts.                                            #
#######################################################################
""")

punto_6()

continuar()

#######################################################################
#######################################################################

print("""
#######################################################################
# 7. Realizar un scrapy. Valor 10 pts.                                #
#######################################################################
""")

punto_7(ruta)

continuar()

#######################################################################
#######################################################################

print("""     
########################################################################
# 9. Graficar los datos de la tasa de mortalidad infantil, publicada   #
# # en la página oficial del INEC, cuya información la puede obtener   #
# del siguiente link: htps://inec.cr/indicadores/                      #
# tasa-mortalidad-infan�l Valor 10 pts.                                #
########################################################################
""")

punto_9()

continuar()

#######################################################################
#######################################################################

if __name__ == "__main__":
    main()