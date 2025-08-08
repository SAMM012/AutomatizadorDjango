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
        
        # Contenedor de error centrado
        self.error_overlay = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.WARNING, color=ft.Colors.WHITE),
                ft.Container(  # Contenedor para centrar el texto un poco más
                    content=ft.Text("", 
                                  color=ft.Colors.WHITE, 
                                  size=15,  # Un punto más grande
                                  text_align=ft.TextAlign.CENTER),
                    expand=True,
                    alignment=ft.alignment.center_left,
                    margin=ft.margin.only(left=20)  # 20% más centrado
                ),
                ft.IconButton(
                    icon=ft.Icons.CLEANING_SERVICES,
                    tooltip="Limpiar campos", 
                    icon_color=ft.Colors.WHITE,
                    on_click=self.limpiar_y_cerrar
                ),
                ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    tooltip="Cerrar",
                    icon_color=ft.Colors.WHITE,
                    on_click=self.cerrar_error
                )
            ]),
            bgcolor=ft.Colors.RED_400,
            padding=15,
            border_radius=8,
            width=750,  # 50% más largo (500 + 250 = 750)
            alignment=ft.alignment.center,  # Centrar contenido
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=15,
                color=ft.Colors.BLACK38,
            ),
            visible=False
        )

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
            icon=ft.Icons.PLAY_ARROW,
            on_click=self.iniciar_servidor,
            bgcolor=ft.Colors.GREEN_800,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=2),
                side=ft.BorderSide(1, ft.Colors.BLACK)
            )
        )

        self.btn_detener_servidor = ft.ElevatedButton(
            "Detener Servidor",
            icon=ft.Icons.STOP,
            on_click=self.detener_servidor,
            bgcolor=ft.Colors.RED_800,
            color=ft.Colors.WHITE,
            disabled=True,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=2),
                side=ft.BorderSide(1, ft.Colors.BLACK)
            )
        )

        self.txt_admin_user = ft.TextField(label="Nombre de admin", width=200)
        self.txt_admin_email = ft.TextField(label="Email", width=200)
        self.txt_admin_pass = ft.TextField(label="Contraseña", password=True, width=200)

        self.btn_crear_su = ft.ElevatedButton(
            "Crear Superusuario",
            icon=ft.Icons.PERSON_ADD,
            on_click=lambda e: self._trigger_async_creation(),
            bgcolor=ft.Colors.BLUE_800,
            color="white",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=2),
                side=ft.BorderSide(1, ft.Colors.BLACK)
            )
        )

        self.btn_aceptar_entorno = ft.ElevatedButton(
            content=ft.Text("ACEPTAR", color="white"),
            bgcolor="#4CAF50",
            height=40,
            on_click=self.crear_entorno_handler,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=2),
                overlay_color=ft.Colors.with_opacity(0.1, "white"),
                side=ft.BorderSide(1, ft.Colors.BLACK)
            )
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
                                            icon=ft.Icons.FOLDER_OPEN,
                                            on_click= self.select_folder,
                                            style=ft.ButtonStyle(
                                                side=ft.BorderSide(1, ft.Colors.BLACK)
                                            )
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
                                        overlay_color="#FFFFFF",
                                        side=ft.BorderSide(1, ft.Colors.BLACK)
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
                                content=self.btn_aceptar_entorno
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
                                        overlay_color=ft.Colors.with_opacity(0.1, "white"),
                                        side=ft.BorderSide(1, ft.Colors.BLACK)
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
                                icon=ft.Icons.ADD,
                                on_click=self.añadir_app,
                                style=ft.ButtonStyle(
                                    side=ft.BorderSide(1, ft.Colors.BLACK)
                                )
                            ),
                            ft.Text("Apps a crear:", weight="bold"),
                            self.lista_apps,
                            ft.ElevatedButton(
                                "Generar Apps",
                                icon=ft.Icons.CHECK,
                                on_click=self.generar_apps,
                                bgcolor="#4CAF50",
                                color="white",
                                style=ft.ButtonStyle(
                                    side=ft.BorderSide(1, ft.Colors.BLACK)
                                )
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
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
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

        # Contenido principal sin overlay
        self.contenido_principal = ft.Column(
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
        
        # Contenedores con overlay centrado
        self.contenedores = ft.Column(
            controls=[
                ft.Container(  # Contenedor para centrar el error
                    content=self.error_overlay,
                    alignment=ft.alignment.center,
                    padding=ft.padding.symmetric(horizontal=20, vertical=10)
                ),
                self.contenido_principal  # Contenido principal
            ],
            spacing=0,
            expand=True
        )

    def _create_disabled_overlay(self):
        return ft.Container(
            expand=True,
            width=float('inf'),  
            height=float('inf'), 
            bgcolor=ft.Colors.with_opacity(0.6, "grey"),  
            border_radius=10,
            alignment=ft.alignment.center,
            content=ft.Column(
                controls=[
                    ft.Icon(ft.Icons.LOCK, size=50, color="white"),
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
            icon = ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN, size=20)
            title_color = ft.Colors.GREEN
        elif is_current:
            icon = ft.Icon(ft.Icons.RADIO_BUTTON_UNCHECKED, color=ft.Colors.BLUE, size=20)
            title_color = ft.Colors.BLUE
        else:
            icon = ft.Icon(ft.Icons.LOCK, color=ft.Colors.GREY_400, size=20)
            title_color = ft.Colors.GREY_400
        
        return ft.Row(
            controls=[
                ft.Container(
                    width=30,
                    height=30,
                    bgcolor=ft.Colors.with_opacity(0.1, title_color),
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
                            bgcolor=ft.Colors.with_opacity(0.85, "grey"),
                            border_radius=10,
                            alignment=ft.alignment.center,
                            content=ft.Column(
                                controls=[
                                    ft.Icon(ft.Icons.LOCK, size=50, color="white"),
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
        # Actualizar solo el contenido principal, no el overlay
        self.contenido_principal.controls = [
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
            
            # Deshabilitar el botón después del éxito
            self.btn_aceptar_entorno.disabled = True
            self.btn_aceptar_entorno.bgcolor = ft.Colors.GREY_600
            self.btn_aceptar_entorno.content = ft.Text("COMPLETADO", color="white", size=12)
            
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
                error_msg = "⚠️ Debes ingresar un nombre para la tabla/modelo."
                print("Ingresa un nombre para la tabla")
                self.mostrar_error_snackbar(error_msg)
                return
                
            if not self.dd_apps.value:
                error_msg = "⚠️ Debes seleccionar una app antes de crear el modelo."
                print("Selecciona una app primero")
                self.mostrar_error_snackbar(error_msg)
                return
                
            app_name = self.dd_apps.value.replace(" (pendiente)", "")
            
            campos = []
            print(f"\n=== DEBUG RECOLECCIÓN DE CAMPOS ===")
            print(f"Total controles en campos_column: {len(self.campos_column.controls)}")
            
            for i, row in enumerate(self.campos_column.controls[1:], 1): 
                print(f"Control {i}: {type(row)}")
                if isinstance(row, ft.Row) and len(row.controls) >= 2:
                    nombre = row.controls[0].value
                    tipo = row.controls[1].value
                    print(f"  Fila {i}: nombre='{nombre}', tipo='{tipo}'")
                    
                    # Filtrar campos problemáticos y vacíos
                    if (nombre and nombre.strip() and tipo and 
                        tipo != 'Tipo' and  # Filtrar tipo inválido
                        nombre.strip() != 'Nombre' and  # Filtrar nombre por defecto
                        tipo in ['CharField', 'IntegerField', 'TextField', 'BooleanField', 'DateTimeField', 'EmailField', 'ForeignKey']):
                        
                        campos.append({"name": nombre.strip(), "type": tipo})
                        print(f"  ✓ Campo agregado: {nombre.strip()} -> {tipo}")
                    else:
                        print(f"  ✗ Campo ignorado (vacío, inválido o fantasma): '{nombre}' -> '{tipo}'")
                        
            print(f"Campos obtenidos: {campos}")
            print("=====================================\n")
            
            if not campos:
                error_msg = "⚠️ No se encontraron campos válidos. Asegúrate de llenar al menos un campo con nombre y tipo válidos."
                print("Añade al menos un campo válido al modelo")
                self.mostrar_error_snackbar(error_msg)
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
                self.mostrar_error_snackbar(f"❌ {resultado['error']}")
                
        except Exception as ex:
            error_msg = f"Error inesperado: {str(ex)}"
            print(f"\n=== ERROR ===\n{error_msg}\n=============")
            self.mostrar_error_snackbar(f"❌ {error_msg}")
            import traceback
            traceback.print_exc()

    def continuar_sin_modelo(self, e):
        """Permite continuar al paso siguiente sin crear un modelo"""
        try:
            if not self.state.wizard_states["apps"]:
                print("Primero debes crear al menos una app Django")
                return
                
            # Marcar el paso de modelos como completado
            if not self.state.wizard_states["modelos"]:
                self.state.update_wizard_step("modelos", True)
                self._refresh_wizard_ui()
                print("Paso de modelos omitido. Puedes continuar al paso del servidor.")
                
        except Exception as ex:
            print(f"Error al continuar sin modelo: {str(ex)}")

    def limpiar_campos_modelo(self, e=None):
        """Limpia todos los campos del modelo para empezar de nuevo"""
        try:
            # Limpiar el nombre de la tabla
            self.txt_tabla.value = ""
            
            # Limpiar solo los TextFields existentes, más simple y seguro
            for i, row in enumerate(self.campos_column.controls[2:], 1):  # Saltar dropdown y header
                if isinstance(row, ft.Row) and len(row.controls) >= 2:
                    # Limpiar el campo de texto
                    if hasattr(row.controls[0], 'value'):
                        row.controls[0].value = ""
                    
                    # Resetear dropdown a CharField
                    if hasattr(row.controls[1], 'value'):
                        row.controls[1].value = "CharField"
            
            # Actualizar la UI
            self.page.update()
            
            print("✅ Campos limpiados. Puedes agregar nuevos valores.")
        except Exception as ex:
            print(f"Error al limpiar campos: {ex}")
            # Método alternativo más simple
            try:
                self.txt_tabla.value = ""
                self.page.update()
                print("✅ Nombre de tabla limpiado. Edita los campos manualmente.")
            except:
                print("❌ Error al limpiar. Edita los campos manualmente.")

    def mostrar_error_snackbar(self, mensaje_error):
        """Muestra un overlay flotante de error con opción de limpiar campos"""
        try:
            # Actualizar el texto del error (ahora está dentro de un Container)
            self.error_overlay.content.controls[1].content.value = mensaje_error
            self.error_overlay.visible = True
            self.page.update()
            print(f"✅ Overlay de error mostrado: {mensaje_error}")
            
        except Exception as ex:
            print(f"Error al mostrar overlay de error: {ex}")
            
    def cerrar_error(self, e=None):
        """Cierra el overlay de error"""
        try:
            self.error_overlay.visible = False
            self.page.update()
        except Exception as ex:
            print(f"Error al cerrar overlay de error: {ex}")
    
    def limpiar_y_cerrar(self, e=None):
        """Limpia los campos del modelo Y cierra el overlay de error"""
        try:
            # Primero limpiar campos
            self.limpiar_campos_modelo(e)
            # Después cerrar el overlay
            self.cerrar_error()
            print("✅ Campos limpiados y overlay cerrado")
        except Exception as ex:
            print(f"Error al limpiar y cerrar: {ex}")

    def crear_dialogo_error(self, mensaje_error):
        """Crea un diálogo modal con información del error y opción de limpiar campos"""
        
        def cerrar_dialogo(e):
            self.dialogo_error.open = False
            self.page.update()
        
        def limpiar_y_cerrar(e):
            # Ejecutar limpieza de campos
            self.limpiar_campos_modelo()
            # Cerrar diálogo
            self.dialogo_error.open = False
            self.page.update()
        
        # Crear contenido del diálogo
        contenido = ft.Column([
            ft.Text("❌ Error en el Modelo", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.RED),
            
            ft.Divider(),
            
            ft.Text(
                "Se encontró un problema con los campos:",
                size=14,
                weight=ft.FontWeight.BOLD
            ),
            
            ft.Container(
                content=ft.Text(
                    mensaje_error,
                    size=12,
                    color=ft.Colors.RED_700
                ),
                bgcolor=ft.Colors.RED_50,
                padding=10,
                border_radius=5,
                border=ft.border.all(1, ft.Colors.RED_200)
            ),
            
            ft.Text(
                "💡 Sugerencias:",
                size=14,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_700
            ),
            
            ft.Column([
                ft.Text("• Corrige manualmente los campos problemáticos", size=12),
                ft.Text("• O usa 'Limpiar Campos' para empezar de nuevo", size=12),
                ft.Text("• Evita nombres reservados como 'id' o 'pk'", size=12),
                ft.Text("• Asegúrate de que no haya campos duplicados", size=12),
            ], spacing=5),
            
            ft.Divider(),
            
            ft.Row([
                ft.ElevatedButton(
                    "✏️ Corregir Manualmente",
                    on_click=cerrar_dialogo,
                    bgcolor=ft.Colors.BLUE_600,
                    color=ft.Colors.WHITE
                ),
                ft.ElevatedButton(
                    "🧹 Limpiar Campos",
                    on_click=limpiar_y_cerrar,
                    bgcolor=ft.Colors.ORANGE_600,
                    color=ft.Colors.WHITE
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ], spacing=15)
        
        # Crear el diálogo
        self.dialogo_error = ft.AlertDialog(
            modal=True,
            title=ft.Text("🚨 Error de Validación"),
            content=contenido,
            actions=[
                ft.TextButton("Corregir", on_click=cerrar_dialogo),
                ft.TextButton("Limpiar", on_click=limpiar_y_cerrar)
            ]
        )
        
        return self.dialogo_error

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
                self.lbl_path.color = ft.Colors.BLACK
                self.page.update()
                
        except Exception as e:
            print(f"Error al seleccionar carpeta: {e}")
            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"Error: {str(e)}"),
                bgcolor=ft.Colors.RED
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
            self.lbl_path.color = ft.Colors.BLACK

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
                    icon=ft.Icons.ADD,
                    on_click=self.añadir_campo,
                    style=ft.ButtonStyle(
                        side=ft.BorderSide(1, ft.Colors.BLACK)
                    )
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Guardar Modelo",
                            icon=ft.Icons.SAVE,
                            on_click=self.guardar_modelo,
                            bgcolor=ft.Colors.GREEN_800,
                            color=ft.Colors.WHITE,
                            style=ft.ButtonStyle(
                                side=ft.BorderSide(1, ft.Colors.BLACK)
                            )
                        ),
                        ft.ElevatedButton(
                            "Continuar sin Modelo",
                            icon=ft.Icons.SKIP_NEXT,
                            on_click=self.continuar_sin_modelo,
                            bgcolor=ft.Colors.ORANGE_800,
                            color=ft.Colors.WHITE,
                            style=ft.ButtonStyle(
                                side=ft.BorderSide(1, ft.Colors.BLACK)
                            )
                        )
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER
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
            self.page.update()  # Usar page.update() en lugar de campos_column.update()
            print(f"Campo {new_index + 1} añadido correctamente")
        except Exception as ex:
            print(f"Error al añadir campo: {ex}")

    def _crear_fila_campo(self, index):
        print(f"\nCreando fila {index}...")  
        return ft.Row(
            controls=[
                ft.TextField(
                    hint_text=f"campo_{index}",
                    width=200,
                    value="",  # Forzar valor vacío
                    autofocus=False
                ),
                ft.Dropdown(
                    width=150,
                    options=[
                        ft.dropdown.Option("CharField"),
                        ft.dropdown.Option("IntegerField"), 
                        ft.dropdown.Option("TextField"),
                        ft.dropdown.Option("BooleanField"),
                        ft.dropdown.Option("DateTimeField"),
                        ft.dropdown.Option("EmailField"),
                        ft.dropdown.Option("ForeignKey")
                    ],
                    value="CharField"  # Valor por defecto seguro
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
                    style=ft.ButtonStyle(color=ft.Colors.GREEN)
                )
            )
        for app in self.state.apps_a_crear:
            self.dd_apps.options.append(
                ft.dropdown.Option(
                    text=f"{app} (pendiente)",
                    style=ft.ButtonStyle(color=ft.Colors.ORANGE)
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
                stderr=subprocess.STDOUT,  # Redirige stderr a stdout
                text=True,
                bufsize=1,  # Buffering de línea
                universal_newlines=True
            )

            print(f"Intentando iniciar servidor en http://127.0.0.1:8000")
            print("Monitoreando salida del servidor...")
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
            
            try:
                # Primero intentamos terminar suavemente
                self.state.proceso_servidor.terminate()
                print("Enviando señal de terminación al servidor...")
                
                # Esperamos un poco para que el proceso termine
                try:
                    self.state.proceso_servidor.wait(timeout=3)
                    print("Servidor detenido correctamente")
                except subprocess.TimeoutExpired:
                    # Si no responde en 3 segundos, lo forzamos
                    print("Forzando detención del servidor...")
                    self.state.proceso_servidor.kill()
                    self.state.proceso_servidor.wait()
                    print("Servidor detenido forzosamente")
                    
            except Exception as ex:
                print(f"Error al detener servidor: {ex}")
                
        else:
            print("No hay servidor ejecutándose")
        
        self.btn_iniciar_servidor.disabled = False
        self.btn_detener_servidor.disabled = True
        self.page.update()

    def monitorear_servidor(self):
        while (self.state.proceso_servidor and 
            self.state.proceso_servidor.poll() is None):
            output = self.state.proceso_servidor.stdout.readline().strip()
            if output:
                print(f"[Servidor]: {output}")
        
        # Si el proceso terminó, mostrar el código de salida
        if self.state.proceso_servidor:
            exit_code = self.state.proceso_servidor.poll()
            if exit_code is not None:
                if exit_code != 0:
                    print(f"SERVIDOR TERMINÓ CON ERROR (código: {exit_code})")
                    # Leer cualquier salida restante
                    try:
                        remaining_output = self.state.proceso_servidor.stdout.read()
                        if remaining_output:
                            print(f"Salida final: {remaining_output}")
                    except:
                        pass
                else:
                    print("Servidor detenido normalmente")
                
                # Actualizar estado de botones cuando el proceso termine
                self.btn_iniciar_servidor.disabled = False
                self.btn_detener_servidor.disabled = True
                try:
                    self.page.update()
                except:
                    pass

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
                bgcolor=ft.Colors.GREEN
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
                        bgcolor=ft.Colors.ORANGE
                    )
                except Exception:
                    self.page.snack_bar = ft.SnackBar(
                        ft.Text("Error: Usuario ya existe y no se pudo actualizar"),
                        bgcolor=ft.Colors.RED
                    )
            else:
                self.page.snack_bar = ft.SnackBar(
                    ft.Text(f"Error: {e.stderr}"),
                    bgcolor=ft.Colors.RED
                )
        except Exception as e:
            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"Error: {str(e)}"),
                bgcolor=ft.Colors.RED
            )
        finally:
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