import flet as ft
from core.crear_carpeta import FolderCreatorLogic
from core.crear_entorno import crear_entorno_virtual
from core.django_manager import DjangoManager
from core.bd_config import DatabaseConfig
from pathlib import Path
import subprocess
import os

class UI:

    def __init__(self, page:ft.Page):
        self.page = page
        self.logic = FolderCreatorLogic(page)
        self.txt_folder_name =ft.TextField(
            label="Ej: Mi proyecto",
            width=150,
            height=40,
            on_change=self.update_folder_name
        )
        self.ruta_base=""
        self.lbl_path = ft.Text("Ninguna", style=ft.TextThemeStyle.BODY_SMALL)
        self.database_choice="sqlite"
        self.db_config = DatabaseConfig()
        self.django_manager = DjangoManager()

        

        self.dd_apps = ft.Dropdown(
            options=[],
            label="Selecciona una app",
            width=200
        )

        self.txt_entorno = ft.TextField(
            label="Ej venv",
            width= 200,
            height=40
        )

        self.txt_tabla = ft.TextField(
            label="Ingresa el nombre de la tabla",
            width=280,
            height=40
        )

        self.txt_nombre_proyecto = ft.TextField(
            label="Ej: Mi proyecto",
            width=200,
            height=40
        )

        self.panel_tablas = self._crear_panel_tablas()

            #VARIABLES PARA APPS/CREAR APPS
        self.apps_a_crear = []
        self.txt_nombre_app = ft.TextField(
            label="Ej: usuarios",
            width=200,
            height=40
        )

        self.apps_generadas=[]
        self.lista_apps = ft.Column()  

        self.color_teal = "teal"

        self.contenedor1 = ft.Container(
            col=4,
            expand=True,
            bgcolor=self.color_teal,
            border_radius=10,
            padding=10,
            content=ft.Column(
                #Contenedor1
                expand=True,
                controls=[
                    ft.Container(
                        expand=True,
                        alignment=ft.alignment.center,
                        content=ft.Row(
                            controls=[
                                ft.Text("Crear carpeta del proyecto", size=20, weight=ft.FontWeight.BOLD)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ),
                    ft.Divider(
                        height=1,
                        color="black"
                    ),
                    ft.Row(
                        expand=True,
                        controls=[
                            ft.Container(               #Contenedor1
                                expand=True,
                                height= 180,
                                content=ft.Column(
                                    controls=[
                                        ft.Text("Nombre de la carpeta:", weight=ft.FontWeight.BOLD),
                                        self.txt_folder_name,
                                        ft.ElevatedButton(
                                            "Seleccionar ubicaciion",
                                            icon=ft.icons.FOLDER_OPEN,
                                            on_click= self.select_folder
                                        ),
                                        ft.Row([
                                            ft.Text("Ubicacion seleccionada:", style=ft.TextThemeStyle.BODY_SMALL),
                                            self.lbl_path
                                        ]
                                        )
                                        
                                    ],
                                    spacing=10
                                ),
                                padding=20
                            ), 
                            ft.Container(
                                width=100,
                                alignment=ft.alignment.center,
                                content=ft.ElevatedButton(
                                    content=ft.Text("ACEPTAR", color="white"),
                                    bgcolor="#4CAF50",
                                    height=40,
                                    on_click=self.create_folder,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=2),
                                        overlay_color="#FFFFFF"
                                    )
                                )
                            )                     
                        ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                ]
            )

        )

        self.contenedor2 = ft.Container(
            col=4,
            expand=True,
            bgcolor=self.color_teal,
            border_radius=10,
            padding=10,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Container(
                        expand=True,
                        alignment=ft.alignment.center,
                        content=ft.Row(
                            controls=[
                                ft.Text("Crear entonrno virtual", size=20, weight=ft.FontWeight.BOLD),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ),
                    ft.Divider(height=1, color="black"),
                    ft.Row(
                        expand=True,
                        controls=[
                            ft.Container(
                                expand=True,
                                height=180,
                                content=ft.Column(
                                    controls=[
                                        ft.Text("Ingresa el nombre de tu entorno virtual", weight=ft.FontWeight.BOLD),
                                        self.txt_entorno,
                                        ft.Text("Ingresa el nombre del proyecto Django", weight=ft.FontWeight.BOLD),
                                        self.txt_nombre_proyecto
                                    ],
                                    spacing=5
                                ),
                                padding=8
                            ),
                            ft.Container(
                                width=100,
                                alignment=ft.alignment.center,
                                content=ft.ElevatedButton(
                                    content=ft.Text("ACEPTAR", color="white"),
                                    bgcolor="#4CAF50",
                                    height=40,
                                    on_click=self.crear_entorno_handler,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=2),
                                        overlay_color=ft.colors.with_opacity(0.1, "white")
                                    )
                                )
                            )
                        ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                ]
            )
        )

        self.contenedor3 = ft.Container(
            col=4,
            expand=True,
            bgcolor=self.color_teal,
            border_radius=10,
            padding=10,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Container(
                        expand=True,
                        alignment=ft.alignment.center,
                        content=ft.Row(
                            controls=[
                                ft.Text("Tipo de Base de Datos", size=20, weight=ft.FontWeight.BOLD)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                           
                        )
                    ),
                    ft.Divider(height=1, color="black"),
                    
                    ft.Row(
                        expand=True,
                        controls=[
                            ft.Container(
                                expand=True,
                                height=180,
                                content=ft.Column(
                                    
                                    controls=[
                                        ft.Text("Seleccione que tipo de base de datos usar:", size=20, weight=ft.FontWeight.BOLD),
                                        
                                        ft.RadioGroup(
                                            content=ft.Row([
                                                ft.Radio(value="sqlite", label="SQLite"),
                                                ft.Radio(value="post", label="PostgreSQL")
                                            ]),
                                            value="sqlite",
                                            on_change= self.update_db_choice
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                )
                            ),
                            ft.Container(
                                width=100,
                                alignment=ft.alignment.center,
                                content=ft.ElevatedButton(
                                    content=ft.Text("ACEPTAR", color="white"),
                                    bgcolor="#4CAF50",
                                    height=40,
                                    on_click=self.save_db_config,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=2),
                                        overlay_color=ft.colors.with_opacity(0.1, "white")
                                    )
                                )
                            )
                        ]
                    )
                ]
            )
        )

        self.contenedor4 = ft.Container(
            col=4,
            expand=True,
            bgcolor=self.color_teal,
            border_radius=10,
            padding=10,
            content=self.panel_tablas
        )

        self.contenedor5 = ft.Container(
            col=4,
            expand=True,
            bgcolor=self.color_teal,
            border_radius=10,
            padding=10,
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text("Crear Apps Django", size=20, weight="bold")
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ),
                    ft.Divider(height=1, color="black"),
                    ft.Column(
                        controls=[
                            ft.Text("Nombre de la App:", weight="bold"),
                            self.txt_nombre_app,
                            ft.ElevatedButton(
                                "Añadir App",
                                icon=ft.icons.ADD,
                                on_click=self.añadir_app
                            ),
                            ft.Text("Apps a crear:", weight="bold"),
                            self.lista_apps,
                            ft.ElevatedButton(
                                "Generar Apps",
                                icon=ft.icons.CHECK,
                                on_click=self.generar_apps,
                                bgcolor="#4CAF50",
                                color="white"
                            )
                        ],
                        spacing=15
                    )
                ],
                expand=True
            )
        )


        self.contenedores = ft.ResponsiveRow(
            controls=[
                self.contenedor1,
                self.contenedor2,
                self.contenedor3,
                self.contenedor5,
                self.contenedor4
            ]
        )
    
    async def crear_entorno_handler(self, e):
        nombre_entorno = self.txt_entorno.value.strip()
        nombre_proyecto = self.txt_nombre_proyecto.value.strip()
        
        if not nombre_entorno or not nombre_proyecto:
            print("Ingresa nombres para entorno y proyecto")
            return
        try:
            self.nombre_proyecto = nombre_proyecto 
            # Crear entorno Y proyecto
            resultado = crear_entorno_virtual(
                nombre_entorno,
                self.ruta_base,
                nombre_proyecto
            )
            print(resultado)
            
            # Actualizar ruta base para las apps
            self.ruta_proyecto = str(Path(self.ruta_base) / nombre_proyecto)
            self.page.update()
            
        except Exception as ex:
            print(f" Error: {str(ex)}")
    
    def update_db_choice(self, e):
        self.database_choice = e.control.value  # Guarda la selección
        print(f"Base de datos seleccionada: {self.database_choice}")  # Para debug

    def save_db_config(self, e):
        if not hasattr(self, 'database_choice'):  # Validación adicional
            self.database_choice = "sqlite"
        
        self.db_config.set_database_type(self.database_choice)
        
        if self.database_choice == "post":
            # Aquí puedes pedir los datos de PostgreSQL si es necesario
            self.db_config.set_postgres_config(
                name="mydb",  # Estos valores deberían venir de inputs
                user="postgres",
                password="secret",
                host="localhost",
                port="5432"
            )
        print(f"Configuración {self.database_choice.upper()} guardada")

    def _validar_campos_modelo(self) -> tuple:
        nombres_campos = []
        for row in self.campos_column.controls[1:]:  
            if isinstance(row, ft.Row) and len(row.controls) >= 2:
                nombre = row.controls[0].value.strip()
                if nombre:  
                    nombres_campos.append(nombre)
        
        # Verificar duplicados
        if len(nombres_campos) != len(set(nombres_campos)):
            return False, nombres_campos
        return True, nombres_campos
    
    async def guardar_modelo(self, e):
        try:
            nombre_tabla = self.txt_tabla.value.strip()
            if not nombre_tabla:
                print("Ingresa un nombre para la tabla")
                return
            
            if not self.dd_apps.value:
                print("Selecciona una app primero")
                return
    
            app_name = self.dd_apps.value.replace(" (pendiente)", "")
            app_dir = Path(self.ruta_proyecto) / "apps" / app_name
            app_dir.mkdir(parents=True, exist_ok=True)
                    
            models_path = app_dir / "models.py"
            modelo_existente = ""
            if models_path.exists():
                with open(models_path, "r") as f:
                    modelo_existente = f.read()

            if "from django.db import models" not in modelo_existente:
                modelo_existente = "from django.db import models\n\n" + modelo_existente
            campos = self.obtener_campos()
            codigo_modelo = f"\nclass {nombre_tabla}(models.Model):\n"
            for campo in campos:
                codigo_modelo += f"    {campo['name']} = models.{campo['type']}()\n"
            
            with open(models_path, "w") as f:
                f.write(modelo_existente + codigo_modelo)
            
            admin_path = app_dir / "admin.py"
            admin_existente = ""
            if admin_path.exists():
                with open(admin_path, "r") as f:
                    admin_existente = f.read()
            
            if "from django.contrib import admin" not in admin_existente:
                admin_existente = "from django.contrib import admin\n\n" + admin_existente
        
            if f"from .models import {nombre_tabla}" not in admin_existente:
                admin_existente += f"\nfrom .models import {nombre_tabla}\n"
            
            if f"admin.site.register({nombre_tabla})" not in admin_existente:
                admin_existente += f"\nadmin.site.register({nombre_tabla})\n"
            
            with open(admin_path, "w") as f:
                f.write(admin_existente)
            
            print(f"Modelo '{nombre_tabla}' creado en {app_name}/models.py")

            if hasattr(self, 'ruta_proyecto') and self.ruta_proyecto:
                try:
                    venv_python = str(Path(self.ruta_base) / "venv" / ("Scripts" if os.name == "nt" else "bin") / "python")
                    manage_py = Path(self.ruta_proyecto) / "manage.py"
                    
                    if venv_python and manage_py.exists():
                        subprocess.run(
                            [venv_python, str(manage_py), "makemigrations", app_name],
                            check=True,
                            cwd=str(self.ruta_proyecto))
                        subprocess.run(
                            [venv_python, str(manage_py), "migrate"],
                            check=True,
                            cwd=str(self.ruta_proyecto))
                        print("¡Migraciones aplicadas exitosamente!")
                except subprocess.CalledProcessError as e:
                    print(f"Error en migraciones: {e.stderr}")
                
            self.page.update()

        except Exception as ex:
            print(f"Error al guardar modelo: {str(ex)}")   


    def obtener_campos(self) -> list:
        """Recolecta campos desde la UI"""
        campos = []
        for row in self.campos_column.controls[1:]:  # Saltar encabezado
            if isinstance(row, ft.Row):
                nombre = row.controls[0].value
                tipo = row.controls[1].value
                campos.append({
                    "name": nombre,
                    "type": tipo,
                    # Agregar más parámetros según necesidad
                })
        return campos
    

    async def generar_proyecto(self, e):
        try:
            if not self.ruta_base:
                raise ValueError("Selecciona una ubicación para el proyecto primero")

            project_path = Path(self.ruta_proyecto) if hasattr(self, 'ruta_proyecto') else Path(self.ruta_base) / "Mi_proyecto"
            
            # 1. Generar archivos de configuración (settings.py, etc.)
            self.db_config.generate_files(str(project_path))
            
            venv_python = str(Path(self.ruta_base) / "venv" / ("Scripts" if os.name == "nt" else "bin") / "python")
            manage_py = project_path / "manage.py"
            
            if not manage_py.exists():
                if not hasattr(self, 'django_manager'):
                    self.django_manager = DjangoManager()
                
                success = self.django_manager.create_standard_project(
                    env_path=str(Path(self.ruta_base) / "venv"),
                    project_name="Mi_proyecto",
                    project_dir=str(project_path.parent)  # ¡Cambio crucial aquí!
                )
                if not success:
                    raise Exception("Falló la creación del proyecto base Django")
            
            if manage_py.exists():
                try:
                    subprocess.run(
                        [venv_python, str(manage_py), "makemigrations"],
                        check=True,
                        cwd=str(project_path)
                    )
                    subprocess.run(
                        [venv_python, str(manage_py), "migrate"],
                        check=True,
                        cwd=str(project_path)
                    )
                    print("¡Proyecto configurado y migraciones aplicadas!")
                except subprocess.CalledProcessError as e:
                    print(f"Error en migraciones: {e.stderr}")
            else:
                print("No se encontró manage.py")
                
        except Exception as ex:
            print(f"Error crítico: {str(ex)}")

    def update_folder_name(self, e):
        folder_name = e.control.value.strip()
        if not folder_name:
            print("El nombre no puede estar vacío")
            return

        invalid_chars = set('/\\:*?"<>|')
        if any(char in invalid_chars for char in folder_name):
            print("Nombre inválido: no usar /, \\, :, *, ?, \", <, >, |")
            return
        
        self.logic.folder_name = folder_name
        self.txt_folder_name.value = folder_name
        self.page.update()
    
    async def select_folder(self, e):
            
            try:
                selected_path = await self.logic.open_folder_dialog()
                if selected_path:
                    selected_path = os.path.normpath(selected_path)
                    self.ruta_base = selected_path
                    self.lbl_path.value = selected_path
                    self.lbl_path.color = ft.colors.BLACK
                    self.page.update()
            except Exception as e:
                print(f"Error al seleccionar carpeta: {e}")
                self.page.snack_bar = ft.SnackBar(
                    ft.Text(f"Error: {str(e)}"),
                    bgcolor=ft.colors.RED
                )
                self.page.snack_bar.open = True
                self.page.update()

    async def create_folder(self, e):
        if not hasattr(self, 'logic'):
            print("Error interno: no se pudo inicializar la lógica de carpetas")
            return
        #Crear carpeta
        success, message, full_path = self.logic.create_folder_action()
        if success:
            self.ruta_base= os.path.normpath(full_path)
            self.lbl_path.value = full_path
            self.lbl_path.color = ft.colors.BLACK

        self.page.snack_bar = ft.SnackBar(
            ft.Text(message),
            bgcolor=ft.colors.GREEN_800 if success else ft.colors.RED_800
        )
        self.page.snack_bar.open = True
        self.page.update()                                       

    def _crear_panel_tablas(self):

        self.campos_column = ft.Column(
            controls=[
                self.dd_apps,
                ft.Row([
                    ft.Text("Nombre", width=200, weight="bold"),
                    ft.Text("Tipo", width=150, weight="bold"),
                ],
                spacing=20
                ),
                *[self._crear_fila_campo(i) for i in range(1, 5)],
            ],
            spacing=10
        )
        
        container_campos = ft.Container(
            content=self.campos_column,
            padding=ft.padding.only(left=20, right=20)
        )
        
        return ft.Column(
            controls=[
                ft.Text("Crear tabla", size=20, weight="bold"),
                self.txt_tabla,
                ft.Divider(height=20),
                container_campos, 
                ft.ElevatedButton(
                    "Añadir campo",
                    icon=ft.icons.ADD,
                    on_click=self.añadir_campo
                ),
                ft.ElevatedButton(
                    "Generar Proyecto",
                    icon=ft.icons.DOWNLOAD,
                    on_click=self.generar_proyecto,
                    bgcolor=ft.colors.BLUE_800,
                    color=ft.colors.WHITE
                )
            ],
            expand=True
        )

    def añadir_campo(self, e):
        try:
            new_index = len(self.campos_column.controls)
            nueva_fila = self._crear_fila_campo(new_index + 1) 
            
            self.campos_column.controls.append(nueva_fila)
            self.campos_column.update()  
            print(f"Campo {new_index + 1} añadido correctamente")
        except Exception as ex:
            print(f"Error: {ex}")

    def _crear_fila_campo(self, index):
        print(f"\nCreando fila {index}...")  
        return ft.Row(
            controls=[
                ft.TextField(
                    hint_text=f"campo_{index}",
                    width=200
                ),
                ft.Dropdown(
                    width=150,
                    options=[
                        ft.dropdown.Option("CharField"),
                        ft.dropdown.Option("IntegerField"),
                        ft.dropdown.Option("DateTimeField")
                    ],
                    value="CharField"
                )
            ],
            spacing=20
        )
        
    def actualizar_dropdown_apps(self):
        self.dd_apps.options = []

        for app in self.apps_generadas:
            self.dd_apps.options.append(
                ft.dropdown.Option(
                    text=app,
                    style=ft.ButtonStyle(color=ft.colors.GREEN)
                )
            )
        
        # Apps pendientes (naranja)
        for app in self.apps_a_crear:
            self.dd_apps.options.append(
                ft.dropdown.Option(
                    text=f"{app} (pendiente)",
                    style=ft.ButtonStyle(color=ft.colors.ORANGE)
                )
            )
        
        self.page.update()

    def añadir_app(self, e):
        nombre_app = self.txt_nombre_app.value.strip()
        
        # Validaciones
        if not nombre_app:
            print("Ingresa un nombre para la app")
            return
        if not nombre_app.isidentifier():
            print("Usa solo letras, números y _")
            return
        if nombre_app in self.apps_a_crear:
            print("Esta app ya fue añadida", color="orange")
            return
        
        self.apps_a_crear.append(nombre_app)
        self.lista_apps.controls.append(ft.Text(f"- {nombre_app}"))
        self.dd_apps.options = [
            ft.dropdown.Option(app) for app in self.apps_a_crear
        ]
        self.dd_apps.value = nombre_app 
        self.txt_nombre_app.value = ""  
        self.page.update()

    def generar_apps(self, e):
        try:
            project_dir = Path(self.ruta_proyecto)
            
            # Crear directorio apps si no existe
            apps_dir = project_dir / "apps"
            apps_dir.mkdir(exist_ok=True)
            
            # Asegurar que cada app tenga estructura completa
            for app_name in self.apps_a_crear:
                app_dir = apps_dir / app_name
                app_dir.mkdir(exist_ok=True)
                
                # Archivos esenciales
                (app_dir / "__init__.py").touch()
                
                # apps.py completo
                with open(app_dir / "apps.py", "w") as f:
                    f.write(f"""from django.apps import AppConfig

class {app_name.capitalize()}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app_name}'
    label = '{app_name.lower()}'
""")
            
            # models.py vacío si no existe
            if not (app_dir / "models.py").exists():
                with open(app_dir / "models.py", "w") as f:
                    f.write("from django.db import models\n\n# Modelos aquí\n")
            
            # Actualizar settings.py
            settings_path = project_dir / "Mi_proyecto" / "settings.py"
            if settings_path.exists():
                with open(settings_path, "r+") as f:
                    content = f.read()
                    if f"'apps.{app_name}'" not in content:
                        new_content = content.replace(
                            "'django.contrib.staticfiles',",
                            f"'django.contrib.staticfiles',\n    'apps.{app_name}',"
                        )
                        f.seek(0)
                        f.write(new_content)
                        f.truncate()
        
        # Limpiar lista y actualizar UI
            self.apps_a_crear.clear()
            self.lista_apps.controls.clear()
            self.actualizar_dropdown_apps()
            self.page.update()
        
        except Exception as ex:
            print(f"Error al generar apps: {str(ex)}" )
        

    def build(self):
        return self.contenedores
    
def main(page: ft.Page):

    page.window_min_height = 820
    page.window_min_width = 530
    page.theme_mode = ft.ThemeMode.SYSTEM 

    ui = UI(page) 
    page.add(ui.build())

ft.app(target=main)