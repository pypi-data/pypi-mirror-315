from .modelbase import ModelBase


class Document(ModelBase):
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
    def isPublic(self) -> bool:
        return self._getValueOfType("public", bool)

    @property
    def link(self) -> str:
        return self._getValueOfType("href", str)
