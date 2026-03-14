# =============================================================================
#  AutoEditor GUI — main.py
#  Interfaz simple para eliminar silencios de videos con auto-editor.
#
#  Dependencias (instalar una sola vez):
#      pip install customtkinter auto-editor
#
#  Uso:
#      python main.py
# =============================================================================

import sys
import shutil
import threading
import subprocess
from pathlib import Path

import customtkinter as ctk
from tkinter import filedialog, messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def is_auto_editor_installed() -> bool:
    return shutil.which("auto-editor") is not None


# ──────────────────────────────────────────────────────────────────────────────
# Localization / Multilenguaje
# ──────────────────────────────────────────────────────────────────────────────
TRANSLATIONS = {
    "English": {
        "title": "✂  AutoJumpCut",
        "subtitle": "Load your video and the app removes silences automatically.",
        "step1": "1.  Choose your video",
        "btn_select": "Select video…",
        "no_video": "No video selected",
        "step2": "2.  How aggressive should the cut be?",
        "step3": "3.  How do you want to save it?",
        "btn_process": "▶  Process video",
        "btn_cancel": "Cancel",
        "log_title": "Activity Log",
        "status_processing": "⏳  Processing your video, please wait…",
        "status_done": "✔  Video ready!",
        "status_error": "✘  There was a problem",
        "status_cancelled": "Cancelled.",
        "msg_install": "auto-editor is not installed.\n\nOpen a terminal and run:\n\n    pip install auto-editor\n\nThen restart the app.",
        "msg_no_video": "Please select a video first (Step 1).",
        "msg_not_found": "The file no longer exists:\n",
        "msg_success": "Done! Your video was saved as:\n\n",
        "msg_fail": "Something went wrong processing the video.",
        "msg_detail": "Error detail:\n",
        "warn_title": "Tool not installed",
        "err_title_missing": "Missing video",
        "err_title_notfound": "File not found",
        "done_title": "Done!",
        "err_title": "Error",
        "sens_low": "Low — cuts only long silences",
        "sens_normal": "Normal — cuts medium silences (recommended)",
        "sens_high": "High — cuts even short pauses",
        "exp_mp4": "Standard Video (.mp4)",
        "exp_xml": "For Premiere Pro (.xml)",
        "exp_resolve": "For DaVinci Resolve (.fcpxml)",
        "exp_fcp": "For Final Cut Pro (.fcpxml)",
        "exp_shotcut": "For Shotcut (.mlt)",
        "exp_kdenlive": "For Kdenlive (.kdenlive)",
        "dlg_select": "Select a video",
        "dlg_vid_files": "Videos",
        "dlg_all_files": "All files",
        "footer_dev": "Developed by Bruno Cicerchia",
        "footer_open": "Open Source ❤",
    },
    "Español": {
        "title": "✂  AutoJumpCut",
        "subtitle": "Cargá tu video y la app borra los silencios automáticamente.",
        "step1": "1.  Elegí tu video",
        "btn_select": "Seleccionar video…",
        "no_video": "Ningún video seleccionado",
        "step2": "2.  ¿Qué tan agresivo querés el corte?",
        "step3": "3.  ¿Cómo querés guardar el resultado?",
        "btn_process": "▶  Procesar video",
        "btn_cancel": "Cancelar",
        "log_title": "Registro de actividad",
        "status_processing": "⏳  Procesando tu video, esperá un momento…",
        "status_done": "✔  ¡Video listo!",
        "status_error": "✘  Hubo un problema",
        "status_cancelled": "Cancelado.",
        "msg_install": "auto-editor no está instalado.\n\nAbrí una terminal y ejecutá:\n\n    pip install auto-editor\n\nLuego reiniciá la aplicación.",
        "msg_no_video": "Primero seleccioná un video (Paso 1).",
        "msg_not_found": "El archivo ya no existe:\n",
        "msg_success": "¡Listo! Tu video fue guardado como:\n\n",
        "msg_fail": "Algo salió mal al procesar el video.",
        "msg_detail": "Detalle del error:\n",
        "warn_title": "Herramienta no instalada",
        "err_title_missing": "Falta el video",
        "err_title_notfound": "Archivo no encontrado",
        "done_title": "¡Listo!",
        "err_title": "Error",
        "sens_low": "Baja — corta solo los silencios largos",
        "sens_normal": "Normal — corta silencios medios (recomendado)",
        "sens_high": "Alta — corta hasta las pausas cortas",
        "exp_mp4": "Video estándar (.mp4)",
        "exp_xml": "Para Premiere Pro (.xml)",
        "exp_resolve": "Para DaVinci Resolve (.fcpxml)",
        "exp_fcp": "Para Final Cut Pro (.fcpxml)",
        "exp_shotcut": "Para Shotcut (.mlt)",
        "exp_kdenlive": "Para Kdenlive (.kdenlive)",
        "dlg_select": "Seleccioná un video",
        "dlg_vid_files": "Videos",
        "dlg_all_files": "Todos los archivos",
        "footer_dev": "Desarrollado por Bruno Cicerchia",
        "footer_open": "Open Source ❤",
    },
    "한국어 (Korean)": {
        "title": "✂  AutoJumpCut",
        "subtitle": "동영상을 불러오면 앱이 자동으로 무음 구간을 제거합니다.",
        "step1": "1. 동영상 선택",
        "btn_select": "동영상 선택…",
        "no_video": "선택된 동영상 없음",
        "step2": "2. 얼마나 자를까요?",
        "step3": "3. 어떻게 저장하시겠습니까?",
        "btn_process": "▶  동영상 처리",
        "btn_cancel": "취소",
        "log_title": "작업 로그",
        "status_processing": "⏳  동영상을 처리 중입니다. 잠시만 기다려주세요…",
        "status_done": "✔  동영상 준비 완료!",
        "status_error": "✘  문제가 발생했습니다",
        "status_cancelled": "취소됨.",
        "msg_install": "auto-editor가 설치되어 있지 않습니다.\n\n터미널을 열고 다음을 실행하세요:\n\n    pip install auto-editor\n\n그런 다음 앱을 다시 시작하세요.",
        "msg_no_video": "먼저 동영상을 선택하세요 (1단계).",
        "msg_not_found": "파일이 더 이상 존재하지 않습니다:\n",
        "msg_success": "완료! 동영상이 다음 일므로 저장되었습니다:\n\n",
        "msg_fail": "동영상을 처리하는 중 문제가 발생했습니다.",
        "msg_detail": "오류 세부 정보:\n",
        "warn_title": "도구 미설치",
        "err_title_missing": "동영상 누락",
        "err_title_notfound": "파일을 찾을 수 없음",
        "done_title": "완료!",
        "err_title": "오류",
        "sens_low": "낮음 — 긴 무음 구간만 잘라냄",
        "sens_normal": "보통 — 중간 길이의 무음 구간 잘라냄 (권장)",
        "sens_high": "높음 — 짧은 일시 정지까지 모두 잘라냄",
        "exp_mp4": "일반 동영상 (.mp4)",
        "exp_xml": "Premiere Pro용 (.xml)",
        "exp_resolve": "DaVinci Resolve용 (.fcpxml)",
        "exp_fcp": "Final Cut Pro용 (.fcpxml)",
        "exp_shotcut": "Shotcut용 (.mlt)",
        "exp_kdenlive": "Kdenlive용 (.kdenlive)",
        "dlg_select": "동영상 선택",
        "dlg_vid_files": "동영상",
        "dlg_all_files": "모든 파일",
        "footer_dev": "개발자: Bruno Cicerchia",
        "footer_open": "Open Source ❤",
    }
}

# Configuración base interna (no traducida directamente en la UI)
SENSITIVITIES_VALS = {"low": 0.02, "normal": 0.04, "high": 0.08}
EXPORTS_VALS = {
    "mp4":      {"flag": None, "ext": ".mp4"},
    "xml":      {"flag": "--export premiere", "ext": ".xml"},
    "resolve":  {"flag": "--export resolve", "ext": ".fcpxml"},
    "fcp":      {"flag": "--export final-cut-pro", "ext": ".fcpxml"},
    "shotcut":  {"flag": "--export shotcut", "ext": ".mlt"},
    "kdenlive": {"flag": "--export kdenlive", "ext": ".kdenlive"},
}

class App(ctk.CTk):
    """AutoEditor GUI — interfaz amigable para no técnicos con soporte multilenguaje."""

    def __init__(self):
        super().__init__()
        self.geometry("540x800")
        self.minsize(540, 760)
        self.resizable(True, True)

        # Cargar icono (funciona tanto en script como compilado)
        icon_path = Path("icon.ico")
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            icon_path = Path(sys._MEIPASS) / "icon.ico"
        
        if icon_path.exists():
            self.iconbitmap(str(icon_path))

        self._input_path: Path | None = None
        self._process: subprocess.Popen | None = None
        
        # Estado actual: inglés, español o coreano
        self._lang = "Español"
        self._t = TRANSLATIONS[self._lang] # dic pointer

        # Mapeos inversos para los dropdowns: String en UI -> ID interno
        self._sens_map = {}
        self._exp_map = {}
        
        # Para el dropdown: guardamos el ID interno actual
        self._current_sens_id = "normal"
        self._current_exp_id = "mp4"

        self._build_ui()
        self._set_language(self._lang) # Inicializa textos

        if not is_auto_editor_installed():
            self.after(300, self._warn_missing_tool)

    # ──────────────────────────────────────────────────────────────────────
    # Construcción de la UI
    # ──────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        px = 28  # padding horizontal

        # Selector de idioma (arriba a la derecha)
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=px, pady=(15, 0))
        
        self._lang_var = ctk.StringVar(value=self._lang)
        self._lang_menu = ctk.CTkOptionMenu(
            header_frame,
            variable=self._lang_var,
            values=["English", "Español", "한국어 (Korean)"],
            width=100,
            height=28,
            font=ctk.CTkFont(size=11),
            command=self._set_language
        )
        self._lang_menu.pack(side="right")

        # ── Título ────────────────────────────────────────────────────────
        self._title_lbl = ctk.CTkLabel(self, font=ctk.CTkFont(size=22, weight="bold"))
        self._title_lbl.pack(pady=(0, 2))

        self._subtitle_lbl = ctk.CTkLabel(self, font=ctk.CTkFont(size=13), text_color="#888899")
        self._subtitle_lbl.pack(pady=(0, 24))

        # ── PASO 1: Elegir video ──────────────────────────────────────────
        self._step1_lbl = ctk.CTkLabel(self, font=ctk.CTkFont(size=13, weight="bold"), text_color="#ccccee")
        self._step1_lbl.pack(padx=px, anchor="w")

        self._file_btn = ctk.CTkButton(
            self, height=44, font=ctk.CTkFont(size=13, weight="bold"), command=self._browse_file
        )
        self._file_btn.pack(padx=px, fill="x", pady=(6, 0))

        self._file_lbl = ctk.CTkLabel(self, font=ctk.CTkFont(size=11), text_color="#555577")
        self._file_lbl.pack(padx=px, anchor="w", pady=(4, 22))

        # ── PASO 2: Sensibilidad ──────────────────────────────────────────
        self._step2_lbl = ctk.CTkLabel(self, font=ctk.CTkFont(size=13, weight="bold"), text_color="#ccccee")
        self._step2_lbl.pack(padx=px, anchor="w")

        self._sens_menu = ctk.CTkOptionMenu(self, height=40, font=ctk.CTkFont(size=12), anchor="w", command=self._on_sens_change)
        self._sens_menu.pack(padx=px, fill="x", pady=(6, 22))

        # ── PASO 3: Formato de salida ─────────────────────────────────────
        self._step3_lbl = ctk.CTkLabel(self, font=ctk.CTkFont(size=13, weight="bold"), text_color="#ccccee")
        self._step3_lbl.pack(padx=px, anchor="w")

        self._exp_menu = ctk.CTkOptionMenu(self, height=40, font=ctk.CTkFont(size=12), anchor="w", command=self._on_exp_change)
        self._exp_menu.pack(padx=px, fill="x", pady=(6, 28))

        # ── Botón principal ───────────────────────────────────────────────
        self._run_btn = ctk.CTkButton(
            self, height=52, font=ctk.CTkFont(size=16, weight="bold"), command=self._start_processing
        )
        self._run_btn.pack(padx=px, fill="x")

        # ── Progreso y estado ─────────────────────────────────────────────
        self._progress = ctk.CTkProgressBar(self, mode="indeterminate", height=8)
        self._progress.pack(padx=px, fill="x", pady=(14, 0))
        self._progress.set(0)

        self._status_lbl = ctk.CTkLabel(self, font=ctk.CTkFont(size=12), text_color="#888899", text="")
        self._status_lbl.pack(padx=px, anchor="w", pady=(8, 0))

        # ── Botón cancelar ─────────────────────────────────────────────────
        self._cancel_btn = ctk.CTkButton(
            self, height=36, width=110, fg_color="#3a3a5a", hover_color="#5a2a2a",
            font=ctk.CTkFont(size=12), command=self._cancel_processing, state="disabled"
        )
        self._cancel_btn.pack(pady=(8, 0))

        # ── Footer ──────────────────────────────────────────────────────────
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.pack(fill="x", side="bottom", pady=(0, 15))

        self._footer_dev_lbl = ctk.CTkLabel(
            footer_frame, font=ctk.CTkFont(size=10), text_color="#555577"
        )
        self._footer_dev_lbl.pack()

        self._footer_open_lbl = ctk.CTkLabel(
            footer_frame, font=ctk.CTkFont(size=10), text_color="#555577"
        )
        self._footer_open_lbl.pack()

        # ── Registro de actividad ──────────────────────────────────────────
        self._log_title_lbl = ctk.CTkLabel(self, font=ctk.CTkFont(size=11, weight="bold"), text_color="#666688")
        self._log_title_lbl.pack(padx=px, anchor="w", pady=(14, 0))

        self._log_box = ctk.CTkTextbox(
            self, height=120, font=ctk.CTkFont(family="Consolas", size=10),
            fg_color="#0d0d1a", text_color="#aaaacc", corner_radius=8, state="disabled", wrap="word"
        )
        self._log_box.pack(padx=px, fill="both", expand=True, pady=(4, 15))

    # ──────────────────────────────────────────────────────────────────────
    # Cambio de idioma
    # ──────────────────────────────────────────────────────────────────────
    def _set_language(self, lang_key: str):
        self._lang = lang_key
        self._t = TRANSLATIONS[lang_key]
        t = self._t

        self.title(t["title"])
        self._title_lbl.configure(text=t["title"])
        self._subtitle_lbl.configure(text=t["subtitle"])
        
        self._step1_lbl.configure(text=t["step1"])
        self._file_btn.configure(text=t["btn_select"])
        if not self._input_path:
            self._file_lbl.configure(text=t["no_video"])
            
        self._step2_lbl.configure(text=t["step2"])
        self._step3_lbl.configure(text=t["step3"])
        
        self._run_btn.configure(text=t["btn_process"])
        self._cancel_btn.configure(text=t["btn_cancel"])
        self._log_title_lbl.configure(text=t["log_title"])
        
        self._footer_dev_lbl.configure(text=t["footer_dev"])
        self._footer_open_lbl.configure(text=t["footer_open"])

        # Actualizar dropdowns construyendo los mapeos para este idioma
        new_sens = {
            t["sens_low"]: "low",
            t["sens_normal"]: "normal",
            t["sens_high"]: "high"
        }
        self._sens_map = new_sens
        
        # Inverso para setear valores
        invers_sens = {v: k for k, v in new_sens.items()}
        self._sens_menu.configure(values=list(new_sens.keys()))
        self._sens_menu.set(invers_sens[self._current_sens_id])

        new_exp = {
            t["exp_mp4"]: "mp4",
            t["exp_xml"]: "xml",
            t["exp_resolve"]: "resolve",
            t["exp_fcp"]: "fcp",
            t["exp_shotcut"]: "shotcut",
            t["exp_kdenlive"]: "kdenlive"
        }
        self._exp_map = new_exp
        
        invers_exp = {v: k for k, v in new_exp.items()}
        self._exp_menu.configure(values=list(new_exp.keys()))
        self._exp_menu.set(invers_exp[self._current_exp_id])

    def _on_sens_change(self, value: str):
        self._current_sens_id = self._sens_map[value]

    def _on_exp_change(self, value: str):
        self._current_exp_id = self._exp_map[value]

    # ──────────────────────────────────────────────────────────────────────
    # Lógica
    # ──────────────────────────────────────────────────────────────────────

    def _browse_file(self):
        t = self._t
        path = filedialog.askopenfilename(
            title=t["dlg_select"],
            filetypes=[
                (t["dlg_vid_files"], "*.mp4 *.mov *.avi *.mkv *.webm *.m4v"),
                (t["dlg_all_files"], "*.*"),
            ],
        )
        if path:
            self._input_path = Path(path)
            display = self._input_path.name
            self._file_lbl.configure(text=f"✔  {display}", text_color="#88dd99")

    def _start_processing(self):
        t = self._t
        if not is_auto_editor_installed():
            self._warn_missing_tool()
            return

        if self._input_path is None:
            messagebox.showerror(t["err_title_missing"], t["msg_no_video"])
            return

        if not self._input_path.exists():
            messagebox.showerror(t["err_title_notfound"], f"{t['msg_not_found']}{self._input_path}")
            return

        # Lookup thresholds/formats using internal ID
        threshold = SENSITIVITIES_VALS[self._current_sens_id]
        export_info = EXPORTS_VALS[self._current_exp_id]
        out_path = self._input_path.with_name(
            self._input_path.stem + "_sin_silencios" + export_info["ext"]
        )

        cmd = [
            "auto-editor",
            str(self._input_path),
            "--margin", "0.2s",
            "--edit", f"audio:threshold={threshold}",
            "--output", str(out_path),
            "--no-open",
        ]
        if export_info["flag"]:
            cmd.extend(export_info["flag"].split())

        self._run_btn.configure(state="disabled")
        self._cancel_btn.configure(state="normal")
        self._progress.start()
        self._set_status(t["status_processing"])

        threading.Thread(
            target=self._run_process, args=(cmd, out_path), daemon=True
        ).start()

    def _run_process(self, cmd: list[str], out_path: Path):
        t = self._t
        output_lines: list[str] = []
        
        # Prevent secondary cmd.exe windows in compiled PyInstaller apps on Windows
        cflags = 0
        if sys.platform == "win32":
            cflags = subprocess.CREATE_NO_WINDOW
            
        try:
            self._process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace", bufsize=1,
                creationflags=cflags
            )
            for line in self._process.stdout:  # type: ignore[union-attr]
                output_lines.append(line)
                self.after(0, lambda l=line: self._log(l))
            self._process.wait()
            code = self._process.returncode
        except FileNotFoundError:
            self.after(0, lambda: self._finish(False, t["msg_install"]))
            return
        except Exception as e:
            self.after(0, lambda e=e: self._finish(False, str(e)))
            return
        finally:
            self._process = None

        if code == 0:
            self.after(0, lambda: self._finish(True, f"{t['msg_success']}{out_path.name}"))
        else:
            last_lines = "".join(output_lines[-15:]).strip()
            msg = t["msg_fail"]
            if last_lines:
                msg += f"\n\n{t['msg_detail']}{last_lines}"
            self.after(0, lambda m=msg: self._finish(False, m))

    def _cancel_processing(self):
        if self._process and self._process.poll() is None:
            self._process.terminate()
            self._finish(False, self._t["status_cancelled"])

    def _finish(self, success: bool, message: str):
        t = self._t
        self._progress.stop()
        self._progress.set(1.0 if success else 0.0)
        self._run_btn.configure(state="normal")
        self._cancel_btn.configure(state="disabled")

        if success:
            self._set_status(t["status_done"])
            messagebox.showinfo(t["done_title"], message)
        else:
            self._set_status(t["status_error"])
            # 'status_cancelled' may vary by language
            if t["status_cancelled"] not in message:
                messagebox.showerror(t["err_title"], message)
            else:
                self._set_status(t["status_cancelled"])

    def _set_status(self, text: str):
        self._status_lbl.configure(text=text)

    def _log(self, text: str):
        self._log_box.configure(state="normal")
        self._log_box.insert("end", text)
        self._log_box.see("end")
        self._log_box.configure(state="disabled")

    def _warn_missing_tool(self):
        t = self._t
        messagebox.showwarning(t["warn_title"], t["msg_install"])
        self._set_status(t["warn_title"])


if __name__ == "__main__":
    App().mainloop()
