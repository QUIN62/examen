
import tkinter as tk
from tkinter import messagebox
import random

TABLERO_TAMANO = 5
NUMERO_BARCOS = 3
INTENTOS_POR_NIVEL = 20


class BattleshipGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Battleship")
        self.nivel = 1
        self.puntaje_total = 0
        self.intentos_restantes = INTENTOS_POR_NIVEL
        self.barcos_hundidos = 0
        self.tablero_botones = []
        self.menu_principal()

    def menu_principal(self):
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack()

        titulo = tk.Label(self.menu_frame, text="¡Bienvenido a Battleship!", font=("Arial", 16))
        titulo.pack(pady=20)

        instrucciones_btn = tk.Button(self.menu_frame, text="Ver Instrucciones", command=self.mostrar_instrucciones)
        instrucciones_btn.pack(pady=5)

        jugar_btn = tk.Button(self.menu_frame, text="Comenzar Juego", command=self.inicializar_juego)
        jugar_btn.pack(pady=5)

        salir_btn = tk.Button(self.menu_frame, text="Salir", command=self.root.quit)
        salir_btn.pack(pady=5)

    def mostrar_instrucciones(self):
        instrucciones = ("Instrucciones:\n\n"
                         "1. El objetivo es hundir los barcos enemigos en un tablero de 5x5.\n"
                         "2. Hay 3 barcos ocultos en posiciones aleatorias.\n"
                         "   - 1 barco de 1 espacio.\n"
                         "   - 1 barco de 2 espacios.\n"
                         "   - 1 barco de 3 espacios.\n"
                         "3. Tienes 20 intentos, por nivel se iran reduciendo en 5 intentos para encontrarlos.\n"
                         "4. Se marcara de azul el recuadro cuando falles y de rojo cuando aciertes.\n\n"
                         "¡Buena suerte!")
        messagebox.showinfo("Instrucciones", instrucciones)

    def inicializar_juego(self):
        self.menu_frame.destroy()
        self.crear_tablero_visual()
        self.nuevo_juego()

    def crear_tablero_visual(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        for i in range(TABLERO_TAMANO):
            fila_botones = []
            for j in range(TABLERO_TAMANO):
                boton = tk.Button(self.frame, text="O", width=4, height=2,
                                  command=lambda i=i, j=j: self.disparar(i, j))
                boton.grid(row=i, column=j)
                fila_botones.append(boton)
            self.tablero_botones.append(fila_botones)

        self.info_label = tk.Label(self.root,
                                   text=f"Nivel: {self.nivel} | Intentos restantes: {self.intentos_restantes} | Barcos hundidos: {self.barcos_hundidos}")
        self.info_label.pack()

        self.puntaje_label = tk.Label(self.root, text=f"Puntaje total: {self.puntaje_total}")
        self.puntaje_label.pack()

    def nuevo_juego(self):

        self.intentos_restantes = INTENTOS_POR_NIVEL - (self.nivel - 1) * 5
        self.barcos_hundidos = 0
        self.tablero = [['O' for _ in range(TABLERO_TAMANO)] for _ in range(TABLERO_TAMANO)]
        self.barcos = self.posicionar_barcos()
        self.reiniciar_botones()
        self.actualizar_informacion()

    def posicionar_barcos(self):
        barcos = []
        barcos.append(self.generar_barco(1, barcos))
        barcos.append(self.generar_barco(2, barcos))
        barcos.append(self.generar_barco(3, barcos))
        return barcos

    def generar_barco(self, tamano, barcos_existentes):
        barco = []
        orientacion = random.choice(['H', 'V'])
        intentos = 0

        while True:
            if orientacion == 'H':
                fila = random.randint(0, TABLERO_TAMANO - 1)
                columna_inicial = random.randint(0, TABLERO_TAMANO - tamano)
                barco = [(fila, columna_inicial + i) for i in range(tamano)]
            else:
                columna = random.randint(0, TABLERO_TAMANO - 1)
                fila_inicial = random.randint(0, TABLERO_TAMANO - tamano)
                barco = [(fila_inicial + i, columna) for i in range(tamano)]

            if not any(coord in sum(barcos_existentes, []) for coord in barco):
                return barco

            intentos += 1
            if intentos > 50:
                raise Exception("Error: No se pudieron colocar los barcos. Intenta nuevamente.")

    def disparar(self, fila, columna):
        if self.tablero[fila][columna] != "O":
            messagebox.showwarning("Atención", "Ya disparaste aquí.")
            return

        if any((fila, columna) in barco for barco in self.barcos):
            self.tablero[fila][columna] = "X"
            self.tablero_botones[fila][columna].config(text="X", bg="red")
            for barco in self.barcos:
                if (fila, columna) in barco:
                    barco.remove((fila, columna))
                    if not barco:
                        self.barcos_hundidos += 1
            messagebox.showinfo("¡Acertaste!", "¡Le diste a un barco!")
            self.puntaje_total += 10
        else:
            self.tablero[fila][columna] = "."
            self.tablero_botones[fila][columna].config(text=".", bg="blue")
            messagebox.showinfo("Fallaste", "No has dado en ningún barco.")
            self.puntaje_total -= 1

        self.intentos_restantes -= 1
        self.actualizar_informacion()

        if self.barcos_hundidos == NUMERO_BARCOS:
            self.fin_del_nivel(True)
        elif self.intentos_restantes == 0:
            self.game_over()

    def actualizar_informacion(self):
        self.info_label.config(
            text=f"Nivel: {self.nivel} | Intentos restantes: {self.intentos_restantes} | Barcos hundidos: {self.barcos_hundidos}")
        self.puntaje_label.config(text=f"Puntaje total: {self.puntaje_total}")

    def fin_del_nivel(self, victoria):
        if victoria:
            messagebox.showinfo("YOU WIN", "¡Has ganado el nivel!")
            if self.nivel < 4:
                self.nivel += 1
                self.limpiar_tablero_para_nuevo_nivel()
            else:
                messagebox.showinfo("Fin del Juego", f"¡Has completado todos los niveles! Puntaje final: {self.puntaje_total}")
                self.root.quit()
        else:
            messagebox.showinfo("Fin del Nivel", "No has hundido todos los barcos. Intenta de nuevo.")

    def limpiar_tablero_para_nuevo_nivel(self):
        self.tablero_botones = []
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.crear_tablero_visual()
        self.nuevo_juego()

    def reiniciar_botones(self):
        for i in range(TABLERO_TAMANO):
            for j in range(TABLERO_TAMANO):
                self.tablero_botones[i][j].config(text="O", bg="SystemButtonFace", command=lambda i=i, j=j: self.disparar(i, j))

    def game_over(self):
        messagebox.showinfo("GAME OVER",
                            f"¡Se han acabado los intentos! GAME OVER.\nPuntaje final: {self.puntaje_total}")
        self.frame.destroy()
        self.info_label.destroy()
        self.puntaje_label.destroy()
        self.menu_principal()


# Crear la ventana principal
if __name__ == "__main__":
    root = tk.Tk()
    app = BattleshipGame(root)
    root.mainloop()
