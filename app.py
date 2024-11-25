from tkinter import ttk
from tkinter import *
import sqlite3
import os
from tkinter import messagebox
#----------------------
# CONFIGURACIÓN GENERAL
#----------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Directorio base del proyecto
DB_PATH = os.path.join(BASE_DIR, 'datos', 'luxury-wheels.db')  # Ruta de la base de datos
LOGO_PATH = os.path.join(BASE_DIR, 'recursos', 'logo_empresa.ico')  # Ruta del logo
IMAGES_DIR = os.path.join(BASE_DIR, 'recursos', 'vehiculos')  # Carpeta de imágenes de vehículos


# -----------------------------
# CONEXIÓN A LA BASE DE DATOS
# -----------------------------
def conectar_db():
    """Conectar a la base de datos."""
    return sqlite3.connect(DB_PATH)

# -----------------------------------------
# CLASE PRINCIPAL: GESTIÓN DE LA APLICACIÓN
# -----------------------------------------
class luxurywheelsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Luxury-Wheels- Gestor de veiculos")
        self.root.geometry("800x600")
        self.root.wm_iconbitmap('recursos/imapp.ico')

    # Componentes de la ventana principal
        self.create_main_interface()

    def create_main_interface(self):
        """Crear la interfaz principal."""
        Label(self.root, text="¡Bienvenido a Luxury Wheels!", font=("Arial", 16, "bold")).pack(pady=20)

        # Botones para funcionalidades principales
        Button(self.root, text="Gestión de Usuarios", command=self.abrir_gestion_usuarios, width=20).pack(pady=10)
        Button(self.root, text="Gestión de Vehículos", command=self.abrir_gestion_vehiculos, width=20).pack(pady=10)
        Button(self.root, text="Gestión de Reservas", command=self.abrir_gestion_reservas, width=20).pack(pady=10)

    # -----------------------------------------
    # FUNCIONES DE GESTIÓN
    # -----------------------------------------
    def abrir_gestion_usuarios(self):
        """Abrir la ventana de gestión de usuarios."""
        VentanaUsuarios(self.root)

    def abrir_gestion_vehiculos(self):
        """Abrir la ventana de gestión de vehículos."""
        VentanaVehiculos(self.root)

    def abrir_gestion_reservas(self):
        """Abrir la ventana de gestión de reservas."""
        VentanaReservas(self.root)

# -----------------------------------------
# CLASES PARA CADA SECCIÓN
# -----------------------------------------
class VentanaUsuarios:
    def __init__(self, parent):
        self.window = Toplevel(parent)
        self.window.title("Gestión de Usuarios")
        self.window.geometry("500x400")

        Label(self.window, text="Gestión de Usuarios", font=("Arial", 14, "bold")).pack(pady=10)
        Button(self.window, text="Registrar Usuario", command=self.registrar_usuario).pack(pady=5)
        Button(self.window, text="Listar Usuarios", command=self.listar_usuarios).pack(pady=5)

    def registrar_usuario(self):
        """Registrar un nuevo usuario."""
        # Crear ventana de registro
        self.registro_window = Toplevel(self.window)
        self.registro_window.title("Registrar Usuario")
        self.registro_window.geometry("400x300")

        Label(self.registro_window, text="Nombre:").pack(pady=5)
        self.nombre_entry = Entry(self.registro_window)
        self.nombre_entry.pack(pady=5)

        Label(self.registro_window, text="Rol:").pack(pady=5)
        self.rol_entry = Entry(self.registro_window)
        self.rol_entry.pack(pady=5)

        Button(self.registro_window, text="Registrar", command=self.guardar_usuario).pack(pady=20)

    def guardar_usuario(self):
        """Guardar los datos del nuevo usuario en la base de datos."""
        nombre = self.nombre_entry.get()
        rol = self.rol_entry.get()

        # Validación básica
        if not nombre or not rol:
            messagebox.showerror("Error", "Por favor complete todos los campos.")
            return

        # Insertar en la base de datos
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, rol) VALUES (?, ?)", (nombre, rol))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")
        self.registro_window.destroy()  # Cerrar la ventana de registro
    def listar_usuarios(self):
        """Listar todos los usuarios."""
        self.usuarios_lista = Toplevel(self.window)
        self.usuarios_lista.title("Lista de Usuarios")
        self.usuarios_lista.geometry("500x300")

        # Crear el Treeview para mostrar los usuarios
        tree = ttk.Treeview(self.usuarios_lista, columns=("ID", "Nombre", "Rol"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Rol", text="Rol")
        tree.pack(fill=BOTH, expand=True)

        # Cargar usuarios de la base de datos
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios")  # Asegúrate de tener una tabla 'usuarios' en la base de datos
        usuarios = cursor.fetchall()
        conn.close()

        for usuario in usuarios:
            tree.insert("", "end", values=usuario)

        # Opciones para editar o eliminar usuario
        tree.bind("<Double-1>", self.editar_usuario)

        def editar_usuario(self, event):
            """Editar los detalles de un usuario."""
            item = event.widget.item(event.widget.focus())
            usuario_id = item['values'][0]  # Obtener el ID del usuario seleccionado
            EditarUsuario(self.window, usuario_id)

    # Clase para editar un usuario
    class EditarUsuario:
        def __init__(self, parent, usuario_id):
            self.window = Toplevel(parent)
            self.window.title("Editar Usuario")
            self.window.geometry("400x300")
            self.usuario_id = usuario_id

            # Obtener los datos del usuario a editar
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, rol FROM usuarios WHERE id = ?", (self.usuario_id,))
            usuario = cursor.fetchone()
            conn.close()

            # Etiquetas y campos de entrada para editar
            Label(self.window, text="Nombre:").pack(pady=5)
            self.nombre = Entry(self.window)
            self.nombre.insert(0, usuario[0])
            self.nombre.pack(pady=5)

            Label(self.window, text="Rol:").pack(pady=5)
            self.rol = Entry(self.window)
            self.rol.insert(0, usuario[1])
            self.rol.pack(pady=5)

            # Botón para guardar los cambios
            Button(self.window, text="Guardar cambios", command=self.guardar_cambios).pack(pady=20)

        def guardar_cambios(self):
            """Guardar los cambios realizados en el usuario."""
            nombre = self.nombre.get()
            rol = self.rol.get()

            if not nombre or not rol:
                messagebox.showerror("Error", "Por favor complete todos los campos.")
                return

            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET nombre = ?, rol = ? WHERE id = ?", (nombre, rol, self.usuario_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Datos del usuario actualizados.")
            self.window.destroy()

    # Clase para eliminar un usuario
    class EliminarUsuario:
        def __init__(self, parent, usuario_id):
            self.window = Toplevel(parent)
            self.window.title("Eliminar Usuario")
            self.window.geometry("300x200")
            self.usuario_id = usuario_id

            # Confirmación para eliminar
            Label(self.window, text="¿Está seguro de eliminar este usuario?").pack(pady=10)

            Button(self.window, text="Sí", command=self.eliminar).pack(pady=5)
            Button(self.window, text="No", command=self.window.destroy).pack(pady=5)

        def eliminar(self):
            """Eliminar el usuario de la base de datos."""
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (self.usuario_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
            self.window.destroy()

class VentanaVehiculos:
    def __init__(self, parent):
        self.window = Toplevel(parent)
        self.window.title("Gestión de Vehículos")
        self.window.geometry("600x500")

        Label(self.window, text="Gestión de Vehículos", font=("Arial", 14, "bold")).pack(pady=10)
        Button(self.window, text="Añadir Vehículo", command=self.anadir_vehiculo).pack(pady=5)
        Button(self.window, text="Listar Vehículos", command=self.listar_vehiculos).pack(pady=5)

    def anadir_vehiculo(self):
        """Añadir un nuevo vehículo."""
        # Lógica para añadir vehículos.
        messagebox.showinfo("Añadir", "Función para añadir vehículos aún no implementada.")

    def listar_vehiculos(self):
        """Listar todos los vehículos."""
        # Lógica para consultar y mostrar vehículos desde la base de datos.
        messagebox.showinfo("Listado", "Función de listado aún no implementada.")

class VentanaReservas:
    def __init__(self, parent):
        self.window = Toplevel(parent)
        self.window.title("Gestión de Reservas")
        self.window.geometry("600x500")

        Label(self.window, text="Gestión de Reservas", font=("Arial", 14, "bold")).pack(pady=10)
        Button(self.window, text="Crear Reserva", command=self.crear_reserva).pack(pady=5)
        Button(self.window, text="Listar Reservas", command=self.listar_reservas).pack(pady=5)

    def crear_reserva(self):
        """Crear una nueva reserva."""
        # Lógica para crear reservas.
        messagebox.showinfo("Reserva", "Función de crear reservas aún no implementada.")

    def listar_reservas(self):
        """Listar todas las reservas."""
        # Lógica para consultar y mostrar reservas desde la base de datos.
        messagebox.showinfo("Listado", "Función de listado aún no implementada.")

# -----------------------------------------
# FUNCIONES DE BASE DE DATOS
# -----------------------------------------
def conectar_db():
    """Establece conexión con la base de datos."""
    return sqlite3.connect(DB_PATH)


# -----------------------------------------
# EJECUCIÓN PRINCIPAL
# -----------------------------------------



if __name__ == '__main__':
    root = Tk() # Instância da janela principal
    app = luxurywheelsApp(root) # Envia-se para a classe Produto o controlo sobre a janela root
    root.mainloop() # Começamos o ciclo de aplicação, é como um while True


