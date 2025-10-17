# Translator Project

## 📖 Descripción

Aplicación de traducción especializada que permite traducir texto y archivos entre múltiples idiomas. Utiliza Google Translate API para proporcionar traducciones precisas y rápidas.

## ✨ Características

- 🌐 Traducción de texto entre múltiples idiomas
- 📄 Traducción de archivos (PDF, Word, TXT)
- 🔍 Detección automática de idioma
- 💾 Exportación de traducciones a diferentes formatos
- 🖥️ Interfaz gráfica intuitiva con CustomTkinter
- 🚀 Gestión rápida con `uv`

## 🛠️ Instalación y ejecución

Este proyecto utiliza `uv` para la gestión de dependencias y entornos virtuales, lo que hace la instalación más rápida y sencilla.

### Prerrequisitos

Asegúrate de tener `uv` instalado. Si no lo tienes, puedes instalarlo con:

```bash
# En Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# O usando pip
pip install uv
```

### Instalación del proyecto

```bash
# Navegar al directorio del proyecto
cd translator-project
```

```bash
# Instalar dependencias (uv creará automáticamente el entorno virtual)
uv sync
```

### Ejecución

```bash
# Ejecutar la aplicación
uv run python app.py
```

### Comandos útiles

```bash
# Agregar una nueva dependencia
uv add nombre-del-paquete

# Instalar dependencias de desarrollo
uv sync --dev

# Ejecutar comandos en el entorno virtual
uv run <comando>

# Activar el entorno virtual manualmente (opcional)
source .venv/bin/activate  # Linux/macOS
# o
.venv\Scripts\activate     # Windows
```
