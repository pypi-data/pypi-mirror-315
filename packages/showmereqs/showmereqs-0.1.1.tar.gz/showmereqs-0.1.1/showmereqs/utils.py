"""
This module contains utility functions for ShowMeReqs.

Some package mapping and stdlib data are derived from pipreqs:
https://github.com/bndr/pipreqs/tree/master
Licensed under Apache License, Version 2.0
"""

import json
import sys
from pathlib import Path

config_dir = Path(__file__).parent / "config"
special_mapping_path = config_dir / "special_mapping"
stdlib_path = config_dir / "stdlib"
ignore_path = config_dir / "ignore.json"

special_mapping: dict[str, str] = {}
stdlib_modules: set[str] = set()
ignore_dirs: set[str] = set()


def get_special_mapping():
    global special_mapping
    if len(special_mapping) == 0:
        with open(special_mapping_path, "r") as f:
            for line in f.read().splitlines():
                import_name, package_name = line.strip().split(":")
                special_mapping[import_name] = package_name

    return special_mapping


def get_builtin_modules() -> set[str]:
    """get python builtin modules"""
    global stdlib_modules
    if len(stdlib_modules) != 0:
        return stdlib_modules

    # method after Python 3.10+
    if hasattr(sys, "stdlib_module_names"):
        return set(sys.stdlib_module_names)

    # method before Python 3.10
    else:
        with open(stdlib_path, "r") as f:
            stdlib_modules = set(f.read().splitlines())
    return stdlib_modules


def get_ignore_dirs():
    global ignore_dirs
    if len(ignore_dirs) != 0:
        return ignore_dirs

    with open(ignore_path, "r") as f:
        ignore_dirs = set(json.load(f)["ignore_dirs"])

    return ignore_dirs


if __name__ == "__main__":
    special_mapping = get_special_mapping()
    builtin_modules = get_builtin_modules()

    print(special_mapping)
