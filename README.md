# 🟢 Matrix Windows Optimization Agent

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![License](https://img.shields.io/badge/license-MIT-purple)

---

### ⚡ Optimiza tu Windows con estilo **Matrix hacker profesional** 😎  
Monitorea recursos, detecta consumo alto, limpia temporales, vacía papelera, cierra procesos pesados y genera logs JSON como un campeón.

---

## ✨ Características

🟢 **Interfaz verde estilo Matrix**  
⚡ **Animaciones CLI**  
🧠 **Monitor automático del sistema**  
🛡 **Detector de modo Administrador**  
🕵️ **Modo Stealth (oculta la ventana)**  
📂 **Logs JSON profesionales (`agent_log.json`)**  
🧹 **Limpieza de archivos temporales y papelera**  
🚫 **Cierre opcional de procesos pesados**  
🔁 **Opción de reinicio automático (si eres admin)**  
🖥️ **Compatible con Windows 10/11**

---

## 📸 Preview

```
██████╗  ██████╗  ██████╗ ███████╗████████╗██╗  ██╗
██╔══██╗██╔═══██╗██╔═══██╗██╔════╝╚══██╔══╝╚██╗██╔╝
██████╔╝██║   ██║██║   ██║███████╗   ██║    ╚███╔╝ 
██╔══██╗██║   ██║██║   ██║╚════██║   ██║    ██╔██╗ 
██████╔╝╚██████╔╝╚██████╔╝███████║   ██║   ██╔╝ ██╗
╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝
     SYSTEM OPTIMIZATION ENGINE
```

---

## 🛠 Instalación

### 1️⃣ Clona el repositorio

```bash
git clone https://github.com/TU-USUARIO/matrix-optimization-agent.git
cd matrix-optimization-agent
```

### 2️⃣ Instala dependencias

```bash
pip install -r requirements.txt
```

> Si no tienes el archivo, instala manualmente:

```bash
pip install psutil colorama
```

---

## ▶ Uso

Ejecuta:

```bash
python agent.py
```

---

## 🕵️ Modo Stealth (oculta la ventana)

```bash
agent.exe --stealth
```

---

## 📊 Logs JSON

Todos los eventos se guardan en:

```
agent_log.json
```

Ejemplo:

```json
{"timestamp": "2026-01-02 12:03:40", "event": "scan", "data": {"cpu": 29.7, "ram": 73.2, "disk": 51.3}}
```

Perfecto para dashboards 🔥

---

## 🧠 Funciones principales

| Función | Descripción |
|--------|-------------|
| Scan | Muestra CPU / RAM / Disco |
| Auto Monitor | Detecta alto consumo |
| Optimize | Limpia temporales y papelera |
| Heavy Process Kill | Detecta procesos pesados |
| JSON Logs | Guarda eventos |
| Admin Check | Verifica permisos |
| Stealth Mode | Oculta ventana |

---

## ⚙ Convertir a `.exe`

Instala pyinstaller:

```bash
pip install pyinstaller
```

Genera el EXE:

```bash
pyinstaller --onefile --console agent.py
```

El archivo estará en:

```
dist/agent.exe
```

---

## 🛡 Requisitos

- Windows 10 / 11
- Python 3.10+
- Permisos Admin (opcional)

---

## 📄 Licencia

MIT — úsalo, mejóralo y comparte 💚

---

## 👨‍💻 Autor

Proyecto creado por **Kevin** con ayuda de su parcero ChatGPT 😎  
💬 Pull Requests y estrellas ⭐ son bienvenidas
