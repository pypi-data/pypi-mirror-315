from nometa.sheet import App
from pytest import fixture, raises, mark

@fixture
def bxml() -> bytes:
    return bytes("""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
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
        <HyperlinksChanged>false</HyperlinksChanged>
        <AppVersion>14.0000</AppVersion>
    </Properties>
    ""","utf8")

def test_init_app_sheet(bxml):
    osheet=App(bxml)
    assert osheet is not None

@mark.parametrize("prop,expec",[
    ("template","Normal.dotm"),
    ("total_time",93),
    ("application","Microsoft Macintosh Word"),
    ("scale_crop",False),
    ("manager","Josh Knuck"),
    ("company","Silverlayer"),
    ("app_version","14.0000")
])
def test_read_props(bxml, prop, expec):
    osheet=App(bxml)
    assert eval("osheet."+prop) == expec


def test_set_invalid_total_time(bxml):
    osheet=App(bxml)
    with raises(TypeError):
        osheet.total_time=3.1456795

def test_set_invalid_scale(bxml):
    osheet=App(bxml)
    with raises(TypeError):
        osheet.scale_crop="True"

def test_change_prop(bxml):
    osheet=App(bxml)
    osheet.manager="Michael Rudson"
    osheet.scale_crop=True
    osheet.total_time=240
    osheet.application="MS Office"
    osheet.company="Neo brand"
    osheet.app_version="12.000"
    osheet.to_element()
    new_sheet=App(osheet.pack())
    
    assert new_sheet.manager == osheet.manager and new_sheet.scale_crop == osheet.scale_crop \
    and new_sheet.total_time == osheet.total_time and new_sheet.application == osheet.application \
    and new_sheet.company == osheet.company and new_sheet.app_version == osheet.app_version