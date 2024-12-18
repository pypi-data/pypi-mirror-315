# core_lib

The `core_lib` implements the `BScintillaEdit` control that inherits from
`QScrollArea` and embeds an `ScintillaEditBase` control from
`src/core_lib/scintilla/qt/ScintillaEditBase`. This control is further exposed
to Python through the `shiboken` bindings.

The `src/core_lib/scintilla` subdir contains the unofficial scintilla mirror
from <https://github.com/borco/scintilla> as a submodule.

The dependencies for compiling `ScintillaEditBase` are manually extracted from
the `src/core_lib/scintilla/qt/ScintillaEditBase/ScintillaEditBase.pro`.

No changes are done to the files under `src/core_lib/scintilla`.
