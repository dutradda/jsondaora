from typing import Any, Dict


class DataclassJsonError(Exception):
    ...


class DeserializationError(DataclassJsonError):
    @property
    def message(self) -> str:
        return ' '.join(self.dict)

    @property
    def dict(self) -> Dict[str, Any]:
        type_name = (
            self.args[0].type.__name__
            if hasattr(self.args[0].type, '__name__')
            else str(self.args[0].type)
        )

        message_args = {'field': self.args[0].name, 'type': type_name}

        if len(self.args) > 1:
            message_args['invalid_value'] = str(self.args[1])

        if len(self.args) > 2:
            message_args['error'] = type(self.args[2]).__name__

        return dict(**message_args)
