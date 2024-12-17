import os
import sys

import click

from showmereqs.analyze import get_third_party_imports
from showmereqs.generate import generate_reqs
from showmereqs.package_info import PackageInfo

logo = """\033[92m
 ____  _                    __  __       ____                
/ ___|| |__   _____  __  _ |  \/  | ___ |  _ \ ___  __ _ ___ 
\___ \| '_ \ / _ \ \/  \/ || |\/| |/ _ \| |_) / _ \/ _` / __|
 ___) | | | | (_) \  /\  / | |  | |  __/|  _ <  __/ (_| \__ \\
|____/|_| |_|\___/ \/  \/  |_|  |_|\___||_| \_\___|\__, |___/
                                                      \_|     
\033[0m"""


@click.command()
@click.argument(
    "path",
    type=click.Path(exists=True, file_okay=True, dir_okay=True, resolve_path=True),
    default=".",
)
@click.option("--outdir", "-o", default=".", help="path to output directory")
@click.option(
    "--force",
    "-f",
    is_flag=True,
    default=False,
    help="whether to force overwrite output file",
)
@click.option(
    "--no-detail",
    "-nd",
    is_flag=True,
    default=False,
    help="detailed information in requirements.txt",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
    help="whether to show detailed information",
)
def main(**kwargs) -> None:
    """Analyze Python project dependencies and generate requirements.txt"""
    print(logo)
    check_outdir(kwargs)

    third_party_imports = get_third_party_imports(kwargs["path"])
    third_party_package_infos = [
        PackageInfo(import_name) for import_name in third_party_imports
    ]
    generate_reqs(third_party_package_infos, **kwargs)

    print(f"\033[92mgenerate {kwargs['outdir']}/requirements.txt successfully\033[0m")


def check_outdir(kwargs):
    if os.path.exists(kwargs["outdir"]):
        if not kwargs["force"]:
            print(
                f"file {kwargs['outdir']}/requirements.txt already exists, use -f to force overwrite"
            )
            sys.exit(1)
    else:
        print(f"create directory {kwargs['outdir']}")
        os.makedirs(kwargs["outdir"], exist_ok=True)


if __name__ == "__main__":
    main()
