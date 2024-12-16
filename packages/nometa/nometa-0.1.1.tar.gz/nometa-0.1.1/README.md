# NoMETA

## What is NoMETA?

NoMETA is a library for editing MS Office documents metadata, it works with documents of Office >= 2007 and has been tested with docx, pptx, xlsx, vsdx and accdt files.

## License

NoMETA is released under the terms of the Apache license v2.0. See LICENSE for information.

## Getting started

NoMETA is available in [PyPI.org](https://pypi.org/), so the recommended method to install is `$ pip install nometa`. Otherwise, you can download the source code and run by yourself.

NoMETA has a command line interface (CLI) that you can run directly. However, only a subset of metadata can be edited by CLI. You can use the command `$ nometa -h` to learn how to execute NoMETA on CLI.

The code snippet below gives a sample of how to use NoMETA programmatically. For more details, read the [documentation](https://silverlayer.github.io/nometa/).

```python
>>> from nometa import Document, Core, App
>>> doc = Document("tests/resource/test.docx",Core,App)
>>> doc.core.creator
'Michael Myers'
>>> doc.core.creator = "Johnny Test"
>>> doc.save("test2.docx")
```