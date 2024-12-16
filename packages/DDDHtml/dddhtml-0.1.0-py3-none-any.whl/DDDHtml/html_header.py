from __future__ import annotations
from .html_element import HTML_Element
from .html_title   import HTML_Title

class HTML_Header(HTML_Element):
    """
    A Html Header to Configure html document
    
    Args:
        tile - the name of the html page
    """
    
    def __init__(self: type[HTML_Header], title: str) -> None:
        super().__init__("head")
        self.html_add_child(HTML_Title(title))
        