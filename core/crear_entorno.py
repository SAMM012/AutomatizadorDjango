# crear_entorno.py
import subprocess
from pathlib import Path
import sys


def crear_entorno_virtual(nombre: str, ruta_base: str) -> str:
    try:
        ruta_completa = Path(ruta_base) / nombre
        
        # Verificar si el nombre es válido
        if not nombre.isidentifier():
            return "Error: Nombre no válido (usar solo letras, números y guiones bajos)"
            
        # Crear el entorno virtual
        subprocess.run(
            [sys.executable, "-m", "venv", str(ruta_completa)], 
            check=True,
            capture_output=True,
            text=True
        )

        pip_path = str(ruta_completa / "Scripts" / "pip") if sys.platform == "win32" else str(ruta_completa / "bin" / "pip")

        #Intalar DJANGO

        subprocess.run(
            [pip_path, "install", "django"],
            check=True,
            capture_output=True,
            text=True
        )
        
        return f"Entorno '{nombre}' creado en:\n{ruta_completa}"
        
    except subprocess.CalledProcessError as e:
        return f"Error al crear entorno:\n{e.stderr}"
    except Exception as e:
        return f"Error inesperado:\n{str(e)}"