# tests/test_ui_contenedor1.py
import pytest
from unittest.mock import MagicMock, AsyncMock
from interfaz import UI

class TestUIContenedor1:
    @pytest.fixture
    def ui(self):
        """Fixture con UI y mocks necesarios"""
        mock_page = MagicMock()
        mock_page.theme_mode = "system"
        return UI(mock_page)
    
    def test_ui_components(self, ui):
        """Prueba que los componentes existen"""
        assert hasattr(ui, 'contenedor1')
        assert hasattr(ui, 'txt_folder_name')
        
    def test_update_folder_name(self, ui):
        """Prueba actualización de nombre"""
        # Simula evento de cambio
        mock_event = MagicMock()
        mock_event.control.value = "nuevo_proyecto"
        
        ui.update_folder_name(mock_event)
        assert ui.logic.folder_name == "nuevo_proyecto"