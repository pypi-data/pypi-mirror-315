import importlib.metadata
from typing import Optional

import requests

from showmereqs.utils import get_mapping


class PackageInfo:
    """a class to get package info, including package name, version, etc."""

    json_api = "https://pypi.org/pypi"

    def __init__(self, import_name: str):
        self.import_name = import_name
        self.version: Optional[str] = self._get_local_version()

        self.mapping_name: Optional[str] = self._get_package_name_from_mapping()

        self.package_name: Optional[str] = None
        if self.mapping_name is None:
            json_info = self._get_pypi_json(self.import_name)
            if json_info is not None:
                self.package_name = json_info["info"]["name"]
        else:
            self.package_name = self.mapping_name

    def __str__(self):
        return f"<PackageInfo> {{\nimport_name: {self.import_name}\nversion: {self.version}\npackage_name: {self.package_name}\n}}"

    def format_row(self):
        """format the package info into a row"""
        return (
            self.version is not None,
            self.package_name is not None,
            self.format_version_info(),
            self.format_import_info(),
        )

    def format_version_info(
        self,
        eq_sign: str = "==",
    ):
        if self.version is None:
            return f"{self.package_name}"
        version_txt = f"{self.package_name}{eq_sign}{self.version}"
        return f"{version_txt}"

    def format_import_info(self):
        return f"# {self.import_name}"

    def _get_local_version(self):
        try:
            version = importlib.metadata.version(self.import_name)
            return version
        except importlib.metadata.PackageNotFoundError:
            return None

    def _get_package_name_from_mapping(self, special_mapping: dict[str, str] = None):
        if special_mapping is None:
            special_mapping = get_mapping()
        if self.import_name in special_mapping:
            return special_mapping[self.import_name]
        return None

    def _get_pypi_json(self, package_name: str):
        api = f"{self.json_api}/{package_name}/json"
        try:
            response = requests.get(api, timeout=2)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(f"Warning: Error checking {package_name} on PyPI: {e}")
