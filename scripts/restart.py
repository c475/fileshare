import subprocess

subprocess.call(["sudo", "systemctl", "stop", "gunicorn.service"])
subprocess.call(["sudo", "systemctl", "start", "gunicorn.service"])

subprocess.call(["sudo", "systemctl", "stop", "signaling_server.service"])
subprocess.call(["sudo", "systemctl", "start", "signaling_server.service"])

subprocess.call(["sudo", "nginx", "-s", "reload"])
