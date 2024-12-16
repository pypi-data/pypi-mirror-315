from nometa.properties import Property
from lxml.etree import _Element



class TextProperty(Property):
    """
    Deal with string values. It reads and keeps all element value as string.
    """
    
    def __init__(self, tname: str) -> None:
        """
        Constructor

        Args:
            tname: tag name in the XML file. Eg: dc:title 

        Raises:
            TypeError
        """
        super().__init__()
        if type(tname) != str:
            raise TypeError("`tname` must be string")
        
        self._tname=tname
        self.value=None
    
    @property
    def value(self) -> str|None:
        """Get the string value of a property"""
        return self._value
    
    @value.setter
    def value(self, val: str|None) -> None:
        if val is None:
            self._value=val
            return
        elif type(val) != str:
            val=str(val)
        
        self._value=val.strip()
    
    @staticmethod
    def from_element(tname: str, elem: _Element) -> Property:
        super(TextProperty, TextProperty).from_element(tname, elem)
        prop=TextProperty(tname)
        node: _Element=prop._find_node(elem)
        prop.value=node.text if node is not None else None
        return prop
    
    def _set_node_value(self, node: _Element) -> None:
        super()._set_node_value(node)
        node.text=self._value # type: ignore
