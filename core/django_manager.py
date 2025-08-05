from pathlib import Path
import re
import subprocess
import os

class DjangoManager:
    @staticmethod
    def create_standard_project(env_path: str, project_name: str, project_dir: str) -> bool:
        try:
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
        try:
            project_dir = Path(project_path)
            results = {"success": [], "errors": []}            
            apps_dir = project_dir / "apps"
            apps_dir.mkdir(exist_ok=True)            
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
        try:
            apps_dir = project_dir / "apps"
            app_dir = apps_dir / app_name
            app_dir.mkdir(exist_ok=True)            
            DjangoManager._create_app_files(app_dir, app_name)
            DjangoManager._update_settings_with_app(project_dir, app_name, project_name)
            return {"success": True, "error": None}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def _create_app_files(app_dir: Path, app_name: str):
        init_file = app_dir / "__init__.py"
        if not init_file.exists():
            init_file.touch()
        
        apps_py = app_dir / "apps.py"
        if not apps_py.exists():
            apps_content = f"""from django.apps import AppConfig

class {app_name.capitalize()}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app_name}'
"""
            with open(apps_py, "w") as f:
                f.write(apps_content)
        models_py = app_dir / "models.py"
        if not models_py.exists():
            with open(models_py, "w") as f:
                f.write("from django.db import models\n\n# Modelos aquí\n")        
        admin_py = app_dir / "admin.py"
        if not admin_py.exists():
            with open(admin_py, "w") as f:
                f.write("from django.contrib import admin\n\n# Registra tus modelos aquí\n")        
        views_py = app_dir / "views.py"
        if not views_py.exists():
            with open(views_py, "w") as f:
                f.write("from django.shortcuts import render\n\n# Vistas aquí\n")

    @staticmethod
    def _update_settings_with_app(project_dir: Path, app_name: str, project_name: str):
        settings_path = project_dir / project_name / "settings.py"
        
        if not settings_path.exists():
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
                if f"'apps.{app_name}'" not in content:
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
    def crear_modelo(project_path: str, app_name: str, nombre_tabla: str, campos: list, venv_path: str) -> dict:
        try:
            project_dir = Path(project_path)
            app_dir = project_dir / "apps" / app_name
            if not app_dir.exists():
                return {"success": False, "error": f"La app {app_name} no existe"}
            TIPOS_VALIDOS = {
                'CharField': 'CharField(max_length=100)',
                'IntegerField': 'IntegerField()',
                'TextField': 'TextField()',
                'BooleanField': 'BooleanField()',
                'DateTimeField': 'DateTimeField(auto_now_add=True)',
                'EmailField': 'EmailField()',
                'ForeignKey': 'ForeignKey(to="self", on_delete=models.CASCADE)'
            }
            models_path = app_dir / "models.py"
            contenido = "from django.db import models\n\n"
            if models_path.exists():
                with open(models_path, "r") as f:
                    contenido = f.read()
            nuevo_modelo = f"class {nombre_tabla}(models.Model):\n"
            for campo in campos:
                tipo_campo = campo['type']
                if tipo_campo not in TIPOS_VALIDOS:
                    tipo_campo = 'CharField'
                    print(f"Tipo '{campo['type']}' no válido. Usando CharField")
                    
                nuevo_modelo += f"    {campo['name']} = models.{TIPOS_VALIDOS[tipo_campo]}\n"
            patron = re.compile(rf"class {nombre_tabla}\(models\.Model\):.*?\n\n", re.DOTALL)
            if patron.search(contenido):
                contenido = patron.sub(nuevo_modelo, contenido)
            else:
                contenido += "\n" + nuevo_modelo
            
            with open(models_path, "w") as f:
                f.write(contenido)
            admin_path = app_dir / "admin.py"
            admin_content = "from django.contrib import admin\n"
            
            if admin_path.exists():
                with open(admin_path, "r") as f:
                    admin_content = f.read()
            if f"from .models import {nombre_tabla}" not in admin_content:
                admin_content += f"\nfrom .models import {nombre_tabla}\n"

            if f"admin.site.register({nombre_tabla})" not in admin_content:
                admin_content += f"\nadmin.site.register({nombre_tabla})\n"
            
            with open(admin_path, "w") as f:
                f.write(admin_content)
            
            venv_python = Path(venv_path) / ("Scripts" if os.name == "nt" else "bin") / "python"
            manage_py = project_dir / "manage.py"
            
            subprocess.run(
                [str(venv_python), str(manage_py), "makemigrations", app_name],
                check=True,
                cwd=str(project_dir)
            )
            subprocess.run(
                [str(venv_python), str(manage_py), "migrate"],
                check=True,
                cwd=str(project_dir)
            )
            
            return {"success": True, "error": None}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def generar_apps_legacy(project_path: str, apps_list: list) -> dict:
        try:
            if not project_path:
                return {"success": False, "apps_creadas": [], "error": "Primero crea el proyecto Django"}
                
            project_dir = Path(project_path)
            apps_dir = project_dir / "apps"
            apps_dir.mkdir(exist_ok=True)
            apps_creadas = []
            for app_name in apps_list:
                app_dir = apps_dir / app_name
                app_dir.mkdir(exist_ok=True)
                init_file = app_dir / "__init__.py"
                if not init_file.exists():
                    init_file.touch()
                apps_py = app_dir / "apps.py"
                if not apps_py.exists():
                    with open(apps_py, "w") as f:
                        f.write(f"""from django.apps import AppConfig
class {app_name.capitalize()}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app_name}'
""")
                models_py = app_dir / "models.py"
                if not models_py.exists():
                    with open(models_py, "w") as f:
                        f.write("from django.db import models\n\n# Modelos aquí\n")
                admin_py = app_dir / "admin.py"
                if not admin_py.exists():
                    with open(admin_py, "w") as f:
                        f.write("from django.contrib import admin\n\n# Registra tus modelos aquí\n")
                views_py = app_dir / "views.py"
                if not views_py.exists():
                    with open(views_py, "w") as f:
                        f.write("from django.shortcuts import render\n\n# Vistas aquí\n")
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

    @staticmethod
    def generar_views_crud(project_path: str, app_name: str, model_name: str) -> dict:
        try:
            project_dir = Path(project_path)
            app_dir = project_dir / "apps" / app_name
            views_path = app_dir / "views.py"
            
            if not app_dir.exists():
                return {"success": False, "error": f"La app {app_name} no existe"}
            
            model_lower = model_name.lower()
            
            views_content = f'''from django.shortcuts import render, get_object_or_404, redirect
    from django.contrib import messages
    from django.urls import reverse
    from .models import {model_name}
    from .forms import {model_name}Form

    def {model_lower}_lista(request):
        """Lista todos los {model_name}s"""
        objetos = {model_name}.objects.all()
        return render(request, '{app_name}/{model_lower}_lista.html', {{
            'objetos': objetos,
            'titulo': 'Lista de {model_name}s'
        }})

    def {model_lower}_detalle(request, id):
        """Muestra el detalle de un {model_name}"""
        objeto = get_object_or_404({model_name}, id=id)
        return render(request, '{app_name}/{model_lower}_detalle.html', {{
            'objeto': objeto,
            'titulo': f'Detalle de {{objeto}}'
        }})

    def {model_lower}_crear(request):
        """Crea un nuevo {model_name}"""
        if request.method == 'POST':
            form = {model_name}Form(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, '{model_name} creado exitosamente.')
                return redirect('{app_name}:{model_lower}_lista')
        else:
            form = {model_name}Form()
        
        return render(request, '{app_name}/{model_lower}_form.html', {{
            'form': form,
            'titulo': 'Crear {model_name}',
            'accion': 'Crear'
        }})

    def {model_lower}_editar(request, id):
        """Edita un {model_name} existente"""
        objeto = get_object_or_404({model_name}, id=id)
        
        if request.method == 'POST':
            form = {model_name}Form(request.POST, instance=objeto)
            if form.is_valid():
                form.save()
                messages.success(request, '{model_name} actualizado exitosamente.')
                return redirect('{app_name}:{model_lower}_detalle', id=objeto.id)
        else:
            form = {model_name}Form(instance=objeto)
        
        return render(request, '{app_name}/{model_lower}_form.html', {{
            'form': form,
            'objeto': objeto,
            'titulo': f'Editar {{objeto}}',
            'accion': 'Actualizar'
        }})

    def {model_lower}_eliminar(request, id):
        """Elimina un {model_name}"""
        objeto = get_object_or_404({model_name}, id=id)
        
        if request.method == 'POST':
            objeto.delete()
            messages.success(request, '{model_name} eliminado exitosamente.')
            return redirect('{app_name}:{model_lower}_lista')
        
        return render(request, '{app_name}/{model_lower}_confirmar_eliminar.html', {{
            'objeto': objeto,
            'titulo': f'Eliminar {{objeto}}'
        }})
    '''
            
            with open(views_path, "w") as f:
                f.write(views_content)
            
            print(f"Views CRUD generadas para {model_name} en {app_name}")
            return {"success": True, "error": None}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def generar_forms_crud(project_path: str, app_name: str, model_name: str) -> dict:
        try:
            project_dir = Path(project_path)
            app_dir = project_dir / "apps" / app_name
            forms_path = app_dir / "forms.py"
            
            if not app_dir.exists():
                return {"success": False, "error": f"La app {app_name} no existe"}
            
            forms_content = f'''from django import forms
    from .models import {model_name}

    class {model_name}Form(forms.ModelForm):
        class Meta:
            model = {model_name}
            fields = '__all__'
            widgets = {{
                # Personaliza widgets aquí si es necesario
            }}
            
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Agregar clases CSS a todos los campos
            for field_name, field in self.fields.items():
                field.widget.attrs.update({{'class': 'form-control'}})
    '''
            
            with open(forms_path, "w") as f:
                f.write(forms_content)
            
            print(f"Forms generado para {model_name}")
            return {"success": True, "error": None}
            
        except Exception as e:
            return {"success": False, "error": str(e)}