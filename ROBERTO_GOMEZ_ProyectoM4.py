# Roberto Gomez Proyecto M4 31/05/2025
#Construye una pokedex
import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import io

# Obtendremos la url de la pagina
def obtener_pokemon(nombre):
    url = f"https://pokeapi.co/api/v2/pokemon/{nombre.lower()}"
    respuesta = requests.get(url)

    # Ahora especificaremos las caracteristicas del pokemon
    if respuesta.status_code == 200:
        datos = respuesta.json()
        pokemon_info = {
            "Nombre": datos["name"].capitalize(),
            "Imagen": datos["sprites"]["front_default"],
            "Peso": datos["weight"] / 10,
            "Altura": datos["height"] / 10,
            "Movimientos": [movimiento["move"]["name"] for movimiento in datos["moves"][:5]],
            "Habilidades": [habilidad["ability"]["name"] for habilidad in datos["abilities"]],
            "Tipos": [tipo["type"]["name"] for tipo in datos["types"]]
        }
        return pokemon_info
    else:
        return None
    
# El usuario tendra que escribir el nombre correcto
def mostrar_pokemon():
    nombre_pokemon = entrada.get().strip()
    if not nombre_pokemon:
        messagebox.showerror("Hay un error", "Escribe un nombre de Pokémon.")
        return

    pokemon = obtener_pokemon(nombre_pokemon)
    if pokemon:
        nombre_label.config(text=f"Nombre: {pokemon['Nombre']}")
        peso_label.config(text=f"Peso: {pokemon['Peso']} kg")
        altura_label.config(text=f"Altura: {pokemon['Altura']} m")
        movimientos_label.config(text=f"Movimientos: {', '.join(pokemon['Movimientos'])}")
        habilidades_label.config(text=f"Habilidades: {', '.join(pokemon['Habilidades'])}")
        tipos_label.config(text=f"Tipos: {', '.join(pokemon['Tipos'])}")

        # Cargar imagen del pokemon elegido
        imagen_url = pokemon["Imagen"]
        imagen_respuesta = requests.get(imagen_url)
        imagen_bytes = io.BytesIO(imagen_respuesta.content)
        imagen_pil = Image.open(imagen_bytes)
        imagen_tk = ImageTk.PhotoImage(imagen_pil)

        imagen_label.config(image=imagen_tk)
        imagen_label.image = imagen_tk

        # Esto por si escribe mal o no esta el pokemon
    else:
        messagebox.showerror("Hay un error", "Pokémon no encontrado.")

# Creamos una ventana
ventana = tk.Tk()
ventana.title("Pokédex")

# Creamos un Widgets
entrada = tk.Entry(ventana)
entrada.pack(pady=5)

buscar_btn = tk.Button(ventana, text="Buscar Pokémon", command=mostrar_pokemon)
buscar_btn.pack(pady=5)

nombre_label = tk.Label(ventana, text="Nombre:")
nombre_label.pack()
peso_label = tk.Label(ventana, text="Peso:")
peso_label.pack()
altura_label = tk.Label(ventana, text="Altura:")
altura_label.pack()
movimientos_label = tk.Label(ventana, text="Movimientos:")
movimientos_label.pack()
habilidades_label = tk.Label(ventana, text="Habilidades:")
habilidades_label.pack()
tipos_label = tk.Label(ventana, text="Tipos:")
tipos_label.pack()

imagen_label = tk.Label(ventana)
imagen_label.pack()

# Ejecutar ventana
ventana.mainloop()