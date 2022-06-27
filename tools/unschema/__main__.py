import json
import os
import time
from argparse import ArgumentParser

from .parser import generate

# fmt: off
parser = ArgumentParser(
    description="Generate TypedDicts from a json schema."
)
parser.add_argument(
    "-f",
    "--from",
    required=True,
    help="The json schema to generate from."
)
parser.add_argument(
    "-t",
    "--to",
    help="The file to write the TypedDicts to."
)
parser.add_argument(
    "-on",
    "--object-name",
    default="GeneratedObjectResult",
    help="The name of the object to generate.",
)
parser.add_argument(
    "-nc",
    "--no-comments",
    action="store_true",
    help="If given, comments wont be added."
)
parser.add_argument(
    "-p",
    "--print",
    action="store_true",
    help="If given, the result will be printed.",
)
# fmt: on

args = parser.parse_args()

with open(args.__getattribute__("from")) as f:
    schema = json.load(f)

start = time.perf_counter()
generated = generate(schema, no_comments=args.no_comments)
end = time.perf_counter() - start

if args.print:
    print(generated)
else:
    if not (to := args.to):
        raise ValueError("-t/--to is required when writing to a file.")

    with open(to, "w") as f:
        f.write(generated)

    os.system(
        f"unimport {to} --gitignore -r --ignore-init; black {to}",
    )

print(f"\n\nSuccess! Finished in {end*1000:.3} milliseconds (formatting excluded)")
