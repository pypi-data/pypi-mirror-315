def main():

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

    #
    # 1. Realizar un programa que cree un directorio con el nombre2
    # Examen + Nombre Estudiante, el cual se debe de crear en la 
    # unidad C, es decir, en la raíz. A su vez el programa al crear 
    # el directorio debe de desplegar el mensaje “Directorio + nombre 
    # directorio creado exitosamente y en caso de error o que no se 
    # pudo crear desplegará el mensaje “Directorio + nombre estudiante 
    # no se pudo crear”. Valor 5 pts.
    #

    # Declarar directorio.
    directorio = "Examen Marcos Daniel Herrera Cervantes"

    # Detectar tipo de sistema operativo (Windows vs Linux).
    tipo_os = platform.system()
    if tipo_os == "Windows":
        ruta = f"C:\\{directorio}"
    else:  # Para MacOS y otros sistemas
        ruta = os.path.join(os.path.expanduser("~"), directorio)

    # Crear directorio tipo de sistema operativo (Windows vs Linux).
    try:
        os.makedirs(ruta)
        print()
        print(f"Directorio '{directorio}' creado exitosamente.")
        print()
    except Exception as error:
        print(f"Directorio {directorio} no se pudo crear. Error: {error}.")
        print()

    #
    # 2. Obtener la úl�ma hora del acceso a la ruta de la Carpeta 
    # creada en el punto anterior. # Valor 5 pts.
    #

    # Mostrar hora de ulimo acceso de directorio creado.
    try:
        ultima_acceso = os.path.getatime(ruta)
        print()
        print("Última hora de acceso:", time.ctime(ultima_acceso))
        print()
    except FileNotFoundError:
        print()
        print("La carpeta no existe.")
        print()

    #
    # 3. Un programa que mediante el uso del subprocess permita mediante
    # la opción de un menú abrir: el Notepad, la calculadora, Word, Excel
    # y Paint. Valor 15 pts.
    #

    # Función para abrir aplicaciones
    def abrir_aplicacion(opcion):
        sistema = platform.system()

        # Comandos para Windows
        aplicaciones_windows = {
            "1": "notepad",
            "2": "calc",
            "3": "winword",
            "4": "excel",
            "5": "mspaint",
            "6": "Teams",
            "7": "code"
        }

        # Comandos para MacOS
        aplicaciones_macos = {
            "1": "open -a 'TextEdit'",
            "2": "open -a 'Calculator'",
            "3": "open -a 'Microsoft Word'",
            "4": "open -a 'Microsoft Excel'",
            "5": "open -a 'Preview'",
            "6": "open -a 'Microsoft Teams'",
            "7": "open -a 'Visual Studio Code'"
        }

        # Selección de aplicaciones según el sistema operativo
        aplicaciones = aplicaciones_windows if sistema == "Windows" else aplicaciones_macos

        try:
            # Ejecutar el comando correspondiente
            if sistema == "Windows":
                subprocess.run(aplicaciones[opcion], check=True)
            else:  # MacOS
                subprocess.run(aplicaciones[opcion], shell=True, check=True)
        except KeyError:
            print("Opción inválida. Por favor, selecciona una opción válida del menú.")
        except FileNotFoundError:
            print("La aplicación seleccionada no está instalada o no se encuentra en el sistema.")
        except Exception as error:
            print(f"Error al intentar abrir la aplicación: {error}")

    # Menú interactivo
    menu = """
    Selecciona una aplicación para abrir:
    1. Editor de texto (Notepad o TextEdit)
    2. Calculadora
    3. Microsoft Word
    4. Microsoft Excel
    5. Paint (o Vista previa en MacOS)
    6. Microsoft Teams
    7. Visual Studio Code
    """
    print(menu)
    opcion = input("Opción: ")
    abrir_aplicacion(opcion)

    #
    # 4. Un programa que valide el ingreso de un nombre y apellido, número 
    # telefónico y de correo, si todos están correctos crear un archivo con 
    # el nombre “Datos Persona.txt”, este archivo se guardará en la carpeta 
    # creada en el punto número uno. Valor 15 pts.
    #

    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    telefono = input("Teléfono (8 dígitos): ")
    correo = input("Correo: ")

    def validar_datos(nombre, apellido, telefono, correo):
        if not re.match(r"^[a-zA-ZÀ-ÿ' -]+$", nombre) or not re.match(r"^[a-zA-ZÀ-ÿ' -]+$", apellido):
            return "Nombre o apellido inválido."
        if not re.match(r'^\d{8}$', telefono):
            return "Teléfono inválido."
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', correo):
            return "Correo electrónico inválido."
        return "OK"

    resultado = validar_datos(nombre, apellido, telefono, correo)
    if resultado == "OK":
        with open(os.path.join(ruta, "Datos Persona.txt"), "w") as archivo:
            archivo.write(f"Nombre: {nombre}\nApellido: {apellido}\nTeléfono: {telefono}\nCorreo: {correo}")
        print("Archivo creado exitosamente.")
    else:
        print(resultado)

    #
    # 5. En la carpeta creada en el punto uno, crear otra carpeta con el
    # nombre Entorno y dentro de esta realizar un entorno virtual que
    # efectué una pe�ción GET a la url = 
    # htps://es.wikipedia.org/w/api.php?ac�on=opensearch&search=
    # ython&limit=5&namespace= 0&format=json 
    # Valor 15 pts.
    #

    sistema = platform.system()
    entorno_path = os.path.join(ruta, "Entorno")

    # Crear carpeta y entorno virtual
    os.makedirs(entorno_path, exist_ok=True)

    if sistema == "Windows":
        subprocess.run(["python", "-m", "venv", os.path.join(entorno_path, "venv")])
    else:  # MacOS
        subprocess.run(["python3", "-m", "venv", os.path.join(entorno_path, "venv")])

    print(f"Entorno virtual creado en {entorno_path}")

    import requests

    url = "https://es.wikipedia.org/w/api.php?action=opensearch&search=Python&limit=5&namespace=0&format=json"
    response = requests.get(url)

    if response.status_code == 200:
        print(response.json())
    else:
        print("Error en la petición:", response.status_code)

    #
    # 6. Crear una carpeta con el nombre “asset” dentro de la carpeta
    # creada en el punto uno, dentro de la carpeta guardar una imagen
    # con el formato jpg. Luego crear un programa que en la imagen 
    # escriba o dibuje su nombre completo con la fecha de creación y 
    # luego que lo muestre. El tipo de fuente y tamaño de la letra la 
    # que guste. Valor 15 pts.
    #

    asset_path = os.path.join(ruta, "asset")
    os.makedirs(asset_path, exist_ok=True)

    url = "https://upload.wikimedia.org/wikipedia/commons/b/bf/Holly_the_Yorkshire_Terrier.jpg"
    response = requests.get(url)

    image_path = os.path.join(asset_path, "imagen.jpg")
    with open(image_path, "wb") as file:
        file.write(response.content)

    imagen = Image.open(image_path)

    draw = ImageDraw.Draw(imagen)
    font = ImageFont.truetype("Arial.ttf", 48)
    fecha = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    texto = f"{nombre} \n {apellido} \n {fecha}" 
    draw.text((50, 50), texto, fill="white", font=font)

    imagen.save(os.path.join(asset_path, "imagen_modificada.jpg"))
    imagen.show()
    #
    # 9. Graficar los datos de la tasa de mortalidad infantil, publicada
    # en la página oficial del INEC, cuya información la puede obtener 
    # del siguiente link: htps://inec.cr/indicadores/
    # tasa-mortalidad-infan�l Valor 10 pts.
    #

    años = [2018, 2019, 2020, 2021, 2022, 2023]
    tasa = [8.37, 8.25, 7.86, 8.68, 9.51, 9.06]

    plt.plot(años, tasa, marker='o')
    plt.title("Tasa de mortalidad infantil")
    plt.xlabel("Año")
    plt.ylabel("Tasa")
    plt.grid()

    # Guardar gráfica dependiendo del sistema operativo
    sistema = platform.system()
    output_path = os.path.join(ruta, "grafica.png")
    print("IMPORTANTE: Cierra la grafica para continuar con el programa! \n")
    plt.savefig(output_path)
    plt.show()

    print("Muchisimas gracias por el tiempo en pasarnos su conocimiento y expertise, Profe Larry! \n")

if __name__ == "__main__":
    main()