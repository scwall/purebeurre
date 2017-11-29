import os


def road_os_path(*roadfile):
    return os.path.join(os.getcwd(), *roadfile)
