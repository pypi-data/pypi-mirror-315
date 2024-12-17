import dearpygui.dearpygui as dpg
from dearpygui.dearpygui import internal_dpg as idpg
from pathlib import Path
# > Typing
from typing_extensions import (
    Any, List, Tuple,
    Iterable,
    Union, Optional,
)
# > Local Imports
from .. import (
    types as dpgmtypes,
)

# ^ Font Class

class Font:
    def __init__(
        self,
        name: str,
        filepath: dpgmtypes.FilePathType,
        size: int,
        *,
        label: Optional[str]=None,
        user_data: Optional[Any]=None,
        use_internal_label: bool=True,
        tag: Optional[dpgmtypes.Tag]=None,
        pixel_snapH: bool=False,
        parent: Optional[dpgmtypes.Tag]=None,
    ) -> None:
        """Creating and adding a font.
        
        ### Args:
            - name (str): The key that will be accessed via Font (font manager).
            - filepath (FilePathType): The path to the file.
            - size (int): Font size.
        
        ### Args DearPyGUI:
            - label (Optional[str], optional): The name in DearPyGUI. `Defaults to None`.
            - user_data (Optional[Any], optional): User data for callbacks. `Defaults to None`.
            - use_internal_label (bool, optional): Use generated internal label instead of user specified (appends ### uuid). `Defaults to True`.
            - tag (Optional[Tag], optional): Unique id used to programmatically refer to the item. If label is unused this will be the label. `Defaults to None`.
            - pixel_snapH (bool, optional): Align every glyph to pixel boundary. Useful e.g. if you are merging a non-pixel aligned font with the default font, or rendering text piece-by-piece (e.g. for coloring). `Defaults to False`.
            - parent (Optional[Tag], optional): Parent to add this item to. `Defaults to None`.
        """
        self.__name = name
        self.__filepath = str(Path(filepath).resolve())
        self.__size = size
        self.__label = label
        self.__user_data = user_data
        self.__use_internal_label = use_internal_label
        self.__tag = tag or 0
        self.__pixel_snapH = pixel_snapH
        self.__parent = parent or idpg.mvReservedUUID_0
        self.__range_hints: List[dpgmtypes.FontRangeHint] = []
        self.__chars: List[dpgmtypes.FontChar] = []
        self.__chars_ranges: List[dpgmtypes.FontCharRange] = []
        self.__registred = False
    
    # ^ Dunder Methods
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}(filepath={self.__filepath!r}, size={self.__size!r})'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    # ^ Properties
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def filepath(self) -> str:
        return self.__filepath
    
    @property
    def size(self) -> int:
        return self.__size
    
    @property
    def registred(self) -> bool:
        return self.__registred
    
    @property
    def tag(self) -> dpgmtypes.Tag:
        return self.__tag
    
    # ^ Methods
    
    def add_range_hints(self, *hints: dpgmtypes.FontRangeHint) -> None:
        if not self.__registred:
            allowed_hints = list(dpgmtypes.FONT_RANGE_HINT.keys())
            for hint in hints:
                if (hint in allowed_hints) and (hint not in self.__range_hints):
                    self.__range_hints.append(hint)
    
    def add_chars_range(self, __start: int, __stop: int) -> None:
        if not self.__registred:
            assert isinstance(__start, int) and isinstance(__stop, int)
            self.__chars_ranges.append((__start, __stop))
    
    def add_chars(self, *chars: dpgmtypes.FontChar) -> None:
        if not self.__registred:
            assert all({isinstance(char, int) for char in chars})
            self.__chars.extend(set(chars))
    
    def add_any_char_ranges(self,
        chorg: Iterable[Union[dpgmtypes.FontChar, dpgmtypes.FontCharRange, dpgmtypes.FontRangeHint]],
    ) -> None:
        if not self.__registred:
            for cr in chorg:
                if isinstance(cr, int):
                    self.add_chars(cr)
                elif isinstance(cr, tuple):
                    assert len(cr) == 2
                    self.add_chars_range(cr[0], cr[1])
                elif isinstance(cr, dpgmtypes.FontRangeHint):
                    self.add_range_hints(cr)
    
    def registring(self) -> None:
        if not self.__registred:
            with dpg.font_registry():
                with dpg.font(
                    self.__filepath,
                    self.__size,
                    label=self.__label,
                    user_data=self.__user_data,
                    use_internal_label=self.__use_internal_label,
                    tag=self.__tag,
                    pixel_snap=self.__pixel_snapH,
                    parent=self.__parent
                ) as font_tag:
                    for char_range_hint in self.__range_hints:
                        dpg.add_font_range_hint(char_range_hint)
                    for char_range in self.__chars_ranges:
                        dpg.add_font_range(char_range[0], char_range[1])
                    if len(self.__chars) > 0:
                        dpg.add_font_chars(self.__chars)
            self.__tag = font_tag