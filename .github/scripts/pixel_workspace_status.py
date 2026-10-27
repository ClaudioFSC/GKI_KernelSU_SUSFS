
#!/usr/bin/env python3
import json
import os
import subprocess
import sys

ORIGINAL_SCM = "-g8d0115b07367-ab16385437"
ORIGINAL_EPOCH = "1789695193"

env = os.environ.copy()
env["SOURCE_DATE_EPOCH"] = ORIGINAL_EPOCH

result = subprocess.run(
    ["bash", "build/kernel/kleaf/workspace_status.sh"],
    env=env,
    capture_output=True,
    text=True
)

if result.returncode != 0:
    sys.stderr.write(result.stderr)
    sys.exit(result.returncode)

found_scm = False
found_date = False

for line in result.stdout.splitlines():
    key, separator, value = line.partition(" ")

    if key == "STABLE_SCMVERSIONS":
        versions = json.loads(value)
        if "common" not in versions:
            sys.exit("ERRO: projeto common nao encontrado")
        versions["common"] = ORIGINAL_SCM
        line = key + " " + json.dumps(versions, sort_keys=True)
        found_scm = True

    elif key == "STABLE_SOURCE_DATE_EPOCHS":
        dates = json.loads(value)
        if "common" not in dates:
            sys.exit("ERRO: data do projeto common ausente")
        dates["common"] = ORIGINAL_EPOCH
        line = key + " " + json.dumps(dates, sort_keys=True)
        found_date = True

    print(line)

if not (found_scm and found_date):
    sys.exit("ERRO: metadados Kleaf incompletos")
