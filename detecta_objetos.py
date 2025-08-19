import argparse
import time
import colorsys
from collections import defaultdict

import cv2
from ultralytics import YOLO


def generar_color_constante(nombre_clase: str):
    """
    Devuelve un BGR determinístico por clase.
    Usamos HSV -> BGR para repartir colores de forma estable.
    """
    # Hash simple y estable
    h = (hash(nombre_clase) % 360) / 360.0
    s, v = 0.8, 1.0
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(b * 255), int(g * 255), int(r * 255)  # BGR para OpenCV


def dibujar_caja_con_etiqueta(frame, xyxy, etiqueta, color):
    x1, y1, x2, y2 = map(int, xyxy)
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    (tw, th), baseline = cv2.getTextSize(etiqueta, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
    # Fondo para legibilidad
    cv2.rectangle(frame, (x1, y1 - th - baseline - 4), (x1 + tw + 6, y1), color, -1)
    cv2.putText(frame, etiqueta, (x1 + 3, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)


def calcular_fps(tiempo_anterior, alpha=0.9, fps_suavizado=0.0):
    ahora = time.time()
    dt = max(ahora - tiempo_anterior, 1e-6)
    fps_instantaneo = 1.0 / dt
    fps_suavizado = alpha * fps_suavizado + (1 - alpha) * fps_instantaneo
    return ahora, fps_suavizado


def main():
    parser = argparse.ArgumentParser(description="Detección de objetos en tiempo real con YOLOv8 + OpenCV")
    parser.add_argument("--source", type=int, default=0, help="Índice de la cámara (0 por defecto)")
    parser.add_argument("--conf", type=float, default=0.5, help="Confianza mínima para mostrar detecciones")
    parser.add_argument("--imgsz", type=int, default=640, help="Tamaño de imagen para la inferencia (ej. 640)")
    parser.add_argument("--model", type=str, default="yolov8n.pt", help="Ruta o nombre del modelo YOLOv8")
    args = parser.parse_args()

    # Carga del modelo
    try:
        model = YOLO(args.model)  # descarga automática si no existe
    except Exception as e:
        print("Error cargando el modelo. Verifica la ruta o tu conexión a internet.")
        print(e)
        return

    # Abrir cámara (DirectShow ayuda en Windows)
    cap = cv2.VideoCapture(args.source, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print(f"No se pudo abrir la cámara con índice {args.source}.")
        return

    # Ajustes básicos (opcional): descomenta si quieres forzar resolución de captura
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Colores por clase (cache)
    clase_a_color = {}
    # Para mostrar conteo por clase si se desea en el futuro
    conteo_clases = defaultdict(int)

    nombre_ventana = "Detección en tiempo real - YOLOv8 (q para salir)"
    cv2.namedWindow(nombre_ventana, cv2.WINDOW_NORMAL)

    tiempo_prev = time.time()
    fps_suav = 0.0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo leer frame de la cámara.")
            break

        # Inferencia
        # stream=True devuelve un generador eficiente; usamos una sola pasada
        results = model.predict(source=frame, imgsz=args.imgsz, conf=args.conf, verbose=False)

        # Reiniciar conteo por frame
        conteo_clases.clear()

        # Dibujar resultados
        for r in results:
            boxes = r.boxes
            names = r.names  # dict id->nombre

            if boxes is None:
                continue

            for box in boxes:
                xyxy = box.xyxy[0].tolist()
                cls_id = int(box.cls[0].item())
                conf = float(box.conf[0].item())
                nombre = names.get(cls_id, f"id_{cls_id}")

                # Color determinístico por clase
                if nombre not in clase_a_color:
                    clase_a_color[nombre] = generar_color_constante(nombre)
                color = clase_a_color[nombre]

                etiqueta = f"{nombre} {conf:.2f}"
                dibujar_caja_con_etiqueta(frame, xyxy, etiqueta, color)

                conteo_clases[nombre] += 1

        # FPS
        tiempo_prev, fps_suav = calcular_fps(tiempo_prev, fps_suavizado=fps_suav)
        cv2.putText(frame, f"FPS: {fps_suav:0.1f}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (20, 20, 20), 4, cv2.LINE_AA)
        cv2.putText(frame, f"FPS: {fps_suav:0.1f}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (240, 240, 240), 2, cv2.LINE_AA)

        # Mostrar
        cv2.imshow(nombre_ventana, frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
