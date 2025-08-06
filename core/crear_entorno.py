
import subprocess
from pathlib import Path
import sys
import os

def crear_entorno_virtual(nombre: str, ruta_base: str, nombre_proyecto: str) -> str:
    try:
        ruta_completa = Path(ruta_base) / nombre
        
        # 1. Crear entorno virtual
        subprocess.run([sys.executable, "-m", "venv", str(ruta_completa)], check=True)

        # 2. Instalar Django - Detectar sistema operativo
        if os.name == "nt":  # Windows
            pip_path = str(ruta_completa / "Scripts" / "pip")
            django_admin = str(ruta_completa / "Scripts" / "python")
        else:  # Linux/macOS
            pip_path = str(ruta_completa / "bin" / "pip")
            django_admin = str(ruta_completa / "bin" / "python")
            
        subprocess.run([pip_path, "install", "django"], check=True)
        
        # 3. Crear proyecto Django usando python -m django (más compatible)
        # Django creará automáticamente la carpeta del proyecto
        subprocess.run(
            [django_admin, "-m", "django", "startproject", nombre_proyecto],
            check=True,
            cwd=ruta_base
        )
        
        return f"Entorno '{nombre}' y proyecto '{nombre_proyecto}' creados correctamente"
    except subprocess.CalledProcessError as e:
        # Si hay error de nombre conflictivo, sugerir alternativa
        if "conflicts with the name" in str(e):
            return f"Error: El nombre '{nombre_proyecto}' está reservado. Prueba con nombres como: sitio_web, mi_app, proyecto_django"
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"