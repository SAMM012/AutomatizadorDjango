# tests/conftest.py
import pytest
import asyncio
from unittest.mock import Mock
import flet as ft

@pytest.fixture
def mock_page():
    """Fixture compartido para mock de Page"""
    page = Mock(spec=ft.Page)
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.window_min_width = 530
    page.window_min_height = 820
    return page

@pytest.fixture(scope="session")
def event_loop():
    """Provee un event loop para pruebas asíncronas"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()