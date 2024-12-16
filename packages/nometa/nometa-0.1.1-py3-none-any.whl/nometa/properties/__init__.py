"""
This subpackage deal with XML tags of diverse data type.
It contains classes to handle tags whose data type are: boolean, datetime, numeric and text.
"""

from abc import ABC, abstractmethod
from lxml import etree
from typing import Any


class Property(ABC):
    """
    Abstract class for dealing with xml nodes/tags
    """
    def __init__(self) -> None:
        self._tname: str = ''
        self._value: Any = None

    @property
    def tname(self) -> str:
        """Get the official tag name of this property"""
        return self._tname

    @staticmethod
    @abstractmethod
    def from_element(tname: str, elem: etree._Element) -> "Property":
        """
        Read an `_Element` and returns the corresponding property object

        Args:
            tname (str): the official tag name in XML documents
            elem (etree._Element): a valid `etree._Element` instance

        Raises:
            TypeError

        Returns:
            Property: an instance of `Property` or its subclasses
        """
        if type(tname) != str:
            raise TypeError("`tname` must be string")
        
        if type(elem) != etree._Element:
            raise TypeError("`elem` must be an instance of `etree._Element`")

    
    def __append(self, elem: etree._Element) -> None:
        if ':' in self._tname:
            xmlns, tag=self._tname.split(':')
            new_node=elem.makeelement(etree.QName(elem.nsmap[xmlns], tag)) # type: ignore
        else:
            new_node=elem.makeelement(self._tname)  # type: ignore
        
        self._set_node_value(new_node)
        elem.append(new_node)

    def __update(self, elem: etree._Element) -> None:
        node=self._find_node(elem)
        self._set_node_value(node)

    def _find_node(self, elem: etree._Element) -> etree._Element:
        node: etree._Element = elem.find(self._tname, namespaces=elem.nsmap)
        if node is None:
            try:
                node=elem.find(self._tname)
            except SyntaxError:
                node=None

        return node

    @abstractmethod
    def _set_node_value(self, node: etree._Element) -> None:
        """
        Hook method to set the tag's value

        Args:
            node (etree._Element): the node corresponding this XML tag
        """
        pass

    def to_element(self, elem: etree._Element) -> None:
        """
        Write the value of this property to `elem` parameter

        Args:
            elem (etree._Element): the target xml tree node

        Raises:
            TypeError
        """
        if type(elem) != etree._Element:
            raise TypeError("`elem` must be an instance of `etree._Element`")
        
        node=elem.find(self._tname, namespaces=elem.nsmap)
        if node is not None:
            self.__update(elem)
        elif node is None and self._value is not None:
            self.__append(elem)
            



__all__ = ["Property"]