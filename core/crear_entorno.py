# crear_entorno.py
import subprocess
from pathlib import Path
import sys

def crear_entorno_virtual(nombre: str, ruta_base: str, nombre_proyecto: str) -> str:
    try:
        ruta_completa = Path(ruta_base) / nombre
        
        # 1. Crear entorno virtual
        subprocess.run([sys.executable, "-m", "venv", str(ruta_completa)], check=True)

        # 2. Instalar Django
        pip_path = str(ruta_completa / "Scripts" / "pip")
        subprocess.run([pip_path, "install", "django"], check=True)
        
        # 3. Crear carpeta del proyecto
        proyecto_path = Path(ruta_base) / nombre_proyecto
        proyecto_path.mkdir(exist_ok=True)
        
        # 4. Crear proyecto Django
        django_admin = str(ruta_completa / "Scripts" / "django-admin")
        subprocess.run(
            [django_admin, "startproject", nombre_proyecto, str(proyecto_path)],
            check=True,
            cwd=ruta_base
        )
        
        return f"Entorno '{nombre}' y proyecto '{nombre_proyecto}' creados correctamente"
    except Exception as e:
        return f"Error: {str(e)}"