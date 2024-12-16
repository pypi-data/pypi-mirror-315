from nometa import Document
from nometa.sheet import App, Core
from pytest import mark, raises
import io

RESOURCE_PATH="tests/resource/"

@mark.parametrize("file",["test.docx","test.xlsx","test.pptx","test.vsdx"])
def test_init_doc(file):
    doc=Document(RESOURCE_PATH+file,Core,App)
    assert doc.core.modified.year == 2024 and float(doc.app.app_version)>=14.0

def test_doc_without_app_sheet():
    doc=Document(RESOURCE_PATH+"test.accdt",Core,App)
    with raises(NotImplementedError):
        doc.app

def test_save_inplace_doc():
    doc=Document(RESOURCE_PATH+"test.docx",Core,App)
    doc.app.total_time=3000
    doc.core.creator="Papaléguas"
    with raises(IOError):
        doc.save(RESOURCE_PATH+"test.docx")

@mark.parametrize("src,dst",[
    ("test.docx","test2.docx"),
    ("test.xlsx","test2.xlsx"),
    ("test.pptx","test2.pptx"),
    ("test.vsdx","test2.vsdx"),
    ("test.accdt","test2.accdt")
])
def test_save_doc(src, dst):
    doc=Document(RESOURCE_PATH+src,Core,App)
    try:
        doc.app.total_time=127
        doc.app.company="Silverlayer"
        doc.app.manager=None
    except NotImplementedError: pass
    doc.core.creator = doc.core.last_modified_by = "Johnny Test"
    doc.save(RESOURCE_PATH+dst)

def test_doc_asbytes():
    buff=io.BytesIO()
    with open(RESOURCE_PATH+"test.docx", "rb") as fd:
        doc=Document(fd,Core,App)
        doc.app.total_time=25
        doc.save(buff)
    
    new_doc=Document(buff,Core,App)
    assert doc.app.total_time == new_doc.app.total_time and doc.core.creator == new_doc.core.creator

def test_read_write_same_buffer():
    with open(RESOURCE_PATH+"test.docx", "rb") as fd:
        doc=Document(fd,Core,App)
        doc.app.total_time=25
        with raises(IOError):
            doc.save(fd)


def test_filepath_to_bytes():
    buff=io.BytesIO()
    doc=Document(RESOURCE_PATH+"test.docx",Core,App)
    doc.app.total_time=25
    doc.save(buff)
    
    new_doc=Document(buff,Core,App)
    assert doc.app.total_time == new_doc.app.total_time and doc.core.creator == new_doc.core.creator
