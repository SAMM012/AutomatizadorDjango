# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AutomatizadorDjango is a Python desktop application built with Flet that automates Django project setup and deployment. It provides a wizard-style GUI interface to help developers quickly create, configure, and manage Django projects without manual command-line work.

## Architecture

### Core Structure
- **Main Application (`interfaz.py`)**: Single Flet-based GUI with complete wizard workflow
- **Core Modules (`core/`)**: Business logic for Django project automation
  - `django_manager.py`: Django project/app creation, model generation, CRUD scaffolding
  - `crear_carpeta.py`: Folder creation with cross-platform validation
  - `crear_entorno.py`: Python virtual environment setup and Django installation
  - `bd_config.py`: Database configuration management (SQLite/PostgreSQL)
  - `project_state.py`: Wizard state management and step validation

### 6-Step Wizard Flow

1. **Carpeta** → Create project root directory
2. **Entorno** → Set up virtual environment and install Django  
3. **BD Config** → Configure database type (SQLite/PostgreSQL)
4. **Apps** → Create Django applications with custom structure
5. **Modelos** → Define database models with automatic CRUD generation
6. **Servidor** → Start Django dev server and create superusers

Each step is locked until the previous one completes, with visual indicators showing progress.

### Key Automation Features

- **Complete Django scaffolding** with custom `apps/` directory structure
- **Full CRUD generation**: Creates models, forms, views, URLs, and admin integration
- **Cross-platform virtual environment** management (Windows/Linux/macOS)
- **Django development server** process management with start/stop controls
- **Superuser creation** through GUI forms
- **Database migration** handling with automatic makemigrations/migrate

## Development Commands

### Running the Application
```bash
python interfaz.py          # Launch the GUI application
```

### Dependencies
The application requires:
- Python 3.7+
- flet (for GUI)
- Standard library modules (subprocess, pathlib, asyncio)

No requirements.txt file exists - dependencies must be installed manually.

## Development Notes

### UI Framework - Flet
- Cross-platform desktop GUI using Flutter-based Flet
- Responsive container-based layout with 6 main panels
- Async/await patterns for non-blocking file operations and subprocesses
- Real-time UI state updates with visual wizard indicators

### Django Project Generation
- Creates projects with organized `apps/` subdirectory structure
- Generates complete CRUD functionality per model:
  - Model definitions with configurable field types
  - Django ModelForms with Bootstrap CSS classes
  - Views for list, detail, create, edit, delete operations
  - URL patterns with proper namespacing
  - Django admin panel integration
- Automatic database migrations after model creation

### State Management
- `ProjectState` dataclass maintains wizard progress and configuration
- Step dependencies enforced - UI panels are disabled until prerequisites complete
- Visual step indicators show completed/current/locked states
- Debug methods available for state inspection

### Cross-Platform Support
- `pathlib.Path` used throughout for consistent path handling
- Virtual environment detection handles Windows (`Scripts/`) vs Unix (`bin/`) differences
- Subprocess execution adapts to platform-specific Python executable locations

## File Structure

```
├── core/                   # Business logic modules
│   ├── django_manager.py   # Django project operations
│   ├── crear_carpeta.py    # Folder creation with validation
│   ├── crear_entorno.py    # Virtual environment setup  
│   ├── bd_config.py        # Database configuration
│   └── project_state.py    # Wizard state management
├── interfaz.py            # Main GUI application
└── README.md              # Basic project description
```

## Common Patterns

### Async Operations
UI operations like folder selection, project creation, and server management use async/await to prevent blocking the interface.

### Error Handling
Comprehensive validation for:
- Folder name restrictions (cross-platform invalid characters)
- Directory permissions and existence
- Virtual environment creation failures
- Django project naming conflicts

### Process Management  
Django development server runs as subprocess with proper cleanup on application exit.