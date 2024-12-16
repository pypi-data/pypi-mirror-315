from collections.abc import Mapping
from typing import Final, Literal, TypeAlias
from typing_extensions import LiteralString

__all__ = ["ConstantWarning", "find", "physical_constants", "precision", "unit", "value"]

_Unit: TypeAlias = Literal[
    "",
    "(GeV/c^2)^-2",
    "A",
    "A J^-1",
    "C",
    "C kg^-1",
    "C m",
    "C m^-3",
    "C m^2",
    "C mol^-1",
    "C^2 m^2 J^-1",
    "C^3 m^3 J^-2",
    "C^4 m^4 J^-3",
    "C_90 mol^-1",
    "E_h",
    "F",
    "F m^-1",
    "GeV",
    "GeV^-2",
    "H",
    "Hz",
    "Hz K^-1",
    "Hz T^-1",
    "Hz V^-1",
    "J",
    "J Hz^-1",
    "J Hz^-1 mol^-1",
    "J K^-1",
    "J T^-1",
    "J T^-2",
    "J m mol^-1",
    "J mol^-1 K^-1",
    "J s",
    "K",
    "K T^-1",
    "MHz T^-1",
    "MeV",
    "MeV fm",
    "MeV/c",
    "N",
    "N A^-2",
    "Pa",
    "S",
    "T",
    "V",
    "V m^-1",
    "V m^-2",
    "W",
    "W m^-2 K^-4",
    "W m^2",
    "W m^2 sr^-1",
    "Wb",
    "eV",
    "eV Hz^-1",
    "eV K^-1",
    "eV T^-1",
    "eV s",
    "kg",
    "kg m s^-1",
    "kg mol^-1",
    "lm W^-1",
    "m",
    "m K",
    "m s^-1",
    "m s^-2",
    "m^-1",
    "m^-1 K^-1",
    "m^-1 T^-1",
    "m^-3",
    "m^2",
    "m^2 s^-1",
    "m^3 kg^-1 s^-2",
    "m^3 mol^-1",
    "mol^-1",
    "ohm",
    "s",
    "s^-1 T^-1",
    "u",
]
_Constant: TypeAlias = tuple[float, _Unit, float]
_Constants: TypeAlias = Mapping[str, _Constant]

# public

physical_constants: Final[_Constants]

class ConstantWarning(DeprecationWarning): ...

def find(sub: str | None = ..., disp: bool = ...) -> list[LiteralString] | None: ...
def value(key: str) -> float: ...
def unit(key: str) -> _Unit: ...
def precision(key: str) -> float: ...

# private

txt2002: Final[str] = ...
txt2006: Final[str] = ...
txt2010: Final[str] = ...
txt2014: Final[str] = ...
txt2018: Final[str] = ...

exact_values: Final[_Constants] = ...
c: Final = 299792458.0
mu0: Final = 1.25663706212e-06
epsilon0: Final = 8.8541878128e-12
k: Final = "electric constant"

def parse_constants_2002to2014(d: str) -> _Constants: ...
def parse_constants_2018toXXXX(d: str) -> _Constants: ...
