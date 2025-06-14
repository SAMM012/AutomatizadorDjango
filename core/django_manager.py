from pathlib import Path
import subprocess
import os

class DjangoManager:
    @staticmethod
    def create_standard_project(env_path: str, project_name: str, project_dir: str) -> bool:
        """Crea estructura Django estándar con manage.py usando el entorno virtual"""
        try:
            # Ruta al python del entorno virtual
            python_executable = str(
                Path(env_path) / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
            )
            
            subprocess.run(
                [python_executable, "-m", "django", "startproject", project_name, str(project_dir)],
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error al crear proyecto: {e}")
            return False

    @staticmethod
    @staticmethod
    def create_app(project_path: str, app_name: str, python_path: str = "python") -> bool:
        try:
            manage_py = Path(project_path) / "manage.py"
            subprocess.run(
                [python_path, str(manage_py), "startapp", app_name],  # Usa python_path
                check=True,
                cwd=project_path
            )
            return True
        except Exception as e:
            raise print(f"Error al crear app {app_name}: {e}")