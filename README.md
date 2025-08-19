````markdown
# Detección de Objetos en Tiempo Real (Windows)

Aplicación sencilla y eficiente para **Windows** que usa la **cámara del PC** y reconoce objetos **en tiempo real** con **YOLOv8**.  
Cada objeto detectado se marca con un **cuadro**, **nombre** y un **color distinto por clase** (mismo color siempre para la misma clase).

> Todo el procesamiento ocurre **localmente** en tu equipo. No se envía video a internet.

---

## 🟢 Opción A: Probar el ejecutable (.exe) — ¡La más fácil!

1. **Descarga** el archivo `detector-objetos.exe` desde la sección **Releases** de este repositorio (o donde te lo compartieron).
2. **Haz doble clic** sobre `detector-objetos.exe`.
3. La primera vez, podría tardar un poco mientras descarga el modelo de IA (si no está en caché).
4. Cuando se abra la ventana de video, verás las detecciones en tiempo real.
5. **Para salir**, presiona la tecla **`q`**.

### Problemas comunes con el .exe
- **Windows SmartScreen/Antivirus:** Al ser un ejecutable nuevo, Windows podría mostrar advertencias. Elige **“Más información” → “Ejecutar de todas formas”** si confías en el archivo.
- **No abre la cámara:** Cierra otras apps que estén usando la cámara (Teams, Zoom, etc.) y vuelve a ejecutar.  
- **Se ve muy lento:** Tu PC puede ser modesta o el modelo estar configurado con resolución alta. Usa la **Opción B** y prueba un tamaño de inferencia menor (`--imgsz 480` o `--imgsz 320`).

---

## 🔵 Opción B: Ejecutar desde el código (instalación guiada)

> Pensado para Windows 10/11 (64 bits) con **Python 3.10+**.

### 1) Instalar Python (si no lo tienes)
- Descarga Python desde [python.org](https://www.python.org/downloads/).  
- Durante la instalación, **marca** “**Add Python to PATH**”.

### 2) Descargar el proyecto
- Botón **Code → Download ZIP**, descomprime; o  
- Con Git:
  ```bash
  git clone https://github.com/tu-usuario/tu-repo.git
  cd tu-repo
````

### 3) Crear entorno virtual (recomendado)

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### 4) Instalar dependencias

```bash
pip install --upgrade pip
pip install ultralytics opencv-python
```

> La primera ejecución descargará automáticamente el modelo `yolov8n.pt` (ligero y rápido).

### 5) Ejecutar la app

```bash
python detecta_objetos.py
```

Si tienes **más de una cámara** o quieres ajustar parámetros:

```bash
# Elegir cámara 0/1/2..., umbral de confianza y tamaño de imagen:
python detecta_objetos.py --source 0 --conf 0.5 --imgsz 640
```

---

## 🧠 ¿Qué hace la app?

* Abre la cámara y procesa cada fotograma con **YOLOv8**.
* Dibuja un **rectángulo** alrededor de cada objeto, con **etiqueta** y **confianza** (0–1).
* Usa **un color distinto por clase** (permanente para cada nombre de clase).
* Muestra los **FPS** (cuadros por segundo).

---

## 🎛️ Controles y parámetros

* **Tecla `q`**: salir.

**Parámetros CLI** (opciones al ejecutar):

* `--source`: índice de cámara (por defecto `0`).
* `--conf`: confianza mínima para mostrar detecciones (recomendado `0.25–0.8`).
* `--imgsz`: tamaño de entrada del modelo (ej. `320/480/640/960`; mayor = mejor precisión / menor FPS).

**Ejemplos:**

```bash
# Cámara integrada con confianza más alta
python detecta_objetos.py --source 0 --conf 0.6

# Resolución más baja para ganar velocidad
python detecta_objetos.py --imgsz 480
```

---

## ⚡ Aceleración por GPU (opcional)

Si tienes **tarjeta NVIDIA** y **CUDA** correctamente instalada, Ultralytics/YOLO suele detectar la GPU automáticamente.
Si no tienes GPU o CUDA, la app funciona en **CPU** (más lenta).

---

## 🧰 Compilar tu propio .exe (opcional, para distribuir)

> Ya te damos un `.exe`, pero si quieres generarlo tú:

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole detecta_objetos.py
```

El ejecutable se guarda en la carpeta `dist/`.
La primera ejecución en una máquina “limpia” puede tardar mientras se descarga el modelo.

---

## 🗂️ Estructura del proyecto

```
.
├─ detecta_objetos.py      # Código principal
├─ README.md               # Este archivo
└─ requirements.txt        # (opcional) ultralytics, opencv-python
```

Los modelos se cachean por defecto en:

```
C:\Users\<TU_USUARIO>\.cache\Ultralytics\
```

---

## 🧩 Solución de problemas (FAQ)

**1) “No se puede abrir la cámara”**

* Cierra otras apps que la estén usando.
* Prueba con otro índice de cámara: `--source 1`, `--source 2`.
* Revisa permisos de cámara en **Configuración de Windows → Privacidad → Cámara**.

**2) “Va lento / se traba”**

* Prueba con `--imgsz 480` o `--imgsz 320`.
* Sube `--conf` (ej. `0.6`) para mostrar menos cajas.
* Cierra programas en segundo plano.

**3) “Falla al descargar el modelo”**

* Verifica tu conexión a internet la primera vez.
* Ejecuta de nuevo; YOLO reintenta la descarga.

**4) “DLL load failed / MSVCP… faltante” (muy raro)**

* Asegúrate de usar **Python 64-bit** en **Windows 64-bit**.
* Instala **Microsoft Visual C++ Redistributable** (última versión x64) desde la web de Microsoft.

**5) Antivirus bloquea el .exe**

* Al ser un ejecutable recién generado, algunos antivirus pueden marcarlo. Si confías en el origen, crea una **excepción**.

---

## 🔒 Privacidad

* El video se procesa **localmente**.
* No se sube ni envía a ningún servidor.
* Puedes borrar la caché de modelos en cualquier momento (carpeta `.cache\Ultralytics` en tu usuario).

---

## 📝 Licencia

Indica aquí la licencia que prefieras (por ejemplo, MIT).

---

## 🙌 Créditos

* **Ultralytics YOLOv8**: framework de detección de objetos.
* **OpenCV**: captura de cámara y dibujo en pantalla.

---

## 🚀 Roadmap (ideas para próximas versiones)

* Grabación de video y captura de imagen con tecla.
* Filtro por clases.
* Barra/slider para cambiar `conf` en vivo.
* Interfaz gráfica (PyQt/Tkinter).
* Paquete instalador (.msi) para Windows.

---

### Contacto / Soporte

¿Dudas o problemas? Abre un **Issue** en este repositorio y describe:

* Versión de Windows.
* Si usaste **.exe** o **código**.
* Mensaje de error y, si es posible, captura de pantalla.

```
```
