"""
NoMETA is a library for editing MS Office documents metadata,
it works with documents of Office >= 2007 and has been tested with docx, pptx, xlsx, vsdx and accdt files.    
"""

from typing import Type, IO
from nometa.sheet import App, Core
from zipfile import is_zipfile, ZipFile, ZIP_DEFLATED

__version__="0.1.1"

def _copy_archive(zin: ZipFile, zout: ZipFile) -> None:
    zout.comment=zin.comment
    for it in zin.infolist():
        if it.filename in ["docProps/app.xml", "docProps/core.xml"]: continue
        zout.writestr(it, zin.read(it))

class Document:
    """
    The Document class aggregates two sheets. One sheet represents the *docProps/app.xml* and the other one represents the *docProps/core.xml*
    """
    def __init__(self, file: str | IO[bytes], cls_core: Type[Core], cls_app: Type[App]) -> None:
        """
        Open the specified document to handle its metadata.

        Args:
            file (str | IO[bytes]): file path of document as string OR an in-memory buffer (`io.BytesIO`)
            cls_core (Type[Core]): type of `nometa.sheet.App` class or its subclasses
            cls_app (Type[App]): type of `nometa.sheet.Core` class or its subclasses

        Raises:
            TypeError
            ValueError
            ValueError
        """
        if not (issubclass(cls_core, Core) and issubclass(cls_app, App)):
            raise TypeError("``cls_app`` must be a subclass of ``sheet.App`` and ``cls_core`` must be a subclass of ``sheet.Core``")
        
        if not is_zipfile(file):
            raise ValueError("'%s' is not a MS Office document"%file)
        
        with ZipFile(file, 'r') as zf:
            try:
                self._core=cls_core(zf.read("docProps/core.xml"))
            except KeyError:
                raise ValueError("'%s' is not a MS Office document"%file)
            
            try:
                self._app=cls_app(zf.read("docProps/app.xml"))
            except KeyError:
                self._app=None
            
            self._file: str | IO[bytes]=file

    @property
    def app(self) -> App:
        """
        Get `App` sheet instance correponding to `docProps/app.xml` file.

        Raises:
            NotImplementedError: throws when there is no `App` instance.

        Returns:
            App: an instance of `nometa.sheet.App`
        """
        if self._app is None:
            raise NotImplementedError("This document doesn't have app.xml sheet")
        
        return self._app

    @property
    def core(self) -> Core:
        """
        Get `Core` sheet instance corresponding to `docProps/core.xml` file.

        Returns:
            Core: an instance of `nometa.sheet.Core`
        """
        return self._core
            
    def save(self, outfile: str|IO[bytes]) -> None:
        """
        Save the changes to the specified document in `outfile` parameter.

        Args:
            outfile (str | IO[bytes]): file path (as string) to document or in memory buffer (`io.BytesIO`)

        Raises:
            IOError: throws when input and output file path/buffer are the same
        """
        if self._file == outfile:
            raise IOError("Input and output documents cannot be the same")
        
        with ZipFile(self._file, 'r') as zr:
            with ZipFile(outfile, 'w', compression=ZIP_DEFLATED) as zw:
                _copy_archive(zr,zw)
                self._core.to_element()
                zw.writestr("docProps/core.xml",self._core.pack())
                if self._app is not None:
                    self._app.to_element()
                    zw.writestr("docProps/app.xml", self._app.pack())



__all__ = ["Document", "App", "Core", "__version__"]