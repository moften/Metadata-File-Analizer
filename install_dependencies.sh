#!/bin/bash

echo "📦 Instalando dependencias para el limpiador de metadatos..."

# Verifica si exiftool está instalado
if ! command -v exiftool &> /dev/null
then
    echo "🔧 exiftool no encontrado. Instalando..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install exiftool
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt update && sudo apt install -y libimage-exiftool-perl
    else
        echo "⚠️ Instala exiftool manualmente para tu sistema operativo."
    fi
else
    echo "✅ exiftool ya está instalado."
fi

# Instalar dependencias de Python
echo "🐍 Instalando paquetes de Python..."
pip install -r requirements.txt

echo "✅ Instalación completada."