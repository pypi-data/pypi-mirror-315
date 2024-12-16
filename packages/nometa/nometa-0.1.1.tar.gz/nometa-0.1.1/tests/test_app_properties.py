from nometa.properties.text import TextProperty
from nometa.properties.numeric import NumericProperty
from nometa.properties.boolean import BooleanProperty
from lxml import etree
from pytest import fixture, mark, raises

XML=bytes("""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
    xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
    <Template>Normal.dotm</Template>
    <TotalTime>93</TotalTime>
    <Pages>1</Pages>
    <Words>7</Words>
    <Characters>41</Characters>
    <Application>Microsoft Macintosh Word</Application>
    <DocSecurity>0</DocSecurity>
    <Lines>1</Lines>
    <Paragraphs>1</Paragraphs>
    <ScaleCrop>false</ScaleCrop>
    <HeadingPairs>
        <vt:vector size="2" baseType="variant">
            <vt:variant>
                <vt:lpstr>Title</vt:lpstr>
            </vt:variant>
            <vt:variant>
                <vt:i4>1</vt:i4>
            </vt:variant>
        </vt:vector>
    </HeadingPairs>
    <TitlesOfParts>
        <vt:vector size="1" baseType="lpstr">
            <vt:lpstr></vt:lpstr>
        </vt:vector>
    </TitlesOfParts>
    <Manager>Josh Knuck</Manager>
    <Company>Silverlayer</Company>
    <LinksUpToDate>false</LinksUpToDate>
    <CharactersWithSpaces>47</CharactersWithSpaces>
    <SharedDoc>false</SharedDoc>
    <HyperlinkBase></HyperlinkBase>
    <AppVersion>14.0000</AppVersion>
</Properties>
""","utf8")

@fixture
def xml_root() -> etree._Element:
    parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
    parser.set_element_class_lookup(etree.ElementNamespaceClassLookup())
    return etree.fromstring(XML, parser)


@mark.parametrize("tname,expected",[
    ("Template", "Normal.dotm"),
    ("Application", "Microsoft Macintosh Word"),
    ("Manager","Josh Knuck"),
    ("Company", "Silverlayer"),
    ("AppVersion", "14.0000")
])
def test_init_text_value(tname,expected,xml_root):
    t=TextProperty.from_element(tname, xml_root)
    assert t.value == expected

def test_init_integer_value(xml_root):
    total=NumericProperty.from_element("TotalTime", xml_root)
    assert total.value == 93

def test_init_boolean_value(xml_root):
    scale=BooleanProperty.from_element("ScaleCrop", xml_root)
    assert scale.value == False

def test_change_scale_crop(xml_root):
    scale=BooleanProperty.from_element("ScaleCrop", xml_root)
    scale.value=True
    scale.to_element(xml_root)
    scale2=BooleanProperty.from_element("ScaleCrop",xml_root)
    assert scale2.value == True

def test_change_scale_crop_none(xml_root):
    scale=BooleanProperty.from_element("ScaleCrop", xml_root)
    scale.value=None
    scale.to_element(xml_root)
    scale2=BooleanProperty.from_element("ScaleCrop",xml_root)
    assert scale2.value == False

def test_set_invalid_to_boolean():
    tst=BooleanProperty("ScaleCrop")
    with raises(TypeError):
        tst.value="True"