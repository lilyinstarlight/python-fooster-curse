import argparse
import sys

from .. import curse


def main():
    argparser = argparse.ArgumentParser(description='rewrite identifiers in Python source code with Unicode characters that still have the same canonical normalization', usage='%(prog)s [-h] [-i] [file.py]')
    argparser.add_argument('-i', '--in-place', action='store_true', dest='inplace', help='rewrite file in place (writes to stdout if omitted)')
    argparser.add_argument('file', metavar='file.py', nargs=None if '-i' in sys.argv or sys.stdin.isatty() else '?', default=None, help='name of Python file to rewrite (reads from stdin if omitted)')

    args = argparser.parse_args()

    if args.file:
        with open(args.file, 'r') as infile:
            source = infile.read()
    else:
        source = sys.stdin.read()

    cursed = curse.rewrite(source)

    if args.inplace:
        with open(args.file, 'w') as outfile:
            outfile.write(cursed)
    else:
        sys.stdout.write(cursed)


if __name__ == '__main__':
    main()
