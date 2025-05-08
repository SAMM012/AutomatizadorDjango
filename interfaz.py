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
                                ft.Text("Panel 3", size=20, weight=ft.FontWeight.BOLD)
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
    
    def crear_entorno_handler(self,e):
        try:
            subprocess.run(["django-admin", "--version"], check=True, capture_output=True)
        except Exception as e:
            print(" Django no está instalado correctamente", color="red")
            return
        nombre_entorno = self.txt_entorno.value.strip()
        nombre_proyecto = self.txt_nombre_proyecto.value.strip()
        nombre_proyecto = nombre_proyecto.replace(" ","_")

        if not nombre_entorno:
            self.mostrar_mensaje("Debes ingresar un nombre", color="red")
            return
        if not nombre_proyecto:
            self.mostrar_mensaje("Ingresa un nombre para el proyecto", color="red")
            return
        
        resultado=crear_entorno_virtual(nombre_entorno, self.ruta_base)
        if "creado" in resultado:
            exito = DjangoManager.create_standard_project(
                env_path=str(Path(self.ruta_base) / nombre_entorno),
                project_name=nombre_proyecto,  
                project_dir=self.ruta_base
            )
            if exito:
                resultado += "\n Proyecto Django estándar generado (con manage.py)"

        self.mostrar_mensaje(resultado)
        self.page.update()


    

    def mostrar_mensaje(self, mensaje: str, color: str = "green"):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text(mensaje, color=color),
            open=True
        )
        self.page.update()

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
        
        self.mostrar_mensaje(f"Configuración {self.database_choice.upper()} guardada")



    def guardar_modelo(self, e):
        nombre_tabla = self.txt_tabla.value.strip()
        if not nombre_tabla:
            self.mostrar_mensaje(" Ingresa un nombre para la tabla", color="red")
            return
        
        campos = []
        for row in self.campos_column.controls[1:]:  # Ignora el encabezado
            if isinstance(row, ft.Row):
                nombre_campo = row.controls[0].value.strip()
                tipo_campo = row.controls[1].value
                if nombre_campo:
                    campos.append({"name": nombre_campo, "type": tipo_campo})
        
        self.db_config.add_model(nombre_tabla, campos)
        self.mostrar_mensaje(f" Modelo '{nombre_tabla}' guardado")


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

            nombre_tabla = self.txt_tabla.value.strip()
            if nombre_tabla:  
                campos = []
                for row in self.campos_column.controls[1:]:  
                    if isinstance(row, ft.Row):
                        nombre_campo = row.controls[0].value.strip()
                        tipo_campo = row.controls[1].value
                        if nombre_campo:  # Ignorar campos vacíos
                            campos.append({"name": nombre_campo, "type": tipo_campo})
                
                self.db_config.add_model(nombre_tabla, campos)

            # 3. Generar archivos
            self.db_config.generate_files(self.ruta_base)
            self.mostrar_mensaje(" Proyecto generado correctamente")

        except Exception as ex:
            self.mostrar_mensaje(f" Error: {str(ex)}", color="red")


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
                ft.Row([  # Encabezado
                    ft.Text("Nombre", width=200, weight="bold"),
                    ft.Text("Tipo", width=150, weight="bold")
                ],
                spacing=20
                ),
                *[self._crear_fila_campo(i) for i in range(1, 5)]  # 4 campos iniciales
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
        
    def añadir_app(self, e):
        nombre_app = self.txt_nombre_app.value.strip()
        
        # Validaciones
        if not nombre_app:
            self.mostrar_mensaje("Ingresa un nombre para la app", color="red")
            return
        if not nombre_app.isidentifier():
            self.mostrar_mensaje("Usa solo letras, números y _", color="red")
            return
        if nombre_app in self.apps_a_crear:
            self.mostrar_mensaje("Esta app ya fue añadida", color="orange")
            return
        
        # Añadir a la lista
        self.apps_a_crear.append(nombre_app)
        self.lista_apps.controls.append(ft.Text(f"- {nombre_app}"))
        self.txt_nombre_app.value = ""  # Limpiar campo
        self.page.update()

    def generar_apps(self, e):
        if not self.apps_a_crear:
            self.mostrar_mensaje("❌ No hay apps para generar", color="red")
            return
        
        try:
            # Ruta exacta (ajusta 'mi_proyecto' si es diferente)
            project_dir = Path(self.ruta_base) / "mi_proyecto"
            
            # Debug forzado
            print("\n" + "="*50)
            print(f"Ruta completa: {project_dir}")
            print(f"¿Existe?: {project_dir.exists()}")
            print(f"Contenido: {list(project_dir.glob('*'))}")
            print("="*50 + "\n")
            
            for app_name in self.apps_a_crear:
                if self.db_config.create_django_app(app_name, str(project_dir)):
                    self.mostrar_mensaje(f"App '{app_name}' creada manualmente")
                    
            self.apps_a_crear.clear()
            self.lista_apps.controls.clear()
            self.page.update()
            
        except Exception as ex:
            self.mostrar_mensaje(f"Error: {str(ex)}", color="red")
        

    def build(self):
        return self.contenedores
    
def main(page: ft.Page):

    page.window_min_height = 820
    page.window_min_width = 530
    page.theme_mode = ft.ThemeMode.SYSTEM 

    ui = UI(page) 
    page.add(ui.build())

ft.app(target=main)