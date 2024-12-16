from nometa.properties import Property
from datetime import datetime
from lxml.etree import _Element



class DatetimeProperty(Property):
    """
    Deal with UTC-ISO formatted dates. It must be used only with ISO formatted dates, and always writes UTC time.
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
    def value(self) -> datetime|None:
        """Get a `datetime` instance in UTC"""
        return self._value
    
    @value.setter
    def value(self, val: datetime|None) -> None:
        if val is None: pass
        elif not isinstance(val, datetime):
            raise TypeError("`value` must be a valid instance of `datetime`")
        
        self._value=val
    
    @staticmethod
    def from_element(tname: str, elem: _Element) -> Property:
        super(DatetimeProperty, DatetimeProperty).from_element(tname, elem)
        prop=DatetimeProperty(tname)
        node=prop._find_node(elem)
        prop.value=datetime.strptime(node.text,"%Y-%m-%dT%H:%M:%SZ") if (node is not None and node.text is not None) else None
        return prop
    
    def _set_node_value(self, node: _Element) -> None:
        super()._set_node_value(node)
        node.text=self._value.strftime("%Y-%m-%dT%H:%M:%SZ") # type: ignore
        