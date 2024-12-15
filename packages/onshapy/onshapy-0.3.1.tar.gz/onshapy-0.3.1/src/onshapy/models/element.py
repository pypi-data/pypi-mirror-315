from typing import Any

from .modelbase import ModelBase


class Element(ModelBase):
    @property
    def id(self) -> str:
        return self._getValueOfType("id", str)

    @id.setter
    def id(self, value: str) -> None:
        self._setValue("id", value)

    @property
    def name(self) -> str:
        return self._getValueOfType("name", str)

    @name.setter
    def name(self, value: str) -> None:
        self._setValue("name", value)

    @property
    def type(self) -> str:
        return self._getValueOfType("elementType", str)


class PartStudio(Element):
    def __init__(self, data: dict[str, Any] | Element | None = None):
        if isinstance(data, Element):
            if not data.type == "PARTSTUDIO":
                raise Exception()
            super().__init__(data._data)
        else:
            super().__init__(data)


class Assembly(Element):
    def __init__(self, data: dict[str, Any] | Element | None = None):
        if isinstance(data, Element):
            if not data.type == "ASSEMBLY":
                raise Exception()
            super().__init__(data._data)
        else:
            super().__init__(data)
