from src.scripts.get_versions import get_python_versions
from argparse import _SubParsersAction, ArgumentParser


def handle_list(parser: ArgumentParser):
    versions = get_python_versions()

    if parser.latest:
        versions = [version for version in versions if version['is_latest']]

    for v in versions:
        print(v['name'])

def list_command(sub_parser: _SubParsersAction[ArgumentParser]):

    parser = sub_parser.add_parser(
        'list',
        help='List all available Python versions'
    )

    parser.add_argument(
        '--latest',
        action='store_true',
        help='Show only the latest stable versions from each major release'
    )

    parser.set_defaults(func=handle_list)

    