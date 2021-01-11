import os

path_sep = "/"
package_path = path_sep.join(os.path.dirname(__file__).split(path_sep)[:-1]) + path_sep


def abs_path(package_relative_path: str):
    return package_path + package_relative_path
