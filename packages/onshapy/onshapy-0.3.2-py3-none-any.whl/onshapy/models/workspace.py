from .modelbase import ModelBase


class Workspace(ModelBase):
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
    def parent(self) -> str:
        return self._getValueOfType("parent", str)

    @property
    def link(self) -> str:
        return self._getValueOfType("href", str)
