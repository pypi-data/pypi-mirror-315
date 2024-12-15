from .modelbase import ModelBase


class Part(ModelBase):
    @property
    def id(self) -> str:
        return self._getValueOfType("partId", str)

    @id.setter
    def id(self, value: str) -> None:
        self._setValue("partId", value)

    @property
    def name(self) -> str:
        return self._getValueOfType("name", str)

    @name.setter
    def name(self, value: str) -> None:
        self._setValue("name", value)

    @property
    def isHidden(self) -> bool:
        return self._getValueOfType("isHidden", bool)

    @property
    def bodyType(self) -> str:
        return self._getValueOfType("bodyType", str)
