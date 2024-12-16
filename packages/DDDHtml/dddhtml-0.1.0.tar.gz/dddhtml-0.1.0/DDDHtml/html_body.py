from __future__ import annotations
from .html_element import HTML_Element

class HTML_Body(HTML_Element):
    """
    A Html Body main body of html doc
    """
    
    def __init__(self: type[HTML_Header]) -> None:
        super().__init__("body")