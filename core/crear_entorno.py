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
    

    
"""
    def generar_proyecto(self, e):
        try:
            if not self.ruta_base:
                raise ValueError("Selecciona una ubicación para el proyecto primero.")

            project_path = Path(self.ruta_proyecto) if hasattr(self, 'ruta_proyecto') else Path(self.ruta_base) / "Mi_proyecto"

            if hasattr(self, 'txt_tabla') and self.txt_tabla.value.strip():
                nombre_tabla = self.txt_tabla.value.strip()
                campos = []
                for row in self.campos_column.controls[1:]:  
                    if isinstance(row, ft.Row):
                        nombre_campo = row.controls[0].value.strip()
                        tipo_campo = row.controls[1].value
                        if nombre_campo:  # Ignorar campos vacíos
                            campos.append({"name": nombre_campo, "type": tipo_campo})
                
                if campos and self.dd_apps.value:
                    app_name = self.dd_apps.value.replace(" (pendiente)", "")
                    self.db_config.add_model(app_name, nombre_tabla, campos)

            self.db_config.generate_files(str(project_path))

            if project_path.exists():
                manage_py = project_path / "manage.py"
                if manage_py.exists():
                    subprocess.run(["python", str(manage_py), "makemigrations"], check=True, cwd=str(project_path))
                    subprocess.run(["python", str(manage_py), "migrate"], check=True, cwd=str(project_path))
                    
                    print("¡Proyecto generado exitosamente!")

        except subprocess.CalledProcessError:
            print("Modelos creados pero falló la migración")
        except Exception as ex:
            print(f"Error: {str(ex)}")
    """

"""
def generar_apps(self, e):
        if not hasattr(self, 'ruta_proyecto') or not self.ruta_proyecto:
            print("Primero crea el proyecto Django")
            return
        
        try:
            project_dir = Path(self.ruta_proyecto)
            print(f"\n[DEBUG] Ruta confirmada: {project_dir}")
            print(f"Contenido: {[f.name for f in project_dir.glob('*')]}")
            
            apps_dir = project_dir / "apps"
            apps_dir.mkdir(exist_ok=True)

            settings_path=None
            possible_paths = [
                project_dir / "settings.py",
                project_dir / project_dir.name / "settings.py",
                project_dir / self.txt_nombre_proyecto.value.strip() / "settings.py"
            ]

            for path in possible_paths:
                if path.exists():
                    settings_path = path
                    break

            if not settings_path:
                settings_files = list(project_dir.glob('**/settings.py'))
                if settings_files:
                    settings_path = settings_files[0]
                else:
                    raise FileNotFoundError("No se encontró settings.py en el proyecto")        
            print(f"Usando settings.py en: {settings_path}")
            
            for app_name in self.apps_a_crear:
                app_path = apps_dir / app_name
                app_path.mkdir(exist_ok=False)
                
                (app_path / "__init__.py").touch()
                (app_path / "apps.py").write_text(f#from django.apps import AppConfig

    #class {app_name.capitalize()}Config(AppConfig):
        #default_auto_field = 'django.db.models.BigAutoField'
       # name = 'apps.{app_name}'
               "")
                with open(settings_path, 'r+') as f:
                    content = f.read()
                    if f"'apps.{app_name}'" not in content:
                        new_content = content.replace(
                            "'django.contrib.staticfiles',",
                            f"'django.contrib.staticfiles',\n    'apps.{app_name}',"
                        )
                        f.seek(0)
                        f.write(new_content)
                        f.truncate()
                
                print(f"App '{app_name}' creada y registrada en settings.py")
                
                if app_name not in self.apps_generadas:
                 self.apps_generadas.append(app_name)
            
            self.actualizar_dropdown_apps()
            self.apps_a_crear.clear()
            self.lista_apps.controls.clear()

            self.dd_apps.options = [
                ft.dropdown.Option(app) for app in self.apps_generadas
            ]

            self.page.update()
            
        except Exception as ex:
            print(f"Error: {str(ex)}")
"""

"""
    async def generar_proyecto(self, e):
        try:
            if not self.ruta_base:
                raise ValueError("Selecciona una ubicación para el proyecto primero")

            project_path = Path(self.ruta_proyecto) if hasattr(self, 'ruta_proyecto') else Path(self.ruta_base) / "Mi_proyecto"
            self.db_config.generate_files(str(project_path))
            manage_py = project_path / "manage.py"

            if manage_py.exists():
                print("Proyecto Django ya existe. Continuando...")
            else:
                venv_python = str(Path(self.ruta_base) / "venv" / ("Scripts" if os.name == "nt" else "bin") / "python")

            if not hasattr(self, 'django_manager'):
                self.django_manager = DjangoManager()

            if not self.django_manager.create_standard_project(
                env_path=str(Path(self.ruta_base) / "venv"),
                project_name="Mi_proyecto",
                project_dir=str(project_path)
            ):
                raise Exception("Falló la creación del proyecto")

            if manage_py.exists():
                try:
                    subprocess.run(
                        [venv_python, str(manage_py), "makemigrations"],
                        check=True,
                        cwd=str(project_path)
                    )
                    subprocess.run(
                        [venv_python, str(manage_py), "migrate"],
                        check=True,
                        cwd=str(project_path)
                    )
                    print("¡Proyecto generado y migraciones ejecutadas correctamente!")
                except subprocess.CalledProcessError as e:
                    error_msg = (
                        "Modelos creados pero falló la migración.\n"
                        f"Ejecuta manualmente:\ncd {project_path}\n{venv_python} manage.py migrate"
                    )
                    print(error_msg)
            
            print("¡Proyecto generado exitosamente!")
        except Exception as ex:
            print(f"Error al generar proyecto: {str(ex)}")
"""

"""
def guardar_modelo(self, e):

        try:
            # Validación de campos duplicados
            es_valido, nombres_campos = self._validar_campos_modelo()
            if not es_valido:
                duplicados = [nombre for nombre in nombres_campos if nombres_campos.count(nombre) > 1]
                print(f"Nombres de campo duplicados: {', '.join(set(duplicados))}")
                return

            nombre_tabla = self.txt_tabla.value.strip()
            if not nombre_tabla:
                print("Ingresa un nombre para la tabla")
                return
    
            if not self.dd_apps.value:
                print("Selecciona una app primero")
                return
                
            app_name = self.dd_apps.value.replace(" (pendiente)", "")
            print(f"Guardando modelo para app: {app_name}")  # Debug
            
            app_dir = Path(self.ruta_proyecto) / "apps" / app_name
            
            if not app_dir.exists():
                print(f"La app {app_name} no existe. Genera la app primero.")
                return

            models_path = app_dir / "models.py"
            print(f"Ruta models.py: {models_path}")  # Debug

            if not models_path.exists():
                with open(models_path, "w") as f:
                    f.write("from django.db import models\n\n")
                print(f"models.py creado en {models_path}")

            campos = []
            for row in self.campos_column.controls[1:]:
                if isinstance(row, ft.Row):
                    nombre_campo = row.controls[0].value.strip()
                    tipo_campo = row.controls[1].value
                    if nombre_campo and tipo_campo:
                        campos.append({"name": nombre_campo, "type": tipo_campo})
            
            print(f"Campos recolectados: {len(campos)}")  # Debug
            
            with open(models_path, "a") as f:
                f.write(f"\nclass {nombre_tabla}(models.Model):\n")
                if campos:
                    for campo in campos:
                        f.write(f"    {campo['name']} = models.{campo['type']}()\n")
                else:
                    f.write("    pass  # Modelo vacío\n")
            
            admin_path = app_dir / "admin.py"
            print(f"Ruta admin.py: {admin_path}")  # Debug
            
            if not admin_path.exists():
                with open(admin_path, "w") as f:
                    f.write("from django.contrib import admin\n")
                    f.write(f"from .models import {nombre_tabla}\n\n")
                    f.write(f"admin.site.register({nombre_tabla})\n")
                print(f"admin.py creado en {admin_path}")
            else:
                with open(admin_path, "a") as f:
                    f.write(f"admin.site.register({nombre_tabla})\n")
                print(f"Modelo registrado en admin.py existente")
            
            print(f"Modelo '{nombre_tabla}' creado en {app_name}/models.py")
            
            if hasattr(self, 'ruta_proyecto') and self.ruta_proyecto:
                try:
                    venv_python = Path(self.ruta_base) / "venv" / "Scripts" / "python"
                    manage_py = Path(self.ruta_proyecto) / "manage.py"
                    
                    if venv_python.exists() and manage_py.exists():
                        subprocess.run(
                            [str(venv_python), str(manage_py), "makemigrations", app_name],
                            check=True,
                            cwd=str(self.ruta_proyecto)
                        )
                        subprocess.run(
                            [str(venv_python), str(manage_py), "migrate"],
                            check=True,
                            cwd=str(self.ruta_proyecto)
                        )
                        print("¡Migraciones ejecutadas correctamente!")
                    else:
                        print("No se encontró el entorno virtual o manage.py")
                except subprocess.CalledProcessError as e:
                    print(f"Error en migraciones: {str(e)}")
                    print("Modelo creado pero falló la migración", color="orange")
            
        except Exception as ex:
            import traceback
            traceback.print_exc()  # Error completo
            print(f"Error: {str(ex)}" )
"""
"""
 async def guardar_modelo(self, e):
        try:
            nombre_tabla = self.txt_tabla.value.strip()
            if not nombre_tabla:
                print("Ingresa un nombre para la tabla")
                return
            
            if not self.dd_apps.value:
                print("Selecciona una app primero")
                return
    
            app_name = self.dd_apps.value.replace(" (pendiente)", "")
            app_dir = Path(self.ruta_proyecto) / "apps" / app_name
            app_dir.mkdir(parents=True, exist_ok=True)
                    
            models_path = app_dir / "models.py"
            modelo_existente = ""
            if models_path.exists():
                with open(models_path, "r") as f:
                    modelo_existente = f.read()

            if "from django.db import models" not in modelo_existente:
                modelo_existente = "from django.db import models\n\n" + modelo_existente
            campos = self.obtener_campos()
            codigo_modelo = f"\nclass {nombre_tabla}(models.Model):\n"
            for campo in campos:
                codigo_modelo += f"    {campo['name']} = models.{campo['type']}()\n"
            
            with open(models_path, "w") as f:
                f.write(modelo_existente + codigo_modelo)
            
            admin_path = app_dir / "admin.py"
            admin_existente = ""
            if admin_path.exists():
                with open(admin_path, "r") as f:
                    admin_existente = f.read()
            
            if "from django.contrib import admin" not in admin_existente:
                admin_existente = "from django.contrib import admin\n\n" + admin_existente
        
            if f"from .models import {nombre_tabla}" not in admin_existente:
                admin_existente += f"\nfrom .models import {nombre_tabla}\n"
            
            if f"admin.site.register({nombre_tabla})" not in admin_existente:
                admin_existente += f"\nadmin.site.register({nombre_tabla})\n"
            
            with open(admin_path, "w") as f:
                f.write(admin_existente)
            
            print(f"Modelo '{nombre_tabla}' creado en {app_name}/models.py")

            if hasattr(self, 'ruta_proyecto') and self.ruta_proyecto:
                try:
                    venv_python = str(Path(self.ruta_base) / "venv" / ("Scripts" if os.name == "nt" else "bin") / "python")
                    manage_py = Path(self.ruta_proyecto) / "manage.py"
                    
                    if venv_python and manage_py.exists():
                        subprocess.run(
                            [venv_python, str(manage_py), "makemigrations", app_name],
                            check=True,
                            cwd=str(self.ruta_proyecto))
                        subprocess.run(
                            [venv_python, str(manage_py), "migrate"],
                            check=True,
                            cwd=str(self.ruta_proyecto))
                        print("¡Migraciones aplicadas exitosamente!")
                except subprocess.CalledProcessError as e:
                    print(f"Error en migraciones: {e.stderr}")
                
            self.page.update()

        except Exception as ex:
            print(f"Error al guardar modelo: {str(ex)}")   

"""