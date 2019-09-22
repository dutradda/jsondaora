from typing import Any, Dict


class JSONDaoraError(Exception):
    ...


class DeserializationError(JSONDaoraError):
    @property
    def message(self) -> str:
        return ' '.join([f'{k}={v}' for k, v in self.dict.items()])

    @property
    def dict(self) -> Dict[str, Any]:
        if hasattr(self.args[0], 'type'):
            type_name = (
                self.args[0].type.__name__
                if hasattr(self.args[0].type, '__name__')
                else str(self.args[0].type)
            )
        else:
            type_name = self.args[0]

        message_args = {'type': type_name}

        if hasattr(self.args[0], 'name'):
            message_args['field'] = self.args[0].name

        if len(self.args) > 1:
            message_args['invalid_value'] = self.args[1]

        if len(self.args) > 2:
            message_args['name'] = type(self.args[2]).__name__

        if len(self.args) > 3:
            message_args['cls'] = self.args[3].__name__

        return dict(**message_args)


class ParameterNotFoundError(JSONDaoraError):
    ...
