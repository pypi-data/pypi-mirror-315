from __future__ import annotations
from .html_element import HTML_Element
from .html_header import HTML_Header
from .html_body import HTML_Body

class HTML_Document(HTML_Element):
    """
    A Html Document to add Elements to
    
    Args:
        tile - the name of the html page
    """
    
    def __init__(self: type[HTML_Document], title: str) -> None:
        self.__body = HTML_Body()
        super().__init__("html")
        super().html_add_child(HTML_Header(title))
        super().html_add_child(self.__body)
        
    def html_add_child(self: type[HTML_Document], child: type[HTML_Element] | str):
        """
        Add a child html element to the document body
        
        Args:
           child - the child element to add
        """
        self.__body.html_add_child(child)
        
    def html_as_str(self: type[HTML_Document]):
        """
        Get the html document as a string
        """
        return "\n".join(self.html_generate_lines())
        
    
        