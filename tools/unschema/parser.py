from __future__ import annotations

from typing import Tuple  # , Any

types = {
    "string": "str",
    "number": "float",
    "integer": "int",
    "boolean": "bool",
    "object": "dict",
    "array": "list",
    "null": "None",
}


# # Used for debugging
# class AppendPrint(list):
#     def append(self, obj: Any) -> None:
#         if obj:
#             print(obj)
#         super().append(obj)


def generate(
    obj: dict, /, *, title: str = "GeneratedObject", no_comments: bool = False
) -> Tuple[str, str]:  # sourcery skip: low-code-quality
    """Makes TypedDict from a JSON Schema object.

    Arguments:
        obj: JSON Schema dict.
        title: The title of the result.
        no_comments: If True, no comments will be added.

    Returns:
        The generated TypedDicts, the result values name and the comments.
    """
    # The other TypedDicts
    result = []

    # The real annotation
    annotation: str

    obj_type = obj.get("type")

    # allOf, anyOf, oneOf, (not)?
    if not obj_type:
        # Treating oneOf as allOf, since is kinda the
        # same and there isn't a way to type it in Python
        if objs := obj.get("anyOf") or obj.get("oneOf"):
            union_items = []
            optional = False
            for obj_schema in objs:
                if obj_schema["type"] == "null":
                    optional = True
                else:
                    extras, target = generate(obj_schema, title=title, no_comments=no_comments)
                    result.append(extras)
                    union_items.append(target)

            annotation = f"{'Optional' if optional else 'Union'}[{', '.join(union_items)}]"
        else:
            annotation = "Any"

    # Union for parameters
    elif isinstance(obj_type, list):
        union_items = []
        is_optional = False

        for obj_type_item in obj_type:
            if obj_type_item == "null":
                is_optional = True
            else:
                union_items.append(types[obj_type_item])

        annotation = f"{'Optional' if is_optional else 'Optional'}[{', '.join(union_items)}]"

    elif obj_type == "boolean":
        annotation = "bool"

    elif obj_type == "null":
        annotation = "None"

    elif obj_type == "string":
        if not no_comments:
            if obj_min_len := obj.get("minLength"):
                result.append(f"    # Minimum length: {obj_min_len}")
            if obj_max_len := obj.get("maxLength"):
                result.append(f"    # Maximum length: {obj_max_len}")
            if obj_pattern := obj.get("pattern"):
                result.append(f"    # Pattern: {obj_pattern!r}")

        annotation = "str"

    elif obj_type in {"integer", "number"}:
        if not no_comments:
            if obj_multiple := obj.get("multipleOf"):
                result.append(f"    # Multiple of: {obj_multiple}")
            if obj_minimum := obj.get("minimum"):
                result.append(f"    # Minimum (x >= N): {obj_minimum}")
            if obj_exclusive_minimum := obj.get("exclusiveMinimum"):
                result.append(f"    # Exclusive minimum (x > N): {obj_exclusive_minimum}")
            if obj_maximum := obj.get("maximum"):
                result.append(f"    # Maximum (x <= N): {obj_maximum}")
            if obj_exclusive_maximum := obj.get("exclusiveMaximum"):
                result.append(f"    # Exclusive maximum (x < N): {obj_exclusive_maximum}")
            if any([obj_minimum, obj_exclusive_minimum, obj_maximum, obj_exclusive_maximum]):
                result.append("     # x = the variable, N = the min/max")

        annotation = "int" if obj_type == "integer" else "float"

    elif obj_type == "object":
        # TODO: add support for patternProperties, unevaluatedProperties,
        # propertyNames, minProperties, maxProperties

        if obj_properties := obj.get("properties"):
            # TODO: make it so the extra properties are typed instead of Any, somehow
            total = ", total=False" if obj.get("additionalProperties") else ""

            annotation = obj_title = obj.get("title", title).replace(" ", "")
            typed_dict = [f"class {obj_title}(TypedDict{total}):"]

            for key, value in obj_properties.items():
                extras, param_annotation = generate(
                    value, title=key.capitalize(), no_comments=no_comments
                )
                result.append(extras)

                if key not in obj.get("required", []):
                    param_annotation = f"NotRequired[{param_annotation}]"

                if not no_comments:
                    examples = (', '.join(str(ex) for ex in exs)).replace("\n", "\\n") if (exs := value.get("examples")) else ""

                    if (example := examples[:70]) != examples:
                        examples = f"{example}[...]"

                    typed_dict.extend(
                        [
                            f"    # Format: {fmt}" if (fmt := value.get("format")) else "",
                            f"    # Example: {examples}"
                        ]
                    )

                typed_dict.append(f"    {key}: {param_annotation}")

            result.extend(typed_dict)
        else:
            annotation = "dict"

    elif obj_type == "array":
        # TODO: add support for contains, minContains,
        # maxContains, minLength, maxLength, uniqueItems

        if obj_items := obj.get("items"):
            extras, target = generate(obj_items, no_comments=no_comments)
            result.append(extras)
            annotation = f"List[{target}]"

        elif obj_prefix_items := obj.get("prefixItems"):
            tuple_annotation = []
            for item in obj_prefix_items:
                (
                    extras,
                    target,
                ) = generate(item, no_comments=no_comments)
                result.append(extras)
                tuple_annotation.append(target)

            if extra_item_type := obj.get("items"):
                if extra_item_type is not True:
                    extras, extra_type = generate(extra_item_type, no_comments=no_comments)
                    result.append(extras)
                    if not no_comments:
                        result.append(
                            f"    # The extra items for the tuple are typed as: {extra_type}"
                        )

                tuple_annotation.append("...")

            annotation = f"Tuple[{', '.join(tuple_annotation)}]"
        else:
            annotation = "list"

    else:
        annotation = "Any"

    result = [i for i in result if i]

    return "\n".join(result), annotation
