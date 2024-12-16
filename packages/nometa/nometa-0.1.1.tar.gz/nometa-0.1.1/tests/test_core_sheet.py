from nometa.sheet import Core
from datetime import datetime
from pytest import fixture, raises, mark

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
        <dc:description>mocked xml</dc:description>
        <cp:lastModifiedBy>Chuck Norris</cp:lastModifiedBy>
        <cp:revision>2</cp:revision>
        <dcterms:created xsi:type="dcterms:W3CDTF">2013-12-15T10:40:00Z</dcterms:created>
        <dcterms:modified xsi:type="dcterms:W3CDTF">2024-09-06T23:10:02Z</dcterms:modified>
        <cp:lastPrinted>2024-12-12T23:10:02Z</cp:lastPrinted>
        <cp:category>Controle</cp:category>
    </cp:coreProperties>""","utf8")

def test_init_core_sheet(bxml):
    osheet=Core(bxml)
    assert osheet is not None

@mark.parametrize("prop,expec",[
    ("title","Insumos"),
    ("subject","Insumos hospitalares restantes"),
    ("creator","Silverlayer Employee"),
    ("description","mocked xml"),
    ("last_modified_by","Chuck Norris"),
    ("revision",2),
    ("created",datetime.strptime("2013-12-15T10:40:00Z","%Y-%m-%dT%H:%M:%SZ")),
    ("modified",datetime.strptime("2024-09-06T23:10:02Z","%Y-%m-%dT%H:%M:%SZ")),
    ("last_printed", datetime.strptime("2024-12-12T23:10:02Z","%Y-%m-%dT%H:%M:%SZ")),
    ("category","Controle")
])
def test_read_props(bxml, prop, expec):
    osheet=Core(bxml)
    assert eval("osheet."+prop) == expec

def test_set_invalid_revision(bxml):
    osheet=Core(bxml)
    with raises(TypeError):
        osheet.revision="1.43.2"

def test_set_invalid_created(bxml):
    osheet=Core(bxml)
    with raises(TypeError):
        osheet.created="undefined"

def test_set_invalid_modified(bxml):
    osheet=Core(bxml)
    with raises(TypeError):
        osheet.modified="11/09/2001T13:01:00Z"

def test_change_props(bxml):
    osheet=Core(bxml)
    osheet.title="My wonderful world"
    osheet.subject="nothing"
    osheet.creator=None
    osheet.description=None
    osheet.last_modified_by="popeye"
    osheet.revision=77
    osheet.created=datetime.strptime("1889-05-29T20:55:43Z","%Y-%m-%dT%H:%M:%SZ")
    osheet.modified=datetime.strptime("2023-12-31T09:25:50Z","%Y-%m-%dT%H:%M:%SZ")
    osheet.category=None
    osheet.to_element()
    new_sheet=Core(osheet.pack())

    assert new_sheet.title == osheet.title and new_sheet.subject == osheet.subject and new_sheet.last_printed == osheet.last_printed \
    and new_sheet.creator == osheet.creator and new_sheet.description == osheet.description and new_sheet.revision == osheet.revision \
    and new_sheet.last_modified_by == osheet.last_modified_by and new_sheet.category == osheet.category and new_sheet.created == osheet.created