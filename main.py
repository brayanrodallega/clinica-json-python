from datetime import datetime, date
import os
import json


archivo_pacientes = "pacientes.json"
archivo_profesionales = "profesionales.json"


def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)


def registrar_paciente():
    with open(archivo_pacientes, 'r') as archivo:
        datos = json.load(archivo)
        datos[0]["contador"] += 1
        id = datos[0]["contador"]
        nombre = input('Nombre del paciente: ')
        apellido = input('Apellido del paciente: ')
        documento = input('Documento del paciente: ')
        nacimiento = input('Fecha de nacimiento del paciente: ')
        nacionalidad = input('Nacionalidad del paciente: ')
        paciente = {
            "id": id,
            "nombre": nombre,
            "apellido": apellido,
            "documento": documento,
            "nacimiento": nacimiento,
            "nacionalidad": nacionalidad
        }
        escribir_paciente_json(paciente, datos)


def escribir_paciente_json(paciente, datos):
    with open(archivo_pacientes, 'r+') as archivo:
        datos = datos
        datos[0]["pacientes"].append(paciente)
        archivo.seek(0)
        json.dump(datos, archivo)


def editar_paciente_json(datos):
    with open(archivo_pacientes, 'w') as archivo:
        json.dump(datos, archivo)


def editar_paciente():
    esta = False
    documento = input(f'''
        ---------MODIFICAR PACIENTE---------

        Digite el documento del paciente ha modificar
        Documento: ''')

    with open(archivo_pacientes, 'r') as archivo:
        datos = json.load(archivo)
        for count, paciente in enumerate(datos[0]['pacientes']):
            if paciente["documento"] == documento:
                esta = True
                opcion = int(input(f'''
            Que desea modificar?
            1. Nombre
            2. Apellido
            3. Documento
            4. Fecha de nacimiento
            5. Nacionalidad
            6. Historia Clinica
            Opcion: '''))

                if opcion == 1:
                    clearConsole()
                    nombre = input('Digite el nuevo nombre: ')
                    datos[0]['pacientes'][count]['nombre'] = nombre
                    editar_paciente_json(datos)
                    print('El cambio fué exitoso!')
                    break
                elif opcion == 2:
                    clearConsole()
                    apellido = input('Digite el nuevo apellido: ')
                    datos[0]['pacientes'][count]['apellido'] = apellido
                    editar_paciente_json(datos)
                    print('El cambio fué exitoso!')
                    break
                elif opcion == 3:
                    clearConsole()
                    documento = input('Digite el nuevo documento: ')
                    datos[0]['pacientes'][count]['documento'] = documento
                    editar_paciente_json(datos)
                    print('El cambio fué exitoso!')
                    break
                elif opcion == 4:
                    clearConsole()
                    nacimiento = input('Digite la nueva fecha de nacimiento: ')
                    datos[0]['pacientes'][count]['nacimiento'] = nacimiento
                    editar_paciente_json(datos)
                    print('El cambio fué exitoso!')
                    break
                elif opcion == 5:
                    clearConsole()
                    nacionalidad = input('Digite la nueva nacionalidad: ')
                    datos[0]['pacientes'][count]['nacionalidad'] = nacionalidad
                    editar_paciente_json(datos)
                    print('El cambio fué exitoso!')
                    break
                elif opcion == 6 and "historiaClinica" in datos[0]['pacientes'][count]:
                    clearConsole()
                    opcion2 = int(input(f'''
            Que desea modificar?
            1. Fecha de historia clinica
            2. Enfermedad
            3. Medico
            Opcion: '''))
                    if opcion2 == 1:
                        clearConsole()
                        fecha = input('Digite la nueva fecha: ')
                        datos[0]['pacientes'][count]['historiaClinica']['fecha'] = fecha
                        editar_paciente_json(datos)
                        print('El cambio fué exitoso!')
                        break
                    elif opcion2 == 2:
                        clearConsole()
                        enfermedad = input('Escriba la nueva enfermedad: ')
                        datos[0]['pacientes'][count]['historiaClinica']['enfermedad'] = enfermedad
                        editar_paciente_json(datos)
                        print('El cambio fué exitoso!')
                        break
                    elif opcion2 == 3:
                        clearConsole()
                        medico = input('Escribe el nombre del nuevo medico: ')
                        datos[0]['pacientes'][count]['historiaClinica']['medico'] = medico
                        editar_paciente_json(datos)
                        print('El cambio fué exitoso!')
                        break
                    else:
                        print('Numero incorrecto!')
                        break
                elif not ("historiaClinica" in datos[0]['pacientes'][count]):
                    print('El paciente no tiene historial clinico')
                else:
                    print('Numero incorrecto!')
                    break
        if not esta:
            print('El paciente no se encuentra registrado!')


def eliminar_un_paciente():
    documento = input(f'''
        ---------ELIMINAR PACIENTE---------

        Digite el documento del paciente ha eliminar
        Documento: ''')

    with open(archivo_pacientes, 'r') as archivo:
        datos = json.load(archivo)
        for paciente in datos[0]['pacientes']:
            if paciente['documento'] == documento:
                datos[0]['pacientes'].remove(paciente)
                editar_paciente_json(datos)
                print('Paciente eliminado!')
                break
            else:
                print('El paciente no se encuentra registrado!')


def agregar_historia_clinica():
    esta = False
    documento = input(f'''
        ---------AGREGAR HISTORIA CLINICA A PACIENTE---------

        Digite el documento del paciente
        Documento: ''')

    with open(archivo_pacientes, 'r') as archivo:
        datos = json.load(archivo)
        for count, paciente in enumerate(datos[0]['pacientes']):
            if paciente["documento"] == documento:
                esta = True
                enfermedad = input('Escriba la enfermedad: ')
                medico = input('Escriba el nombre del medico: ')
                fecha = str(datetime.today().strftime('%d/%m/%Y'))
                datos[0]['pacientes'][count]["historiaClinica"] = {
                    "fecha": fecha,
                    "enfermedad": enfermedad,
                    "medico": medico
                }
                editar_paciente_json(datos)
        if not esta:
            print('El paciente no se encuentra registrado!')


def calculateAge(birthDate):
    today = date.today()
    age = today.year - birthDate.year - \
          ((today.month, today.day) < (birthDate.month, birthDate.day))

    return age


def listar_pacientes():
    with open(archivo_pacientes, 'r') as archivo:
        datos = json.load(archivo)
        if len(datos):
            for paciente in datos[0]["pacientes"]:
                fecha = paciente['nacimiento'].split('/')
                edad = calculateAge(date(int(fecha[2]), int(fecha[1]), int(fecha[0])))
                print(f'''
                    ----------INFO PACIENTE----------
                    Paciente id: #{paciente['id']}
                    Nombre: {paciente['nombre']}
                    Apellido: {paciente['apellido']}
                    Edad: {edad} años
                    Documento: {paciente['documento']}
                    Fecha de nacimiento: {paciente['nacimiento']}
                    Nacionalidad: {paciente['nacionalidad']}''')
                if "historiaClinica" in paciente:
                    print(f'''
                    ----------INFO HISTORIAL MEDICO----------
                    Paciente id: #{paciente['id']}
                    Fecha: {paciente['historiaClinica']['fecha']}
                    Enfermedad: {paciente['historiaClinica']['enfermedad']}
                    Medico: {paciente['historiaClinica']['medico']}
                    ''')
                else:
                    print(f'''
                    ----------INFO HISTORIAL MEDICO----------
                    El paciente no tiene historia medica
                    ''')

        else:
            print('La lista esta vacia')


def buscar_paciente_documento():
    esta = False
    documento = input(f'''
        ---------BUSCAR PACIENTE---------

        Digite el documento del paciente ha buscar
        Documento: ''')

    with open(archivo_pacientes, 'r') as archivo:
        datos = json.load(archivo)
        for paciente in datos[0]['pacientes']:
            if paciente["documento"] == documento:
                esta = True
                fecha = paciente['nacimiento'].split('/')
                edad = calculateAge(date(int(fecha[2]), int(fecha[1]), int(fecha[0])))
                print(f'''
                    ----------INFO PACIENTE----------
                    Paciente id: #{paciente['id']}
                    Nombre: {paciente['nombre']}
                    Apellido: {paciente['apellido']}
                    Edad: {edad} años
                    Documento: {paciente['documento']}
                    Fecha de nacimiento: {paciente['nacimiento']}
                    Nacionalidad: {paciente['nacionalidad']}
                ''')
                if "historiaClinica" in paciente:
                    print(f'''
                    ----------INFO HISTORIAL MEDICO----------
                    Paciente id: #{paciente['id']}
                    Fecha: {paciente['historiaClinica']['fecha']}
                    Enfermedad: {paciente['historiaClinica']['enfermedad']}
                    Medico: {paciente['historiaClinica']['medico']}
                    ''')
                else:
                    print(f'''
                    ----------INFO HISTORIAL MEDICO----------
                    El paciente no tiene historia medica
                    ''')
                break

        if not esta:
            print('El paciente no se encuentra registrado!')


def registrar_medico():
    with open(archivo_profesionales, 'r') as archivo:
        datos = json.load(archivo)
        datos[0]['contador'] += 1
        id = datos[0]['contador']
        nombre = input('Escriba el nombre del medico: ')
        apellido = input('Escriba el apellido: ')
        especialidad = input('Escriba la especialidad: ')
        profesional = {
            "id": id,
            "nombre": nombre,
            "apellido": apellido,
            "especialidad": especialidad
        }
        escribir_profesional_json(profesional, datos)


def escribir_profesional_json(profesional, datos):
    with open(archivo_profesionales, 'r+') as archivo:
        datos = datos
        datos[0]["profesionales"].append(profesional)
        archivo.seek(0)
        json.dump(datos, archivo)


def listar_medicos():
    with open(archivo_profesionales, 'r') as archivo:
        datos = json.load(archivo)
        if len(datos):
            for medico in datos[0]["profesionales"]:
                print(f'''
                    Medico id: #{medico['id']}
                    Nombre: {medico['nombre']}
                    Apellido: {medico['apellido']}
                    Especialidad: {medico['especialidad']}
                ''')
        else:
            print('La lista esta vacia')


def menu_operaciones_pacientes():
    opcion = 0

    while (opcion != 7):
        opcion = int(input(f'''
        --------- MENU (PACIENTES) ---------
        1. Registrar un paciente
        2. Editar datos de paciente
        3. Eliminar un paciente
        4. Buscar paciente
        5. Listar pacientes
        6. Volver atras
        7. Salir
        Opcion: '''))

        if opcion == 1:
            clearConsole()
            registrar_paciente()
        elif opcion == 2:
            clearConsole()
            editar_paciente()
        elif opcion == 3:
            clearConsole()
            eliminar_un_paciente()
        elif opcion == 4:
            clearConsole()
            buscar_paciente_documento()
        elif opcion == 5:
            clearConsole()
            listar_pacientes()
        elif opcion == 6:
            clearConsole()
            return
        elif opcion == 7:
            clearConsole()
            quit(f'\n\tGracias por usar el sistema\n')
        else:
            clearConsole()
            print(f'\n\tOpcion incorrecta!')


def menu_operaciones_clinicas():
    opcion = 0

    while (opcion != 4):
        opcion = int(input(f'''
        --------- MENU (HISTORIAL CLINICO)---------
        1. Agregar historial clinico a paciente
        2. Buscar paciente
        3. Volver atras
        4. Salir
        Opcion: '''))

        if opcion == 1:
            clearConsole()
            agregar_historia_clinica()
        elif opcion == 2:
            clearConsole()
            buscar_paciente_documento()
        elif opcion == 3:
            clearConsole()
            return
        elif opcion == 4:
            clearConsole()
            quit(f'\n\tGracias por usar el sistema\n')
        else:
            clearConsole()
            print(f'\n\tOpcion incorrecta!')


def menu_operaciones_medico():
    opcion = 0

    while (opcion != 4):
        opcion = int(input(f'''
        --------- MENU (MEDICOS)---------
        1. Registrar medico 
        2. Listar medicos
        3. Volver atras
        4. Salir
        Opcion: '''))

        if opcion == 1:
            clearConsole()
            registrar_medico()
        elif opcion == 2:
            clearConsole()
            listar_medicos()
        elif opcion == 3:
            clearConsole()
            return
        elif opcion == 4:
            clearConsole()
            quit(f'\n\tGracias por usar el sistema\n')
        else:
            clearConsole()
            print(f'\n\tOpcion incorrecta!')


def menu_principal():
    opcion = 0

    while (opcion != 4):
        opcion = int(input(f'''
                --------- M E N U ---------
        Eliga la operacion que desea realizar:
        1. Pacientes
        2. Historias Clinicas
        3. Profesionales (Medicos)
        4. Salir
        Opcion: '''))

        if opcion == 1:
            clearConsole()
            menu_operaciones_pacientes()
        elif opcion == 2:
            clearConsole()
            menu_operaciones_clinicas()
        elif opcion == 3:
            clearConsole()
            menu_operaciones_medico()
        elif opcion == 4:
            clearConsole()
            quit(f'\n\tGracias por usar el sistema\n')
        else:
            clearConsole()
            print(f'\n\tOpcion incorrecta!')


menu_principal()