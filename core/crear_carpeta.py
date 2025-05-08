import os
import flet as ft
from typing import Tuple, Optional
import asyncio

class FolderCreatorLogic:

    def __init__(self, page:ft.Page):
        self.page = page
        self.folder_path = ""
        self.folder_name = ""
        self.file_picker = ft.FilePicker(on_result=self._folder_selected)
        page.overlay.append(self.file_picker)


    async def open_folder_dialog(self) -> Optional[str]:
        #Abre el diálogo nativo para seleccionar carpeta
        self.file_picker.get_directory_path()
        while not hasattr(self.file_picker, 'result'):
            await asyncio.sleep(0.1)
        return self.folder_path

    def _folder_selected(self, e: ft.FilePickerResultEvent):
        "Cuando se selecciona carpeta"
        if e.path:
            self.folder_path = e.path
            # Se conecta a la interfaz
        return e.path if e.path else None
    
    def create_folder_action(self) -> Tuple[bool, str, Optional[str]]:
        "Crear carpeta y validar"
        if not self.folder_path:
            return False, "Selecciona una ubicacion", None
        
        if not self.folder_name:
            return False, "El nombre no puede estar vacio", None
        
        try:
            full_path = os.path.join(self.folder_path, self.folder_name)
            os.makedirs(full_path, exist_ok=False)
            return True, f"Carpeta '{self.folder_name}' creada en {self.folder_path}", full_path
        
        except FileExistsError:
            return False, f"La carpeta '{self.folder_name}' ya existe", None
        
        except Exception as e:
            return False, f"Error: {str(e)}", None
        
    async def get_selected_path(self):
        return self.folder_path
    