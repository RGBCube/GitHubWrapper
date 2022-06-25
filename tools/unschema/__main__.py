import json
import time
from argparse import ArgumentParser

from .parser import generate

parser = ArgumentParser(description="Generate TypedDicts from a json schema.")
parser.add_argument("-f", "--from", required=True, help="The json schema to generate from.")
parser.add_argument("-t", "--to", help="The file to write the TypedDicts to.")
parser.add_argument(
    "-ne", "--no-examples", action="store_true", help="If given, examples wont be added."
)
parser.add_argument(
    "-nf", "--no-formats", action="store_true", help="If given, formats wont be added."
)
parser.add_argument(
    "-p",
    "--print",
    action="store_true",
    help="If given, the result will be printed instead of being writing to a file",
)
args = parser.parse_args()

with open(args.__getattribute__("from")) as g:
    schema = json.load(g)

start = time.monotonic()
text = f"""
from __future__ import annotations

from typing import List, Optional, TypedDict, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import NotRequired{generate(schema, no_examples=args.no_examples, no_formats=args.no_formats)}  # Rename this to your liking.
"""[
    1:
]

if args.print:
    print(text)
else:
    if not args.to:
        raise ValueError("-t/--to is required when writing to a file.")

    with open(args.to, "w") as f:
        f.write(text)

end = time.monotonic() - start

print(f"Success! Finished in {end*1000:.3} milliseconds.")
