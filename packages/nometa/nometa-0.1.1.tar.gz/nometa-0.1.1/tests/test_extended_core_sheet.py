from nometa.properties.text import TextProperty
from typing import cast
from pytest import fixture
from nometa import *

@fixture
def bxml() -> bytes:
    return bytes(
    """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <cp:coreProperties
        xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
        xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/"
        xmlns:dcmitype="http://purl.org/dc/dcmitype/"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <dc:title>Insumos</dc:title>
        <dc:subject>Insumos hospitalares restantes</dc:subject>
        <dc:creator>Silverlayer Employee</dc:creator>
        <dc:unreal>Anything</dc:unreal>
        <dc:description>mocked xml</dc:description>
        <cp:lastModifiedBy>Chuck Norris</cp:lastModifiedBy>
        <cp:revision>2</cp:revision>
        <dcterms:created xsi:type="dcterms:W3CDTF">2013-12-15T10:40:00Z</dcterms:created>
        <dcterms:modified xsi:type="dcterms:W3CDTF">2024-09-06T23:10:02Z</dcterms:modified>
        <cp:lastPrinted>2024-12-12T23:10:02Z</cp:lastPrinted>
        <cp:category>Controle</cp:category>
    </cp:coreProperties>""","utf8")


class UnrealCore(Core):
    def __init__(self, raw) -> None:
        super().__init__(raw)
        self._unreal=TextProperty.from_element("dc:unreal", self._xml_root)

    def to_element(self) -> None:
        super().to_element()
        self._unreal.to_element(self._xml_root)

    @property
    def unreal(self) -> str|None:
        return self._unreal.value
    
    @unreal.setter
    def unreal(self, val: str) -> None:
        self._unreal.value=val
    

def test_extended_sheet_with_new_property(bxml) -> None:
    prop=UnrealCore(bxml)
    assert prop.unreal == "Anything" and prop.category == "Controle"

def test_open_document_with_unreal_class() -> None:
    doc=Document("tests/resource/test.xlsx",UnrealCore,App)
    ucore=cast(UnrealCore, doc.core)
    assert ucore.unreal is None and ucore.modified.year == 2024

def test_save_doc_with_unreal_prop() -> None:
    doc=Document("tests/resource/test.xlsx",UnrealCore,App)
    ucore=cast(UnrealCore, doc.core)
    ucore.unreal="paradise"
    doc.save("tests/resource/test20.xlsx")