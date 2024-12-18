# BScintillaEdit

The `BScintillaEdit` is a simple text edit control derived from a `QScrollArea` that embeds a `ScintillaBaseEdit` from [Scintilla](https://www.scintilla.org/).

The Python bindings are made with [shiboken](https://doc.qt.io/qtforpython-6/shiboken6/index.html).

## PyPi

The package can be installed from [PyPi](https://pypi.org/project/bscintillaedit/):

```bash
pip install bscintillaedit
```

## License

This project uses the code from the [Scintilla](https://www.scintilla.org/) project as a submodule installed in `src/core_lib/scintilla`. All the code under `src/core_lib/scintilla` is covered by the [scintilla license](https://www.scintilla.org/License.txt), a [Historical Permission Notice and Disclaimer](https://en.wikipedia.org/wiki/Historical_Permission_Notice_and_Disclaimer) type of license.

All the other code from this project is licensed under the [MIT License](https://gitlab.com/iborco-pyside/bscintillaedit/-/blob/master/LICENSE.md).

This software is <ins>**not related**</ins> to the [QScintilla](https://www.riverbankcomputing.com/software/qscintilla/) or [PyQt](https://www.riverbankcomputing.com/software/pyqt/) projects.
