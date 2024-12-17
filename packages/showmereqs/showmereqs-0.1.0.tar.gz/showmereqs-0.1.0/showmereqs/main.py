import sys

from showmereqs.analyze import get_third_party_imports
from showmereqs.generate import generate_reqs
from showmereqs.package_info import PackageInfo


def main():
    args = sys.argv
    print(args)
    if len(args) < 2:
        print("Usage: showmereqs <path_to_project>")
        return

    third_party_imports = get_third_party_imports(args[1])
    third_party_package_infos = [
        PackageInfo(import_name) for import_name in third_party_imports
    ]
    generate_reqs(third_party_package_infos)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
