import os
from pathlib import Path


from subprocess import check_output


def find_pony_stdlib_path():
    """
    Retrun the pony std lib path. If `PONY_STDLIB` env var
    is set, use this. Otherwise, return the stdlib of current ponyc
    """
    path = os.environ.get("PONY_STDLIB", None)
    if path is None:
        # TODO: this relies on which. Pretty sure it's not in MSwin and
        #       I'm not sure that it's available on OSX
        ponyc_path = check_output(["which", "ponyc"])
        ponyc_path = Path(ponyc_path.decode().strip())
        path = ponyc_path.resolve().joinpath("../../packages").resolve()
        if not path.exists():
            raise FileNotFoundError()
        path = str(path)
    return path


def is_package(path):
    if not os.path.isdir(path):
        return False
    for f in os.listdir(path):
        if f.endswith(".pony"):
            if os.path.isfile(os.path.join(path, f)):
                return True
    return False
