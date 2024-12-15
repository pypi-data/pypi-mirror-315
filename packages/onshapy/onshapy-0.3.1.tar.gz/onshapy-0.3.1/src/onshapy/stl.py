from __future__ import annotations

from enum import StrEnum
from typing import Any, Callable, Iterable, SupportsIndex


class StlMode(StrEnum):
    BINARY = "binary"
    ASCII = "ascii"
    DEFAULT = BINARY


class StlUnit(StrEnum):
    METER = "meter"
    DEFAULT = METER


class StlResolution(StrEnum):
    COARSE = "coarse"
    MEDIUM = "medium"
    FINE = "fine"
    CUSTOM = "custom"
    DEFAULT = MEDIUM


class MonitoredList(list[str]):
    _callback: Callable[[list[str]], None]

    def __init__(
        self,
        iterable: Iterable[str],
        callback: Callable[[list[str]], None],
    ) -> None:
        self._callback = callback
        super().__init__(iterable)

    def append(self, object: str) -> None:
        super().append(object)
        self._callback(self)

    def extend(self, iterable: Iterable[str]) -> None:
        super().extend(iterable)
        self._callback(self)

    def remove(self, value: str) -> None:
        super().remove(value)
        self._callback(self)

    def reverse(self) -> None:
        super().reverse()
        self._callback(self)

    def insert(self, index: SupportsIndex, object: str) -> None:
        super().insert(index, object)
        self._callback(self)

    def pop(self, index: SupportsIndex = -1) -> str:
        result = super().pop(index)
        self._callback(self)
        return result

    def clear(self) -> None:
        super().clear()
        self._callback(self)

    def __setitem__(self, *args, **kwargs) -> None:  # type: ignore
        super().__setitem__(*args, **kwargs)  # type: ignore
        self._callback(self)

    def __add__(self, *args, **kwargs) -> None:  # type: ignore
        super().__add__(*args, **kwargs)  # type: ignore
        self._callback(self)


class STLExportSettings:
    _data: dict[str, Any]
    _tempList: list[str]

    def __init__(self, data: dict[str, Any] | STLExportSettings | None = None) -> None:
        if isinstance(data, STLExportSettings):
            self._data = data._data
        else:
            self._data = {}
            self._data.update(_SETTINGS_BASIC)
            self._data.update(self._resolutionSettings(StlResolution.DEFAULT))
            if data:
                self._data.update(data)

    @property
    def name(self) -> str:
        return self._data["destinationName"]

    @name.setter
    def name(self, value: str) -> None:
        self._data["destinationName"] = value

    @property
    def mode(self) -> StlMode:
        return StlMode(self._data["mode"])

    @mode.setter
    def mode(self, value: StlMode) -> None:
        self._data["mode"] = value

    @property
    def scale(self) -> float:
        return self._data["scale"]

    @scale.setter
    def scale(self, value: float) -> None:
        self._data["scale"] = value

    @property
    def units(self) -> StlUnit:
        return StlUnit(self._data["units"])

    @units.setter
    def units(self, value: StlUnit) -> None:
        self._data["units"] = value

    @property
    def yAsUp(self) -> bool:
        return self._data["useYAxisAsUp"]

    @yAsUp.setter
    def yAsUp(self, value: bool) -> None:
        self._data["useYAxisAsUp"] = value

    @property
    def parts(self) -> list[str]:
        value: str = self._data["partIds"]
        parts = [v for v in value.split(",") if len(v) > 0]
        return MonitoredList(parts, self._updateParts)

    @parts.setter
    def parts(self, value: list[str]) -> None:
        self._data["partIds"] = ",".join(value)

    def _updateParts(self, list: list[str]) -> None:
        self.parts = list

    @property
    def excludeHidden(self) -> bool:
        return self._data["excludeHiddenEntities"]

    @excludeHidden.setter
    def excludeHidden(self, value: bool) -> None:
        self._data["excludeHiddenEntities"] = value

    @property
    def angleTolerance(self) -> float:
        return self._data["angleTolerance"]

    @angleTolerance.setter
    def angleTolerance(self, value: float) -> None:
        current = self.angleTolerance
        if value != current:
            self._data["resolution"] = StlResolution.CUSTOM
        self._data["angleTolerance"] = value

    @property
    def chordTolerance(self) -> float:
        return self._data["chordTolerance"]

    @chordTolerance.setter
    def chordTolerance(self, value: float) -> None:
        current = self.chordTolerance
        if value != current:
            self._data["resolution"] = StlResolution.CUSTOM
        self._data["chordTolerance"] = value

    @property
    def minFacetWidth(self) -> float:
        return self._data["minFacetWidth"]

    @minFacetWidth.setter
    def minFacetWidth(self, value: float) -> None:
        current = self.minFacetWidth
        if value != current:
            self._data["resolution"] = StlResolution.CUSTOM
        self._data["minFacetWidth"] = value

    @property
    def resolution(self) -> StlResolution:
        return self._data["resolution"]

    @resolution.setter
    def resolution(self, value: StlResolution) -> None:
        self._data["resolution"] = value
        settings = self._resolutionSettings(value)
        self._data.update(settings)

    def _resolutionSettings(self, resolution: StlResolution) -> dict[str, Any]:
        if resolution == StlResolution.CUSTOM:
            settings = self._resolutionSettings(StlResolution.MEDIUM)
        else:
            allSettings = [
                s for s in _SETTINGS_QUALITY if s["resolution"] == resolution
            ]
            if len(allSettings) == 0:
                raise Exception("how?")
            settings = allSettings[0]

        settings["resolution"] = resolution
        return settings

    def dict(self) -> dict[str, Any]:
        return self._data


_SETTINGS_BASIC: dict[str, Any] = {
    "format": "STL",
    "destinationName": "EXPORT",
    "mode": StlMode.DEFAULT,
    "scale": 1.0,
    "units": StlUnit.DEFAULT,
    "grouping": True,
    "useYAxisAsUp": False,
    "triggerAutoDownload": True,
    "storeInDocument": False,
    "configuration": None,
    "partIds": "",
    "excludeHiddenEntities": True,
}

_SETTINGS_QUALITY = [
    {
        "resolution": StlResolution.FINE,
        "angleTolerance": 0.04363323129985824,
        "chordTolerance": 0.00006,
        "minFacetWidth": 0.0000254,
    },
    {
        "resolution": StlResolution.MEDIUM,
        "angleTolerance": 0.1090830782496456,
        "chordTolerance": 0.00012,
        "minFacetWidth": 0.000254,
    },
    {
        "resolution": StlResolution.COARSE,
        "angleTolerance": 0.2181661564992912,
        "chordTolerance": 0.00024,
        "minFacetWidth": 0.000635,
    },
]
