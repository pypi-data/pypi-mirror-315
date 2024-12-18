# For developers

Notes for updating and maintaining this package.

## Cloning the repo

```bash
git clone git@gitlab.com:iborco-pyside/borco-pyside6-scintilla.git
```

```bash
git submodule update --init --recursive
```

## Updating (unofficial) upstream scintilla

* go to `src/core_lib/scintilla`
* fetch the latest tags
* switch to the new tag you want
* commit your changes

```bash
pushd src/core_lib/scintilla
```

```bash
git fetch --tags
```

```bash
git tag
```

```bash
git checkout rel-5-5-3
```

```bash
popd
```

```bash
git add src/core_lib/scintilla
```

```bash
git commit -m "updated scintilla to rel-5-5-3"
```
