import ipaddress
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import colorchooser
from tkinter import font
from tkinter import simpledialog
from tkinter import filedialog

opciones_guardadas = {}

def calcular_subredes():
    ip = entry_ip.get()
    prefix_value = prefix.get()

    if not prefix_value:
        try:
            ip_obj = ipaddress.ip_network(ip, strict=False)
            prefix_value = ip_obj.prefixlen
        except ValueError:
            messagebox.showerror("Error", "La dirección IP ingresada no es válida.")
            return

    try:
        ip_obj = ipaddress.ip_network(ip+"/"+str(prefix_value), strict=False)
        subred = list(ip_obj.subnets(new_prefix=int(prefix_value)))[0]

        resultados_text.delete(1.0, tk.END)  # Limpiar el widget Text

        resultados_text.insert(tk.END, f"IP ingresada: {ip}/{prefix_value}\n")
        resultados_text.insert(tk.END, "--------------------------------------\n")
        resultados_text.insert(tk.END, f"Tipo de red: {detectar_tipo_red(ip_obj.network_address)}\n")
        resultados_text.insert(tk.END, f"Cantidad de subredes: {cantidad_subredes.get()}\n")
        resultados_text.insert(tk.END, "--------------------------------------\n")
        resultados_text.insert(tk.END, "--------------------------------------\n")
        resultados_text.insert(tk.END, f"Cantidad de redes válidas disponibles: {calcular_cantidad_redes(subred)}\n")
        resultados_text.insert(tk.END, "--------------------------------------\n")
        resultados_text.insert(tk.END, "--------------------------------------\n")
        resultados_text.insert(tk.END, f"Máscara de Red: {subred.netmask}\n")
        resultados_text.insert(tk.END, f"Broadcast: {subred.broadcast_address}\n")
        resultados_text.insert(tk.END, f"IP de Red: {subred.network_address}\n")
        resultados_text.insert(tk.END, f"Primera IP válida: {subred.network_address + 1}\n")
        resultados_text.insert(tk.END, f"Última IP válida: {subred.broadcast_address - 1}\n")
        resultados_text.insert(tk.END, f"Puerta de enlace: {subred.network_address + 1}\n")
        resultados_text.insert(tk.END, "--------------------------------------\n")
        resultados_text.insert(tk.END, "--------------------------------------\n")

    except ValueError:
        messagebox.showerror("Error", "La dirección IP ingresada no es válida.")

def calcular_cantidad_redes(subred):
    total_redes = subred.num_addresses
    return total_redes - 2  # Restar 2 para excluir la dirección de red y el broadcast

def detectar_tipo_red(ip):
    if ipaddress.ip_address(ip) in ipaddress.ip_network("10.0.0.0/8"):
        return "Clase A"
    elif ipaddress.ip_address(ip) in ipaddress.ip_network("172.16.0.0/12"):
        return "Clase B"
    elif ipaddress.ip_address(ip) in ipaddress.ip_network("192.168.0.0/16"):
        return "Clase C"
    else:
        return "Desconocida"

def aceptar_ip(event=None):
    calcular_subredes()
    seleccionar_prefijo()

def aceptar_prefix(event=None):
    calcular_subredes()
    dropdown_cantidad_subredes.focus_set()

def aceptar_cantidad_subredes(event=None):
    calcular_subredes()

def seleccionar_prefijo():
    prefix_entry.focus_set()
    prefix_entry.selection_range(0, tk.END)

def incrementar_prefijo(event=None):
    current_prefix = int(prefix.get())
    if current_prefix < 32:
        prefix.set(str(current_prefix + 1))
        calcular_subredes()

def decrementar_prefijo(event=None):
    current_prefix = int(prefix.get())
    if current_prefix > 1:
        prefix.set(str(current_prefix - 1))
        calcular_subredes()


def cambiar_color_fuente():
    color = colorchooser.askcolor(title="Seleccionar color de fuente")
    if color[1]:
        resultados_text.configure(foreground=color[1])

def cambiar_color_fondo_resultado():
    color = colorchooser.askcolor(title="Seleccionar color de fondo para la sección de resultado")
    if color[1]:
        resultados_text.configure(bg=color[1])

def cambiar_tamano_fuente():
    top_level = tk.Toplevel(window)
    top_level.title("Configuración de Fuente")
    top_level.geometry("300x100")
    
    tamano_actual = font.Font(font=resultados_text["font"]).actual()["size"]
    
    label_tamano = tk.Label(top_level, text="Tamaño de fuente:")
    label_tamano.pack()
    
    entry_tamano = tk.Entry(top_level)
    entry_tamano.insert(tk.END, tamano_actual)
    entry_tamano.pack()
    
    def incrementar_tamano():
        tamano_actual = int(entry_tamano.get())
        tamano_nuevo = tamano_actual + 1
        entry_tamano.delete(0, tk.END)
        entry_tamano.insert(tk.END, str(tamano_nuevo))
        resultados_text.configure(font=("Arial", tamano_nuevo))
    
    def decrementar_tamano():
        tamano_actual = int(entry_tamano.get())
        tamano_nuevo = tamano_actual - 1
        entry_tamano.delete(0, tk.END)
        entry_tamano.insert(tk.END, str(tamano_nuevo))
        resultados_text.configure(font=("Arial", tamano_nuevo))
    
    frame_botones = tk.Frame(top_level)
    frame_botones.pack()
    
    button_incrementar = tk.Button(frame_botones, text="▲", width=2, height=1, command=incrementar_tamano)
    button_incrementar.pack(side=tk.LEFT)
    
    button_decrementar = tk.Button(frame_botones, text="▼", width=2, height=1, command=decrementar_tamano)
    button_decrementar.pack(side=tk.LEFT, padx=(0, 5))
    
    
    
    def confirmar_cambio():
        tamano_nuevo = int(entry_tamano.get())
        resultados_text.configure(font=("Arial", tamano_nuevo))
        opciones_guardadas["tamano_fuente"] = tamano_nuevo
        top_level.destroy()
    
    button_confirmar = tk.Button(top_level, text="Confirmar", command=confirmar_cambio)
    button_confirmar.pack()

def guardar_perfil():
    opciones = {
        "color_fuente": resultados_text["foreground"],
        "color_fondo_resultado": resultados_text["background"],
        "tamano_fuente": font.Font(font=resultados_text["font"]).actual()["size"]

    }
    opciones_guardadas.update(opciones)
    messagebox.showinfo("Guardar perfil", "El perfil se ha guardado correctamente.")

def mostrar_about():
    messagebox.showinfo("Acerca de", "Desarrollado por [Nombre del desarrollador]")


        
# Crear la ventana principal
window = tk.Tk()
window.title("PeterH4ck-Subnetting")
window.geometry("400x500")

# Menú superior
menu_bar = tk.Menu(window)
window.config(menu=menu_bar)

# Menú Archivo
archivo_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Archivo", menu=archivo_menu)
archivo_menu.add_command(label="Guardar perfil", command=guardar_perfil)

# Menú Opciones
opciones_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Opciones", menu=opciones_menu)
opciones_menu.add_command(label="Cambiar color de fuente", command=cambiar_color_fuente)
opciones_menu.add_command(label="Cambiar color de fondo en la sección de resultado", command=cambiar_color_fondo_resultado)
opciones_menu.add_command(label="Cambiar tamaño de fuente", command=cambiar_tamano_fuente)

# Menú About
about_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="About", command=mostrar_about)

# Etiqueta y campo de entrada para la dirección IP
label_ip = tk.Label(window, text="Dirección IP:")
label_ip.pack()
entry_ip = tk.Entry(window)
entry_ip.pack()
entry_ip.bind("<Return>", aceptar_ip)

# Etiqueta para el prefijo de máscara de subred
label_prefix = tk.Label(window, text="Prefijo de Máscara:")
label_prefix.pack()

# Frame para el apartado de prefijo
frame_prefijo = tk.Frame(window)
frame_prefijo.pack()

# Botón para decrementar el prefijo
button_decrementar = tk.Button(frame_prefijo, text="▼", width=1, height=1, command=decrementar_prefijo)
button_decrementar.pack(side=tk.RIGHT, padx=2, pady=(2, 0))

# Botón para incrementar el prefijo
button_incrementar = tk.Button(frame_prefijo, text="▲", width=1, height=1, command=incrementar_prefijo)
button_incrementar.pack(side=tk.RIGHT, padx=2, pady=(0, 2))

# Campo de entrada para el prefijo de máscara de subred
prefix = tk.StringVar()
prefix_entry = tk.Entry(frame_prefijo, textvariable=prefix)
prefix_entry.pack(side=tk.RIGHT)
prefix_entry.bind("<Return>", aceptar_prefix)
prefix_entry.bind("<Up>", incrementar_prefijo)
prefix_entry.bind("<Down>", decrementar_prefijo)

# Menú desplegable para seleccionar la cantidad de subredes
label_cantidad_subredes = tk.Label(window, text="Cantidad de Subredes:")
label_cantidad_subredes.pack()
cantidad_subredes = tk.StringVar()
dropdown_cantidad_subredes = ttk.Combobox(window, textvariable=cantidad_subredes, values=list(range(1, 21)))
dropdown_cantidad_subredes.pack()
dropdown_cantidad_subredes.current(0)
dropdown_cantidad_subredes.bind("<<ComboboxSelected>>", aceptar_cantidad_subredes)
dropdown_cantidad_subredes.bind("<Return>", aceptar_cantidad_subredes)

# Botón para calcular las subredes
button_calcular = tk.Button(window, text="Calcular", command=calcular_subredes)
button_calcular.pack()

# Botón para limpiar la pantalla
button_limpiar = tk.Button(window, text="Limpiar pantalla", command=lambda: resultados_text.delete(1.0, tk.END))
button_limpiar.pack()

# Frame para el apartado de derechos de autor
frame_derechos = tk.Frame(window)
frame_derechos.pack(fill=tk.BOTH, expand=True)

# Widget Text para mostrar los resultados
resultados_text = tk.Text(window)
resultados_text.pack(fill="both", expand=True)

# Etiqueta de derechos de autor
derechos_label = tk.Label(frame_derechos, text="© PeterH4ck 2023 ©", font=("Arial", 14, "bold"))
derechos_label.pack(pady=10)

# Ejecutar el bucle principal de la interfaz gráfica
window.mainloop()
