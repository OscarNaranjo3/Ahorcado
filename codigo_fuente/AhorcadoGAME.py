import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from urllib.request import urlopen
import random
import time
import os.path
import os


def get_words():
    '''
    Abre el archivo 'palabras.txt' en modo lectura, si el archivo se encuentra vacío,
    llama a la función webscrapping() para añadir nuevas palabras al juego;
    :return: se retorna a sí misma si el archivo está vacío y una lista con las palabras
    encontradas dentro del archivo en caso de que no
    '''

    arch_palabras = open("palabras.txt", "r")
    palabras = arch_palabras.readlines()
    arch_palabras.close()
    if palabras == []:
        webscrapping()
        return get_words()
    return palabras

def ventana_inicio():
    '''
    Crea la ventana inicial del juego, donde se le pregunta al usuario
    si ya posee una cuenta o si desea registrarse, además se le da la
    opción de agregar nuevas palabras al juego por medio de un botón.
    :return:
    '''
    global principal_ventana
    global label_mensaje_nuevas_palabras

    Color = "DarkGrey"
    principal_ventana = tk.Tk()
    principal_ventana.geometry("300x275")
    principal_ventana.title("¡Bienvenido a Ahorcado!")
    Label(text="¿Ya tiene una cuenta?", bg="CadetBlue1", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Acceder", height="2", width="30", bg=Color, command=login).pack()
    Label(text="").pack()
    Button(text="Registrarse", height="2", width="30", bg=Color, command=registrarse).pack()
    Label(text="").pack()
    Label(text="").pack()
    label_mensaje_nuevas_palabras = tk.Label(principal_ventana, text="", font=("calibri", 11))
    label_mensaje_nuevas_palabras.pack()
    Button(text="Añadir palabras", height="1", width="15", bg=Color, command=añadir_palabras).pack()
    principal_ventana.mainloop()

def registrarse():
    '''
    Crea la ventana de registro de un nuevo usuario, donde se le solicita ingresar
    el nombre de usuario que desea crear y su respectiva contraseña. Ejecuta la
    función UsuarioRegistro cada vez que se presiona el botón "Registrarse"
    :return:
    '''
    global ventana_registro
    ventana_registro = Toplevel(principal_ventana)
    ventana_registro.title("Registrarse")
    ventana_registro.geometry("300x250")

    global nombre_usuario
    global clave
    global entrada_nombre
    global entrada_clave
    global label_mensaje_registro

    nombre_usuario = StringVar()
    clave = StringVar()

    Label(ventana_registro, text="Introduzca datos", bg="LightGreen").pack()
    Label(ventana_registro, text="").pack()
    etiqueta_nombre = Label(ventana_registro, text="Nombre de usuario * ")
    etiqueta_nombre.pack()
    entrada_nombre = Entry(ventana_registro, textvariable=nombre_usuario)
    entrada_nombre.pack()
    etiqueta_clave = Label(ventana_registro, text="Contraseña * ")
    etiqueta_clave.pack()
    entrada_clave = Entry(ventana_registro, textvariable=clave, show='*')

    entrada_clave.pack()
    Label(ventana_registro, text="").pack()
    Button(ventana_registro, text="Registrarse", width=10, height=1, bg="LightGreen", command=usuario_registro).pack()

    label_mensaje_registro = tk.Label(ventana_registro, text="", font=("calibri", 11))
    label_mensaje_registro.pack()

def añadir_palabras():
    '''
    Genera una ventana emergente que pregunta si está de acuerdo
    con ejecutar la función, cuya respuesta, en caso de ser positiva
    llamará a la función webscrapping() para que añada 20 palabras
    nuevas al archivo de palabras posibles para el juego, de lo contrario
    no hará nada.
    :return:
    '''

    global label_mensaje_nuevas_palabras

    info = messagebox.askquestion("Hola!",
                                  "¿Deseas hacer esto? \n\n"
                                  "El objetivo de este botón es ampliar la\n" 
                                  "cantidad de palabras posibles entre las\n" 
                                  "que el programa puede elegir al azar\n"
                                  "para el juego")
    if info == "yes":
        webscrapping()
        label_mensaje_nuevas_palabras.config(text="Se han añadido 20 palabras nuevas", fg="green")
    else:
        label_mensaje_nuevas_palabras.config(text="")

def login():
    '''
    Crea la ventana de incio de sesión de un usuario ya previamente registrado.
    Se le solicita al usuario ingresar su nombre de usuario y su respectiva contraseña.
    Ejecuta la función verificaLogin
    :return:
    '''

    global ventana_login
    global label_mensaje_login

    ventana_login = Toplevel(principal_ventana)
    ventana_login.title("Acceso a la cuenta")
    ventana_login.geometry("300x270")
    Label(ventana_login, text="Introduzca nombre de usuario y contraseña").pack()
    Label(ventana_login, text="").pack()

    global verifica_usuario
    global verifica_clave

    verifica_usuario = StringVar()
    verifica_clave = StringVar()

    global entrada_login_usuario
    global entrada_login_clave

    Label(ventana_login, text="Nombre usuario * ").pack()
    entrada_login_usuario = Entry(ventana_login, textvariable=verifica_usuario)
    entrada_login_usuario.pack()
    Label(ventana_login, text="").pack()
    Label(ventana_login, text="Contraseña * ").pack()
    entrada_login_clave = Entry(ventana_login, textvariable=verifica_clave, show='*')
    entrada_login_clave.pack()
    Label(ventana_login, text="").pack()
    Button(ventana_login, text="Acceder", width=10, height=1, command=verifica_login).pack()
    Label(ventana_login, text="").pack()
    label_mensaje_login = tk.Label(ventana_login, text="", font=("calibri", 11))
    label_mensaje_login.pack()

def verifica_login():
    global jugador
    global ventana_login
    global principal_ventana
    global label_mensaje_login

    usuario1 = verifica_usuario.get()
    clave1 = verifica_clave.get()
    entrada_login_usuario.delete(0, END)
    entrada_login_clave.delete(0, END)
    jugador = usuario1

    try:
        dic_usuarios = recolectar_datos_jugadores()
    except AttributeError:
        label_mensaje_login.config(text="No hay usuarios registrados\n por favor registrese e intente\n de nuevo", fg="red")

    if dic_usuarios == {}:
        label_mensaje_login.config(text="No hay usuarios registrados\n por favor registrese e intente\n de nuevo", fg="red")
    elif usuario1 in dic_usuarios.keys():
        if clave1 == dic_usuarios[usuario1]:
            ventana_login.destroy()
            principal_ventana.destroy()
            init_window()
        else:
            no_clave()
    else:
        no_usuario()

def no_clave():
    global ventana_clave_no
    ventana_clave_no = Toplevel(ventana_login)
    ventana_clave_no.title("ERROR")
    ventana_clave_no.geometry("150x100")
    Label(ventana_clave_no, text="Contraseña incorrecta ").pack()
    Button(ventana_clave_no, text="OK", command=borrar_no_clave).pack()

def no_usuario():
    global ventana_usuario_no
    ventana_usuario_no = Toplevel(ventana_login)
    ventana_usuario_no.title("ERROR")
    ventana_usuario_no.geometry("150x100")
    Label(ventana_usuario_no, text="Usuario no encontrado").pack()
    Button(ventana_usuario_no, text="OK", command=borrar_no_usuario).pack()

def borrar_no_clave():
    ventana_clave_no.destroy()

def borrar_no_usuario():
    ventana_usuario_no.destroy()

def usuario_registro():
    global ventana_registro
    global label_mensaje_registro

    info_usuario = nombre_usuario.get().strip()
    info_clave = clave.get()

    entrada_nombre.delete(0, END)
    entrada_clave.delete(0, END)

    file = open("datos_usuarios.txt", "a+")

    try:
        dic_usuarios = recolectar_datos_jugadores()
    except AttributeError:
        if info_usuario == "" or info_clave == "":
            file.close()
            label_mensaje_registro.config(text="\nRegistro inválido, ninguno\n de los campos puede estar vacío", fg="red")
        else:
            file.write(info_usuario + "," + info_clave + "\n")
            file.close()
            label_mensaje_registro.config(text="\nRegistro completado con éxito", fg="green")
            ventana_registro.destroy()

    if info_usuario == "" or info_clave == "":
        file.close()
        label_mensaje_registro.config(text="\nRegistro inválido, ninguno\n de los campos puede estar vacío", fg="red")
    elif info_usuario in dic_usuarios.keys():
        file.close()
        label_mensaje_registro.config(text="\nRegistro inválido, ya existe\n un usuario con este nombre", fg="red")
    else:
        file.write(info_usuario + "," + info_clave + "\n")
        file.close()
        label_mensaje_registro.config(text="\nRegistro completado con éxito", fg="green")
        ventana_registro.destroy()

def init_window():
    """
    Abre la ventana de la interfaz gráfica del juego
    :return:
    """
    global boton2
    window = tk.Tk()
    window.wm_title("Ahorcado")
    window.geometry = ('2000x2000')
    window.minsize(600, 400)
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    window.rowconfigure(0, weight=1)
    window.rowconfigure(2, weight=1)
    window.rowconfigure(5, weight=1)
    window.rowconfigure(8, weight=1)
    style = ttk.Style()
    style.theme_use("clam")

    label = tk.Label(window,
                     text="Ahorcado",
                     font=("Arial bold", 20))
    label.grid(column=0, row=0, columnspan=2)

    label2 = tk.Label(window,
                      text="\n\n\n\n\n",
                      font=("Arial bold", 20))
    label2.grid(column=0, row=1, columnspan=2)

    label3 = tk.Label(window,
                     text=" ".join(espacios_palabra),
                     font=("Arial bold", 20))
    label3.grid(column=0, row=3, columnspan=2)

    label4 = tk.Label(window,
                      text="Letras usadas: "+ ", ".join(letras_repetidas),
                      font=("Arial bold", 12))
    label4.grid(column=0, row=4, columnspan=2)

    label_entrada1 = tk.Label(window, text="Ingrese letra:", font=("Arial bold", 15))
    label_entrada1.grid(column=0, row=6)

    label_num_fails = tk.Label(window, text="Número de"+"\n" "fallos:"+"\n\n", font=("Arial bold", 15))
    label_num_fails.grid(column=0, row=1)

    entrada1 = tk.Entry(window, width=22)


    entrada1.focus()

    entrada1.grid(column=1, row=6)

    # Crear botón
    boton = tk.Button(window,
                      command=lambda: juego(entrada1, window, label, label2, label3, label4, label_entrada1, label_num_fails, boton),
                      text="Aceptar",
                      bg="Brown",
                      fg="white")
    boton.grid(column=1, row=7)

    boton2 = tk.Button(window,
                      command=lambda: volver_a_inicio(window),
                      text="Volver",
                      bg="gray",
                      fg="white")
    boton2.grid(column=0, row=0, sticky= W, padx=10)

    window.mainloop()

def init_stats_window():
    """
    Abre la ventana de las estadisticas, con una tabla mostrando las estadisticas
    del jugador actual y otra global de algunos de los otros jugadores
    :return:
    """
    global jugador
    filas = recolectar_estadisticas()

    stats_window = tk.Tk()
    stats_window.wm_title("Estad\u00edsticas")
    stats_window.geometry = ('2000x2000')
    stats_window.minsize(300, 400)
    style = ttk.Style()
    style.theme_use("clam")

    estadisticas_jugadores = tk.Frame(stats_window, borderwidth=2, relief="raised")

    estadisticas_jugadores.pack(side="top", fill="x", expand=1)
    estadisticas_jugadores.config(cursor="pirate")

    stats_window.config(bg="lightblue")

    encabezado1 = tk.Label(estadisticas_jugadores,
                          text="Tus estad\u00edsticas \t ^‿^",
                          font=("Arial bold", 12), anchor="center")
    encabezado1.pack()

    tabla = ttk.Treeview(estadisticas_jugadores, columns=("jugadas", "ganadas", "perdidas"), height=1)

    tabla.heading("#0", text="Jugador")
    tabla.heading("jugadas", text="Jugadas")
    tabla.heading("ganadas", text="Ganadas")
    tabla.heading("perdidas", text="Perdidas")

    tabla.column("#0", width=100, anchor="center")
    tabla.column("jugadas", width=25, anchor="center")
    tabla.column("ganadas", width=27, anchor="center")
    tabla.column("perdidas", width=27, anchor="center")

    if jugador not in filas.keys():
        tabla.insert("", tk.END, text=jugador, values=(0,0,0))
    else:
        tabla.insert("", tk.END, text=jugador, values=(filas[jugador]))

    tabla.pack(fill="x", expand=1)

    estadisticas_jugadores = tk.Frame(stats_window, borderwidth=2, relief="raised")

    estadisticas_jugadores.pack(side="top", fill="x", expand=1)
    estadisticas_jugadores.config(cursor="pirate")


    encabezado1 = tk.Label(estadisticas_jugadores,
                           text="Estad\u00edsticas Globales ",
                           font=("Arial bold", 12), anchor="center")
    encabezado1.pack()

    cantidad_filas = len(filas)
    if cantidad_filas >= 10:
        cantidad_filas = 10

    tabla2 = ttk.Treeview(estadisticas_jugadores, columns=("jugadas", "ganadas", "perdidas"), height=cantidad_filas)
    style = ttk.Style()
    style.theme_use("clam")

    tabla2.heading("#0", text="Jugador")
    tabla2.heading("jugadas", text="Jugadas")
    tabla2.heading("ganadas", text="Ganadas")
    tabla2.heading("perdidas", text="Perdidas")

    tabla2.column("#0", width=100, anchor="center")
    tabla2.column("jugadas", width=25, anchor="center")
    tabla2.column("ganadas", width=27, anchor="center")
    tabla2.column("perdidas", width=27, anchor="center")

    contador = 0

    for llave in filas:
        tabla2.insert("", tk.END, text=llave, values=(filas[llave]))
        if contador >= 9:
            break
        contador += 1


    tabla2.pack(fill="x", expand=1)

    stats_window.mainloop()

def win_mode(ventana, label_1, label_2, label_3, label_4, label_5, label_6):
    """
    Hace que la ventana cambie de colores
    :param ventana: La ventana a la que se le va a aplicar la función
    :param label_1: Etiqueta 1 a la que se le va a aplicar la función
    :param label_2: Etiqueta 2 a la que se le va a aplicar la función
    :param label_3: Etiqueta 3 a la que se le va a aplicar la función
    :param label_4: Etiqueta 4 a la que se le va a aplicar la función
    :param label_5: Etiqueta 5 a la que se le va a aplicar la función
    :param label_6: Etiqueta 6 a la que se le va a aplicar la función
    :return:
    """
    ventana.wm_title("GANASTE B)")
    for i in range(0, 16777200, 200000):
        o = convertir_a_hex(i)
        if len(o) < 2:
            a = "#00000" + o
        elif len(o) < 3:
            a = "#0000" + o
        elif len(o) < 4:
            a = "#000" + o
        elif len(o) < 5:
            a = "#00" + o
        elif len(o) < 6:
            a = "#0" + o
        else:
            a = "#" + o

        ventana["background"] = a
        label_1["background"] = a
        label_2["background"] = a
        label_3["background"] = a
        label_4["background"] = a
        label_5["background"] = a
        label_6["background"] = a
        ventana.update_idletasks()
        time.sleep(0.1)

    ventana.config(bg="lightgray")
    label_1.config(bg="lightgray", fg="black")
    label_2.config(bg="lightgray", fg="black")
    label_3.config(bg="lightgray", fg="black")
    label_4.config(bg="lightgray", fg="black")
    label_5.config(bg="lightgray", fg="black")
    label_6.config(bg="lightgray", fg="black")

    ventana.update_idletasks()

def convertir_a_hex(n):
    """
    Convierte un número decimal a hexadecimal
    :param n: Número decimal a convertir
    :return: Número hexadecimal (decimal convertido)
    """
    r = int(n)
    conv = ""
    while r >= 16:
        if r % 16 == 10:
            conv += "A"
        elif r % 16 == 11:
            conv += "B"
        elif r % 16 == 12:
            conv += "C"
        elif r % 16 == 13:
            conv += "D"
        elif r % 16 == 14:
            conv += "E"
        elif r % 16 == 15:
            conv += "F"
        else:
            conv += str(r % 16)
        r = r // 16
    if r % 16 == 10:
        conv += "A"
    elif r % 16 == 11:
        conv += "B"
    elif r % 16 == 12:
        conv += "C"
    elif r % 16 == 13:
        conv += "D"
    elif r % 16 == 14:
        conv += "E"
    elif r % 16 == 15:
        conv += "F"
    else:
        conv += str(r % 16)
    return conv[::-1]

def volver_a_inicio(ventana):
    ventana.destroy()
    ventana_inicio()

def traducir_a_vocal(letra):
    carac_especiales = 'AÁáÄäEÉéËëIÍíÏïOÓóÖöUÚúÜü'
    carac = 'aaaaaeeeeeiiiiiooooouuuuu'
    trans = str.maketrans(carac_especiales, carac)
    return letra.translate(trans)

def verifica_letra(letter, evolution, palabra):
    """
    Verifica si la letra ingresada hace parte de las letras de la palabra a adivinar
    y la pone en la lista de espacios en su lugar respectivo
    :param letter: Letra a verificar
    :param evolution: Lista de espacios
    :param palabra: Palabra a adivinar
    :return: 1 en caso de que la letra ya haya sido usada, Lista de espacios con las letras adivinadas
    """

    error = True
    for l in range(len(palabra)):

        if traducir_a_vocal(letter).lower() == traducir_a_vocal(palabra[l]) or traducir_a_vocal(letter).upper() == traducir_a_vocal(palabra[l]):
            evolution[l] = palabra[l]
            error = False
    if error:
        return 1, evolution
    else:
        return 0, evolution

def dibujar_ahorcado(fail_num, label_1, label_2, entrada, fail_incr, fail_label):
    """
    Cambia el estado del dibujo del ahorcado entre sus distintas fases y
    en caso de que este sea máximo, termina el juego (Deshabilita el ingreso de nuevas letras)
    :param fail_num: Número actual de fallos
    :param label_1: Etiqueta del título principal
    :param label_2: Etiqueta del dibujo
    :param entrada: Nombre del parámetro de entrada de texto
    :param fail_incr: Etiqueta de la lista de letras ya usadas
    :param fail_label: Etiqueta de el número de fallos
    :return: 0 en caso de que el jugador aún tenga fallos menores a 10
    1 caso de que se le hayan acabado los posibles fallos
    """
    lista_dibujos = ["\n\n\n\n\n",
                     "\n\n\n\n\n" + "---    ",
                     "\n" + "|      " + "\n" + "|      " + "\n" + "|      " + "\n" + "|      " + "\n" + "---    ",
                     '-------' + "\n" + "|      " + "\n" + "|      " + "\n" + "|      " + "\n" + "|      " + "\n" + "---    ",
                     '-------' + "\n" + "|     |" + "\n" + "|      " + "\n" + "|      " + "\n" + "|      " + "\n" + "---    ",
                     '-------' + "\n" + "|     |" + "\n" + "|     o" + "\n" + "|      " + "\n" + "|      " + "\n" + "---    ",
                     '-------' + "\n" + "|     |" + "\n" + "|     o" + "\n" + "|     |" + "\n" + "|      " + "\n" + "---    ",
                     '-------' + "\n" + "|     |" + "\n" + "|     o" + "\n" + "|    /|" + "\n" + "|      " + "\n" + "---    ",
                     '-------' + "\n" + "|     |" + "\n" + "|     o" + "\n" + "|    /|\\" + "\n" + "|      " + "\n" + "---    ",
                     '-------' + "\n" + "|     |" + "\n" + "|     o" + "\n" + "|    /|\\" + "\n" + "|    / " + "\n" + "---    ",
                     '-------' + "\n" + "|     |" + "\n" + "|     o" + "\n" + "|    /|\\" + "\n" + "|    / \\" + "\n" + "---    "
                     ]
    if fail_num >= 10:
        label_2.config(text=lista_dibujos[10])
        label_1.config(text="¡Has Perdido!")
        entrada.configure(state="disabled")
        fail_label.config(text="Número de" + "\n" "fallos:" + "\n\n" + str(10) + "/" + str(len(lista_dibujos)-1))
        return 1
    else:
        label_2.config(text=lista_dibujos[fail_num])
    fail_incr.config(text="Letras usadas: "+ ", ".join(letras_repetidas))
    fail_label.config (text= "Número de" + "\n" "fallos:" + "\n\n" + str(fail_num) + "/" + str(len(lista_dibujos)-1))
    return 0

def juego(entrada, ventana, label_1, label_2, label_3, label_4, label_entrada, fail_label, boton):
    """
    Inicia el juego:
        *Llama a las funciones dibujar_ahorcado, verify_letra_repetida y verficar_win
    :param entrada: Nombre del parámetro de entrada de texto
    :param ventana: La ventana a la que se le va a aplicar la función
    :param label_1: Etiqueta del título principal
    :param label_2: Etiqueta del dibujo
    :param label_3: Etiqueta de el número de fallos
    :param label_4: Etiqueta de la lista de letras ya usadas
    :param label_entrada: Etiqueta de la entrada
    :param fail_label: Etiqueta de el número de fallos
    :return: Se retorna a sí misma en caso de que el jugador decida seguir jugando luego de
    acabada la partida
    """
    global jugador
    global boton2

    label_1.config(text="Ahorcado")
    if dibujar_ahorcado(fails, label_1, label_2, entrada, label_4, fail_label):
        actualizar_estadisticas(recolectar_estadisticas(), jugador, 0)
        boton['state'] = tk.DISABLED
        boton2['state'] = tk.DISABLED
        res = messagebox.askquestion("Hola!", "¿Deseas volver a jugar?")
        if res == "yes":
            res2 = messagebox.askquestion("Hola!", "¿Deseas intentar el mismo juego?")
            if res2 == "yes":
                reiniciar_mismo_juego_valores()
            else:
                reiniciar_valores()
            entrada.configure(state="normal")
            label_3.config(text=" ".join(espacios_palabra))
            return juego(entrada, ventana, label_1, label_2, label_3, label_4, label_entrada, fail_label, boton)
        else:
            ventana.destroy()
            init_stats_window()
    else:
        boton['state'] = tk.NORMAL
        boton2['state'] = tk.NORMAL

    try:
        if len(entrada.get()) > 1:
            varias_letras(label_1, label_2, label_3, entrada, label_4, fail_label)
        else:
            verify_letra_repetida(label_1, label_2, label_3, entrada, label_4, fail_label)
    except TclError:
        None

    if verficar_win(entrada, ventana, label_1, label_2, label_3, label_4, label_entrada, fail_label):
        actualizar_estadisticas(recolectar_estadisticas(), jugador, 1)
        boton['state'] = tk.DISABLED
        boton2['state'] = tk.DISABLED
        res = messagebox.askquestion("Hola!", "¿Deseas volver a jugar?")
        if res == "yes":
            reiniciar_valores()
            entrada.configure(state="normal")
            label_3.config(text=" ".join(espacios_palabra))
            return juego(entrada, ventana, label_1, label_2, label_3, label_4, label_entrada, fail_label, boton)
        else:
            ventana.destroy()
            init_stats_window()

def caracteres_validos():
    """
    Funcion que crea una lista con los valores ascci de los caracteres que el juego considera cómo válidos para las palabras
    :return: La lista creada
    """
    # Espacio
    lista_validos = [32]
    # Letras mayúsculas
    lista_validos += range(65, 91)
    # Letras minúsculas
    lista_validos += range(97, 123)
    # Vocales con tilde
    lista_validos += ord("á"), ord("é"), ord("í"), ord("ó"), ord("ú"), ord("Á"), ord("É"), ord("Í"), ord("Ó"), ord("Ú")
    # Vocales con diéresis
    lista_validos += ord("ä"), ord("ë"), ord("ï"), ord("ö"), ord("ü"), ord("Ä"), ord("Ë"), ord("Ï"), ord("Ö"), ord("Ü")
    # "Ñ"
    lista_validos += ord("ñ"), ord("Ñ")
    return lista_validos

def varias_letras(label_1, label_2, label_3, entrada, label_4, fail_label):
    """
    Esta función lo que hace es que divide la palabra que recibe letra por letra y las verifica como si fueran entradas
    individuales
    :param label_1: Etiqueta del título principal
    :param label_2: Etiqueta del dibujo
    :param label_3: Etiqueta de el número de fallos
    :param entrada: Nombre del parámetro de entrada de texto
    :param label_4: Etiqueta de la lista de letras ya usadas
    :param fail_label:  Etiqueta de el número de fallos
    :return:
    """
    palabra = entrada.get()
    entrada.delete(0, tk.END)

    for letra in palabra:
        if verify_letra_palabra(letra, label_1, label_2, label_3, entrada, label_4, fail_label) == 0:
            break

def verify_letra_repetida(label_1, label_2, label_3, entrada, label_4, fail_label):
    """
    Toma una letra de la entrada y verifica si hace parte de la lista de letras ya
    usadas e imprime "Esta letra ya la usaste" en caso de que si o actualiza esta
    lista, el dibujo y el número de fallos en caso de que no.

    :param label_1: Etiqueta del título principal
    :param label_2: Etiqueta del dibujo
    :param label_3: Etiqueta de el número de fallos
    :param entrada: Nombre del parámetro de entrada de texto
    :param label_4: Etiqueta de la lista de letras ya usadas
    :param fail_label: Etiqueta de el número de fallos
    :return: None si al comprobar verify_letra_palabra obtiene 0
    """
    letra = entrada.get()
    entrada.delete(0, tk.END)
    global espacios_palabra
    global fails
    global letras_repetidas

    if traducir_a_vocal(letra).lower() in letras_repetidas:
        label_1.config(text="Esta letra ya la usaste")
    else:
        if not verify_letra_palabra(letra, label_1, label_2, label_3, entrada, label_4, fail_label):
            return None
        letras_repetidas.append(traducir_a_vocal(letra).lower())
        resultados = verifica_letra(letra, espacios_palabra, word)
        fails += resultados[0]
        espacios_palabra = resultados[1]
        label_3.config(text=" ".join(espacios_palabra))

    dibujar_ahorcado(fails, label_1, label_2, entrada, label_4, fail_label)

def verify_letra_palabra(letra, label_1, label_2, label_3, entrada, label_4, fail_label):
    """
    Toma la letra que se le pase cómo parámetro y verifica si hace parte de la lista de letras ya
    usadas en caso de que no, actualiza esta lista, el dibujo y el número de fallos.

    :param letra: Letra a verificar
    :param label_1: Etiqueta del título principal
    :param label_2: Etiqueta del dibujo
    :param label_3: Etiqueta de el número de fallos
    :param entrada: Nombre del parámetro de entrada de texto
    :param label_4: Etiqueta de la lista de letras ya usadas
    :param fail_label: Etiqueta de el número de fallos
    :return: retorna 0 si recibe alguna entrada inválida
    """
    caracteres = caracteres_validos()
    let = letra
    global espacios_palabra
    global fails
    global letras_repetidas

    if len(letra) < 1:
        messagebox.showinfo("Hola!", "Debes ingresar alguna letra")
        return 0

    if ord(letra) not in caracteres:
        messagebox.showinfo("Hola!", "Entrada inválida (Solo puedes usar letras)")
        return 0

    if traducir_a_vocal(let).lower() not in letras_repetidas:
        letras_repetidas.append(traducir_a_vocal(let).lower())
    resultados = verifica_letra(let, espacios_palabra, word)
    fails += resultados[0]
    espacios_palabra = resultados[1]
    label_3.config(text=" ".join(espacios_palabra))

    dibujar_ahorcado(fails, label_1, label_2, entrada, label_4, fail_label)

def verficar_win(entrada, ventana, label_1, label_2, label_3, label_4, label_entrada, fail_label):
    """
    Crea una lista (comparador) de las letras en la palabra a adivinar
    :param entrada:
    :param ventana: La ventana a la que se le va a aplicar la función
    :param label_1: Etiqueta del título principal
    :param label_2: Etiqueta del dibujo
    :param label_3: Etiqueta de el número de fallos
    :param label_4: Etiqueta de la lista de letras ya usadas
    :param label_entrada: Etiqueta de la entrada
    :param fail_label: Etiqueta de el número de fallos
    :return: Retorna 1 sí espacios_palabra es igual a comparador,
    es decir si el jugador ganó la partida, retorna 0 si aún no ha
    ganado
    """
    global word
    global espacios_palabra
    comparador = []

    for caracter in word:
        comparador += caracter
    if espacios_palabra == comparador:
        label_3.config(text=" ".join(comparador))
        label_1.config(text="¡Has Ganado!")
        entrada.configure(state="disabled")
        win_mode(ventana, label_1, label_2, label_3, label_4, label_entrada, fail_label)
        return 1
    return 0

def reiniciar_valores():
    '''
    En caso de que se desee volver a jugar, esta función reinicia todos los valores del juego
    a su inicio predeterminado (desde ceros).
    Toma una nueva palabra al azar, redefine y actualiza la variable espacios_palabra en base
    a dicha palabra
    :return:
    '''
    global word
    global espacios_palabra
    global fails
    global letras_repetidas

    try:
        word = random.choice(get_words()).strip()
    except FileNotFoundError:
        webscrapping()
        word = random.choice(get_words()).strip()

    espacios_palabra = []
    fails = 0
    letras_repetidas = []
    for iterador in range(len(word)):
        espacios_palabra += ["_ "]

def reiniciar_mismo_juego_valores():
    '''
    Se reinician todos los valores del juego, exceptuando la palabra a descifrar, en caso
    de que el usuario quiera volver a jugar con la misma palabra.
    :return:
    '''

    global word
    global espacios_palabra
    global fails
    global letras_repetidas

    espacios_palabra = []
    fails = 0
    letras_repetidas = []
    for iterador in range(len(word)):
        espacios_palabra += ["_ "]

def recolectar_estadisticas():
    '''
    Lee el archivo stats.txt y crea un diccionario con los datos dentro del mismo
    :return: Un diccionario con las estadísticas de los usuarios que han jugado
    '''

    if not os.path.isfile("stats.txt"):
        return 0
    old = open('stats.txt', "r+")
    archivo = old.readlines()
    estadisticas = {}
    for linea in archivo:
        lista = linea.split(",")
        contadores = [int(item) for item in lista[1:]]
        estadisticas[lista[0]] = contadores
    old.close()
    return estadisticas

def recolectar_datos_jugadores():
    '''
    Lee el archivo datos_usuarios.txt y crea un diccionario con los datos dentro del mismo
    :return: Un diccionario con los nombres de usuarios  como llaves y sus respectivas contraseñas
    como valores
    '''

    old = open('datos_usuarios.txt', "r+")
    archivo = old.readlines()
    jugadores_claves = {}
    for linea in archivo:
        lista = linea.split(",")
        jugadores_claves[lista[0]] = lista[1].strip("\n")
    old.close()
    return jugadores_claves

def actualizar_estadisticas(diccionario, llave, gana_o_pierde):
    '''
    Esta función se encarga de actualizar las estadisticas en el diccionario obtenido
    por la funcion recolectar_estadistis de un jugador según si gana o pierde una
    partida y sobre escribe el archivo stats.txt con los valores actualizados.
    En caso de que el usuario no tenga estadísticas en el archivo, crea el nuevo usuario
    con sus primeras estadísticas.
    :param diccionario: diccionario de cada ususario registrado
    :param llave: lista con cada partida jugada, ganada y perdida.
    :param gana_o_pierde: True si el jugador ha ganado la partida, False si no
    :return:
    '''

    if diccionario == 0:
        diccionario = {llave:[0, 0, 0]}
    if llave not in diccionario.keys():
        diccionario[llave] = [0, 0, 0]
    diccionario[llave][0] += 1
    if gana_o_pierde:
        diccionario[llave][1] += 1
    else:
        diccionario[llave][2] += 1

    new = open('stats.txt', "w")

    for llave in diccionario.keys():
        contador = [str(item) for item in diccionario[llave]]
        new.write(llave+","+",".join(contador)+"\n")
    new.close()

def webscrapping():
    """
    Función que obtiene 20 palabras aleatorias de una página web y las añade
     al archivo "palabras.txt"
    :return:
    """
    url = "https://www.epasatiempos.es/sopas-de-letras-al-azar.php"
    page = urlopen(url)
    html = page.read().decode("utf-8")

    wordlist_index = html.find("wordlist=[")
    iterador = wordlist_index+10
    cadena = ""
    while html[iterador] != "]":
        cadena += html[iterador]
        iterador += 1
    linea = cadena.strip('"').split('","')
    diccionario_vocales_especiales = {"\\u00c1":"Á", "\\u00e1":"á", "\\u00c9":"É", "\\u00e9":"é", "\\u00cd":"Í",
                                      "\\u00ed":"í", "\\u00d3":"Ó", "\\u00f3":"ó", "\\u00da":"Ú", "\\u00fa":"ú",
                                      "\\u00dc":"Ü", "\\u00fc":"ü", "\\u00d1":"Ñ", "\\u00f1":"ñ"}

    arch_palabras = open("palabras.txt", "a")
    variable = 0
    for palabra in linea:
        for iterador in range (len(palabra)-1):
            if 0 < variable < 6:
                variable += 1
                continue
            if palabra[iterador:iterador+1] == "\\":
                arch_palabras.write(diccionario_vocales_especiales[palabra[iterador:iterador+6]])
                variable = 1
            else:
                arch_palabras.write(palabra[iterador])
        arch_palabras.write(palabra[iterador+1] + "\n")
    arch_palabras.close()

def main():
    reiniciar_valores()
    ventana_inicio()

main()
