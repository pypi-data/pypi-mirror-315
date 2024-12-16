from __future__ import annotations
from .html_element import HTML_Element

class HTML_Title(HTML_Element):
    """
    A Html Title to set header title
    
    Args:
        tile - the name of the html page
    """
    
    def __init__(self: type[HTML_Title], title: str) -> None:
        super().__init__("title")
        self.html_add_child(title)
        