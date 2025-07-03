#!/bin/bash

# --- Configuración ---
PRISM_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/Prism" && pwd )"
PYTHON_BIN="/usr/bin/python3"  # Python del sistema (cambia a "$PRISM_DIR/Python311/python" para usar el de Prism)
PYTHON_SCRIPT="$PRISM_DIR/Scripts/PrismInstaller.py"
PYTHON_LIBS_DIR="/PythonLibs/Python3"

# --- Verificar si el script existe ---
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ Error: No se encontró PrismInstaller.py en: $PYTHON_SCRIPT"
    echo "Asegúrate de que el archivo .command esté en la misma carpeta que 'Prism'."
    exit 1
fi

# --- Función para verificar PySide6 ---
check_pyside6() {
    local pyside6_path="$PYTHON_LIBS_DIR/PySide6"
    
    if [ -d "$pyside6_path" ]; then
        echo "✅ PySide6 encontrado en: $pyside6_path"
        return 0
    else
        echo "❌ Error: No se encontró PySide6 en: $pyside6_path"
        echo "Asegúrate de que la biblioteca PySide6 esté en la carpeta PythonLibs/Python3"
        exit 1
    fi
}

# --- Función para verificar psutil ---
check_psutil() {
    local psutil_path="$PYTHON_LIBS_DIR/Psutil"
    
    if [ -d "$psutil_path" ]; then
        echo "✅ psutil encontrado en: $psutil_path"
        return 0
    else
        echo "❌ Error: No se encontró psutil en: $psutil_path"
        echo "Asegúrate de que la biblioteca psutil esté en la carpeta PythonLibs/Python3"
        exit 1
    fi
}

# --- Verificar dependencias de Python ---
echo "🔍 Verificando dependencias de Python..."

# Verificar PySide6
check_pyside6

# Verificar psutil
check_psutil

# --- Ejecutar PrismInstaller.py ---
echo ""
echo "🚀 Iniciando Prism..."
echo "Directorio de Prism: $PRISM_DIR"
echo "Python usado: $PYTHON_BIN"
echo ""

"$PYTHON_BIN" "$PYTHON_SCRIPT"
