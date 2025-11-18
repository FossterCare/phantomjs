installed with other command 

brew install qwt-qt5
==> Fetching downloads for: qwt-qt5
✔︎ Bottle Manifest qwt-qt5 (6.3.0)                             [Downloaded   63.8KB/ 63.8KB]
✔︎ Bottle Manifest md4c (0.5.2)                                [Downloaded   11.2KB/ 11.2KB]
✔︎ Bottle Manifest qt@5 (5.15.17_1)                            [Downloaded   75.4KB/ 75.4KB]
✔︎ Bottle md4c (0.5.2)                                         [Downloaded   82.9KB/ 82.9KB]
✔︎ Bottle qwt-qt5 (6.3.0)                                      [Downloaded    6.0MB/  6.0MB]
✔︎ Bottle qt@5 (5.15.17_1)                                     [Downloaded  119.7MB/119.7MB]
==> Installing dependencies for qwt-qt5: md4c and qt@5
==> Installing qwt-qt5 dependency: md4c
==> Pouring md4c--0.5.2.arm64_sequoia.bottle.tar.gz
🍺  /opt/homebrew/Cellar/md4c/0.5.2: 20 files, 309.4KB
==> Installing qwt-qt5 dependency: qt@5
==> Pouring qt@5--5.15.17_1.arm64_sequoia.bottle.tar.gz
🍺  /opt/homebrew/Cellar/qt@5/5.15.17_1: 10,849 files, 358.1MB
==> Installing qwt-qt5
==> Pouring qwt-qt5--6.3.0.arm64_sequoia.bottle.tar.gz
==> Caveats
qwt-qt5 is keg-only, which means it was not symlinked into /opt/homebrew,
because it conflicts with qwt.

For compilers to find qwt-qt5 you may need to set:
  export LDFLAGS="-L/opt/homebrew/opt/qwt-qt5/lib"
  export CPPFLAGS="-I/opt/homebrew/opt/qwt-qt5/include"

For pkgconf to find qwt-qt5 you may need to set:
  export PKG_CONFIG_PATH="/opt/homebrew/opt/qwt-qt5/lib/pkgconfig"
==> Summary
🍺  /opt/homebrew/Cellar/qwt-qt5/6.3.0: 2,213 files, 34.9MB
==> Running `brew cleanup qwt-qt5`...
Disable this behaviour by setting `HOMEBREW_NO_INSTALL_CLEANUP=1`.
Hide these hints with `HOMEBREW_NO_ENV_HINTS=1` (see `man brew`).
==> Caveats
==> qwt-qt5
qwt-qt5 is keg-only, which means it was not symlinked into /opt/homebrew,
because it conflicts with qwt.

For compilers to find qwt-qt5 you may need to set:
  export LDFLAGS="-L/opt/homebrew/opt/qwt-qt5/lib"
  export CPPFLAGS="-I/opt/homebrew/opt/qwt-qt5/include"

For pkgconf to find qwt-qt5 you may need to set:
  export PKG_CONFIG_PATH="/opt/homebrew/opt/qwt-qt5/lib/pkgconfig"







  #####

  export QTWEBKIT_PREFIX="/Users/senthil/fosstercare/qtwebkit/install"

# Let CMake/qmake locate the freshly installed package files
export CMAKE_PREFIX_PATH="$QTWEBKIT_PREFIX:${CMAKE_PREFIX_PATH:-}"
export PKG_CONFIG_PATH="$QTWEBKIT_PREFIX/lib/pkgconfig:${PKG_CONFIG_PATH:-}"
export QMAKEPATH="$QTWEBKIT_PREFIX:${QMAKEPATH:-}"
export QML2_IMPORT_PATH="$QTWEBKIT_PREFIX/lib/qml:${QML2_IMPORT_PATH:-}"
export QMAKEFEATURES="$QTWEBKIT_PREFIX/mkspecs:${QMAKEFEATURES:-}"

# Ensure the frameworks and libexec helpers are picked up at runtime
export DYLD_FRAMEWORK_PATH="$QTWEBKIT_PREFIX/lib:${DYLD_FRAMEWORK_PATH:-}"
export DYLD_LIBRARY_PATH="$QTWEBKIT_PREFIX/lib:${DYLD_LIBRARY_PATH:-}"
export PATH="$QTWEBKIT_PREFIX/lib/libexec:$PATH"