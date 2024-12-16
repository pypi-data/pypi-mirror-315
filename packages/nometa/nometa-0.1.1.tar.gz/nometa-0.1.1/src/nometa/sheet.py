"""
This module contains the main XML sheets of metadata.
You can extend the App and Core classes in order to add new properties.
"""

from lxml import etree
from typing import cast
from abc import ABC, abstractmethod
from datetime import datetime
from nometa.properties.text import TextProperty
from nometa.properties.boolean import BooleanProperty
from nometa.properties.numeric import NumericProperty
from nometa.properties.datetime import DatetimeProperty


class Sheet(ABC):

    def __init__(self, raw: bytes) -> None:
        parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
        parser.set_element_class_lookup(etree.ElementNamespaceClassLookup())
        self._xml_root=etree.fromstring(raw, parser)

    def pack(self) -> bytes:
        """
        Create the binary representation of `etree._Element`

        Returns:
            bytes: `etree._Element` as bytes
        """
        return etree.tostring(self._xml_root)
    
    @abstractmethod
    def to_element(self) -> None:
        """
        persist changes in this instance to the `etree._Element`
        """
        pass


class App(Sheet):

    def __init__(self, raw: bytes) -> None:
        """
        Create an instance of `App` representing the `docProps/app.xml` sheet.

        Args:
            raw (bytes): the `app.xml` sheet as binary
        """
        super().__init__(raw)
        node=self._xml_root
        self._template: TextProperty = cast(TextProperty, TextProperty.from_element("Template", node))
        self._total_time: NumericProperty = cast(NumericProperty, NumericProperty.from_element("TotalTime", node))
        self._application: TextProperty = cast(TextProperty, TextProperty.from_element("Application", node))
        self._scale_crop: BooleanProperty = cast(BooleanProperty, BooleanProperty.from_element("ScaleCrop", node))
        self._manager: TextProperty = cast(TextProperty, TextProperty.from_element("Manager", node))
        self._company: TextProperty = cast(TextProperty, TextProperty.from_element("Company", node))
        self._app_version: TextProperty = cast(TextProperty, TextProperty.from_element("AppVersion", node))

    def to_element(self) -> None:
        node=self._xml_root
        self._template.to_element(node)
        self._total_time.to_element(node)
        self._application.to_element(node)
        self._scale_crop.to_element(node)
        self._manager.to_element(node)
        self._company.to_element(node)
        self._app_version.to_element(node)

        return node
    
    @property
    def template(self) -> str|None:
        """
        The document's template. It's a read-only property.
        """
        return self._template.value
    
    @property
    def total_time(self) -> int|None:
        """The work time (measured in minutes)."""
        return cast(int, self._total_time.value)
    
    @total_time.setter
    def total_time(self, val: int) -> None:
        if type(val) != int:
            raise TypeError("``val`` must be an integer")
        
        self._total_time.value=val
    
    @property
    def application(self) -> str|None:
        """The description name of application"""
        return self._application.value
    
    @application.setter
    def application(self, val: str) -> None:
        self._application.value=val
    
    @property
    def scale_crop(self) -> bool|None:
        """
        Scale crop.
        
        This element indicates the display mode of the document thumbnail.
        Set this element to TRUE to enable scaling of the document thumbnail to the display. 
        Set this element to FALSE to enable cropping of the document thumbnail to show only sections that fits the display.
        """
        return self._scale_crop.value
    
    @scale_crop.setter
    def scale_crop(self, val: bool) -> None:
        self._scale_crop.value=val
    
    @property
    def manager(self) -> str|None:
        """Manager name"""
        return self._manager.value
    
    @manager.setter
    def manager(self, val: str) -> None:
        self._manager.value=val
    
    @property
    def company(self) -> str|None:
        """Company name"""
        return self._company.value
    
    @company.setter
    def company(self, val: str) -> None:
        self._company.value=val
    
    @property
    def app_version(self) -> str|None:
        """The application version. eg. 14.0000"""
        return self._app_version.value
    
    @app_version.setter
    def app_version(self, val: str) -> None:
        self._app_version.value=val


class Core(Sheet):

    def __init__(self, raw: bytes) -> None:
        """
        Create an instance of `Core` representing the `docProps/core.xml` sheet.

        Args:
            raw (bytes): the `core.xml` sheet as binary
        """
        super().__init__(raw)
        node=self._xml_root
        self._title: TextProperty = cast(TextProperty, TextProperty.from_element("dc:title", node))
        self._subject: TextProperty = cast(TextProperty, TextProperty.from_element("dc:subject", node))
        self._keyword: TextProperty = cast(TextProperty, TextProperty.from_element("cp:keywords", node))
        self._creator: TextProperty = cast(TextProperty, TextProperty.from_element("dc:creator", node))
        self._description: TextProperty = cast(TextProperty, TextProperty.from_element("dc:description", node))
        self._lastmdod: TextProperty = cast(TextProperty, TextProperty.from_element("cp:lastModifiedBy", node))
        self._category: TextProperty = cast(TextProperty, TextProperty.from_element("cp:category",node))
        self._revision: NumericProperty = cast(NumericProperty, NumericProperty.from_element("cp:revision",node))
        self._created: DatetimeProperty = cast(DatetimeProperty, DatetimeProperty.from_element("dcterms:created",node))
        self._modified: DatetimeProperty = cast(DatetimeProperty, DatetimeProperty.from_element("dcterms:modified",node))
        self._contentstat: TextProperty = cast(TextProperty, TextProperty.from_element("cp:contentStatus",node))
        self._version: TextProperty = cast(TextProperty, TextProperty.from_element("cp:version", node))
        self._identifier: TextProperty = cast(TextProperty, TextProperty.from_element("dc:identifier", node))
        self._last_printed: DatetimeProperty = cast(DatetimeProperty, DatetimeProperty.from_element("cp:lastPrinted", node))
        
    def to_element(self) -> None:
        node=self._xml_root
        self._title.to_element(node)
        self._subject.to_element(node)
        self._keyword.to_element(node)
        self._creator.to_element(node)
        self._description.to_element(node)
        self._lastmdod.to_element(node)
        self._category.to_element(node)
        self._revision.to_element(node)
        self._created.to_element(node)
        self._modified.to_element(node)
        self._contentstat.to_element(node)
        self._version.to_element(node)
        self._identifier.to_element(node)
        self._last_printed.to_element(node)

    @property
    def title(self) -> str|None:
        """The title"""
        return self._title.value
    
    @title.setter
    def title(self, val: str) -> None:
        self._title.value=val
    
    @property
    def subject(self) -> str|None:
        """The subject"""
        return self._subject.value
    
    @subject.setter
    def subject(self, val: str) -> None:
        self._subject.value=val
    
    @property
    def keywords(self) -> str|None:
        """
        The keywords.
        
        It is not compliance with CT_Keywords complex type specification.
        It's a simplified implementation that doesn't support multiple languages.
        """
        return self._keyword.value
    
    @keywords.setter
    def keywords(self, val: str) -> None:
        self._keyword.value=val

    @property
    def creator(self) -> str|None:
        """The creator/author"""
        return self._creator.value
    
    @creator.setter
    def creator(self, val: str) -> None:
        self._creator.value=val

    @property
    def description(self) -> str|None:
        """The description"""
        return self._description.value
    
    @description.setter
    def description(self, val: str) -> None:
        self._description.value=val

    @property
    def last_modified_by(self) -> str|None:
        """The last person that modified the document"""
        return self._lastmdod.value
    
    @last_modified_by.setter
    def last_modified_by(self, val: str) -> None:
        self._lastmdod.value=val

    @property
    def category(self) -> str|None:
        """The category"""
        return self._category.value
    
    @category.setter
    def category(self, val: str) -> None:
        self._category.value=val

    @property
    def revision(self) -> int|None:
        """The revision"""
        return cast(int, self._revision.value)
    
    @revision.setter
    def revision(self, val: int) -> None:
        if type(val) != int:
            raise TypeError("``val`` must be integer")
        
        self._revision.value=val

    @property
    def created(self) -> datetime|None:
        """When the document was created"""
        return self._created.value
    
    @created.setter
    def created(self, val: datetime) -> None:
        self._created.value=val

    @property
    def modified(self) -> datetime|None:
        """When the document was modified"""
        return self._modified.value
    
    @modified.setter
    def modified(self, val: datetime) -> None:
        self._modified.value=val

    @property
    def content_status(self) -> str|None:
        """
        The content status, its value should be 'Draft', 'Reviewed' or 'Final'.
        """
        return self._contentstat.value
    
    @content_status.setter
    def content_status(self, val: str) -> None:
        self._contentstat.value=val

    @property
    def version(self) -> str|None:
        """The version"""
        return self._version.value
    
    @version.setter
    def version(self, val: str) -> None:
        self._version.value=val
    
    @property
    def identifier(self) -> str|None:
        """The document's identifier. Only some documents apply it"""
        return self._identifier.value
    
    @identifier.setter
    def identifier(self, val: str) -> None:
        self._identifier.value=val

    @property
    def last_printed(self) -> datetime|None:
        """When the document was printed"""
        return self._last_printed.value
    
    @last_printed.setter
    def last_printed(self, val: datetime) -> None:
        self._last_printed.value=val