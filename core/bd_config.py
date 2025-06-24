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
        self.apps={}

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

    def add_model(self, app_name: str, model_name: str, fields: list):
        if app_name not in self.apps:
            self.apps[app_name] = []
            
        self.apps[app_name].append({
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
        project_dir = Path(output_path)
        
        apps_dir = project_dir / "apps"
        apps_dir.mkdir(exist_ok=True)

        settings_dir = project_dir / "mi_proyecto"
        settings_dir.mkdir(parents=True, exist_ok=True)
        
        if not (settings_dir / "settings.py").exists():
            with open(settings_dir / "settings.py", "w") as f:
                f.write(self.generate_django_settings()) 
        
        for app_name, models in self.apps.items():
            app_dir = project_dir / "apps" / app_name
            app_dir.mkdir(exist_ok=True)
            
            with open(app_dir / "models.py", "w") as f:
                f.write("from django.db import models\n\n")
                for model in models:
                    f.write(f"class {model['name']}(models.Model):\n")
                    for field in model['fields']:
                        f.write(f"    {field['name']} = models.{field['type']}\n")
                    f.write("\n\n")

            with open(app_dir / "admin.py", "w") as f:
                f.write("from django.contrib import admin\nfrom .models import *\n\n")
                for model in models:
                    f.write(f"admin.site.register({model['name']})\n")

    def _generate_db_config(self) -> str:
        if self.db_type == "sqlite":
            return self._generate_sqlite_config()
        elif self.db_type == "postgres":
            return self._generate_postgres_config()
        else:
            raise ValueError(f"Tipo de BD no soportado: {self.db_type}")
        

    #Métodos para añadir apps a Setting.py
        
    def create_django_app(self, app_name: str, project_path: str) -> bool:
        try:
            app_path = Path(project_path) / "apps" / app_name
            app_path.mkdir(parents=True, exist_ok=True)
            
            # Crear solo los archivos básicos si no existen
            (app_path / "__init__.py").touch(exist_ok=True)
            (app_path / "apps.py").write_text(f"""
    from django.apps import AppConfig

    class {app_name.capitalize()}Config(AppConfig):
        default_auto_field = 'django.db.models.BigAutoField'
        name = 'apps.{app_name}'
    """.strip(), exist_ok=True)
            (app_path / "models.py").write_text("from django.db import models\n\n# Modelos aquí\n", exist_ok=True)
            (app_path / "admin.py").write_text("from django.contrib import admin\n\n# Registra tus modelos aquí\n", exist_ok=True)
            (app_path / "views.py").write_text("from django.shortcuts import render\n\n# Vistas aquí\n", exist_ok=True)
            
            return True
        except Exception as e:
            print(f"Error al crear app: {e}")
            return False


    def update_installed_apps(self, settings_path: str, app_name: str):
        """Añade la app a INSTALLED_APPS en settings.py"""
        try:
            with open(settings_path, 'r+') as f:
                content = f.read()
                
                # Verificar si la app ya está registrada
                if f"'apps.{app_name}'" in content:
                    return
                
                # Buscar el bloque INSTALLED_APPS
                if "'django.contrib.staticfiles'" in content:
                    nuevo_content = content.replace(
                        "'django.contrib.staticfiles',",
                        f"'django.contrib.staticfiles',\n    'apps.{app_name}',"
                    )
                    f.seek(0)
                    f.write(nuevo_content)
                    f.truncate()
        except Exception as e:
            print(f"Error al actualizar settings.py: {e}")

    def generar_modelo(self, app_name: str, model_name: str, fields: dict):
        """Genera código para un modelo y lo añade a models.py"""
        model_code = f"\nclass {model_name}(models.Model):\n"
        for field_name, field_type in fields.items():
            model_code += f"    {field_name} = models.{field_type}\n"
        return model_code

    def ejecutar_migraciones(self, project_path: str):
        """Ejecuta makemigrations y migrate"""
        try:
            manage_py = Path(project_path) / "manage.py"
            subprocess.run(["python", str(manage_py), "makemigrations"], check=True)
            subprocess.run(["python", str(manage_py), "migrate"], check=True)
            return True
        except Exception as e:
            print(f"Error en migraciones: {e}")
            return False