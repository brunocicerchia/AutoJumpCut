# AutoJumpCut ✂️

**AutoJumpCut** is a lightweight, modern desktop GUI for the powerful `auto-editor` command-line tool. It allows you to automatically remove silences and dead air from your videos with a single click, perfectly tailored for YouTubers, podcasters, and content creators.

[Spanish version below]

---

## 🚀 Features
- **One-Click Silence Removal:** Clean your videos automatically without manual cutting.
- **Multilingual Support:** Fully translated into **English, Spanish, and Korean**.
- **Modern UI:** Sleek dark-mode interface built with CustomTkinter.
- **Multiple Export Formats:**
  - Standard Video (.mp4) — *Perfect for CapCut, TikTok, etc.*
  - Premiere Pro (.xml)
  - DaVinci Resolve (.fcpxml)
  - Final Cut Pro (.fcpxml)
  - Shotcut (.mlt)
  - Kdenlive (.kdenlive)
- **Standalone:** No complex setup required when using the `.exe` version.

## 🛠️ Installation (Developers)
If you want to run the source code:
1. Clone the repository: `git clone https://github.com/yourusername/AutoJumpCut.git`
2. Install dependencies:
   ```bash
   pip install customtkinter auto-editor pillow
   ```
3. Run the app:
   ```bash
   python main.py
   ```

## 📦 How to Compile
To generate your own `.exe` file:
```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --windowed --name "AutoJumpCut" --icon=icon.ico --add-data "icon.ico;." main.py
```

---

# AutoJumpCut ✂️ (Español)

**AutoJumpCut** es una interfaz gráfica moderna y ligera para la herramienta de línea de comandos `auto-editor`. Te permite eliminar silencios y pausas muertas de tus videos automáticamente, ideal para YouTubers, creadores de podcasts y contenido educativo.

## 🚀 Características
- **Eliminación de silencios con un clic:** Limpia tus videos sin edición manual.
- **Soporte Multilingüe:** Traducido completamente al **Inglés, Español y Coreano**.
- **Interfaz Moderna:** Diseño oscuro elegante basado en CustomTkinter.
- **Múltiples Formatos de Exportación:**
  - Video estándar (.mp4) — *Ideal para CapCut, TikTok, etc.*
  - Premiere Pro (.xml)
  - DaVinci Resolve (.fcpxml)
  - Final Cut Pro (.fcpxml)
  - Shotcut (.mlt)
  - Kdenlive (.kdenlive)
- **Portable:** No requiere configuración compleja usando la versión `.exe`.

## 🛠️ Instalación (Desarrolladores)
Si quieres ejecutar el código fuente:
1. Clona el repositorio: `git clone https://github.com/tuusuario/AutoJumpCut.git`
2. Instala las dependencias:
   ```bash
   pip install customtkinter auto-editor pillow
   ```
3. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

## 📜 License
MIT License. Created by [Bruno Cicerchia](https://github.com/BrunoCicerchia).
