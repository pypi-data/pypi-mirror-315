import json
import os
import tempfile
from pathlib import Path
from subprocess import run

import pytest


def test_compile():
    # First, compile from the SDK and check that behavior
    tmpdirname = tempfile.mkdtemp()
    sdk_cli = "connector"
    compile_command = [
        sdk_cli,
        "compile-on-prem",
        "mock_connector",
        "projects/connectors/python/mock-connector",
        "--output-directory",
        str(tmpdirname),
    ]
    result = run(
        " ".join(compile_command),
        shell=True,
        capture_output=True,
        cwd=Path(os.path.dirname(__file__)).parent.parent.parent.parent.parent,
    )
    stdout = str(result.stdout, "utf-8")
    stderr = str(result.stderr, "utf-8")
    if result.returncode != 0:
        print("stdout:\n", stdout)
        print("stderr:\n", stderr)
        pytest.fail(f"Exited {result.returncode}: {' '.join(compile_command)}")
    executable = stdout.strip(" \n\t")
    assert (
        len(executable) > 0 and len(executable.split(" ")) == 1
    ), f"The output doesn't look like a single file: '{executable}'"
    assert os.path.exists(executable), f"The output isn't a file: '{executable}'"
    assert os.access(executable, os.X_OK), f"The file isn't executable: '{executable}'"

    # Now, check the compiled connector execution
    info_command = [executable, "info"]
    result = run(
        " ".join(info_command),
        shell=True,
        capture_output=True,
    )
    assert result.returncode == 0, f"Exited {result.returncode}: {' '.join(info_command)}"
    try:
        info_json = json.loads(str(result.stdout, "utf-8"))
    except json.JSONDecodeError:
        pytest.fail("Non JSON emitted from compiled connector")
    assert "response" in info_json, "Unexpected JSON structure from compiled connector"
    assert "version" in info_json["response"], "Unexpected JSON structure from compiled connector"
