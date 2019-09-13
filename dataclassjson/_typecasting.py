import dataclasses
from logging import getLogger
from typing import Any, Dict, _GenericAlias  # type: ignore

from dataclassjson.exceptions import TypeCastingError


logger = getLogger(__name__)


def _typecasting_args(self: Any, *args: Any, **kwargs: Any) -> Dict[str, Any]:
    fields = dataclasses.fields(type(self))
    args_len = len(args)

    try:
        for i, field in enumerate(fields):
            field_type = field.type
            field_name = field.name

            if i < args_len:
                value = args[i]
            else:
                value = kwargs.get(field_name)

            if isinstance(value, dict) and not issubclass(field_type, dict):
                kwargs[field_name] = field_type(**value)

            elif isinstance(field_type, _GenericAlias):
                self._set_kwargs_generic_type(
                    field_type, kwargs, field_name, value
                )

            elif isinstance(value, field_type):
                kwargs[field_name] = value

            elif (
                isinstance(field_type, type)
                and issubclass(field_type, str)
                and isinstance(value, bytes)
            ):
                kwargs[field_name] = value.decode()

            else:
                kwargs[field_name] = field_type(value)

        return kwargs

    except TypeError as error:
        logger.exception(error)
        raise TypeCastingError(field.name, *error.args) from error


def _set_kwargs_generic_type(
    self: Any, generic: Any, kwargs: Dict[str, Any], field: str, value: Any
) -> None:
    if 'Union' in str(generic):
        for arg in generic.__args__:
            if issubclass(arg, str) and isinstance(value, bytes):
                kwargs[field] = value.decode()

            elif not isinstance(arg, type(None)):
                try:
                    kwargs[field] = arg(value)
                except TypeError:
                    message = (
                        'Attempt Union typecasting for '
                        f'type={arg.__name__} and field={field} '
                        'was failed'
                    )
                    logger.warning(message)
                    continue
                else:
                    return

        error = TypeCastingError(f'Invalid type={generic} for field={field}')
        logger.exception(error)
        raise error
