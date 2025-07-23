import subprocess
import datetime
import re

DEVICE_IP = ""

ADB_PATH = "adb.exe"
LOG_FILE = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

print(f"[*]{DEVICE_IP}")
print(f"[*]{LOG_FILE}")
print("---------------------------------------------")

pattern = re.compile(r"CameraDevice|CameraManager|android\.hardware\.Camera|libwebrtc|PeerConnection|SurfaceView|TextureView|MediaRecorder|openCamera|Camera permission|Failed to connect camera")

process = subprocess.Popen(
    [ADB_PATH, "-s", DEVICE_IP, "logcat"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

with open(LOG_FILE, "a", encoding="utf-8") as log_file:
    try:
        for line in process.stdout:
            if pattern.search(line):
                print(line.strip())
                log_file.write(line)

                if "CameraManager" in line or "CameraDevice" in line:
                    msg = "🟢 Camera2 API ➜ Recomendado: Hook o Modificación en APK"
                elif "android.hardware.Camera" in line:
                    msg = "🟢 API antigua ➜ Recomendado: Modificación fácil en APK"
                elif "libwebrtc" in line or "PeerConnection" in line:
                    msg = "🟡 WebRTC ➜ Recomendado: Redirigir stream o manipulación WebRTC"
                elif "SurfaceView" in line or "TextureView" in line:
                    msg = "🟡 vista estándar ➜ Recomendado: Overlay visual o reemplazo en layout"
                elif "MediaRecorder" in line:
                    msg = "🟡 grabación de video ➜ Recomendado: Interceptar flujo de audio/video"
                elif "openCamera" in line:
                    msg = "🟢 Llamada directa a la cámara ➜ Recomendado: Hook directo en APK"
                elif "Permission" in line:
                    msg = "🔴 Manejo de permisos detectado ➜ Recomendado: Bypass o manipulación de permisos"
                elif "Failed to connect camera" in line:
                    msg = "🔴 Error al conectar cámara ➜ Recomendado: Controlar acceso vía ADB o bloqueo"
                else:
                    msg = ""

                if msg:
                    print(msg)
                    log_file.write(msg + "\n")

                print("---------------------------------------------")
                log_file.write("---------------------------------------------\n")

    except KeyboardInterrupt:
        print("\n[!] Monitoreo detenido por el usuario.")
        process.terminate()
