import argparse
import sys

from countfiles import __version__
from countfiles.node import SortBy, Tree


class HelpFormatter(argparse.HelpFormatter):
    _positionals: argparse._ArgumentGroup

    def _format_usage(self, usage, actions, groups, prefix):
        if prefix is None:
            prefix = "Usage: "
        return super()._format_usage(usage, actions, groups, prefix)

    def start_section(self, heading):
        return super().start_section(heading.capitalize())


def cli():
    parser = argparse.ArgumentParser(
        prog="countfiles",
        description="Show accumulated number of files per directory.",
        add_help=False,
        formatter_class=HelpFormatter,
    )

    parser.add_argument("path", type=str, default=".", nargs="?", help="Defaults to current working directory")
    parser.add_argument("--help", "-h", action="store_true", help="Show this help message and exit")
    parser.add_argument(
        "--max-depth", "-d", type=int,
        help="Iterate all the way, but only show directories down to this depth"
    )
    parser.add_argument(
        "--min-filecount", "-m", type=int,
        help="Iterate all the way, but only show directories with this number of files or more"
    )
    parser.add_argument("--sizes", "-s", action="store_true", help="Also show the total size of every directory")
    parser.add_argument("--count-dirs", "-c", action="store_true", help="Also include directories in the file counts")
    parser.add_argument("--reverse", "-r", action="store_true", help="Reverse result sorting")
    parser.add_argument("--no-color", "--no-colour", action="store_true", help="Output without colours")
    parser.add_argument("--no-hidden", action="store_true", help="Ignore hidden files and directories")
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version="%(prog)s " + __version__,
        help="Show program's version number and exit",
    )
    parser.add_argument(
        "--symlinks",
        "-ln",
        action="store_true",
        help="Follow symlinks (will throw exception if an infinite recursion is detected)",
    )

    sort_group = parser.add_mutually_exclusive_group()
    sort_group.add_argument("--sort-count", "-sc", action="store_true", help="Sort results by file count")
    sort_group.add_argument("--sort-size", "-ss", action="store_true", help="Sort results by total size")

    args = parser.parse_args()

    if args.help:
        parser.print_help()
        sys.exit(0)

    sort_by = SortBy.NAME
    if args.sort_count:
        sort_by = SortBy.FILECOUNT
    elif args.sort_size:
        sort_by = SortBy.SIZE

    tree = Tree(
        path=args.path,
        count_dirs=args.count_dirs,
        show_sizes=args.sizes,
        max_depth=args.max_depth,
        min_filecount=args.min_filecount,
        color=not args.no_color,
        sort_by=sort_by,
        reverse=args.reverse,
        symlinks=args.symlinks,
        hidden=not args.no_hidden,
    )
    print(str(tree))


if __name__ == "__main__":
    cli()
