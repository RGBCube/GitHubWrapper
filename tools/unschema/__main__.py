import json
import os
import time
from argparse import ArgumentParser

from .parser import generate

parser = ArgumentParser(description="Generate TypedDicts from a json schema.")
parser.add_argument("-f", "--from", required=True, help="The json schema to generate from.")
parser.add_argument("-t", "--to", help="The file to write the TypedDicts to.")
parser.add_argument(
    "-on",
    "--object-name",
    default="GeneratedObjectResult",
    help="The name of the object to generate.",
)
parser.add_argument(
    "-nc", "--no-comments", action="store_true", help="If given, comments wont be added."
)
parser.add_argument(
    "-p",
    "--print",
    action="store_true",
    help="If given, the result will be printed.",
)

args = parser.parse_args()

with open(args.__getattribute__("from")) as f:
    generated = generate(json.load(f), no_comments=args.no_comments)

start = time.perf_counter()

text = f"""from __future__ import annotations

from typing import Any, List, Optional, TypedDict, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import NotRequired

{generated[0]}

{args.object_name} = {generated[1]}
"""

if args.print:
    print(text)

    end = time.perf_counter() - start

else:
    if not (to := args.to):
        raise ValueError("-t/--to is required when writing to a file.")

    with open(to, "w") as f:
        f.write(text)

    end = time.perf_counter() - start

    os.system(
        f"unimport {to} --gitignore -r --ignore-init; isort {to}; black {to}; flynt {to} -tc",
    )

print(f"\n\nSuccess! Finished in {end*1000:.3} milliseconds")
