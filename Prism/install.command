#!/bin/bash

# --- Configuración ---
PRISM_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_BIN="/usr/bin/python3"  # Python del sistema
PYTHON_SCRIPT="$PRISM_DIR/Scripts/PrismInstaller.py"
PYTHON_LIBS_DIR="$PRISM_DIR/PythonLibs/Python3"

# --- Verificación de estructura ---
echo "🔍 Verificando estructura en: $PRISM_DIR"
echo "Contenido del directorio:"
ls -l

# --- Verificar script principal ---
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ Error: No se encontró PrismInstaller.py en: $PYTHON_SCRIPT"
    echo ""
    echo "Estructura requerida:"
    echo "- Prism/ (esta carpeta)"
    echo "  - Scripts/PrismInstaller.py"
    echo "  - PythonLibs/Python3/"
    echo "    - PySide6/"
    echo "    - psutil/"
    exit 1
fi

# --- Función para verificar dependencias ---
check_dependency() {
    if [ -d "$PYTHON_LIBS_DIR/$1" ]; then
        echo "✅ $1 encontrado en: $PYTHON_LIBS_DIR/$1"
    else
        echo "❌ Error: No se encontró $1 en: $PYTHON_LIBS_DIR/$1"
        echo "Contenido de $PYTHON_LIBS_DIR:"
        ls -l "$PYTHON_LIBS_DIR"
        exit 1
    fi
}

# --- Verificar dependencias ---
echo "🔍 Verificando dependencias en: $PYTHON_LIBS_DIR"
check_dependency "PySide6"
check_dependency "psutil"

# --- Ejecutar Prism ---
echo ""
echo "🚀 Iniciando Prism..."
cd "$PRISM_DIR" || exit 1
"$PYTHON_BIN" "$PYTHON_SCRIPT"