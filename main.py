import tkinter as tk
from tkinter import messagebox, ttk
import os
import re

# --- Configuración ---
CONTACT_FILE = "friendsContact.txt" # Nombre del archivo para guardar los contactos
SEPARATOR = "!" # Separador usado en el archivo de texto

class ContactBookApp:
    """
    Una aplicación simple de Gestor de Contactos Amigos usando Tkinter.
    Gestiona contactos (nombre y número) almacenados en un archivo de texto.
    """
    def __init__(self, master):
        self.master = master
        master.title("Gestor de Contactos Python")
        master.resizable(False, False)

        # --- CONFIGURACIÓN DE ESTILO AVANZADO ---
        style = ttk.Style()
        style.theme_use('clam') # Usamos un tema base limpio
        
        # Colores personalizados
        COLOR_BACKGROUND = '#F9F9F9'
        COLOR_PRIMARY = '#1E88E5' # Azul para títulos y acentos
        COLOR_SUCCESS = '#43A047' # Verde para acciones principales
        
        # Estilos Generales
        style.configure('TFrame', background=COLOR_BACKGROUND)
        style.configure('TLabel', background=COLOR_BACKGROUND, font=('Inter', 10))
        style.configure('TEntry', fieldbackground='white', foreground='black')
        
        # Estilo para el LabelFrame (Marco de la sección)
        style.configure('TLabelFrame', background=COLOR_BACKGROUND, bordercolor='#CCCCCC', relief='flat')
        style.configure('TLabelFrame.Label', font=('Inter', 12, 'bold'), foreground=COLOR_PRIMARY)
        
        # Estilo para el botón principal (Agregar)
        style.configure('Success.TButton', 
          font=('Inter', 11, 'bold'), 
          background=COLOR_SUCCESS, 
          foreground='white',
          padding=[10, 8])
        style.map('Success.TButton', 
          background=[('active', '#5CB85C')],
          foreground=[('active', 'white')])

        # Estilo para los botones secundarios (Buscar, Eliminar, Editar)
        style.configure('Secondary.TButton', 
          font=('Inter', 10), 
          background='#607D8B', # Gris azulado
          foreground='white',
          padding=[8, 5])
        style.map('Secondary.TButton', 
          background=[('active', '#78909C')],
          foreground=[('active', 'white')])
        
        self.contacts = {} # Diccionario {nombre: número} para almacenar en memoria
        self.contact_list_var = tk.StringVar()

        # --- Frame Principal de la Aplicación ---
        main_frame = ttk.Frame(master, padding="20 20 20 20")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # --- 1. Sección de Control Unificada (Agregar, Buscar, Eliminar) ---
        self._setup_control_section(main_frame, row=0)

        # --- 2. Sección para Mostrar Contactos ---
        self._setup_display_section(main_frame, row=1)
        
        # Cargar datos iniciales del archivo
        self.load_contacts()

    def _setup_control_section(self, parent, row):
        """
        Configura la interfaz de usuario para todas las funciones de gestión 
        (Agregar, Buscar, Eliminar, Editar) en una sola sección.
        """
        # --- PUNTO CLAVE DE EXTENSIÓN: Interfaz de usuario ---
        # Los desarrolladores futuros pueden modificar el diseño (grid) dentro de este frame
        # para funciones como Editar, Exportar, etc.
        control_frame = ttk.LabelFrame(parent, 
          text="Gestión de Contactos (Agregar, Buscar, Eliminar, Editar)", 
          padding="15 15 15 15")
        control_frame.grid(row=row, column=0, pady=15, sticky="ew")

        # --- Seccion 1: Agregar Contacto ---
        ttk.Label(control_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(control_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(control_frame, text="Número:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.number_entry = ttk.Entry(control_frame, width=30)
        self.number_entry.grid(row=1, column=1, padx=5, pady=5)

        # Aplicando estilo de éxito al botón principal
        add_button = ttk.Button(control_frame, text="1. Agregar Contacto", style='Success.TButton', command=self.add_contact)
        add_button.grid(row=2, column=0, columnspan=2, pady=(10, 15))

        # Separador visual para diferenciar la acción de agregar de las acciones secundarias
        ttk.Separator(control_frame, orient='horizontal').grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)
        
        # --- Seccion 2: Buscar y Acciones Adicionales ---
        
        # Búsqueda
        ttk.Label(control_frame, text="Buscar Nombre o Número:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.search_entry = ttk.Entry(control_frame, width=30)
        self.search_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # Botón Buscar
        ttk.Button(control_frame, text="2. Buscar", style='Secondary.TButton', command=self.search_contact).grid(row=5, column=0, padx=5, pady=5, sticky="w")
        
        # Botón Eliminar (Placeholder)
        # TODO: PUNTO CLAVE DE EXTENSIÓN: Implementación de la UI para la eliminación
        ttk.Button(control_frame, text="3. Eliminar Contacto (Pendiente)", style='Secondary.TButton', command=self.delete_contact_placeholder).grid(row=5, column=1, padx=5, pady=5, sticky="w")
        
        # Botón Editar (Placeholder)
        # TODO: PUNTO CLAVE DE EXTENSIÓN: Implementación de la UI para la edición
        ttk.Button(control_frame, text="4. Editar Contacto (Pendiente)", style='Secondary.TButton', command=self.edit_contact_placeholder).grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    def delete_contact_placeholder(self):
        """Placeholder para la función de eliminar."""
        messagebox.showinfo("Funcionalidad Pendiente", "La función de eliminar contacto debe implementarse en la lógica del programa.")
        
    def edit_contact_placeholder(self):
        """Placeholder para la función de editar/actualizar."""
        # TODO: CLAVE DE EXTENSIÓN: Conectar este botón con la lógica de edición
        messagebox.showinfo("Funcionalidad Pendiente", "La función de editar/actualizar contacto debe implementarse en la lógica del programa.")

    def search_contact(self):
        """Busca y muestra contactos que coincidan con la consulta."""
        # TODO: PUNTO CLAVE DE EXTENSIÓN: Implementación de Búsqueda
        # La lógica de filtrado ya está implementada aquí, pero puede ser mejorada (e.g., búsqueda exacta).
        query = self.search_entry.get().strip().lower()
        if not query:
            self.update_display() # Si está vacío, muestra todos
            return
            
        # Filtra contactos por coincidencia de nombre o número
        filtered_contacts = {name: number for name, number in self.contacts.items() if query in name.lower() or query in number}
        self.update_display(filtered_contacts)

    def _setup_display_section(self, parent, row):
        """Configura la interfaz de usuario para mostrar todos los contactos."""
        # Aplicando el estilo LabelFrame para el título
        display_frame = ttk.LabelFrame(parent, text="Todos los Contactos", padding="15 15 15 15")
        display_frame.grid(row=row, column=0, sticky="nsew")

        # Usar un widget Text para mostrar, ya que maneja mejor el formato y el desplazamiento
        self.contact_display = tk.Text(display_frame, 
            height=15, 
            width=45, 
            state=tk.DISABLED, 
            font=('Consolas', 10), 
            wrap=tk.WORD, 
            borderwidth=2, 
            relief="sunken", # Cambiado a sunken para un mejor contraste
            bg='white')
        self.contact_display.pack(padx=5, pady=5)

    def load_contacts(self):
        """Lee el archivo de contactos y llena el diccionario interno."""
        self.contacts = {}
        if not os.path.exists(CONTACT_FILE):
            self.update_display()
            return

        try:
            with open(CONTACT_FILE, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    if SEPARATOR in line:
                        # Usamos split(SEPARATOR, 1) para manejar nombres que puedan contener el separador
                        name, number_str = line.split(SEPARATOR, 1) 
                        
                        # Almacenar el contacto en el diccionario
                        self.contacts[name.strip()] = number_str.strip()
                        
        except Exception as e:
            messagebox.showerror("Error de Archivo", f"No se pudo leer el archivo de contactos: {e}")

        self.update_display()

    def update_display(self, contacts_to_show=None):
        """Limpia y repopula el área de visualización de contactos."""
        if contacts_to_show is None:
            contacts_to_show = self.contacts
            
        self.contact_display.config(state=tk.NORMAL)
        self.contact_display.delete('1.0', tk.END)

        if not contacts_to_show:
            self.contact_display.insert(tk.END, "Aún no hay amigos guardados o no se encontraron resultados.")
        else:
            # Ordenar por nombre
            sorted_contacts = sorted(contacts_to_show.items())
            for name, number in sorted_contacts:
                self.contact_display.insert(tk.END, f"Nombre: {name}\n")
                self.contact_display.insert(tk.END, f"Número: {number}\n")
                self.contact_display.insert(tk.END, "-" * 30 + "\n")

        self.contact_display.config(state=tk.DISABLED)

    def is_duplicate(self, new_name, new_number_str):
        """Verifica si el nombre o número de contacto ya existe."""
        if new_name in self.contacts:
            return f"Error: El nombre '{new_name}' ya existe."

        # Verificación del número (revisa si el valor existe en el diccionario)
        if new_number_str in self.contacts.values():
            return f"Error: El número '{new_number_str}' ya existe."

        return None

    def add_contact(self):
        """Valida la entrada, verifica duplicados, guarda el contacto y actualiza la visualización."""
        new_name = self.name_entry.get().strip()
        new_number_str = self.number_entry.get().strip()

        # --- 1. Validación ---
        if not new_name:
            messagebox.showerror("Error de Entrada", "El campo Nombre no puede estar vacío.")
            return

        # Validación simple: solo dígitos
        if not re.fullmatch(r'\d+', new_number_str):
            messagebox.showerror("Error de Entrada", "El número debe contener solo dígitos.")
            return

        # --- 2. Verificación de Duplicados ---
        duplicate_message = self.is_duplicate(new_name, new_number_str)
        if duplicate_message:
            messagebox.showwarning("Contacto Duplicado", duplicate_message)
            return

        # --- 3. Persistencia/Escritura ---
        try:
            # Añadir el nuevo registro al archivo
            record_line = f"{new_name}{SEPARATOR}{new_number_str}\n"
            with open(CONTACT_FILE, 'a') as file:
                file.write(record_line)

            # --- 4. Actualizar estado interno e interfaz gráfica ---
            self.contacts[new_name] = new_number_str
            self.update_display()

            # Limpiar entradas
            self.name_entry.delete(0, tk.END)
            self.number_entry.delete(0, tk.END)

            messagebox.showinfo("Éxito", f"Contacto '{new_name}' agregado exitosamente.")

        except Exception as e:
            messagebox.showerror("Error al Guardar", f"Ocurrió un error al guardar el contacto: {e}")

    # --- PUNTO DE EXTENSIÓN: Lógica para funcionalidades adicionales ---

    # TODO: CLAVE DE EXTENSIÓN: Implementar Lógica de Eliminación/Actualización

    # Para implementar la funcionalidad de **Eliminar** (por ejemplo, un método llamado delete_contact_by_name):
    # 1. Obtén el nombre del contacto a eliminar (quizás del campo de búsqueda).
    # 2. Verifica si el contacto existe en self.contacts.
    # 3. Usa 'del self.contacts[nombre_a_eliminar]' para quitarlo del diccionario.
    # 4. Debes crear un nuevo método (ej. 'rewrite_contact_file') que reescriba completamente 
    #    el archivo CONTACT_FILE con los datos actualizados de self.contacts (modo 'w').
    # 5. Llama a self.update_display() para actualizar la interfaz.

    # Para implementar la funcionalidad de **Editar/Actualizar** (update_contact):
    # 1. Se necesitaría un mecanismo para seleccionar un contacto de la lista o usar su nombre.
    # 2. Una vez seleccionado, actualiza los datos (Nombre o Número) usando los campos de entrada de la sección "Agregar Contacto".
    # 3. Actualiza los datos en self.contacts.
    # 4. Llama al método para reescribir el archivo (paso 4 de Eliminación).
    # 5. Llama a self.update_display().

    
if __name__ == '__main__':
    # Inicializar la ventana principal de Tkinter
    root = tk.Tk()

    # Crear la instancia de la aplicación
    app = ContactBookApp(root)

    # Iniciar el bucle de eventos de Tkinter
    root.mainloop()