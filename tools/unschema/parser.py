from __future__ import annotations

from typing import Iterable, Tuple

types = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
    "object": "dict",
    "array": "list",
    "null": "None",
}

untypes = {v: k for k, v in types.items()}


def unspace(s: str) -> str:
    return s.replace(" ", "")


def mklist(s: Iterable) -> str:
    return f"[{', '.join(s)}]"


def generate(
    _schema: dict,
    /,
    *,
    no_examples: bool = False,
    no_formats: bool = False,
    title: str = "GeneratedObject",
) -> str:
    def inner_generate(
        schema: dict,
        /,
        *,
        _no_examples: bool = no_examples,
        _no_formats: bool = no_formats,
        _title: str = title,
    ) -> Tuple[str, str]:  # sourcery skip: low-code-quality

        # GeneratedObject = Union[..., ..., ...]
        if objects := schema.get("oneOf"):
            text = []
            union_items = []

            for item_schema in objects:
                generated_text, union_item = generate(item_schema, title=_title)

                text.append(generated_text)
                union_items.append(union_item)

            text.append(f"{_title} = Union{mklist(union_items)}")
            return "\n\n".join(_title), _title
        del objects

        # class GeneratedObject(TypedDict):
        if (object_type := schema["type"]) == untypes["dict"]:
            _title = unspace(schema["title"])

            dependencies = []
            current = [f'class {_title}(TypedDict):\n    """{schema["description"]}"""']

            for key, value in schema["properties"].items():
                if isinstance(value_type := value["type"], str):
                    param_type = types[value_type]

                elif isinstance(value_type, list):
                    combiner = "Union"
                    contents = []

                    for type in value_type:
                        if type == untypes["None"]:
                            combiner = "Optional"
                        else:
                            contents.append(types[type])

                    param_type = f"{combiner}{mklist(contents)}"

                elif isinstance(value_type, dict):
                    text, target = inner_generate(
                        value_type, _title=key, _no_examples=_no_examples, _no_formats=_no_formats
                    )
                    dependencies.append(text)
                    param_type = target

                else:
                    param_type = f"Unknown[{value_type}]"

                if key not in schema["required"]:
                    param_type = f"NotRequired[{param_type}]"

                eg = (
                    ""
                    if no_examples
                    else f"    # example: {mklist(str(eg) for eg in egs)[1:-1]}\n"
                    if (egs := value.get("examples"))
                    else ""
                )

                fmt = (
                    ""
                    if no_formats
                    else f"    # format: {fmt}\n"
                    if (fmt := value.get("format"))
                    else ""
                )

                sep = "\n" if eg or fmt else ""

                com = "# " if param_type.startswith("Unknown") else ""

                current.append(f"{sep}{eg}{fmt}    {com}{key}: {param_type}")

            dependencies.append("\n".join(current))
            result = "\n\n".join(dependencies[:-1]) + "\n\n\n" + dependencies[-1]

            return result, _title

        # GeneratedObject = List[...]
        elif object_type == untypes["list"]:
            generated, target = inner_generate(
                schema["items"], _title=_title, _no_examples=_no_examples, _no_formats=_no_formats
            )
            return f"{generated}\n\n\n{_title} = List[{target}]", _title

        else:
            print("Unknown/Unimplemented Object Type:", object_type)
            return "", ""

    return inner_generate(_schema)[0]
