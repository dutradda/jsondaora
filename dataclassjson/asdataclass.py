import dataclasses
from logging import getLogger
from typing import Any, Dict, Type, _GenericAlias  # type: ignore

from dataclassjson.exceptions import TypeCastingError


logger = getLogger(__name__)


def asdataclass(jsondict: Dict[str, Any], cls: Type[Any]) -> Any:
    _cast_jsondict_values(jsondict, cls)
    return cls(**jsondict)


def _cast_jsondict_values(
    jsondict: Dict[str, Any], cls: Type[Any]
) -> Dict[str, Any]:
    fields = dataclasses.fields(cls)

    try:
        for field in fields:
            field_type = field.type
            field_name = field.name
            value = jsondict.get(field_name)

            if isinstance(value, dict) and not issubclass(field_type, dict):
                jsondict[field_name] = field_type(**value)

            elif isinstance(field_type, _GenericAlias):
                _set_jsondict_generic_type(
                    field_type, jsondict, field_name, value
                )

            elif isinstance(value, field_type):
                jsondict[field_name] = value

            elif (
                isinstance(field_type, type)
                and issubclass(field_type, str)
                and isinstance(value, bytes)
            ):
                jsondict[field_name] = value.decode()

            else:
                jsondict[field_name] = field_type(value)

        return jsondict

    except TypeError as error:
        logger.exception(error)
        raise TypeCastingError(field.name, *error.args) from error


def _set_jsondict_generic_type(
    generic: Any, jsondict: Dict[str, Any], field: str, value: Any
) -> None:
    if 'Union' in str(generic):
        for arg in generic.__args__:
            if issubclass(arg, str) and isinstance(value, bytes):
                jsondict[field] = value.decode()

            elif not isinstance(arg, type(None)):
                try:
                    jsondict[field] = arg(value)
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
