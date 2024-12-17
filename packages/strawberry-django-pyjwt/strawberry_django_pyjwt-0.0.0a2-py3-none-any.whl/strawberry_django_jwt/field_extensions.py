from __future__ import annotations

from typing import Any, Dict

import strawberry
from strawberry.annotation import StrawberryAnnotation
from strawberry.types.arguments import StrawberryArgument
from strawberry.types.field import StrawberryField
from strawberry.field_extensions import InputMutationExtension
from strawberry.utils.str_converters import capitalize_first, to_camel_case


class DynamicInputMutationExtension(InputMutationExtension):
    """
    Inspired from
    https://raw.githubusercontent.com/strawberry-graphql/strawberry/main/strawberry/field_extensions/input_mutation.py
    """

    def apply(self, field: StrawberryField) -> None:
        resolver = field.base_resolver
        assert resolver

        name = field.graphql_name or to_camel_case(resolver.name)
        type_dict: Dict[str, Any] = {
            "__doc__": f"Input data for `{name}` mutation",
            "__annotations__": {},
        }

        for arg in field.arguments:
            arg_field = StrawberryField(
                python_name=arg.python_name,
                graphql_name=arg.graphql_name,
                description=arg.description,
                default=arg.default,
                type_annotation=arg.type_annotation,
                directives=tuple(arg.directives),
            )
            type_dict[arg_field.python_name] = arg_field
            type_dict["__annotations__"][
                arg_field.python_name
            ] = arg.type_annotation.annotation

        caps_name = capitalize_first(name)
        new_type = strawberry.input(type(f"{caps_name}Input", (), type_dict))
        field.arguments = [
            StrawberryArgument(
                python_name="input",
                graphql_name=None,
                type_annotation=StrawberryAnnotation(
                    new_type,
                    namespace=resolver._namespace,
                ),
                description=type_dict["__doc__"],
            )
        ]
