import flet as ft
from core.crear_carpeta import FolderCreatorLogic

class UI:

    def __init__(self):
        self.color_teal = "teal"
        self.contenedor1 = ft.Container(
            col=4,
            expand=True,
            bgcolor=self.color_teal,
            #border=ft.border.all(2, "black"),
            border_radius=10,
            padding=10,
            content=ft.Column(
                #Contenedor1
                expand=True,
                controls=[
                    ft.Container(
                        expand=True,
                        #padding=ft.padding.only(bottom=10),
                        alignment=ft.alignment.center,
                        content=ft.Row(
                            controls=[
                                ft.Text("PANEL 1", size=20, weight=ft.FontWeight.BOLD)
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
                                content=ft.Column(
                                    controls=[
                                        ft.Text("Nombre de la carpeta:", weight=ft.FontWeight.BOLD),
                                        ft.TextField(
                                            label="Ej: Mi proyecto",
                                            width= 150,
                                            height= 40
                                        ),
                                        ft.ElevatedButton(
                                            "Seleccionar ubicaciion",
                                            icon=ft.icons.FOLDER_OPEN,
                                            on_click=lambda e: self.open_folder_dialog()
                                        ),
                                        ft.Text("Ubicacion seleccionada:", style=ft.TextThemeStyle.BODY_SMALL)
                                    ],
                                    spacing=10
                                ),
                                padding=20
                            ), 
                            ft.Container(

                            ),
                            ft.Container(
                                width=100,
                                alignment=ft.alignment.center,
                                content=ft.ElevatedButton(
                                    content=ft.Text("CREAR", color="white"),
                                    bgcolor="#4CAF50",
                                    height=40,
                                    on_click=lambda e: self.create_folder_action(),
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=2),
                                        overlay_color=ft.colors.with_opacity(0.1, "white")
                                    )
                                )
                            ),                     
                        ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                ]
            )

        )

        self.contenedores = ft.ResponsiveRow(
            controls=[
                self.contenedor1
            ]
        )



    def build(self):
        return self.contenedores
    
def main(page: ft.Page):

    page.window_min_height = 820
    page.window_min_width = 530
    page.theme_mode = ft.ThemeMode.SYSTEM 

    ui = UI() 
    page.add(ui.build())

ft.app(target=main)