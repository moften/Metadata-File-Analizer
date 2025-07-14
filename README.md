# 🧽 Metadata File Analyzer

Herramienta en Python para revisar y limpiar metadatos de archivos comunes como PDF, DOCX, imágenes, archivos comprimidos, SQL, TXT y más. Ideal para proteger la privacidad antes de compartir documentos.

---

## 🚀 Características

- ✅ Escaneo de archivos individuales o carpetas completas
- 🧾 Soporte para múltiples formatos: `.pdf`, `.docx`, `.jpg`, `.png`, `.zip`, `.rar`, `.sql`, `.txt`
- 🧼 Limpieza automática de metadatos
- 📂 Procesamiento recursivo de carpetas
- 🧠 Detección automática del tipo de archivo
- 🧑‍💻 Interfaz de línea de comandos (CLI)

---

## 🔧 Requisitos

- Python 3.11+ (se recomienda evitar 3.13 vía Homebrew en macOS por problemas con Tkinter, que ya eliminé del código)
- `exiftool` instalado en el sistema para limpiar imágenes

### 📦 Instalación de dependencias

```bash
# Clona este repositorio
git clone https://github.com/tuusuario/Metadata-File-Analyzer.git
cd Metadata-File-Analyzer

# Crea entorno virtual (opcional)
python3 -m venv .venv
source .venv/bin/activate

# Instala las dependencias
pip install -r requirements.txt

# Instala exiftool (si no lo tienes)
# macOS (brew):
brew install exiftool

# Debian/Ubuntu:
sudo apt install libimage-exiftool-perl
```
---

## 🧪 Cómo se usa

### ▶️ Ejecución básica

Puedes ejecutar la herramienta con o sin argumentos:

#### ✅ Modo 1: Especificar ruta directamente

```bash
python3 main.py /ruta/a/carpeta/o/archivo
```

#### ✅ Modo 2: Sin argumentos (el sistema te pregunta la ruta)

```bash
python3 main.py
```

### 📋 Menú interactivo

Al ejecutar el script, verás un menú como este:

```
¿Qué deseas hacer?
1. Revisar metadatos
2. Eliminar metadatos
3. Salir
```

Selecciona la opción deseada y deja que la magia ocurra.

---

## 📁 Formatos soportados

| Tipo         | Extensiones            | Limpieza              |
|--------------|------------------------|------------------------|
| PDF          | `.pdf`                 | Limpieza con PyPDF2    |
| Documentos   | `.docx`                | Limpieza con python-docx |
| Imágenes     | `.jpg`, `.jpeg`, `.png`| Limpieza con `exiftool` |
| Texto plano  | `.txt`, `.sql`         | Limpieza básica        |
| Comprimidos  | `.zip`, `.rar`         | Descomprime y limpia recursivamente |

---

## 🙌 Apóyame

Si esta herramienta te ha sido útil o quieres apoyar futuros desarrollos, puedes invitarme un café ☕ o hacer una donación. ¡Cualquier apoyo cuenta!

[![Donate with PayPal](https://img.shields.io/badge/PayPal-Donate-blue.svg)](https://www.paypal.com/paypalme/moften)

---

## 📬 Contacto y redes

- 💌 Correo: [m10sec@proton.me](mailto:m10sec@proton.me)
- 🌐 Blog: [https://m10.com.mx](https://m10.com.mx)
- 🐦 Twitter: [@hack4lifemx](https://twitter.com/hack4lifemx)
- 💼 LinkedIn: [Francisco Santibañez](https://www.linkedin.com/in/franciscosantibanez)
- 🐙 GitHub: [github.com/m10sec](https://github.com/moften)

---

## 🛡️ Filosofía

Creo en un mundo donde los usuarios tienen control sobre su privacidad. Esta herramienta nace desde la trinchera del pentesting real, con amor por la libertad digital y el hacking con propósito.

---

⭐ Si te gustó este proyecto, dale una estrella en GitHub y compártelo con tu comunidad.