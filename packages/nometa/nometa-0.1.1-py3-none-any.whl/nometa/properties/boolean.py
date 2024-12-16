from nometa.properties import Property
from lxml import etree


def _to_bool(val: str) -> bool:
    """
    Convert string to boolean.

    For these string values 'false','no','not','n','0' and '', it returns `False`. For any other value, it returns `True`.
    For any numeric representation >= '1.0', it returns `True`. Otherwise, `False`.
    """
    if not val: return False
    try:
        return not int(float(val))<1
    except ValueError:
        return not val.strip().lower() in ("false","no","not",'n','0','')


class BooleanProperty(Property):
    """
    Deal with boolean values. It can be used with any xml-tag data type, the assignment of value is determined as:

    For these string values 'false','no','not','n','0' and '', it puts `False`. For any other value, it puts `True`.
        
    For any numeric representation >= '1.0', it puts `True`. Otherwise, `False`.
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
        self.value=False
    
    @property
    def value(self) -> bool|None:
        """Get the value of this property"""
        return self._value
    
    @value.setter
    def value(self, val: bool|None) -> None:
        if val is None: pass
        elif type(val) != bool:
            raise TypeError("`value` must be boolean")
        
        self._value=val
        
    @staticmethod
    def from_element(tname: str, elem: etree._Element) -> Property:
        super(BooleanProperty, BooleanProperty).from_element(tname, elem)
        prop=BooleanProperty(tname)
        node=prop._find_node(elem)
        prop.value=_to_bool(node.text) if node is not None else None
        return prop
    
    def _set_node_value(self, node: etree._Element) -> None:
        super()._set_node_value(node)
        node.text="true" if self._value else "false" # type: ignore
        