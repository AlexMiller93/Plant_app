import os


def check_path_or_create_dir(path, filename):
    if os.path.exists:
        return os.path.join(path, filename)
    else:
        os.mkdir(path)
        return os.path.join(path, filename)