import subprocess

subprocess.call(["sudo", "systemctl", "stop", "gunicorn.service"])
subprocess.call(["sudo", "systemctl", "start", "gunicorn.service"])

subprocess.call(["sudo", "systemctl", "stop", "websockets.service"])
subprocess.call(["sudo", "systemctl", "start", "websockets.service"])

subprocess.call(["sudo", "nginx", "-s", "reload"])
