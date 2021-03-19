#!/usr/bin/python3
# Name: Elasticsearch JSON Import
# Author: K4YT3X
# Date Created: March 18, 2021
# Last Updated: March 18, 2021

# local imports
import argparse
import json
import pathlib
import sys
import warnings

# third-party imports
from tqdm import tqdm
from elasticsearch import Elasticsearch


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="esimportndjson",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-i",
        "--input",
        type=pathlib.Path,
        help="input file path or input directory path",
        required=True,
    )

    parser.add_argument(
        "--index", help="name of the Elasticsearch index to import into", required=True
    )

    parser.add_argument(
        "--host",
        help="Elasticsearch instance hostname or IP",
        default="127.0.0.1",
    )

    parser.add_argument(
        "--port", type=int, help="Elasticsearch listening port", default=9200
    )

    parser.add_argument("-u", "--user", help="Elasticsearch username")

    parser.add_argument("-p", "--password", help="Elasticsearch password")

    parser.add_argument("-s", "--ssl", help="enable SSL", action="store_true")

    parser.add_argument(
        "--insecure", help="disable SSL certificate verifications", action="store_false"
    )

    parser.add_argument(
        "--disable-file-length-count",
        help="do not count file length in progress bar, may save some time for large files",
        action="store_true",
    )

    return parser.parse_args()


def import_file(ndjson_file: pathlib.Path):
    """import the given NDJSON file into Elasticsearch

    Args:
        ndjson_file (pathlib.Path): NDJSON file path
    """
    with ndjson_file.open("r") as file_handle:

        file_length = None
        if not args.disable_file_length_count:
            file_length = len([_ for _ in file_handle])
            file_handle.seek(0)

        document_id = 1
        for line in tqdm(
            file_handle,
            ascii=True,
            desc=f"Importing {ndjson_file.name}",
            total=file_length,
        ):
            elasticsearch.index(
                index=args.index,
                ignore=400,
                doc_type="docket",
                id=document_id,
                body=json.loads(line),
            )
            document_id += 1


# parse command line arguments
args = parse_arguments()

# create an Elasticsearch connection instance
elasticsearch = Elasticsearch(
    [{"host": args.host, "port": args.port}],
    http_auth=(args.user, args.password),
    scheme="https" if args.ssl else "http",
    verify_certs=args.insecure,
    ssl_show_warn=False,
)

# if the input path is a single file
if args.input.is_file():
    files_to_import = [args.input]

# if the input path is a directory
elif args.input.is_dir():
    files_to_import = [f for f in args.input.iterdir() if f.suffix == ".json"]

else:
    print("Error: The input path is neither a file nor a directory", file=sys.stderr)
    sys.exit(1)

# for every NDJSON file in the current directory
try:
    print(f"Found {len(files_to_import)} files to import in total")
    for ndjson_file in files_to_import:

        # suppress all Elasticsearch warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            import_file(ndjson_file)

except (SystemExit, KeyboardInterrupt):
    print("Warning: Exit signal caught, import aborted")
