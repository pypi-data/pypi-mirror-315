from typing import Any


class ModelBase:
    _data: dict[str, Any]

    def __init__(self, data: dict[str, Any] | None = None):
        self._data = data or {}

    def _setValue(self, key: str, value: Any) -> None:
        self._data[key] = value

    def _getValue(self, key: str) -> Any:
        if key not in self._data.keys():
            return None
        return self._data[key]

    def _getValueOfType(self, key: str, _type: type) -> Any:
        value = self._getValue(key)
        if not isinstance(value, _type):
            raise Exception("wrong type")
        return value
