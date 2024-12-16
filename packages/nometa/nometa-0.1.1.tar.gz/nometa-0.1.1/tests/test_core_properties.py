from nometa.properties.text import TextProperty
from nometa.properties.numeric import NumericProperty
from nometa.properties.datetime import DatetimeProperty
from nometa.properties.boolean import BooleanProperty
from datetime import datetime
from lxml import etree
from pytest import fixture, mark, raises

XML="""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties
    xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
    xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/"
    xmlns:dcmitype="http://purl.org/dc/dcmitype/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <dc:title></dc:title>
    <dc:subject></dc:subject>
    <dc:creator>Silverlayer Employee</dc:creator>
    <dc:description>mocked xml</dc:description>
    <cp:lastModifiedBy>Chuck Norris</cp:lastModifiedBy>
    <cp:revision>2</cp:revision>
    <dcterms:created xsi:type="dcterms:W3CDTF">2013-12-15T10:40:00Z</dcterms:created>
    <dcterms:modified xsi:type="dcterms:W3CDTF">2024-09-06T23:10:02Z</dcterms:modified>
    <cp:category></cp:category>
</cp:coreProperties>"""

@fixture
def xml_root() -> etree._Element:
    bxml=bytes(XML,"utf8")
    parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
    parser.set_element_class_lookup(etree.ElementNamespaceClassLookup())
    return etree.fromstring(bxml, parser)


def test_wrong_initialization():
    check=[True,True,True,True,True]
    
    try: TextProperty(None); check[1]=False
    except TypeError: pass
    
    try: TextProperty(123); check[2]=False
    except TypeError: pass

    try: NumericProperty(None); check[3]=False
    except TypeError: pass

    try: DatetimeProperty(None); check[4]=False
    except TypeError: pass

    assert not False in check

def test_set_none_to_numeric_property():
    t=NumericProperty("cp:version")
    t.value=None
    assert t.value == None

def test_set_none_to_datetime_property():
    t=DatetimeProperty("dcterms:created")
    t.value=None
    assert t.value == None

def test_set_invalid_to_numeric_property():
    with raises(TypeError):
        t=NumericProperty("cp:version")
        t.value="23.4"

def test_set_invalid_to_datetime_property():
    with raises(TypeError):
        t=DatetimeProperty("dcterms:modified")
        t.value="2023-09-25T10:05:22"

def test_initial_integer_value(xml_root):
    t=NumericProperty.from_element("cp:revision", xml_root)
    assert t.value == int(2)

def test_initial_datetime_value(xml_root):
    created=datetime.strptime("2013-12-15T10:40:00Z","%Y-%m-%dT%H:%M:%SZ")
    modified=datetime.strptime("2024-09-06T23:10:02Z", "%Y-%m-%dT%H:%M:%SZ")
    c=DatetimeProperty.from_element("dcterms:created", xml_root)
    m=DatetimeProperty.from_element("dcterms:modified", xml_root)
    assert c.value == created and m.value == modified

def test_change_integer_value(xml_root):
    t=NumericProperty.from_element("cp:version", xml_root)
    t.value=1.34
    t.to_element(xml_root)
    u=NumericProperty.from_element("cp:version", xml_root)
    assert type(u.value) == float and u.value == 1.34

def test_change_datetime_value(xml_root):
    expected=datetime.strptime("2024-11-22T23:00:07Z","%Y-%m-%dT%H:%M:%SZ")
    t=DatetimeProperty.from_element("dcterms:modified", xml_root)
    t.value=expected
    t.to_element(xml_root)
    u=DatetimeProperty.from_element("dcterms:modified", xml_root)
    assert u.value == expected

def test_load_none_to_numeric_property(xml_root):
    t=NumericProperty.from_element("cp:category", xml_root)
    assert t.value == None

def test_load_none_to_datetime_property(xml_root):
    t=DatetimeProperty.from_element("cp:category", xml_root)
    assert t.value == None

def test_load_none_to_boolean_property(xml_root):
    t=BooleanProperty.from_element("cp:category", xml_root)
    assert t.value == False

def test_load_none_to_text_property(xml_root):
    t=TextProperty.from_element("cp:category", xml_root)
    assert t.value == None

@mark.parametrize("tname,expected",[
    ("dc:title",None), 
    ("dc:subject",None),
    ("cp:category",None),
    ("dc:creator","Silverlayer Employee"),
    ("dc:description","mocked xml"),
    ("cp:lastModifiedBy","Chuck Norris"),
    ("cp:revision",'2')
])
def test_initial_value(tname, expected, xml_root):
    t=TextProperty.from_element(tname, xml_root)
    if expected is None:
        assert t.value is expected
    else:
        assert t.value == expected


@mark.parametrize("tname",["dc:title", "dc:subject", "dc:creator", "dc:description", "cp:lastModifiedBy", "cp:category"])
def test_change_value(xml_root, tname):
    t=TextProperty.from_element(tname, xml_root)
    t.value=" 1984  "
    t.to_element(xml_root)
    u=TextProperty.from_element(tname, xml_root)
    assert u.value == "1984"

@mark.parametrize("tname",["dc:title", "dc:subject", "dc:creator", "dc:description", "cp:lastModifiedBy", "cp:category"])
def test_change_value_not_string(xml_root, tname):
    t=TextProperty.from_element(tname, xml_root)
    t.value=133
    t.to_element(xml_root)
    u=TextProperty.from_element(tname, xml_root)
    assert type(u.value) == str and u.value == "133"

def test_append_new_element(xml_root):
    expected="research, finance"
    new_prop=TextProperty("cp:keywords")
    new_prop.value=expected
    new_prop.to_element(xml_root)
    read_prop=TextProperty.from_element("cp:keywords",xml_root)
    assert read_prop.value == expected
