import asyncio
import threading
import flet as ft
from core.crear_carpeta import FolderCreatorLogic
from core.crear_entorno import crear_entorno_virtual
from core.django_manager import DjangoManager
from core.bd_config import DatabaseConfig
from pathlib import Path
import subprocess
import os
import re

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

        self.btn_iniciar_servidor = ft.ElevatedButton(
            "Iniciar Servidor",
            icon=ft.icons.PLAY_ARROW,
            on_click=self.iniciar_servidor,
            bgcolor=ft.colors.GREEN_800,
            color=ft.colors.WHITE
            )
        
        self.btn_detener_servidor = ft.ElevatedButton(
            "Detener Servidor",
            icon=ft.icons.STOP,
            on_click=self.detener_servidor,
            bgcolor=ft.colors.RED_800,
            color=ft.colors.WHITE,
            disabled=True
            )
        
        self.txt_admin_user = ft.TextField(label="Nombre de admin", width=200)
        self.txt_admin_email = ft.TextField(label="Email", width=200)
        self.txt_admin_pass = ft.TextField(label="Contraseña", password=True, width=200)

        self.btn_crear_su = ft.ElevatedButton(
            "Crear Superusuario",
            icon=ft.icons.PERSON_ADD,
            on_click=lambda e: self._trigger_async_creation(),
            bgcolor=ft.colors.BLUE_800,
            color="white"
        )

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
            height=550,
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

        self.contenedor6 = ft.Container(
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
                                ft.Text("INICIAR / DETENER SERVIDOR", size=20, weight="bold")
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ),
                    ft.Divider(height=1, color="black"),
                    ft.Row(
                        controls=[
                            self.btn_iniciar_servidor,  
                            self.btn_detener_servidor  
                        ],
                        spacing=15
                    ),
                    ft.Divider(height=30, color=ft.colors.TRANSPARENT),
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text("CREAR SUPER USUARIO", size=20, weight="bold")
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ),
                    ft.Divider(height=1, color="black"),
                    ft.Column(
                        controls=[

                            self.txt_admin_user,
                            self.txt_admin_email,
                            self.txt_admin_pass,
                            ft.Text("* Todos los campos son obligatorios", style="italic")
                        ]
                    ),
                    ft.Row(
                        controls=[ 
                            self.btn_crear_su
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
                self.contenedor4,
                self.contenedor6,
            ],
            expand=True
        
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
    
    # En interfaz.py - REEMPLAZAR el método guardar_modelo() existente con este:

    async def guardar_modelo(self, e):
        try:
            print("\n=== INICIO DE guardar_modelo() ===")
            
            # 1. Validaciones básicas (SE MANTIENEN EN UI)
            nombre_tabla = self.txt_tabla.value.strip()
            if not nombre_tabla:
                print("Ingresa un nombre para la tabla")
                return
                
            if not self.dd_apps.value:
                print("Selecciona una app primero")
                return
                
            app_name = self.dd_apps.value.replace(" (pendiente)", "")
            
            # 2. Obtener y validar campos (SE MANTIENE EN UI)
            campos = []
            for row in self.campos_column.controls[1:]:  # Saltar encabezado
                if isinstance(row, ft.Row) and len(row.controls) >= 2:
                    nombre = row.controls[0].value.strip()
                    tipo = row.controls[1].value
                    if nombre and tipo:
                        campos.append({"name": nombre, "type": tipo})
            
            print(f"Campos obtenidos: {campos}")
            
            if not campos:
                print("Añade al menos un campo válido al modelo")
                return
            
            # 3. Llamar al método migrado en DjangoManager (LÓGICA MIGRADA)
            resultado = DjangoManager.crear_modelo(
                project_path=self.ruta_proyecto,
                app_name=app_name,
                nombre_tabla=nombre_tabla,
                campos=campos,
                venv_path=str(Path(self.ruta_base) / "venv")
            )
            
            if resultado["success"]:
                print(f"Modelo '{nombre_tabla}' guardado y migrado exitosamente")
            else:
                print(f"Error: {resultado['error']}")
            
        except Exception as ex:
            print(f"\n=== ERROR ===\n{str(ex)}\n=============")
            print(f"Error al guardar modelo: {str(ex)}")
            import traceback
            traceback.print_exc()

    def obtener_campos(self) -> list:
        campos = []
        for row in self.campos_column.controls[1:]:  # Saltar encabezado
            if isinstance(row, ft.Row) and len(row.controls) >= 2:
                nombre = row.controls[0].value.strip()
                tipo = row.controls[1].value
                if nombre and tipo:  # Solo campos válidos
                    campos.append({"name": nombre, "type": tipo})
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
                    project_dir=str(project_path.parent) 
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
                    "Guardar Modelo",
                    icon=ft.icons.SAVE,
                    on_click=self.guardar_modelo,
                    bgcolor=ft.colors.GREEN_800,
                    color=ft.colors.WHITE
                )
            ],
            expand=True,
            scroll=True

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

    async def generar_apps(self, e):
        try:
            if not hasattr(self, 'ruta_proyecto') or not self.ruta_proyecto:
                print("Primero crea el proyecto Django")
                return
            
            # Llamar al método migrado en DjangoManager
            resultado = DjangoManager.generar_apps_legacy(self.ruta_proyecto, self.apps_a_crear)
            
            if resultado["success"]:
                # Limpiar lista y actualizar UI - EXACTAMENTE como en tu código original
                self.apps_generadas.extend(self.apps_a_crear)
                self.apps_a_crear.clear()
                self.lista_apps.controls.clear()
                self.actualizar_dropdown_apps()
                print(f"Apps generadas: {', '.join(self.apps_generadas)}")
                self.page.update()
            else:
                print(resultado["error"])
            
        except Exception as ex:
            print(f"Error al generar apps: {str(ex)}")        

    async def iniciar_servidor(self, e):
        try:
            if not hasattr(self, 'ruta_base') or not self.ruta_base:
                print("Primero selecciona una ubicación para el proyecto")
                return
                
            if not hasattr(self, 'ruta_proyecto') or not self.ruta_proyecto:
                print("Primero genera el proyecto Django")
                return

            venv_dir = Path(self.ruta_base) / "venv"
            scripts_dir = venv_dir / ("Scripts" if os.name == "nt" else "bin")
            
            python_exe = None
            for exe_name in ["python.exe", "python", "python3"]:
                exe_path = scripts_dir / exe_name
                if exe_path.exists():
                    python_exe = exe_path
                    break

            if not python_exe:
                print(f"No se encontró el ejecutable Python en: {scripts_dir}")
                print("Archivos disponibles en el directorio:")
                for f in scripts_dir.iterdir():
                    print(f" - {f.name}")
                return

            manage_py = Path(self.ruta_proyecto) / "manage.py"
            if not manage_py.exists():
                print(f"No se encontró manage.py en {manage_py}")
                return

            self.proceso_servidor = subprocess.Popen(
                [str(python_exe.resolve()), str(manage_py.resolve()), "runserver"],
                cwd=str(self.ruta_proyecto),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True  
            )

            print(f"Servidor iniciado en http://127.0.0.1:8000")
            print(f"Python usado: {python_exe}")
            threading.Thread(target=self.monitorear_servidor, daemon=True).start()
            
            self.btn_iniciar_servidor.disabled = True
            self.btn_detener_servidor.disabled = False
            self.page.update()

        except Exception as ex:
            error_msg = f"Error al iniciar servidor: {str(ex)}"
            print(error_msg)
            self.page.snack_bar = ft.SnackBar(
                ft.Text(error_msg),
                bgcolor=ft.colors.RED
            )
            self.page.snack_bar.open = True
            self.page.update()

    def monitorear_servidor(self):
        while self.proceso_servidor.poll() is None:
            output = self.proceso_servidor.stdout.readline().strip()
            if output:
                print(f"[Servidor]: {output}")
    

    def detener_servidor(self, e):
        if hasattr(self, 'proceso_servidor') and self.proceso_servidor.poll() is None:
            self.proceso_servidor.terminate()
            print("Servidor detenido")
        
        self.btn_iniciar_servidor.disabled = False
        self.btn_detener_servidor.disabled = True
        self.page.update()

    def _trigger_async_creation(self):
        """Método puente síncrono para iniciar la operación async"""
        self.page.run_task(self._crear_su_handler_wrapper)

    async def _crear_su_handler_wrapper(self):
        """Wrapper async para manejo de errores"""
        try:
            await self._crear_su_handler()
        except Exception as ex:
            print(f"Error: {str(ex)}")

    async def _crear_su_handler(self):
        """Manejador principal"""
        if not all([
            self.txt_admin_user.value.strip(),
            self.txt_admin_email.value.strip(),
            self.txt_admin_pass.value.strip()
        ]):
            raise ValueError("Complete todos los campos")
        
        await self._run_django_command([
            "createsuperuser",
            "--noinput",
            f"--username={self.txt_admin_user.value}",
            f"--email={self.txt_admin_email.value}"
        ])
        
        await self._set_password()

    async def _run_django_command(self, args):
        """Ejecuta un comando de Django de forma async"""
        proc = await asyncio.create_subprocess_exec(
            str(Path(self.ruta_base)/"venv"/"Scripts"/"python"),
            str(Path(self.ruta_proyecto)/"manage.py"),
            *args,
            cwd=str(self.ruta_proyecto),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(stderr.decode().strip())

    async def _set_password(self):
        """Establece la contraseña del superusuario"""
        script = (f"""
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.get(username='{self.txt_admin_user.value}')
            user.set_password('{self.txt_admin_pass.value}')
            user.save()
            """
        )
        await self._run_django_command(["shell", "-c", script])
        print("Superusuario creado exitosamente!")

    def _crear_superusuario_sync(self, username: str, email: str, password: str):
        """Lógica síncrona para crear el usuario"""
        try:
            venv_python = str(Path(self.ruta_base) / "venv" / "Scripts" / "python")
            manage_py = str(Path(self.ruta_proyecto) / "manage.py")

            # 1. Crear superusuario
            subprocess.run([
                venv_python, manage_py,
                "createsuperuser",
                "--noinput",
                f"--username={username}",
                f"--email={email}"
            ], check=True, capture_output=True, text=True, cwd=str(self.ruta_proyecto))

            # 2. Establecer contraseña
            script = f"""
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(username='{username}')
user.set_password('{password}')
user.save()
print("Contraseña actualizada exitosamente")
        """
            subprocess.run([
                venv_python, manage_py,
                "shell", "-c", script
            ], check=True, capture_output=True, text=True, cwd=str(self.ruta_proyecto))

            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"Superusuario {username} creado"),
                bgcolor=ft.colors.GREEN
            )
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if e.stderr else "Error desconocido al crear usuario"
            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"{error_msg}"),
                bgcolor=ft.colors.RED
            )
        finally:
            self.page.snack_bar.open = True
            self.page.update()

    def build(self):
        return self.contenedores
    
def main(page: ft.Page):

    page.window_min_height = 820
    page.window_min_width = 530
    page.theme_mode = ft.ThemeMode.SYSTEM 

    ui = UI(page) 
    page.add(ui.build())

ft.app(target=main)