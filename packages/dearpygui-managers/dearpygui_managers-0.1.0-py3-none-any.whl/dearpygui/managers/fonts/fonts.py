import dearpygui.dearpygui as dpg
# > Typing
from typing_extensions import (
    Dict,
    Iterable,
    Union
)
# > Local Imports
from .font import Font
from .. import (
    types as dpgmtypes,
)

# ^ Fonts Class

class Fonts:
    def __init__(self) -> None:
        self.__fonts: Dict[str, Font] = {}
    
    # ^ Dunder Methods
    
    def __getitem__(self, name: str) -> Font:
        return self.__fonts[name]
    
    def __setitem__(self, name: str, font: Font) -> None:
        self.__fonts[name] = font
    
    # ^ Fonts Manager Methods
    
    def add_font(self,
        name: str,
        filepath: dpgmtypes.FilePathType,
        size: int,
        **kwargs
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
        self[name] = Font(name, filepath, size, **kwargs)
    
    def registring(self) -> None:
        for font in self.__fonts.values():
            font.registring()
    
    def add_any_char_ranges(self,
        name: str,
        chorg: Iterable[Union[dpgmtypes.FontRangeHint, dpgmtypes.FontChar, dpgmtypes.FontCharRange]]
    ) -> None:
        if name in self.__fonts:
            self.__fonts[name].add_any_char_ranges(chorg)
    
    def bind_font(self, name: str) -> None:
        if name in self.__fonts:
            if self.__fonts[name].registred:
                dpg.bind_font(self.__fonts[name].tag)
    
    def bind_item_font(self, name: str, item: dpgmtypes.Tag) -> None:
        if name in self.__fonts:
            if self.__fonts[name].registred:
                dpg.bind_item_font(self.__fonts[name].tag, item)