#!/bin/bash

# --- Configuración ---
APP_NAME="Prism"
VERSION="2.0.16"
DMG_NAME="${APP_NAME}-${VERSION}.dmg"
VOLUME_NAME="${APP_NAME} ${VERSION}"
WORK_DIR=$(pwd)

# --- Verificación del sistema ---
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Error: Este script solo funciona en macOS"
    exit 1
fi 

# --- Directorios temporales ---
TEMP_DIR="${WORK_DIR}/temp_dmg"
APP_CONTENTS_DIR="${TEMP_DIR}/${APP_NAME}"

# --- Limpieza inicial ---
rm -rf "${TEMP_DIR}"
mkdir -p "${APP_CONTENTS_DIR}"

# --- Copiar estructura completa ---
echo "=== Copiando archivos al DMG ==="

# 1. Componentes principales
components=("Plugins" "Presets" "Python311" "PythonLibs" "Scripts" "Tools" "license_GPL.txt" "license-LGPL.txt")
for item in "${components[@]}"; do
    if [ -e "${WORK_DIR}/${item}" ]; then
        echo "✓ Copiando ${item}..."
        cp -R "${WORK_DIR}/${item}" "${APP_CONTENTS_DIR}/"
    else
        echo "⚠️ Advertencia: ${item} no encontrado"
    fi
done

# 2. Scripts de instalación
cp "${WORK_DIR}/install.command" "${TEMP_DIR}/"
chmod +x "${TEMP_DIR}/install.command"

# 3. Crear instrucciones de instalación
cat > "${TEMP_DIR}/INSTALL.txt" <<EOF
Para instalar ${APP_NAME}:

1. Arrastre la carpeta "${APP_NAME}" a su carpeta de Aplicaciones
2. Ejecute "install.command" para completar la instalación
EOF

# --- Crear DMG ---
echo "=== Creando imagen de disco ==="
hdiutil create \
    -srcfolder "${TEMP_DIR}" \
    -volname "${VOLUME_NAME}" \
    -fs HFS+ \
    -format UDZO \
    -ov "${WORK_DIR}/${DMG_NAME}" || {
    echo "❌ Fallo al crear DMG"
    exit 1
}

# --- Icono personalizado ---
if [ -f "${WORK_DIR}/Prism.icns" ]; then
    echo "Añadiendo icono personalizado..."
    hdiutil attach "${WORK_DIR}/${DMG_NAME}" >/dev/null
    VOLUME=$(mount | grep "${VOLUME_NAME}" | awk '{print $3}')
    cp "${WORK_DIR}/Prism.icns" "${VOLUME}/.VolumeIcon.icns"
    SetFile -a C "${VOLUME}"
    hdiutil detach "${VOLUME}" >/dev/null
fi

# --- Limpieza final ---
rm -rf "${TEMP_DIR}"

echo "✅ ${DMG_NAME} creado exitosamente en:"
echo "   ${WORK_DIR}/${DMG_NAME}"
open "${WORK_DIR}"