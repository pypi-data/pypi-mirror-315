from __future__ import annotations
from collections.abc import Iterator

class HTML_Element:
    """
    Any HTML_Element can inherit from this class and bee added to the html tree
    
    Args:
        html_tag_name - the name of the html tag
    """
    def __init__(self: type[HTML_Element], html_tag_name: str) -> None:
        self.__html_tag_name:   str  = html_tag_name
        self.__html_properties: dict = {}
        self.__html_style:      dict = {}
        self.__html_children:   list = []
        
    
    def html_add_prop(self: type[HTML_Element], prop_name: str, prop_value: str) -> None:
        """
        Add a property to the html tag
        
        Args:
            prop_name  - the name of the property to add
            prop_value - the value of the property to add
        """
        self.__html_properties[prop_name] = prop_value
        
    def html_add_style(self: type[HTML_Element], style_name: str, style_value: str) -> None:
        """
        Add a property to the html tag
        
        Args:
            style_name  - the name of the style to add
            style_value - the value of the style to add
        """
        self.__html_style[style_name] = style_value
        
    def html_add_child(self: type[HTML_Element], child: type[HTML_Element] | str):
        """
        Add a child html element to this html element
        note you can add a raw string as a child too
        
        Args:
           child - the child element to add
        """
        self.__html_children.append(child)
        
    def __tup_lam(self, func):
        """
        pull tuple into multiple args for lambda
        """
        return lambda args: func(*args)
        
    def __html_generate_style(self: type[HTML_Element]) -> str:
        """
        Generate the style property string
        
        Returns:
            style prop value string
        """
        styles = self.__html_style.items()
        styles = map(self.__tup_lam(lambda name, style: (name.strip(), style.strip())), styles)
        styles = filter(self.__tup_lam(lambda _, style : len(style.strip()) > 0), styles)
        styles = map(self.__tup_lam(lambda name, style: f"{name}: {style};"), styles)
        return "".join(styles)
        
    def __html_generate_props(self: type[HTML_Element]) -> str:
        """
        Generate the properties string for the html tag
        
        Returns:
            properties html string
        """
        self.__html_properties["style"] = self.__html_generate_style()
        props = self.__html_properties.items()
        props = map(self.__tup_lam(lambda name, prop: (name.strip(), prop.strip())), props)
        props = filter(self.__tup_lam(lambda _, prop : len(prop.strip()) > 0), props)
        props = map(self.__tup_lam(lambda name, prop: f'{name}="{prop}",'), props)
        return " ".join(props)
        
    def __html_generate_open_tag(self: type[HTML_Element]) -> str:
        """
        Generate the opening tag for this html element
        
        Returns:
            html opening tag string
        """
        content=f"{self.__html_tag_name} {self.__html_generate_props()}"
        return f"<{content.strip()}>"
        
    def __html_generate_close_tag(self: type[HTML_Element]) -> str:
        """
        Generate the closing tag for this html element
        
        Returns:
            html closing tag string
        """
        return f"</{self.__html_tag_name}>"
        
    def __html_generate_child_lines(self: type[HTML_Element], child: type[HTML_Element] | str) -> Iterator[str]:
        """
        Generate html for a child element
        
        Args:
            child - the child to get lines for
        Returns:
            iterator of all lines for child
        """
        if isinstance(child, HTML_Element):
            for child_line in child.html_generate_lines():
                yield from self.__html_generate_child_lines(child_line)
        else:
            yield f"    {child}"
        
    def html_generate_lines(self: type[HTML_Element]) -> Iterator[str]:
        """
        Generate all needed lines for this element as a generator
        
        Returns:
            iterator of all lines for this html element
        """
        yield self.__html_generate_open_tag()
        if len(self.__html_children) > 0:
            for child in self.__html_children:
                yield from self.__html_generate_child_lines(child)
            yield self.__html_generate_close_tag()
        