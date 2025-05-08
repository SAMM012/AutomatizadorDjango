# db_config.py
import random
from textwrap import dedent
from pathlib import Path
import subprocess
from pathlib import Path
import os

class DatabaseConfig:
    def __init__(self):
        self.db_type = "sqlite"  # Valor por defecto
        self.postgres_config = {}
        self.models = []

    def set_database_type(self, db_type: str):
        """Define el tipo de base de datos (sqlite/postgres)"""
        self.db_type = db_type

    def set_postgres_config(self, name: str, user: str, password: str, host: str = "localhost", port: str = "5432"):
        """Configuración para PostgreSQL"""
        self.postgres_config = {
            "name": name,
            "user": user,
            "password": password,
            "host": host,
            "port": port
        }

    def add_model(self, model_name: str, fields: list):
        """Añade un modelo con sus campos"""
        self.models.append({
            "name": model_name,
            "fields": fields
        })
    
    def generate_django_settings(self) -> str:
        return dedent('''\
            import os
            from pathlib import Path

            BASE_DIR = Path(__file__).resolve().parent.parent
            SECRET_KEY = '{}'

            DEBUG = True
            ALLOWED_HOSTS = ['*']
            LANGUAGE_CODE = 'es-mx'
            TIME_ZONE = 'America/Mexico_City'

            DATABASES = {{
                'default': {{
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': BASE_DIR / 'db.sqlite3',
                }}
            }}

            INSTALLED_APPS = [
                'django.contrib.admin',
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.messages',
                'django.contrib.staticfiles',
            ]

            STATIC_URL = 'static/'
            STATIC_ROOT = BASE_DIR / 'static'
            '''.format(''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=50))))

    def _generate_sqlite_config(self) -> str:
        return '''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}'''

    def _generate_postgres_config(self) -> str:
        return f'''DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '{self.postgres_config["name"]}',
        'USER': '{self.postgres_config["user"]}',
        'PASSWORD': '{self.postgres_config["password"]}',
        'HOST': '{self.postgres_config["host"]}',
        'PORT': '{self.postgres_config["port"]}',
    }}
}}'''

    def generate_models_code(self) -> str:
        if not self.models:
            return "from django.db import models\n\n# Añade tus modelos aquí."
        code = "from django.db import models\n\n"
        for model in self.models:
            class_name = model['name'].replace("_", "").title()  # "prueba_1" -> "Prueba1"
            code += f"class {class_name}(models.Model):\n"
            for field in model['fields']:
                code += f"    {field['name']} = models.{field['type']}(max_length=100)\n"
            code += "\n\n"
        return code

    def _map_field_type(self, field: dict) -> str:
        tipo = field['type']
        if tipo == "CharField":
            return "models.CharField(max_length=100, blank=True)"
        elif tipo == "EmailField":
            return "models.EmailField(unique=True)"
        elif tipo == "DateTimeField":
            return "models.DateTimeField(auto_now_add=True)"

    def generate_files(self, output_path: str):
        """Genera los archivos de configuración"""
        output_dir = Path(output_path)
        output_dir.mkdir(exist_ok=True)

        # Generar settings.py
        with open(output_dir / "settings.py", "w") as f:
            f.write(self.generate_django_settings())

        # Generar models.py
        with open(output_dir / "models.py", "w") as f:
            f.write(self.generate_models_code())

    def _generate_db_config(self) -> str:
        if self.db_type == "sqlite":
            return self._generate_sqlite_config()
        elif self.db_type == "postgres":
            return self._generate_postgres_config()
        else:
            raise ValueError(f"Tipo de BD no soportado: {self.db_type}")
        

    #Métodos para añadir apps a Setting.py
        
    def create_django_app(self, app_name: str, project_path: str) -> bool:
        """Versión 100% funcional"""
        try:
            project_path = Path(project_path)
            apps_dir = project_path / "apps"
            
            # 1. Crear estructura de directorios
            app_path = apps_dir / app_name
            app_path.mkdir(parents=True, exist_ok=True)
            
            # 2. Crear archivos básicos manualmente
            app_files = {
                "__init__.py": "",
                "apps.py": f"""
    from django.apps import AppConfig

    class {app_name.capitalize()}Config(AppConfig):
        default_auto_field = 'django.db.models.BigAutoField'
        name = 'apps.{app_name}'
                """,
                "models.py": "from django.db import models\n\n# Modelos aquí",
                "admin.py": "from django.contrib import admin\n\n# Registros aquí",
                "views.py": "from django.shortcuts import render\n\n# Vistas aquí"
            }
            
            for filename, content in app_files.items():
                (app_path / filename).write_text(content.strip())
            
            return True
            
        except Exception as e:
            error_msg = f"""
            Error crítico al crear app:
            Ruta usada: {project_path}
            Error: {str(e)}
            """
            print(error_msg)
            return False


    def update_installed_apps(self, app_name: str, settings_path: str) -> None:
        """Añade la app a INSTALLED_APPS en settings.py."""
        try:
            with open(settings_path, "r+") as f:
                content = f.read()
                if f"'django.contrib.staticfiles'" in content:
                    # Insertar la app antes de las apps de terceros
                    new_content = content.replace(
                        "'django.contrib.staticfiles',",
                        f"'django.contrib.staticfiles',\n    '{app_name}',"
                    )
                    f.seek(0)
                    f.write(new_content)
        except Exception as e:
            print(f"Error al actualizar settings.py: {e}")

    