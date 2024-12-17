import dearpygui.dearpygui as dpg
from os import PathLike
from pathlib import Path, PosixPath, PurePath, PurePosixPath, PureWindowsPath, WindowsPath
from typing_extensions import (
    Dict, Tuple,
    Literal, Union,
    TypeAlias
)

# ! Global Types

FilePathType: TypeAlias = Union[
    str, bytes, int,
    PathLike, PathLike[str], PathLike[bytes],
    Path, PosixPath, PurePath, PurePosixPath, PureWindowsPath, WindowsPath
]

# ! DearPyGUI Types

Tag: TypeAlias = Union[int, str]

# ! DearPyGUI Alias Types

FontChar: TypeAlias = int
FontCharRange: TypeAlias = Tuple[FontChar, FontChar]
FontRangeHint: TypeAlias = Literal[
    'default',
    'japanese',
    'chinese-full', 'chinese-simple', 'chinese-simplified-common',
    'cyrillic',
    'thai',
    'vietnamese'
]

# ! DearPyGUI Types Variables

FONT_RANGE_HINT: Dict[str, int] = {
    'default': dpg.mvFontRangeHint_Default,
    'japanese': dpg.mvFontRangeHint_Japanese,
    'chinese-full': dpg.mvFontRangeHint_Chinese_Full,
    'chinese-simple': dpg.mvFontRangeHint_Chinese_Simplified_Common,
    'chinese-simplified-common': dpg.mvFontRangeHint_Chinese_Simplified_Common,
    'cyrillic': dpg.mvFontRangeHint_Cyrillic,
    'thai': dpg.mvFontRangeHint_Thai,
    'vietnamese': dpg.mvFontRangeHint_Vietnamese
}

# ! Annotations

__all__ = [
    'FilePathType'
]