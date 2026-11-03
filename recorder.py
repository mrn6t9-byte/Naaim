
import os
import sys
import time
import requests

DURATION = 5 * 60 * 60 + 30 * 60
VIDEO = "recording.mp4"

def main():
    source = os.getenv("VIDEO_EXPORT_URL")

    if not source:
        sys.exit("Missing VIDEO_EXPORT_URL")

    print("Waiting for authorized video export...")

    deadline = time.time() + DURATION

    while time.time() < deadline:
        response = requests.get(
            source,
            timeout=60,
            stream=True
        )
        response.raise_for_status()

        with open(VIDEO, "wb") as f:
            for chunk in response.iter_content(1024 * 1024):
                if chunk:
                    f.write(chunk)

        break

    if not os.path.exists(VIDEO):
        sys.exit("Video export unavailable")

    if os.path.getsize(VIDEO) == 0:
        sys.exit("Empty video file")

    print("Export downloaded successfully")

if __name__ == "__main__":
    main()
