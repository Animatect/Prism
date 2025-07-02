#!/bin/bash

# --- Configuración ---
APP_NAME="Prism"
VERSION="2.0.16"
APP_DIR="/Applications/${APP_NAME}.app"
CONTENTS_DIR="${APP_DIR}/Contents"
RESOURCES_DIR="${CONTENTS_DIR}/Resources"

# --- 1. Verificar estructura del proyecto ---
if [ ! -f "Scripts/PrismTray.py" ]; then
    echo "❌ Error: El archivo Scripts/PrismTray.py no existe"
    echo "Ejecuta este script desde la raíz del proyecto donde están las carpetas Plugins, Scripts, etc."
    exit 1
fi
 
# --- 2. Limpiar instalación previa ---
rm -rf "${APP_DIR}"

# --- 3. Crear estructura de directorios ---
mkdir -p "${CONTENTS_DIR}/MacOS"
mkdir -p "${RESOURCES_DIR}"

# --- 4. Copiar TODOS los componentes ---
echo "Copiando archivos a la aplicación..."
components=("Plugins" "Presets" "Python311" "PythonLibs" "Scripts" "Tools")
for component in "${components[@]}"; do
    if [ -d "$component" ]; then
        cp -R "$component" "${RESOURCES_DIR}/"
        echo "✓ $component"
    else
        echo "⚠️ $component no encontrado (se omitió)"
    fi
done

# Copiar archivos adicionales
cp -v license_*.txt "${RESOURCES_DIR}/"

# --- 5. Crear ejecutable principal ---
cat > "${CONTENTS_DIR}/MacOS/${APP_NAME}" <<EOF
#!/bin/bash
DIR=\$(dirname "\$0")
/usr/bin/python3 "\$DIR/../Resources/Scripts/PrismTray.py"
EOF
chmod +x "${CONTENTS_DIR}/MacOS/${APP_NAME}"

# --- 6. Crear Info.plist ---
cat > "${CONTENTS_DIR}/Info.plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>${APP_NAME}</string>
    <key>CFBundleIdentifier</key>
    <string>com.prism.${APP_NAME}</string>
    <key>CFBundleVersion</key>
    <string>${VERSION}</string>
    <key>CFBundleName</key>
    <string>${APP_NAME}</string>
</dict>
</plist>
EOF

# --- 7. Reparar permisos ---
find "${APP_DIR}" -type d -exec chmod 755 {} \;
find "${APP_DIR}" -type f -exec chmod 644 {} \;
chmod +x "${CONTENTS_DIR}/MacOS/${APP_NAME}"

# --- 8. Firma temporal (para desarrollo) ---
codesign --force --deep --sign - "${APP_DIR}"

echo "✅ ${APP_NAME} ${VERSION} instalado correctamente en:"
echo "   ${APP_DIR}"