import os

path_sep = os.path.sep
package_path = "/".join(os.path.dirname(__file__).split(path_sep)[:-1]) + "/"


def abs_path(package_relative_path: str):
    return package_path + package_relative_path
