import pathlib


path = pathlib.Path(__file__).parent.resolve()
n_path = str(path) + "\sound"
print(n_path)