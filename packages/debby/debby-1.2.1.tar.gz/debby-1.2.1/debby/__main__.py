import sys
from pathlib import Path
from typing import Optional, Sequence

from debby.args import Args
from debby.control_file import ControlFile
from debby.exceptions import DebbyError
from debby.files import Files
from debby.meta import MetaLoaderFactory
from debby.package import Package
from debby.scripts import Scripts


def create_package(args: Args) -> Path:
    meta = MetaLoaderFactory(args).loader().load()
    files = Files(args.files)
    package = Package(
        meta, ControlFile(meta, files, args.template), files, Scripts(args)
    )
    return package.create(args.out_dir)


def main(argv: Optional[Sequence[str]] = None):
    print(create_package(Args.parse(argv)))


if __name__ == "__main__":
    try:
        main()
    except DebbyError as e:
        print(e, file=sys.stderr)
