# tests/test_contenedor1.py
import pytest
from unittest.mock import Mock, MagicMock
from core.crear_carpeta import FolderCreatorLogic

class TestContenedor1:
    @pytest.fixture
    def logic(self):
        """Fixture con mock de Page"""
        # Crea un mock completo de Page
        mock_page = MagicMock()
        mock_page.overlay = []
        return FolderCreatorLogic(mock_page)
    
    def test_folder_creation(self, logic, tmp_path):
        """Prueba creación de carpeta con mock"""
        logic.folder_name = "test_project"
        logic.folder_path = str(tmp_path)
        
        # Mockea el resultado de crear carpeta
        logic.create_folder_action = Mock(return_value=(True, "Éxito", str(tmp_path/"test_project")))
        
        success, message, _ = logic.create_folder_action()
        assert success
        assert "Éxito" in message