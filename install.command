#!/bin/bash

# --- Configuración ---
PRISM_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/Prism" && pwd )"
PYTHON_BIN="/usr/bin/python3"  # Python del sistema (cambia a "$PRISM_DIR/Python311/python" para usar el de Prism)
PYTHON_SCRIPT="$PRISM_DIR/Scripts/PrismInstaller.py"

# --- Verificar si el script existe ---
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ Error: No se encontró PrismInstaller.py en: $PYTHON_SCRIPT"
    echo "Asegúrate de que el archivo .command esté en la misma carpeta que 'Prism'."
    exit 1
fi

# --- Función para instalar PySide6 ---
install_pyside6() {
    echo "🔧 Instalando PySide6 (timeout extendido)..."
    echo "Esto puede tomar varios minutos dependiendo de tu conexión..."
    
    # Primero actualizar pip para evitar problemas
    "$PYTHON_BIN" -m pip install --upgrade pip --default-timeout=60 --user
    
    # Luego instalar PySide6
    "$PYTHON_BIN" -m pip install --default-timeout=60 --user PySide6
    
    if [ $? -ne 0 ]; then
        echo "❌ Error: Falló la instalación automática. Prueba esto:"
        echo "   1. Actualiza pip manualmente: '$PYTHON_BIN -m pip install --upgrade pip'"
        echo "   2. Instala PySide6 manualmente: '$PYTHON_BIN -m pip install --user PySide6'"
        echo "   3. Verifica tu conexión a internet"
        exit 1
    fi
    echo "✅ PySide6 instalado correctamente."
}

# --- Función para instalar psutil ---
install_psutil() {
    echo "🔧 Instalando psutil..."
    "$PYTHON_BIN" -m pip install --user psutil
    
    if [ $? -ne 0 ]; then
        echo "❌ Error: Falló la instalación de psutil. Prueba esto:"
        echo "   1. Verifica tu conexión a internet"
        echo "   2. Intenta instalarlo manualmente: '$PYTHON_BIN -m pip install --user psutil'"
        exit 1
    fi
    echo "✅ psutil instalado correctamente."
}

# --- Verificar dependencias de Python ---
echo "🔍 Verificando dependencias de Python..."

# Verificar PySide6
"$PYTHON_BIN" -c "import PySide6" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️ PySide6 no está instalado."
    install_pyside6
else
    echo "✅ PySide6 ya está instalado."
fi

# Verificar psutil
"$PYTHON_BIN" -c "import psutil" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️ psutil no está instalado."
    install_psutil
else
    echo "✅ psutil ya está instalado."
fi

# --- Ejecutar PrismInstaller.py ---
echo ""
echo "🚀 Iniciando Prism..."
echo "Directorio de Prism: $PRISM_DIR"
echo "Python usado: $PYTHON_BIN"
echo ""

"$PYTHON_BIN" "$PYTHON_SCRIPT"

# --- Mantener la terminal abierta ---
echo ""
read -p "Presiona Enter para cerrar esta ventana..." dummy