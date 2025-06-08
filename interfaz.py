import flet as ft
from core.crear_carpeta import FolderCreatorLogic
from core.crear_entorno import crear_entorno_virtual
from core.django_manager import DjangoManager
from core.bd_config import DatabaseConfig
from pathlib import Path
import subprocess

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
                self.contenedor4,
                self.contenedor5
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
    

    """def mostrar_mensaje(self, mensaje: str, color: str = "green"):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text(mensaje, color=color),
            open=True
        )
        self.page.update()
    """
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


    def guardar_modelo(self, e):
        nombre_tabla = self.txt_tabla.value.strip()
        if not nombre_tabla:
            print("Ingresa un nombre para la tabla")
            return
        
        try:
            app_name = self.dd_apps.value
            if not app_name:
                raise ValueError
            
            campos = []
            for row in self.campos_column.controls[1:]:
                if isinstance(row, ft.Row):
                    nombre_campo = row.controls[0].value.strip()
                    tipo_campo = row.controls[1].value
                    if nombre_campo:
                        campos.append({"name": nombre_campo, "type": tipo_campo})
              
            models_path = Path(self.ruta_proyecto) / "mi_proyecto" / "apps" / app_name / "models.py"
            
            if not models_path.exists():
                models_path.parent.mkdir(parents=True, exist_ok=True)
                models_path.write_text("from django.db import models\n\n")
            
            if not (Path(self.ruta_proyecto) / "apps" / app_name).exists():
                print(f"La app {app_name} no existe en el proyecto")
                return
            
            with open(models_path, "a") as f:
                f.write(f"\nclass {nombre_tabla}(models.Model):\n")
                for campo in campos:
                    f.write(f"    {campo['name']} = models.{campo['type']}\n")
            
            admin_path = models_path.parent / "admin.py"
            if not admin_path.exists():
                admin_path.write_text("from django.contrib import admin\nfrom .models import *\n\n")
            
            with open(admin_path, "a") as f:
                f.write(f"admin.site.register({nombre_tabla})\n")
            
            if hasattr(self, 'ruta_proyecto') and self.ruta_proyecto:
                manage_py = Path(self.ruta_proyecto) / "mi_proyecto" / "manage.py"
                subprocess.run(["python", str(manage_py), "makemigrations", app_name], check=True)
                subprocess.run(["python", str(manage_py), "migrate"], check=True)
            
            print(f"Modelo '{nombre_tabla}' creado en {app_name}/models.py y migrado")
            
        except subprocess.CalledProcessError:
            print("Modelo creado pero falló migración", color="orange")
        except Exception as ex:
            print(f"Error: {str(ex)}")
        

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

    def generar_proyecto(self, e):
        try:
            if not self.ruta_base:
                raise ValueError("Selecciona una ubicación para el proyecto primero.")

            if hasattr(self, 'txt_tabla') and self.txt_tabla.value.strip():
                nombre_tabla = self.txt_tabla.value.strip()
                campos = []
                for row in self.campos_column.controls[1:]:  
                    if isinstance(row, ft.Row):
                        nombre_campo = row.controls[0].value.strip()
                        tipo_campo = row.controls[1].value
                        if nombre_campo:  # Ignorar campos vacíos
                            campos.append({"name": nombre_campo, "type": tipo_campo})
                
                if campos and self.dd_apps.value:
                    app_name = self.dd_apps.value.replace(" (pendiente)", "")
                    self.db_config.add_model(app_name, nombre_tabla, campos)

            self.db_config.generate_files(self.ruta_base)

            if hasattr(self, 'ruta_proyecto') and self.ruta_proyecto:
                manage_py = Path(self.ruta_proyecto) / "manage.py"
                subprocess.run(["python", str(manage_py), "makemigrations"], check=True)
                subprocess.run(["python", str(manage_py), "migrate"], check=True)
            print("Proyecto generado correctamente con todos los modelos")    

        except subprocess.CalledProcessError:
            print("Modelos creados pero falló la migración")
        except Exception as ex:
            print(f"Error: {str(ex)}")


    def update_folder_name(self, e):
        #Actualizar nombre
        self.logic.folder_name = e.control.value
    
    async def select_folder(self, e):
            
            try:
                selected_path = await self.logic.open_folder_dialog()
                if selected_path:
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
        #Crear carpeta
        success, message, full_path = self.logic.create_folder_action()
        if success:
            self.ruta_base= str(full_path)
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
        if not hasattr(self, 'ruta_proyecto') or not self.ruta_proyecto:
            print("Primero crea el proyecto Django")
            return
        
        try:
            project_dir = Path(self.ruta_proyecto)
            print(f"\n[DEBUG] Ruta confirmada: {project_dir}")
            print(f"Contenido: {[f.name for f in project_dir.glob('*')]}")
            
            apps_dir = project_dir / "apps"
            apps_dir.mkdir(exist_ok=True)

            settings_path=None
            possible_paths = [
                project_dir / "settings.py",
                project_dir / project_dir.name / "settings.py",
                project_dir / self.txt_nombre_proyecto.value.strip() / "settings.py"
            ]

            for path in possible_paths:
                if path.exists():
                    settings_path = path
                    break

            if not settings_path:
                settings_files = list(project_dir.glob('**/settings.py'))
                if settings_files:
                    settings_path = settings_files[0]
                else:
                    raise FileNotFoundError("No se encontró settings.py en el proyecto")        
            print(f"Usando settings.py en: {settings_path}")
            
            for app_name in self.apps_a_crear:
                app_path = apps_dir / app_name
                app_path.mkdir(exist_ok=False)
                
                (app_path / "__init__.py").touch()
                (app_path / "apps.py").write_text(f"""from django.apps import AppConfig

    class {app_name.capitalize()}Config(AppConfig):
        default_auto_field = 'django.db.models.BigAutoField'
        name = 'apps.{app_name}'
                """)
                
                with open(settings_path, 'r+') as f:
                    content = f.read()
                    if f"'apps.{app_name}'" not in content:
                        new_content = content.replace(
                            "'django.contrib.staticfiles',",
                            f"'django.contrib.staticfiles',\n    'apps.{app_name}',"
                        )
                        f.seek(0)
                        f.write(new_content)
                        f.truncate()
                
                print(f"App '{app_name}' creada y registrada en settings.py")
                
                if app_name not in self.apps_generadas:
                 self.apps_generadas.append(app_name)
            
            self.actualizar_dropdown_apps()
            self.apps_a_crear.clear()
            self.lista_apps.controls.clear()

            self.dd_apps.options = [
                ft.dropdown.Option(app) for app in self.apps_generadas
            ]

            self.page.update()
            
        except Exception as ex:
            print(f"Error: {str(ex)}")
        

    def build(self):
        return self.contenedores
    
def main(page: ft.Page):

    page.window_min_height = 820
    page.window_min_width = 530
    page.theme_mode = ft.ThemeMode.SYSTEM 

    ui = UI(page) 
    page.add(ui.build())

ft.app(target=main)