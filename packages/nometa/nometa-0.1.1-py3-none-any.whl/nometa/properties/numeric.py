from nometa.properties import Property
from lxml.etree import _Element


class NumericProperty(Property):
    """
    Deal with numeric (integer or float) values. It must be used only in float or integer xml elements.
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
    def value(self) -> int|float|None:
        """Get the value of this property"""
        return self._value
    
    @value.setter
    def value(self, val: int|float|None) -> None:
        if val is None: pass
        elif type(val) != int and type(val) != float:
            raise TypeError("type of `value` must be int or float")
        
        self._value=val
    
    @staticmethod
    def from_element(tname: str, elem: _Element) -> Property:
        super(NumericProperty, NumericProperty).from_element(tname, elem)
        prop=NumericProperty(tname)
        node=prop._find_node(elem)
        try:
            prop.value=int(node.text)
        except (TypeError, AttributeError):
            prop.value=None
        except ValueError:
            try:
                prop.value=float(node.text)
            except TypeError:
                prop.value=None
            except ValueError:
                raise ValueError("The tag value isn't numeric")
        
        return prop
    
    
    def _set_node_value(self, node: _Element) -> None:
        super()._set_node_value(node)
        node.text=str(self._value) # type: ignore
        