# get_version.py
with open("_version.py") as f:
    exec(f.read())
print(__version__)  # type: ignore
