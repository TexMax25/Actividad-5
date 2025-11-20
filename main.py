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
        COLOR_PRIMARY = '#11E88E5' # Azul para títulos y acentos
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
        control_frame = ttk.LabelFrame(parent, 
            text="Gestión de Contactos (Agregar, Buscar, Eliminar, Editar)", 
            padding="15 15 15 15")
        control_frame.grid(row=row, column=0, pady=15, sticky="ew")

        ttk.Label(control_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(control_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(control_frame, text="Número:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.number_entry = ttk.Entry(control_frame, width=30)
        self.number_entry.grid(row=1, column=1, padx=5, pady=5)

        add_button = ttk.Button(control_frame, text="1. Agregar Contacto", style='Success.TButton', command=self.add_contact)
        add_button.grid(row=2, column=0, columnspan=2, pady=(10, 15))

        ttk.Separator(control_frame, orient='horizontal').grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)
        
        ttk.Label(control_frame, text="Buscar Nombre o Número:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.search_entry = ttk.Entry(control_frame, width=30)
        self.search_entry.grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Button(control_frame, text="2. Buscar", style='Secondary.TButton', command=self.search_contact).grid(row=5, column=0, padx=5, pady=5, sticky="w")
        
        ttk.Button(control_frame, 
           text="3. Eliminar Contacto",
           style='Secondary.TButton',
           command=self.delete_contact).grid(row=5, column=1, padx=5, pady=5, sticky="w")
        
        ### --- UPDATE AGREGADO: botón editar REAL ---
        ttk.Button(control_frame, text="4. Editar Contacto", style='Secondary.TButton', command=self.edit_contact).grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    def delete_contact(self):
        """Elimina un contacto por nombre usando el campo de búsqueda."""
        name_to_delete = self.search_entry.get().strip()
    
        if not name_to_delete:
            messagebox.showerror("Error", "Debes escribir el nombre del contacto a eliminar.")
            return
    
        # Verificar existencia
        if name_to_delete not in self.contacts:
            messagebox.showwarning("No encontrado", f"El contacto '{name_to_delete}' no existe.")
            return
    
        # Confirmación
        confirm = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Deseas eliminar el contacto '{name_to_delete}'?"
        )
        if not confirm:
            return
    
        # 1. Eliminar del diccionario
        del self.contacts[name_to_delete]
    
        # 2. Reescribir el archivo completo
        try:
            with open(CONTACT_FILE, "w") as f:
                for name, number in self.contacts.items():
                    f.write(f"{name}{SEPARATOR}{number}\n")
        except Exception as e:
            messagebox.showerror("Error al Guardar", f"Hubo un error reescribiendo el archivo: {e}")
            return
    
        # 3. Actualizar interfaz
        self.update_display()
    
        # 4. Mensaje éxito
        messagebox.showinfo("Éxito", f"Contacto '{name_to_delete}' eliminado exitosamente.")

        
    def edit_contact_placeholder(self):
        messagebox.showinfo("Funcionalidad Pendiente", "La función de editar/actualizar contacto debe implementarse en la lógica del programa.")

    def search_contact(self):
        query = self.search_entry.get().strip().lower()
        if not query:
            self.update_display()
            return
            
        filtered_contacts = {name: number for name, number in self.contacts.items() if query in name.lower() or query in number}
        self.update_display(filtered_contacts)

    def _setup_display_section(self, parent, row):
        display_frame = ttk.LabelFrame(parent, text="Todos los Contactos", padding="15 15 15 15")
        display_frame.grid(row=row, column=0, sticky="nsew")

        self.contact_display = tk.Text(display_frame, 
            height=15, 
            width=45, 
            state=tk.DISABLED, 
            font=('Consolas', 10), 
            wrap=tk.WORD, 
            borderwidth=2, 
            relief="sunken",
            bg='white')
        self.contact_display.pack(padx=5, pady=5)

    def load_contacts(self):
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
                        name, number_str = line.split(SEPARATOR, 1) 
                        self.contacts[name.strip()] = number_str.strip()
                        
        except Exception as e:
            messagebox.showerror("Error de Archivo", f"No se pudo leer el archivo de contactos: {e}")

        self.update_display()

    def update_display(self, contacts_to_show=None):
        if contacts_to_show is None:
            contacts_to_show = self.contacts
            
        self.contact_display.config(state=tk.NORMAL)
        self.contact_display.delete('1.0', tk.END)

        if not contacts_to_show:
            self.contact_display.insert(tk.END, "Aún no hay amigos guardados o no se encontraron resultados.")
        else:
            sorted_contacts = sorted(contacts_to_show.items())
            for name, number in sorted_contacts:
                self.contact_display.insert(tk.END, f"Nombre: {name}\n")
                self.contact_display.insert(tk.END, f"Número: {number}\n")
                self.contact_display.insert(tk.END, "-" * 30 + "\n")

        self.contact_display.config(state=tk.DISABLED)

    def is_duplicate(self, new_name, new_number_str):
        if new_name in self.contacts:
            return f"Error: El nombre '{new_name}' ya existe."

        if new_number_str in self.contacts.values():
            return f"Error: El número '{new_number_str}' ya existe."

        return None

    def add_contact(self):
        new_name = self.name_entry.get().strip()
        new_number_str = self.number_entry.get().strip()

        if not new_name:
            messagebox.showerror("Error de Entrada", "El campo Nombre no puede estar vacío.")
            return

        if not re.fullmatch(r'\d+', new_number_str):
            messagebox.showerror("Error de Entrada", "El número debe contener solo dígitos.")
            return

        duplicate_message = self.is_duplicate(new_name, new_number_str)
        if duplicate_message:
            messagebox.showwarning("Contacto Duplicado", duplicate_message)
            return

        try:
            record_line = f"{new_name}{SEPARATOR}{new_number_str}\n"
            with open(CONTACT_FILE, 'a') as file:
                file.write(record_line)

            self.contacts[new_name] = new_number_str
            self.update_display()

            self.name_entry.delete(0, tk.END)
            self.number_entry.delete(0, tk.END)

            messagebox.showinfo("Éxito", f"Contacto '{new_name}' agregado exitosamente.")

        except Exception as e:
            messagebox.showerror("Error al Guardar", f"Ocurrió un error al guardar el contacto: {e}")

    # --- PUNTO DE EXTENSIÓN: Lógica para funcionalidades adicionales ---
    # TODO: implementar lógica de eliminación
    # TODO: implementar lógica de actualización

    ### --------------------------------------------------------------------
    ### ---------------------- UPDATE AGREGADO ------------------------------
    ### --------------------------------------------------------------------

    def edit_contact(self):
        """Ventana emergente para seleccionar un contacto y editarlo."""
        
        if not self.contacts:
            messagebox.showwarning("Advertencia", "No hay contactos para editar.")
            return
        
        # ventana emergente
        edit_win = tk.Toplevel(self.master)
        edit_win.title("Editar Contacto")
        edit_win.resizable(False, False)

        ttk.Label(edit_win, text="Seleccione contacto:").pack(pady=5)

        # selector de contactos
        contact_names = list(self.contacts.keys())
        selected_var = tk.StringVar(value=contact_names[0])
        contact_menu = ttk.Combobox(edit_win, values=contact_names, textvariable=selected_var, state="readonly")
        contact_menu.pack(pady=5)

        ttk.Label(edit_win, text="Nuevo Nombre:").pack(pady=5)
        entry_name = ttk.Entry(edit_win, width=30)
        entry_name.pack()

        ttk.Label(edit_win, text="Nuevo Número:").pack(pady=5)
        entry_number = ttk.Entry(edit_win, width=30)
        entry_number.pack()

        def load_fields(*args):
            """Carga el contacto en los campos."""
            name = selected_var.get()
            entry_name.delete(0, tk.END)
            entry_number.delete(0, tk.END)
            entry_name.insert(0, name)
            entry_number.insert(0, self.contacts[name])

        # cargar inicialmente
        load_fields()
        selected_var.trace("w", load_fields)

        ttk.Button(edit_win, text="Guardar Cambios", style="Success.TButton",
            command=lambda: self.update_contact(selected_var.get(),
                    entry_name.get().strip(),
                    entry_number.get().strip(),
                    edit_win)).pack(pady=10)

    def update_contact(self, old_name, new_name, new_number, window_ref):
        """Actualiza el contacto en memoria, reescribe archivo y actualiza interfaz."""
        
        # Validaciones
        if not new_name or not new_number:
            messagebox.showerror("Error", "Los campos no pueden estar vacíos.")
            return
        
        if not re.fullmatch(r'\d+', new_number):
            messagebox.showerror("Error", "El número debe contener solo dígitos.")
            return

        # Verifica duplicados si se cambia el nombre
        if new_name != old_name and new_name in self.contacts:
            messagebox.showerror("Error", f"El nombre '{new_name}' ya existe.")
            return

        # Actualizar en memoria
        self.contacts.pop(old_name)
        self.contacts[new_name] = new_number

        # Reescribir archivo como en todo el programa
        try:
            with open(CONTACT_FILE, "w") as file:
                for name, number in self.contacts.items():
                    file.write(f"{name}{SEPARATOR}{number}\n")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar cambios: {e}")
            return

        self.update_display()
        window_ref.destroy()
        messagebox.showinfo("Éxito", "Contacto actualizado correctamente.")

### --------------------------------------------------------------------

if __name__ == '__main__':
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()
