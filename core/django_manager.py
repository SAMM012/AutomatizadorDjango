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
    def create_app(project_path: str, app_name: str, python_path: str = "python") -> bool:
        """Crea una nueva app Django"""
        try:
            # Validación básica
            if not app_name.strip():
                print("Error: El nombre de la app no puede estar vacío")
                return False
                
            manage_py = Path(project_path) / "manage.py"
            if not manage_py.exists():
                print(f"Error: manage.py no encontrado en {project_path}")
                return False
                
            subprocess.run(
                [python_path, str(manage_py), "startapp", app_name],
                check=True,
                cwd=project_path
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error al crear app {app_name}: {e}")
            return False
        except Exception as e:
            print(f"Error inesperado al crear app {app_name}: {e}")
            return False

    @staticmethod
    def generate_apps_structure(project_path: str, apps_list: list, project_name: str) -> dict:
        """
        Genera la estructura completa de apps Django
        
        Args:
            project_path: Ruta del proyecto Django
            apps_list: Lista de nombres de apps a crear
            project_name: Nombre del proyecto para actualizar settings.py
            
        Returns:
            dict: Resultado con éxito/fallo y mensajes
        """
        try:
            project_dir = Path(project_path)
            results = {"success": [], "errors": []}
            
            # 1. Crear directorio apps si no existe
            apps_dir = project_dir / "apps"
            apps_dir.mkdir(exist_ok=True)
            
            # 2. Crear cada app
            for app_name in apps_list:
                try:
                    app_result = DjangoManager._create_single_app(project_dir, app_name, project_name)
                    if app_result["success"]:
                        results["success"].append(app_name)
                    else:
                        results["errors"].append(f"{app_name}: {app_result['error']}")
                except Exception as e:
                    results["errors"].append(f"{app_name}: {str(e)}")
            
            return results
            
        except Exception as e:
            return {"success": [], "errors": [f"Error general: {str(e)}"]}

    @staticmethod
    def _create_single_app(project_dir: Path, app_name: str, project_name: str) -> dict:
        """Crea una app individual con todos sus archivos"""
        try:
            apps_dir = project_dir / "apps"
            app_dir = apps_dir / app_name
            app_dir.mkdir(exist_ok=True)
            
            # Crear archivos esenciales
            DjangoManager._create_app_files(app_dir, app_name)
            
            # Actualizar settings.py
            DjangoManager._update_settings_with_app(project_dir, app_name, project_name)
            
            return {"success": True, "error": None}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def _create_app_files(app_dir: Path, app_name: str):
        """Crea los archivos básicos de una app Django"""
        # __init__.py
        init_file = app_dir / "__init__.py"
        if not init_file.exists():
            init_file.touch()
        
        # apps.py
        apps_py = app_dir / "apps.py"
        if not apps_py.exists():
            apps_content = f"""from django.apps import AppConfig

class {app_name.capitalize()}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app_name}'
"""
            with open(apps_py, "w") as f:
                f.write(apps_content)

        # models.py
        models_py = app_dir / "models.py"
        if not models_py.exists():
            with open(models_py, "w") as f:
                f.write("from django.db import models\n\n# Modelos aquí\n")
        
        # admin.py
        admin_py = app_dir / "admin.py"
        if not admin_py.exists():
            with open(admin_py, "w") as f:
                f.write("from django.contrib import admin\n\n# Registra tus modelos aquí\n")
        
        # views.py
        views_py = app_dir / "views.py"
        if not views_py.exists():
            with open(views_py, "w") as f:
                f.write("from django.shortcuts import render\n\n# Vistas aquí\n")

    @staticmethod
    def _update_settings_with_app(project_dir: Path, app_name: str, project_name: str):
        """Actualiza settings.py para incluir la nueva app"""
        settings_path = project_dir / project_name / "settings.py"
        
        if not settings_path.exists():
            # Buscar settings.py en posibles ubicaciones
            possible_paths = [
                project_dir / "Mi_proyecto" / "settings.py",
                project_dir / project_name.lower() / "settings.py"
            ]
            
            for path in possible_paths:
                if path.exists():
                    settings_path = path
                    break
        
        if settings_path.exists():
            with open(settings_path, "r+") as f:
                content = f.read()
                
                # Verificar si la app ya está registrada
                if f"'apps.{app_name}'" not in content:
                    # Buscar INSTALLED_APPS y agregar la app
                    if "'django.contrib.staticfiles'," in content:
                        new_content = content.replace(
                            "'django.contrib.staticfiles',",
                            f"'django.contrib.staticfiles',\n    'apps.{app_name}',"
                        )
                        f.seek(0)
                        f.write(new_content)
                        f.truncate()
        else:
            print(f"Advertencia: No se encontró settings.py para registrar {app_name}")

    @staticmethod
    def generar_apps_legacy(project_path: str, apps_list: list) -> dict:
        """
        Migración exacta del método generar_apps() original
        Mantiene la misma lógica que funcionaba en interfaz.py
        
        Args:
            project_path: Ruta del proyecto Django
            apps_list: Lista de apps a crear
            
        Returns:
            dict: {"success": bool, "apps_creadas": list, "error": str}
        """
        try:
            if not project_path:
                return {"success": False, "apps_creadas": [], "error": "Primero crea el proyecto Django"}
                
            project_dir = Path(project_path)
            
            # Crear directorio apps si no existe
            apps_dir = project_dir / "apps"
            apps_dir.mkdir(exist_ok=True)
            
            apps_creadas = []
            
            # Asegurar que cada app tenga estructura completa
            for app_name in apps_list:
                app_dir = apps_dir / app_name
                app_dir.mkdir(exist_ok=True)
                
                # Archivos esenciales
                init_file = app_dir / "__init__.py"
                if not init_file.exists():
                    init_file.touch()
                
                # apps.py completo
                apps_py = app_dir / "apps.py"
                if not apps_py.exists():
                    with open(apps_py, "w") as f:
                        f.write(f"""from django.apps import AppConfig
class {app_name.capitalize()}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app_name}'
""")
                
                # models.py vacío si no existe
                models_py = app_dir / "models.py"
                if not models_py.exists():
                    with open(models_py, "w") as f:
                        f.write("from django.db import models\n\n# Modelos aquí\n")
                
                # admin.py (vacío)
                admin_py = app_dir / "admin.py"
                if not admin_py.exists():
                    with open(admin_py, "w") as f:
                        f.write("from django.contrib import admin\n\n# Registra tus modelos aquí\n")
                
                # views.py (vacío)
                views_py = app_dir / "views.py"
                if not views_py.exists():
                    with open(views_py, "w") as f:
                        f.write("from django.shortcuts import render\n\n# Vistas aquí\n")
                
                # Actualizar settings.py - EXACTAMENTE como en tu código original
                settings_path = project_dir / "Mi_proyecto" / "settings.py"
                if settings_path.exists():
                    with open(settings_path, "r+") as f:
                        content = f.read()
                        if f"'apps.{app_name}'" not in content:
                            new_content = content.replace(
                                "'django.contrib.staticfiles',",
                                f"'django.contrib.staticfiles',\n    'apps.{app_name}',"
                            )
                            f.seek(0)
                            f.write(new_content)
                            f.truncate()
                
                apps_creadas.append(app_name)
                print(f"App '{app_name}' creada exitosamente")
            
            print(f"Apps generadas: {', '.join(apps_creadas)}")
            return {"success": True, "apps_creadas": apps_creadas, "error": None}
        
        except Exception as ex:
            error_msg = f"Error al generar apps: {str(ex)}"
            print(error_msg)
            return {"success": False, "apps_creadas": [], "error": error_msg}