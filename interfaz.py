import asyncio
import threading
import flet as ft
from core.crear_carpeta import FolderCreatorLogic
from core.crear_entorno import crear_entorno_virtual
from core.django_manager import DjangoManager
from core.bd_config import DatabaseConfig
from core.project_state import ProjectState 
from pathlib import Path
import subprocess
import os
import re


class UI:

    def debug_state(self):
        """Método helper para debugging del estado"""
        print("\n=== ESTADO ACTUAL ===")
        print(f"Ruta base: {self.state.ruta_base}")
        print(f"Ruta proyecto: {self.state.ruta_proyecto}")
        print(f"Nombre proyecto: {self.state.nombre_proyecto}")
        print(f"Base de datos: {self.state.database_choice}")
        print(f"Apps a crear: {self.state.apps_a_crear}")
        print(f"Apps generadas: {self.state.apps_generadas}")
        print(f"Wizard states: {self.state.wizard_states}")
        print("=====================\n")

    def __init__(self, page:ft.Page):

        self.page = page
        self.state = ProjectState()
        self.logic = FolderCreatorLogic(page)
        self.db_config = DatabaseConfig()
        self.django_manager = DjangoManager()

        self.txt_folder_name =ft.TextField(
            label="Ej: Mi proyecto",
            width=150,
            height=40,
            on_change=self.update_folder_name
        )
        self.lbl_path = ft.Text("Ninguna", style=ft.TextThemeStyle.BODY_SMALL)
        self.dd_apps = ft.Dropdown(
                    options=[],
                    label="Selecciona una app",
                    width=200
        )
        
        self.txt_entorno = ft.TextField(
            label="Ej venv",
            width=200,
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
        
        self.txt_nombre_app = ft.TextField(
            label="Ej: usuarios",
            width=200,
            height=40
        )
        
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

        self.panel_tablas = self._crear_panel_tablas()

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

        self.contenedores = ft.Column(
                controls=[
                    ft.ResponsiveRow(
                        controls=[
                            self._wrap_container_with_wizard(self.contenedor1, "carpeta", 1, "Crear carpeta del proyecto"),
                            self._wrap_container_with_wizard(self.contenedor2, "entorno", 2, "Crear entorno virtual"),
                            self._wrap_container_with_wizard(self.contenedor3, "bd_config", 3, "Configurar base de datos"),
                        ]
                    ),
                    ft.ResponsiveRow(
                        controls=[
                            self._wrap_container_with_wizard(self.contenedor5, "apps", 5, "Crear Apps Django"),
                            self._wrap_container_with_wizard(self.contenedor4, "modelos", 4, "Crear modelos"),
                            self._wrap_container_with_wizard(self.contenedor6, "servidor", 6, "Servidor y usuarios"),
                        ]
                    )
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True
            )

    def _create_disabled_overlay(self):
        return ft.Container(
            expand=True,
            width=float('inf'),  
            height=float('inf'), 
            bgcolor=ft.colors.with_opacity(0.6, "grey"),  
            border_radius=10,
            alignment=ft.alignment.center,
            content=ft.Column(
                controls=[
                    ft.Icon(ft.icons.LOCK, size=50, color="white"),
                    ft.Text(
                        "Completa el paso anterior",
                        color="white",
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        size=16
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                tight=True
            )
        )

    def _create_step_indicator(self, step_number: int, title: str, is_completed: bool, is_current: bool):
        if is_completed:
            icon = ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN, size=20)
            title_color = ft.colors.GREEN
        elif is_current:
            icon = ft.Icon(ft.icons.RADIO_BUTTON_UNCHECKED, color=ft.colors.BLUE, size=20)
            title_color = ft.colors.BLUE
        else:
            icon = ft.Icon(ft.icons.LOCK, color=ft.colors.GREY_400, size=20)
            title_color = ft.colors.GREY_400
        
        return ft.Row(
            controls=[
                ft.Container(
                    width=30,
                    height=30,
                    bgcolor=ft.colors.with_opacity(0.1, title_color),
                    border_radius=15,
                    alignment=ft.alignment.center,
                    content=ft.Text(str(step_number), color=title_color, weight=ft.FontWeight.BOLD)
                ),
                icon,
                ft.Text(title, color=title_color, weight=ft.FontWeight.BOLD, size=16)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5
        )

    def _wrap_container_with_wizard(self, container, step_key: str, step_number: int, title: str):
        is_completed = self.state.wizard_states[step_key] 
        is_current = self._is_current_step(step_key)
        is_enabled = is_completed or is_current
        
        if hasattr(container.content, 'controls') and len(container.content.controls) > 0:
            container.content.controls[0] = ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=self._create_step_indicator(step_number, title, is_completed, is_current)
            )
        if is_enabled:
            return ft.Container(
                col=4,
                expand=True,
                content=container.content,
                bgcolor=container.bgcolor,
                border_radius=container.border_radius,
                padding=container.padding
            )
        else:
            return ft.Container(
                col=4,
                expand=True,
                content=ft.Stack(
                    controls=[
                        ft.Container(
                            expand=True,
                            content=container.content,
                            bgcolor=container.bgcolor,
                            border_radius=container.border_radius,
                            padding=container.padding
                        ),
                        ft.Container(
                            left=0,
                            top=0,
                            right=0,
                            bottom=0,
                            bgcolor=ft.colors.with_opacity(0.85, "grey"),
                            border_radius=10,
                            alignment=ft.alignment.center,
                            content=ft.Column(
                                controls=[
                                    ft.Icon(ft.icons.LOCK, size=50, color="white"),
                                    ft.Text(
                                        "Completa el paso anterior",
                                        color="white",
                                        weight=ft.FontWeight.BOLD,
                                        size=16
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=15
                            )
                        )
                    ]
                )
            )


    def _is_current_step(self, step_key: str) -> bool:
        steps_order = ["carpeta", "entorno", "bd_config", "apps", "modelos", "servidor"]
        
        for i, step in enumerate(steps_order):
            if step == step_key:
                if i == 0:
                    return not self.state.wizard_states[step] 
                else:
                    prev_completed = all(self.state.wizard_states[prev_step] for prev_step in steps_order[:i])  
                    return prev_completed and not self.state.wizard_states[step] 
        return False

    def _update_wizard_state(self, step_key: str, completed: bool = True):
        self.state.wizard_states[step_key] = completed 
        self._refresh_wizard_ui()

    def _refresh_wizard_ui(self):
        self.contenedores.controls = [
            ft.ResponsiveRow(
                controls=[
                    self._wrap_container_with_wizard(self.contenedor1, "carpeta", 1, "Crear carpeta del proyecto"),
                    self._wrap_container_with_wizard(self.contenedor2, "entorno", 2, "Crear entorno virtual"),
                    self._wrap_container_with_wizard(self.contenedor3, "bd_config", 3, "Configurar base de datos"),
                ]
            ),
            ft.ResponsiveRow(
                controls=[
                    self._wrap_container_with_wizard(self.contenedor5, "apps", 5, "Crear Apps Django"),
                    self._wrap_container_with_wizard(self.contenedor4, "modelos", 4, "Crear modelos"),
                    self._wrap_container_with_wizard(self.contenedor6, "servidor", 6, "Servidor y usuarios"),
                ]
            )
        ]
        self.page.update()
    
    async def crear_entorno_handler(self, e):
        if not self.state.wizard_states["carpeta"]:
            print("Primero debes crear la carpeta del proyecto")
            return

        nombre_entorno = self.txt_entorno.value.strip()
        nombre_proyecto = self.txt_nombre_proyecto.value.strip()
        
        if not nombre_entorno or not nombre_proyecto:
            print("Ingresa nombres para entorno y proyecto")
            return
            
        try:
            self.state.nombre_proyecto = nombre_proyecto
            resultado = crear_entorno_virtual(
                nombre_entorno,
                self.state.ruta_base,
                nombre_proyecto
            )
            print(resultado)
            self.state.ruta_proyecto = str(Path(self.state.ruta_base) / nombre_proyecto)
            self.state.update_wizard_step("entorno", True)
            self._refresh_wizard_ui()
            
        except Exception as ex:
            print(f" Error: {str(ex)}")

    def update_db_choice(self, e):
        self.state.database_choice = e.control.value
        print(f"Base de datos seleccionada: {self.state.database_choice}")

    def save_db_config(self, e):
        if not self.state.wizard_states["entorno"]:
            print("Primero debes crear el entorno virtual")
            return
        self.db_config.set_database_type(self.state.database_choice)
        
        if self.state.database_choice == "post":
            self.db_config.set_postgres_config(
                name="mydb",
                user="postgres", 
                password="secret",
                host="localhost",
                port="5432"
            )
        print(f"Configuración {self.state.database_choice.upper()} guardada")
        
        self.state.update_wizard_step("bd_config", True)
        self._refresh_wizard_ui()

    def _validar_campos_modelo(self) -> tuple:
        nombres_campos = []
        for row in self.campos_column.controls[1:]:  
            if isinstance(row, ft.Row) and len(row.controls) >= 2:
                nombre = row.controls[0].value.strip()
                if nombre:  
                    nombres_campos.append(nombre)
        
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
            
            campos = []
            for row in self.campos_column.controls[1:]: 
                if isinstance(row, ft.Row) and len(row.controls) >= 2:
                    nombre = row.controls[0].value.strip()
                    tipo = row.controls[1].value
                    if nombre and tipo:
                        campos.append({"name": nombre, "type": tipo})
            
            print(f"Campos obtenidos: {campos}")
            
            if not campos:
                print("Añade al menos un campo válido al modelo")
                return
            venv_path = str(Path(self.state.ruta_base) / "venv")
            resultado = DjangoManager.crear_modelo(
                project_path=self.state.ruta_proyecto, 
                app_name=app_name,
                nombre_tabla=nombre_tabla,
                campos=campos,
                venv_path=venv_path
            ) 
            if resultado["success"]:
                print(f"Modelo '{nombre_tabla}' guardado y migrado exitosamente")
                
                if not self.state.wizard_states["modelos"]:
                    self.state.update_wizard_step("modelos", True)
                    self._refresh_wizard_ui()
            else:
                print(f"Error: {resultado['error']}")      
        except Exception as ex:
            print(f"\n=== ERROR ===\n{str(ex)}\n=============")
            print(f"Error al guardar modelo: {str(ex)}")
            import traceback
            traceback.print_exc()

    def obtener_campos(self) -> list:
        campos = []
        for row in self.campos_column.controls[1:]: 
            if isinstance(row, ft.Row) and len(row.controls) >= 2:
                nombre = row.controls[0].value.strip()
                tipo = row.controls[1].value
                if nombre and tipo: 
                    campos.append({"name": nombre, "type": tipo})
        return campos
    
    async def generar_proyecto(self, e):
        try:
            if not self.state.ruta_base:
                raise ValueError("Selecciona una ubicación para el proyecto primero")
            project_path = Path(self.state.ruta_proyecto) if self.state.ruta_proyecto else Path(self.state.ruta_base) / "Mi_proyecto"
            self.db_config.generate_files(str(project_path))
            venv_python = str(self.state.get_venv_python_path())
            manage_py = self.state.get_manage_py_path()
            
            if not manage_py.exists():
                if not hasattr(self, 'django_manager'):
                    self.django_manager = DjangoManager()
                
                success = self.django_manager.create_standard_project(
                    env_path=str(Path(self.state.ruta_base) / "venv"),
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
                self.state.ruta_base = selected_path
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
        success, message, full_path = self.logic.create_folder_action()
        if success:
            self.state.ruta_base = os.path.normpath(full_path)
            self.lbl_path.value = full_path
            self.lbl_path.color = ft.colors.BLACK

            self.state.update_wizard_step("carpeta", True)
            self._refresh_wizard_ui()
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
                ),
                ft.ElevatedButton(
                    "PASO 1: Generar Views+Forms",
                    icon=ft.icons.SCIENCE,
                    on_click=self.generar_views_forms_solo,
                    bgcolor=ft.colors.BLUE_800,
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
        for app in self.state.apps_generadas:
            self.dd_apps.options.append(
                ft.dropdown.Option(
                    text=app,
                    style=ft.ButtonStyle(color=ft.colors.GREEN)
                )
            )
        for app in self.state.apps_a_crear:
            self.dd_apps.options.append(
                ft.dropdown.Option(
                    text=f"{app} (pendiente)",
                    style=ft.ButtonStyle(color=ft.colors.ORANGE)
                )
            )
        self.page.update()

    def añadir_app(self, e):
        nombre_app = self.txt_nombre_app.value.strip()
        if not nombre_app:
            print("Ingresa un nombre para la app")
            return
        if not nombre_app.isidentifier():
            print("Usa solo letras, números y _")
            return
        if self.state.add_app_to_create(nombre_app):
            self.lista_apps.controls.append(ft.Text(f"- {nombre_app}"))
            self.dd_apps.options = [
                ft.dropdown.Option(app) for app in self.state.apps_a_crear
            ]
            self.dd_apps.value = nombre_app
            self.txt_nombre_app.value = ""
            self.page.update()
        else:
            print("Esta app ya fue añadida")


    async def generar_apps(self, e):
        try:
            if not self.state.ruta_proyecto:
                print("Primero crea el proyecto Django")
                return
            
            resultado = DjangoManager.generar_apps_legacy(
                self.state.ruta_proyecto, 
                self.state.apps_a_crear 
            )
            
            if resultado["success"]:
                apps_creadas = self.state.move_apps_to_generated()
                
                self.lista_apps.controls.clear()
                self.actualizar_dropdown_apps()
                print(f"Apps generadas: {', '.join(apps_creadas)}")
                
                self.state.update_wizard_step("apps", True)
                self._refresh_wizard_ui()
                
                self.page.update()
            else:
                print(resultado["error"]) 
        except Exception as ex:
            print(f"Error al generar apps: {str(ex)}")      

    async def iniciar_servidor(self, e):
        try:
            if not self.state.ruta_base:
                print("Primero selecciona una ubicación para el proyecto")
                return
                
            if not self.state.ruta_proyecto:
                print("Primero genera el proyecto Django")
                return

            python_exe = self.state.get_venv_python_path()
            manage_py = self.state.get_manage_py_path()
            
            if not python_exe.exists():
                print(f"No se encontró el ejecutable Python en: {python_exe}")
                return

            if not manage_py.exists():
                print(f"No se encontró manage.py en {manage_py}")
                return
            self.state.proceso_servidor = subprocess.Popen(
                [str(python_exe), str(manage_py), "runserver"],
                cwd=str(self.state.ruta_proyecto),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            print(f"Servidor iniciado en http://127.0.0.1:8000")
            threading.Thread(target=self.monitorear_servidor, daemon=True).start()
            
            self.btn_iniciar_servidor.disabled = True
            self.btn_detener_servidor.disabled = False
            self.page.update()

        except Exception as ex:
            print(f"Error al iniciar servidor: {str(ex)}")

    def detener_servidor(self, e):
        if (hasattr(self.state, 'proceso_servidor') and 
            self.state.proceso_servidor and 
            self.state.proceso_servidor.poll() is None):
            
            self.state.proceso_servidor.terminate()
            print("Servidor detenido")
        
        self.btn_iniciar_servidor.disabled = False
        self.btn_detener_servidor.disabled = True
        self.page.update()

    def monitorear_servidor(self):
        while (self.state.proceso_servidor and 
            self.state.proceso_servidor.poll() is None):
            output = self.state.proceso_servidor.stdout.readline().strip()
            if output:
                print(f"[Servidor]: {output}")

    def _trigger_async_creation(self):
        """Método puente síncrono para iniciar la operación async"""
        self.page.run_task(self._crear_su_handler_wrapper)

    async def _crear_su_handler_wrapper(self):
        try:
            await self._crear_su_handler()
        except Exception as ex:
            print(f"Error: {str(ex)}")

    async def _crear_su_handler(self):
        """Método principal para crear superusuario"""
        if not all([
            self.txt_admin_user.value.strip(),
            self.txt_admin_email.value.strip(),
            self.txt_admin_pass.value.strip()
        ]):
            raise ValueError("Complete todos los campos")
        
        # Usar el método síncrono que funciona mejor
        try:
            self._crear_superusuario_alternativo(
                self.txt_admin_user.value.strip(),
                self.txt_admin_email.value.strip(),
                self.txt_admin_pass.value.strip()
            )
        except Exception as e:
            print(f"Error al crear superusuario: {str(e)}")
            raise


    async def _run_django_command(self, args):
        python_path = str(self.state.get_venv_python_path())
        manage_py = str(self.state.get_manage_py_path())
        
        proc = await asyncio.create_subprocess_exec(
            python_path,
            manage_py,
            *args,
            cwd=str(self.state.ruta_proyecto), 
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(stderr.decode().strip())


    async def _set_password(self):
        script = f'''
    import os
    import django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Mi_proyecto.settings")
    django.setup()

    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        user = User.objects.get(username="{self.txt_admin_user.value}")
        user.set_password("{self.txt_admin_pass.value}")
        user.save()
        print("Contraseña establecida correctamente")
    except User.DoesNotExist:
        print("Error: Usuario no encontrado")
    except Exception as e:
        print(f"Error: {{e}}")
    '''.strip()
        
        await self._run_django_command(["shell", "-c", script])
        print("Superusuario creado exitosamente!")

    def _crear_superusuario_alternativo(self, username: str, email: str, password: str):
        try:
            venv_python = str(self.state.get_venv_python_path())
            manage_py = str(self.state.get_manage_py_path())
            one_liner = f"from django.contrib.auth import get_user_model; User = get_user_model(); user = User.objects.create_superuser('{username}', '{email}', '{password}'); print('Superuser created')"
            
            result = subprocess.run([
                venv_python, manage_py, "shell", "-c", one_liner
            ], check=True, capture_output=True, text=True, cwd=str(self.state.ruta_proyecto))
            
            print("Superusuario creado exitosamente!")
            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"Superusuario {username} creado"),
                bgcolor=ft.colors.GREEN
            )
            
        except subprocess.CalledProcessError as e:
            # Si el usuario ya existe, intentar solo cambiar contraseña
            if "already exists" in str(e.stderr):
                try:
                    change_pass = f"from django.contrib.auth import get_user_model; User = get_user_model(); u = User.objects.get(username='{username}'); u.set_password('{password}'); u.save(); print('Password updated')"
                    subprocess.run([
                        venv_python, manage_py, "shell", "-c", change_pass
                    ], check=True, capture_output=True, text=True, cwd=str(self.state.ruta_proyecto))
                    
                    self.page.snack_bar = ft.SnackBar(
                        ft.Text(f"Contraseña actualizada para {username}"),
                        bgcolor=ft.colors.ORANGE
                    )
                except Exception:
                    self.page.snack_bar = ft.SnackBar(
                        ft.Text("Error: Usuario ya existe y no se pudo actualizar"),
                        bgcolor=ft.colors.RED
                    )
            else:
                self.page.snack_bar = ft.SnackBar(
                    ft.Text(f"Error: {e.stderr}"),
                    bgcolor=ft.colors.RED
                )
        except Exception as e:
            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"Error: {str(e)}"),
                bgcolor=ft.colors.RED
            )
        finally:
            self.page.snack_bar.open = True
            self.page.update()
    
    async def generar_views_forms_solo(self, e):
        try:
            nombre_tabla = self.txt_tabla.value.strip()
            if not nombre_tabla:
                print("❌ Ingresa un nombre para la tabla primero")
                return
                
            if not self.dd_apps.value:
                print("❌ Selecciona una app primero")
                return
            
            app_name = self.dd_apps.value.replace(" (pendiente)", "")
            
            print(f"🚀 PASO 1: Generando Views+Forms para {nombre_tabla} en app {app_name}...")
            views_result = DjangoManager.generar_views_crud(
                self.state.ruta_proyecto,
                app_name, 
                nombre_tabla
            )
            
            if views_result["success"]:
                print(f"✅ Views generadas para {nombre_tabla}")
            else:
                print(f"❌ Error en views: {views_result['error']}")
                return
            forms_result = DjangoManager.generar_forms_crud(
                self.state.ruta_proyecto,
                app_name, 
                nombre_tabla
            )
            
            if forms_result["success"]:
                print(f"✅ Forms generado para {nombre_tabla}")
                
                self.page.snack_bar = ft.SnackBar(
                    ft.Text(f"Views+Forms generados para {nombre_tabla}"),
                    bgcolor=ft.colors.GREEN
                )
            else:
                print(f"❌ Error en forms: {forms_result['error']}")
                self.page.snack_bar = ft.SnackBar(
                    ft.Text("Error al generar Forms"),
                    bgcolor=ft.colors.RED
                )
            
            self.page.snack_bar.open = True
            self.page.update()
            
        except Exception as ex:
            error_msg = f"Error inesperado: {str(ex)}"
            print(f"❌ {error_msg}")
            self.page.snack_bar = ft.SnackBar(
                ft.Text(error_msg),
                bgcolor=ft.colors.RED
            )
            self.page.snack_bar.open = True
            self.page.update()

    def build(self):
        return self.contenedores
    
def main(page: ft.Page):

    page.window_min_height = 600
    page.window_min_width = 400
    page.theme_mode = ft.ThemeMode.SYSTEM 
    page.scroll = ft.ScrollMode.AUTO

    ui = UI(page) 
    page.add(ui.build())

ft.app(target=main)