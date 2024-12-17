import subprocess
import json
from pathlib import Path

from EVMVerifier.certoraContextClass import CertoraContext
from Shared import certoraUtils as Util
import os


def run_script_and_parse_json(context: CertoraContext) -> None:
    if not context.build_script:
        return
    try:
        env = os.environ.copy()
        result = subprocess.run(["python3", Path(context.build_script).resolve(), '--json'], capture_output=True, text=True,
                                env=env, cwd=Path(context.build_script).resolve().parent)

        # Check if the script executed successfully
        if result.returncode != 0:
            raise Util.CertoraUserInputError(f"Error running the script {context.build_script}\n{result.stderr}")

        json_obj = json.loads(result.stdout)

        if not json_obj or not json_obj.get("success"):
            raise Util.CertoraUserInputError(f"{result.stderr}\nBuild from {context.build_script} failed")

        context.rust_project_directory = json_obj.get("project_directory")
        context.rust_sources = json_obj.get("sources")
        context.rust_executables = json_obj.get("executables")

    except FileNotFoundError as e:
        raise Util.CertoraUserInputError(f"File not found: {e}")
    except json.JSONDecodeError as e:
        raise Util.CertoraUserInputError(f"Error decoding JSON: {e}")
    except Exception as e:
        raise Util.CertoraUserInputError(f"An unexpected error occurred: {e}")
