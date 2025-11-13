import subprocess
import time
import os

last_detected = 0
COOLDOWN = 1.0
LOG_FILE = "detections_log.txt"

with open(LOG_FILE, "a") as log:
    process = subprocess.Popen(
        ['./luckfox_pico_rtsp_yolov5'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=os.environ.copy()
    )

    print("Watching for 'person' detections...\n")

    for line in iter(process.stdout.readline, ''):
        if "person @" in line:
            now = time.time()
            if now - last_detected > COOLDOWN:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                entry = f"[{timestamp}] DETECTED: {line.strip()}\n"
                print(entry.strip())
                log.write(entry)
                log.flush()
                last_detected = now

    process.wait()

