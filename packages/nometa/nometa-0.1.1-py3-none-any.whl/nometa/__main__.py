from nometa import *
from pathlib import Path
from datetime import datetime
from argparse import ArgumentParser, SUPPRESS, RawDescriptionHelpFormatter
import sys

_MESSAGE=f"""
***********************************************************************************************************************************
* © 2024 Silverlayer
* NoMETA v{__version__}
* 
* NoMETA edits MS Office documents metadata (Office>=2007). On success, it will give a copy of provided document with modfications.
* To clean the properties `creator|last_modified_by|last_printed|manager|company`, use the corresponding option with empty string.
* Tested on documents *.docx, *.xlsx, *.pptx, *.vsdx and *.accdt.
* 
* This software is licensed under the Apache License version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
***********************************************************************************************************************************
Eg.
    nometa --creator '' sample.docx --> clean property creator
    nometa --created 2024-12-09T13:09:23 --manager 'Josh Kool' sample.xlsx --> set properties `created` and `manager` at same time.
"""

def main() -> None:
    parser=ArgumentParser(
        prog="nometa",
        description=_MESSAGE,
        allow_abbrev=False,
        formatter_class=RawDescriptionHelpFormatter
    )

    dt_conv=lambda dts: datetime.strptime(dts,"%Y-%m-%dT%H:%M:%SZ")

    parser.add_argument("docpath", type=str, help="The document path")
    # properties of core.xml
    parser.add_argument("--creator", default=SUPPRESS, help="who has created the document")
    parser.add_argument("--last_modified_by", default=SUPPRESS, help="who has modified the document")
    parser.add_argument("--created", default=SUPPRESS, type=dt_conv, help="when the doc. has been created (ISO 8601 UTC)")
    parser.add_argument("--modified", default=SUPPRESS, type=dt_conv, help="when the doc. has been modified (ISO 8601 UTC)")
    parser.add_argument("--last_printed", default=SUPPRESS, help="when the doc. has been printed")

    # properties of app.xml
    parser.add_argument("--manager", default=SUPPRESS, help="manager's name")
    parser.add_argument("--company", default=SUPPRESS, help="company's name")
    args=parser.parse_args()
    dargs=vars(args)

    docfile=Path(dargs["docpath"]).expanduser()
    del dargs["docpath"]

    if not docfile.is_file():
        raise FileNotFoundError("file not found at '%s'"%docfile)

    doc=Document(str(docfile),Core,App)

    for prop,value in dargs.items():
        if prop in ["creator","last_modified_by"]:
            setattr(doc.core,prop,None if len(value)<=0 else value)
        elif prop in ["manager","company"]:
            setattr(doc.app,prop,None if len(value)<=0 else value)
        elif prop == "last_printed":
            setattr(doc.core,prop,datetime.fromisoformat(value) if len(value)>0 else None)
        else:
            setattr(doc.core,prop,value)

    outfile=docfile.name.replace(docfile.suffix,'')+"_copy"+docfile.suffix
    doc.save(outfile)

if __name__ == "__main__":
    rc: int = 1
    try:
        main()
        rc = 0
    except Exception as e:
        print("Err: %s"%e, file=sys.stderr)
    finally:
        sys.exit(rc)