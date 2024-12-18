import argparse
import getpass
import logging
import json
from pathlib import Path

import pykeepass

from .secret import Secret

logger = logging.getLogger(__name__)

DESCRIPTION = """
Convert a Keepass database into DuckDB secrets
https://duckdb.org/docs/configuration/secrets_manager.html
"""


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("keepass_file", type=Path, help="Keepass database file")
    parser.add_argument(
        "--log_level",
        default="WARNING",
        choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
    )
    parser.add_argument("--password")
    parser.add_argument(
        "--type", "-t", help="DuckDB secret type e.g. S3", required=True
    )
    parser.add_argument("--persistent", action="store_true")
    parser.add_argument("--replace", action="store_true")
    parser.add_argument("--if_not_exists", action="store_true")
    parser.add_argument(
        "--keys",
        "-k",
        help='JSON dictionary of key-value pairs e.g. {"region":"eu-west-2"}',
        type=json.loads,
        default=dict(),
    )

    return parser.parse_args()


def entry_title_to_sql_name(title: str) -> str:
    """
    Convert any string into a valid SQL name.
    """
    name = title.replace(" ", "_").replace("-", "_").lower()
    name = "".join((c for c in name if c.isalnum() or c == "_"))
    return name


def main():
    args = get_args()
    logging.basicConfig(level=args.log_level)

    # Load Keepass database file
    keepass = pykeepass.PyKeePass(
        args.keepass_file, password=args.password or getpass.getpass("Enter password: ")
    )

    # Iterate over all password entries
    for group in keepass.find_groups(recursive=True):
        for entry in group.entries:
            logger.info(entry)

            # Convert entry to a secret
            secret = Secret(
                name=entry_title_to_sql_name(entry.title),
                key_id=entry.username,
                secret=entry.password,
                secret_type=args.type,
                persistent=args.persistent,
                replace=args.replace,
                if_not_exists=args.if_not_exists,
                scope=entry.url,
                **args.keys,
            )

            print(secret)


if __name__ == "__main__":
    main()
