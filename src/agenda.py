"""
# TODO: (SI ME DA TIEMPO)comprobar si el numero al agregar contacto ya existe o no
# TODO: (SI MEDA TIEMPO) que al mostrar contacto por criterio si elije numero, mostrarlo si lo introduce con el +34 o no, mostrarlo igualemnte

27/11/2023

Práctica del examen para realizar en casa
-----------------------------------------

* El programa debe estar correctamente documentado.

* Debes intentar ajustarte lo máximo que puedas a lo que se pide en los comentarios TODO.

* Tienes libertad para desarrollar los métodos o funciones que consideres, pero estás obligado a usar como mínimo todos los que se solicitan en los comentarios TODO.

* Además, tu programa deberá pasar correctamente las pruebas unitarias que se adjuntan en el fichero test_agenda.py, por lo que estás obligado a desarrollar los métodos que se importan y prueban en la misma: pedir_email(), validar_email() y validar_telefono()

"""

import os
import pathlib
from os import path
import copy

# Constantes globales
RUTA = pathlib.Path(__file__).parent.absolute() 

NOMBRE_FICHERO = 'contactos.csv'

RUTA_FICHERO = path.join(RUTA, NOMBRE_FICHERO)

#TODO: Crear un conjunto con las posibles opciones del menú de la agenda
OPCIONES_MENU = {1, 2, 3, 4, 5, 6, 7, 8}
#TODO: Utiliza este conjunto en las funciones agenda() y pedir_opcion()


def borrar_consola():
    """ Limpia la consola
    """
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")


def pulse_tecla_para_continuar():
    """ Muestra un mensaje y realiza una pausa hasta que se pulse una tecla
    """
    print("\n")
    os.system("pause")


def mostrar_menu():
    """Muestra las opciones de la agenda"""
    print("AGENDA")
    print("------")
    print("1. Nuevo contacto")
    print("2. Modificar contacto")
    print("3. Eliminar contacto")
    print("4. Vaciar agenda")
    print("5. Cargar agenda inicial")
    print("6. Mostrar contactos por criterio")
    print("7. Mostrar la agenda completa")
    print("8. Salir")


def pedir_opcion():
    opcion_bien = False
    while not opcion_bien:
        try:
            opcion = int(input("Elije una opcion: "))
            if opcion in OPCIONES_MENU:
                return opcion 
            else:
                print("Elije opcion correcta (1-8)")

        except ValueError:
            print("Debes ingresar valor numerico (1-8))")


def agenda(contactos: list):
    """ Ejecuta el menú de la agenda con varias opciones
    ...
    """
    #TODO: Crear un bucle para mostrar el menú y ejecutar las funciones necesarias según la opción seleccionada...
    opcion = 0
    while opcion != 8:
        mostrar_menu()
        opcion = pedir_opcion()

        #TODO: Se valorará que utilices la diferencia simétrica de conjuntos para comprobar que la opción es un número entero del 1 al 7

        if opcion == 1:
            agregar_contacto(contactos)
        elif opcion == 2:
            email = input("Introduce email de contacto a modificar: ")
            modificar_contacto(contactos, email)   
        elif opcion == 3:
            email = input("Introduce email de contacto a eliminar: ")
            eliminar_contacto(contactos, email)
        elif opcion == 4:
            vaciar_agenda(contactos)
        elif opcion == 5:
            cargar_contactos(contactos)
        elif opcion == 6:
            mostrar_contactos_criterio(contactos)
        elif opcion == 7:
            mostrar_contactos(contactos)


def pedir_nombre():
    nombre_ok = False
    while not nombre_ok:
        try:
            nombre = input("Nombre: ").title().strip()
            validar_nombre(nombre)
            if " " in nombre:
                nombre = formatear_espacios(nombre)
            return nombre
        except ValueError as e:
            print("Error " + str(e))


def formatear_espacios(cadena):
    
    palabras = cadena.split(" ")
    cadena_sin_espacio = list((palabra for palabra in palabras if palabra != "" ))
    cadena_nueva = " ".join(cadena_sin_espacio)

    return cadena_nueva


def validar_nombre(nombre):
    if nombre == "":
        raise ValueError("Nombre incorrecto")



def pedir_apellido():
    apelllido_bien = False
    while not apelllido_bien:
        try:
            apellido = input("Apellido: ").title().strip()
            validar_apellido(apellido)
            return apellido
        except ValueError:
            print("**Error**")
        except Exception:
            print("**error**")


def validar_apellido(apellido):
    if apellido == '':
        raise ValueError("Apellido incorrecto")



def pedir_email(contactos):
    email_bien = False
    while not email_bien:
        try:
            email = input("Email: ").strip()

            validar_email(email, contactos)
            return email
        except ValueError:
            print("**Error**")
            continue
        except Exception:
            print("**error**")


def validar_email(email:str, contactos:list): 
    if email.lower() in (correo["email"].lower() for correo in contactos):
        raise ValueError("el email ya existe en la agenda")
    
    if email.strip() == '':
        raise ValueError("el email no puede ser una cadena vacía")
    
    if "@" not in email:
        raise ValueError("el email no es un correo válido")
    
    if " " in email:
        raise ValueError("el email no puede tener espacios")


def pedir_telefonos() -> list:
    telefono_bien = False
    lista_telefonos = []
    while not telefono_bien:
        try:
            telefono = input("Introduce telefonos (enter vacio para parar): ").strip().replace(" ", "")

            if telefono == '':
                telefono_bien = True
                return lista_telefonos
            
            if validar_telefono(telefono):
                lista_telefonos.append(telefono)
        except ValueError:
            print("**Error**")
        except Exception:
            print("**error**")


def validar_telefono(telefono):
    """
    Comprueba que el telefono este correctamente puesto
    """
    if (len(telefono) == 9 and not telefono.isdigit()) or (telefono[:3] == "+34" and not telefono[3:12].isdigit()):
        raise ValueError("Debes introducir caracteres numericos")
    
    if len(telefono) > 9:
        if telefono[-12:-9] == "+34":
            return True
        else:
            raise ValueError("Numero debe contener 9 digitos y opcionalmente un prefijo +34")
    else:
        if len(telefono) < 9:
            raise ValueError("Numero debe contener 9 digitos y opcionalmente un prefijo +34")
    
    return True



def agregar_contacto(contactos:list):
    """
    Añade un contacto a la lista con los valores introducidos
    """
    print("Datos a introducir")
    print("-----------------")
    nombre = pedir_nombre()
    apellido = pedir_apellido()
    email = pedir_email(contactos)
    telefonos = pedir_telefonos()

    contactos.append(dict([("nombre", nombre), ("apellido", apellido), ("email", email), ("telefonos", telefonos) ]))
    print("Contacto añadido correctamente")


def modificar_contacto(contactos:list, email):
    """
    Modifica el contacto que le des
    """
    try:
        pos = buscar_contacto(contactos, email)
        if pos != None:
            print("Introduce nuevos datos para el contacto ")
            introducir_nuevos_datos(contactos, pos)
            print("Se modificó 1 contacto")
        else:
            print("No se encontró el contacto para modificar")
    except Exception :
            print("**Error**")
            print("No se eliminó ningún contacto")


def introducir_nuevos_datos(contactos, pos):
    """
    Introduce los nuevos contactos
    """
    nombre = pedir_nombre()
    apellido = pedir_apellido()
    email = pedir_email(contactos)
    telefonos = pedir_telefonos()

    contactos[pos] = dict([ ("nombre", nombre), ("apellido", apellido), ("email", email), ("telefonos", telefonos) ])


def buscar_contacto(contactos:list, email:str):
    """
    Busca la posicion de un contacto en la lista, a partir de su email 
    """
    for contacto in range(len(contactos)):
        if contactos[contacto]["email"] == email:
            return contacto
    
    return None


def eliminar_contacto(contactos: list, email:str):
    """ 
    Elimina un contacto de la agenda utilizando un correo
    """
    try:
        pos = buscar_contacto(contactos, email)

        if pos != None:
            del contactos[pos]
            print("Se eliminó 1 contacto")
        else:
            print("No se encontró el contacto para eliminar")
    except Exception:
        print("**Error**")
        print("No se eliminó ningún contacto")


def vaciar_agenda(contactos:list):
    """
    Vacia la agenda
    """
    contactos.clear()
    print("Agenda vaciada correctamente")


def cargar_contactos(contactos: list):
    """ 
    Carga los contactos iniciales de la agenda desde un fichero y los añade a una lista
    """
    #TODO: Controlar los posibles problemas derivados del uso de ficheros...

    with open(RUTA_FICHERO, 'r') as fichero:
        for linea in fichero:
            # .strip() para eliminar espacios y que no aparezca /n
            datos = linea.strip().split(";")
            contactos.append(dict([ ("nombre", datos[0]), ("apellido", datos[1]), ("email", datos[2]), ("telefonos", datos[3:]) ]))



def mostrar_contactos_criterio(contactos:list):
    """
    Muestra todos los datos de el contacto deseado, segun el criterio elegido
    """
    criterio = input("Mediante que criterio de busqueda quieres idetificar al contacto (nombre,apellido,email,telefono): ").lower().strip().replace(" ", "")

    while criterio not in {"nombre", "apellido", "email", "telefono"}:
        criterio = input("Debe elejir un criterio correcto (nombre,apellido,email,telefono): ").lower().strip().replace(" ", "")

    valor_criterio = input(f"Introduce {criterio}: ").title()
    cont = 0
    for contacto in range(len(contactos)):
        if criterio == "telefono":
            for numero in contactos[contacto]["telefonos"]:
                if numero == valor_criterio.lower():
                    imprimir_contacto_criterio([contactos[contacto]], criterio, valor_criterio, cont)
                    cont +=1
        else: 
            if contactos[contacto][criterio] == valor_criterio.lower():
                imprimir_contacto_criterio([contactos[contacto]], criterio, valor_criterio, cont)
                cont+=1
    if cont == 0:
        print(f"No hay ningun {criterio} -> {valor_criterio}")



def imprimir_contacto_criterio(contactos:list, criterio, valor_criterio, cont):
    """
    Comprueba si tiene telefono, si no tiene no le damos valor, per si tiene, formateamos el telefono en caso necesario y comprobamos si tiene uno o más
    """
    if cont == 0 :
        print(f"Contactos con el criterio '{criterio}' y valor '{valor_criterio}'")
    print("---------------------------------------------")
    for contacto in contactos:
        nombre = contacto["nombre"]
        apellido = contacto["apellido"]
        email = contacto["email"]
        telefonos = contacto["telefonos"]
    if not telefonos:
        msgTelefonos = "Ninguno"
    else:
        contacto["telefonos"] = list(formatearTelefono(telefono) for telefono in telefonos) 
        
        if len(telefonos) > 1:
            msgTelefonos =  " / ".join(map(str, contacto["telefonos"]))
        else:
            msgTelefonos = contacto["telefonos"][0]
    print(f"Nombre: {nombre} {apellido} ({email})\nTeléfonos: {msgTelefonos}")



def formatearTelefono(telefono:str):
    """
    Comrpueba si el telefono tiene prefijo y le añade un guion para separar el prefijo y el numero

    """
    if len(telefono) > 9:
        telefono = telefono[:-9] + "-" + telefono[-9:]
    return telefono


def mostrar_contactos(contactos: list):
    """
    Muestra de forma visual la lista de contactos ordenados por nombre y su informacion.
    """
    contactosOrdenados = copy.deepcopy(contactos)
    contactosOrdenados.sort(key=lambda nom: nom["nombre"])

    print(f"AGENDA ({len(contactos)})\n------")
    for contacto in contactosOrdenados:
        nombre = contacto["nombre"]
        apellido = contacto["apellido"]
        email = contacto["email"]
        telefonos = contacto["telefonos"]
        if not telefonos:
            msgTelefonos = "Ninguno"
        else:
            contacto["telefonos"] = list(formatearTelefono(telefono) for telefono in telefonos) 
            
            if len(telefonos) > 1:
                msgTelefonos =  " / ".join(map(str, contacto["telefonos"]))
            else:
                msgTelefonos = contacto["telefonos"][0]

        print(f"Nombre: {nombre} {apellido} ({email})\nTeléfonos: {msgTelefonos}")
        print("......")
        


def main():
    """ 
    Función principal del programa
    """
    borrar_consola()

    #TODO --: Asignar una estructura de datos vacía para trabajar con la agenda

    contactos = []

    #TODO --: Modificar la función cargar_contactos para que almacene todos los contactos del fichero en una lista con un diccionario por contacto (claves: nombre, apellido, email y telefonos)
    #TODO --: Realizar una llamada a la función cargar_contacto con todo lo necesario para que funcione correctamente.

    cargar_contactos(contactos)
    print(contactos)
    
    

    #TODO: Crear función para agregar un contacto. Debes tener en cuenta lo siguiente:
    # - El nombre y apellido no pueden ser una cadena vacía o solo espacios y se guardarán con la primera letra mayúscula y el resto minúsculas (ojo a los nombre compuestos)
    # - El email debe ser único en la lista de contactos, no puede ser una cadena vacía y debe contener el carácter @.
    # - El email se guardará tal cuál el usuario lo introduzca, con las mayúsculas y minúsculas que escriba. 
    #  (CORREO@gmail.com se considera el mismo email que correo@gmail.com)
    # - Pedir teléfonos hasta que el usuario introduzca una cadena vacía, es decir, que pulse la tecla <ENTER> sin introducir nada.
    # - Un teléfono debe estar compuesto solo por 9 números, aunque debe permitirse que se introduzcan espacios entre los números.
    # - Además, un número de teléfono puede incluir de manera opcional un prefijo +34.
    # - De igual manera, aunque existan espacios entre el prefijo y los 9 números al introducirlo, debe almacenarse sin espacios.
    # - Por ejemplo, será posible introducir el número +34 600 100 100, pero guardará +34600100100 y cuando se muestren los contactos, el telófono se mostrará como +34-600100100. 
    #TODO: Realizar una llamada a la función agregar_contacto con todo lo necesario para que funcione correctamente.

    agregar_contacto(contactos)

    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Realizar una llamada a la función eliminar_contacto con todo lo necesario para que funcione correctamente, eliminando el contacto con el email rciruelo@gmail.com
    eliminar_contacto(contactos, "emailcualquiera@gmail.com")

    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO --: Crear función mostrar_contactos para que muestre todos los contactos de la agenda con el siguiente formato:
    # ** IMPORTANTE: debe mostrarlos ordenados según el nombre, pero no modificar la lista de contactos de la agenda original **
    #
    # AGENDA (6)
    # ------
    # Nombre: Antonio Amargo (aamargo@gmail.com)
    # Teléfonos: niguno
    # ......
    # Nombre: Daniela Alba (danalba@gmail.com)
    # Teléfonos: +34-600606060 / +34-670898934
    # ......
    # Nombre: Laura Iglesias (liglesias@gmail.com)
    # Teléfonos: 666777333 / 666888555 / 607889988
    # ......
    # ** resto de contactos **
    #
    #TODO --: Realizar una llamada a la función mostrar_contactos con todo lo necesario para que funcione correctamente.

    mostrar_contactos(contactos)

    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Crear un menú para gestionar la agenda con las funciones previamente desarrolladas y las nuevas que necesitéis:
    # AGENDA
    # ------
    # 1. Nuevo contacto
    # 2. Modificar contacto
    # 3. Eliminar contacto
    # 4. Vaciar agenda
    # 5. Cargar agenda inicial
    # 6. Mostrar contactos por criterio
    # 7. Mostrar la agenda completa
    # 8. Salir
    #
    # >> Seleccione una opción: 
    #
    #TODO: Para la opción 3, modificar un contacto, deberás desarrollar las funciones necesarias para actualizar la información de un contacto.
    #TODO: También deberás desarrollar la opción 6 que deberá preguntar por el criterio de búsqueda (nombre, apellido, email o telefono) y el valor a buscar para mostrar los contactos que encuentre en la agenda.

    agenda(contactos)


if __name__ == "__main__":
    main()