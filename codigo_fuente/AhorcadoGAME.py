import tkinter as tk
from tkinter import ttk
import time

word = input("Ingrese palabra: ")
espacios_palabra = []
fails = 0
letras_repetidas = []

for o in range(len(word)):
    espacios_palabra += ["_ "]

def init_window():
    """
    Abre la ventana de la interfaz gráfica del juego
    :return:
    """
    window = tk.Tk()
    window.wm_title("Ahorcado")
    window.geometry = ('900x600')


    label = tk.Label(window,
                     text="Ahorcado",
                     font=("Arial bold", 15))
    label.grid(column=0, row=0, columnspan=2)

    label2 = tk.Label(window,
                      text='-------' + "\n" + "|     |" + "\n" + "|      " + "\n" + "|      " + "\n" + "|      " + "\n" + "---    ",
                      font=("Arial bold", 15))
    label2.grid(column=1, row=1, columnspan=2)

    label3 = tk.Label(window,
                     text=" ".join(espacios_palabra),
                     font=("Arial bold", 15))
    label3.grid(column=0, row=2, columnspan=2)

    label4 = tk.Label(window,
                      text="Letras usadas: "+ ", ".join(letras_repetidas),
                      font=("Arial bold", 10))
    label4.grid(column=0, row=3, columnspan=2)

    label_entrada1 = tk.Label(window, text="Ingrese letra:", font=("Arial bold", 10))
    label_entrada1.grid(column=0, row=4)

    label_num_fails = tk.Label(window, text="Número de"+"\n" "fails:"+"\n\n"+"0/6", font=("Arial bold", 10))
    label_num_fails.grid(column=0, row=1)

    entrada1 = tk.Entry(window, width=22)


    entrada1.focus()

    entrada1.grid(column=1, row=4)

    # Crear botón
    boton = tk.Button(window,
                      command=lambda: juego(entrada1, window, label, label2, label3, label4, label_entrada1, label_num_fails),
                      text="Aceptar",
                      bg="Brown",
                      fg="white")
    boton.grid(column=1, row=5)

    window.mainloop()


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

def verifica_letra(letter, evolution, palabra):
    """
    Verifica si la letra ingresada hace parte de las letras de la palabra a adivinar
    y la pone en la lista de espacios en su lugar respectivo
    :param letter: Letra a verificar
    :param evolution: Lista de espacios
    :param palabra: Palabra a adivinar
    :return: Lista de espacios con las letras adivinadas
    """
    error = True
    for l in range(len(palabra)):
        if letter == palabra[l]:
            evolution[l] = letter
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
    :return:
    """
    if fail_num == 0:
        label_2.config(
            text='-------' + "\n" + "|     |" + "\n" + "|      " + "\n" + "|      " + "\n" + "|      " + "\n" + "---    ")
    elif fail_num == 1:
        label_2.config(
            text='-------' + "\n" + "|     |" + "\n" + "|     o" + "\n" + "|      " + "\n" + "|      " + "\n" + "---    ")
    elif fail_num == 2:
        label_2.config(
            text='-------' + "\n" + "|     |" + "\n" + "|     o" + "\n" + "|     |" + "\n" + "|      " + "\n" + "---    ")
    elif fail_num == 3:
        label_2.config(
            text='-------' + "\n" + "|     |" + "\n" + "|     o" + "\n" + "|    /|" + "\n" + "|      " + "\n" + "---    ")
    elif fail_num == 4:
        label_2.config(
            text='-------' + "\n" + "|     |" + "\n" + "|     o" + "\n" + "|    /|\\" + "\n" + "|      " + "\n" + "---    ")
    elif fail_num == 5:
        label_2.config(
            text='-------' + "\n" + "|     |" + "\n" + "|     o" + "\n" + "|    /|\\" + "\n" + "|    / " + "\n" + "---    ")
    elif fail_num == 6:
        label_2.config(
            text='-------' + "\n" + "|     |" + "\n" + "|     o" + "\n" + "|    /|\\" + "\n" + "|    / \\" + "\n" + "---    ")
        label_1.config(text="¡Has Perdido!")
        entrada.configure(state="disabled")
    fail_incr.config(text="Letras usadas: "+ ", ".join(letras_repetidas))
    fail_label.config (text= "Número de" + "\n" "fails:" + "\n\n" + str(fail_num) + "/6")
#entrada1, window, label, label2, label3, label4, label_entrada1, label_num_fails

def juego(entrada, ventana, label_1, label_2, label_3, label_4, label_entrada, fail_label):
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
    :return:
    """
    dibujar_ahorcado(fails, label_1, label_2, entrada, label_4, fail_label)
    verify_letra_repetida(label_1, label_2, label_3, entrada, label_4, fail_label)
    verficar_win(entrada, ventana, label_1, label_2, label_3, label_4, label_entrada, fail_label)

def verify_letra_repetida(label_1, label_2, label_3, entrada, label_4, fail_label):
    """
    Toma una letra de la entrada y verifica si hace parte de la lista de letras ya
    usadas e imprime "Esta letra ya la usaste" en caso de que si o actualiza esta
    lista en caso de que no.

    :param label_1: Etiqueta del título principal
    :param label_2: Etiqueta del dibujo
    :param label_3: Etiqueta de el número de fallos
    :param entrada: Nombre del parámetro de entrada de texto
    :param label_4: Etiqueta de la lista de letras ya usadas
    :param fail_label: Etiqueta de el número de fallos
    :return:
    """
    letra = entrada.get()
    global espacios_palabra
    global fails
    global letras_repetidas

    if letra in letras_repetidas:
        label_1.config(text="Esta letra ya la usaste")

    else:
        letras_repetidas.append(letra)
        resultados = verifica_letra(letra, espacios_palabra, word)
        fails += resultados[0]
        espacios_palabra = resultados[1]
        label_3.config(text=" ".join(espacios_palabra))

    dibujar_ahorcado(fails, label_1, label_2, entrada, label_4, fail_label)

def verficar_win(entrada, ventana, label_1, label_2, label_3, label_4, label_entrada, fail_label):
    """
    * Crea una lista (comparador) de las letras en la palabra a adivinar
    :param entrada:
    :param ventana: La ventana a la que se le va a aplicar la función
    :param label_1: Etiqueta del título principal
    :param label_2: Etiqueta del dibujo
    :param label_3: Etiqueta de el número de fallos
    :param label_4: Etiqueta de la lista de letras ya usadas
    :param label_entrada: Etiqueta de la entrada
    :param fail_label: Etiqueta de el número de fallos
    :return:
    """
    global word
    global espacios_palabra
    comparador = []

    for c in word:
        comparador += c
    if espacios_palabra == comparador:
        label_3.config(text=" ".join(comparador))
        label_1.config(text="¡Has Ganado!")
        entrada.configure(state="disabled")
        win_mode(ventana, label_1, label_2, label_3, label_4, label_entrada, fail_label)


def main():
    init_window()

main()
