# Agents Playbook

Purpose: coordinate local or automated agents so PhantomJS builds successfully on macOS before any downstream work (experiments, docs, release engineering) proceeds.

## Agent Roster & Expectations

1. **Dependency Agent**
   - Ensures Homebrew (or pkg manager) packages are installed.
   - Verifies the Community QtWebKit build is reachable by CMake.
   - Produces a short report with exact prefix paths.

2. **Build Agent**
   - Configures CMake in an out-of-source `build/` tree.
   - Compiles `phantomjs` with maximum parallelism supported by the host.
   - Persists `compile_commands.json` for tooling by passing `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON`.

3. **Test Agent**
   - Runs the JavaScript suite via `make check` (which invokes `python test/run-tests.py`).
   - Uses Python 2.7 specifically; fails fast if only Python 3 is available.
   - Archives `test/output` (created by the harness) for later inspection.

4. **Review Agent**
   - Tracks deltas in `src/` and `CMakeLists.txt` that impact the build (Qt version checks, new modules, etc.).
   - Blocks merges when QtWebKit, Python, or OpenSSL requirement changes are undocumented.

Each agent should leave artifacts (`logs/deps.txt`, `logs/build.txt`, `logs/tests.txt`, `reports/review.md`) so later steps can short-circuit if nothing changed.

## macOS Build Checklist (Sonoma / Apple Silicon)

> Assumes a clean checkout at `/Users/<you>/fosstercare/phantomjs`.

### 1. Install prerequisites

```bash
brew update
brew install cmake ninja pkg-config qt@5 qtwebkit openssl@3 python@3.12
brew install --ignore-dependencies [email protected] || true   # needed only for the legacy test runner
pyenv install 2.7.18 --skip-existing
pyenv virtualenv 2.7.18 phantomjs-py2
```

- `qtwebkit` is the Community QtWebKit 5.212 build. Homebrew may mark it as deprecated; force-install if necessary.
- Python 2 is required only for `test/run-tests.py` (imports `SimpleHTTPServer`, `SocketServer`, etc.). Keep it isolated via `pyenv` to avoid polluting the system interpreter.

### 2. Export environment for this shell

```bash
export PATH="$(brew --prefix qt@5)/bin:$(brew --prefix ninja)/bin:$PATH"
export CMAKE_PREFIX_PATH="$(brew --prefix qt@5);$(brew --prefix qtwebkit);$(brew --prefix openssl@3)"
export Qt5_DIR="$(brew --prefix qt@5)/lib/cmake/Qt5"
export PKG_CONFIG_PATH="$(brew --prefix qtwebkit)/lib/pkgconfig:$(brew --prefix qt@5)/lib/pkgconfig"
```

These hints allow CMake to locate `Qt5WebKitWidgets` without manual cache edits.

### 3. Configure (out-of-source)

```bash
cmake -S . -B build \
  -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX="$PWD/dist" \
  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
```

- Pass `-DCMAKE_PREFIX_PATH` or `Qt5_DIR` inline if the environment variables above are not exported.
- Logs land in `build/CMakeFiles/CMakeOutput.log`—capture them for the `Review Agent`.

### 4. Build & smoke-test

```bash
cmake --build build --parallel
./build/bin/phantomjs --version
```

Expect the binary under `build/bin/phantomjs`. The version string should match `src/consts.h` (`PHANTOMJS_VERSION_STRING`).

### 5. Test (optional but recommended)

```bash
( pyenv activate phantomjs-py2 && cmake --build build --target check )
```

The `check` target simply runs `python test/run-tests.py -v`. If you prefer manual control, run

```bash
( pyenv activate phantomjs-py2 && python test/run-tests.py -v basics/*.js )
```

to narrow down failures.

## Troubleshooting Tips

- **QtWebKit not found**: Ensure `qtwebkit` keg is linked (`brew link --overwrite qtwebkit`). If CMake still fails, set `-DQt5WebKit_DIR=$(brew --prefix qtwebkit)/lib/cmake/Qt5WebKit`.
- **Linker errors around SSL**: Add `-DOPENSSL_ROOT_DIR=$(brew --prefix openssl@3)` (Qt WebKit on macOS still expects OpenSSL 1.1 style includes).
- **Python errors (`ModuleNotFoundError: SimpleHTTPServer`)**: You are accidentally using Python 3. Switch to the `pyenv` 2.7 shim or edit `test/run-tests.py` to be Python 3 compatible before re-running `make check`.
- **`QWebSettings` symbol missing**: Verify you are not picking up a Qt 6 installation; only Qt 5.15.x with Community QtWebKit 5.212 is supported.

## Review Observations Feeding This Plan

- `INSTALL` intentionally leaves macOS instructions blank, so this document fills that gap while referencing the existing Linux/Windows guidance (`INSTALL`).
- `CMakeLists.txt` hard-requires `Qt5::WebKitWidgets` but only checks that `Qt5Core_VERSION >= 5.5`. Community QtWebKit currently needs Qt >= 5.12, so agents should enforce that higher floor during dependency validation (`CMakeLists.txt`).
- `test/run-tests.py` imports Python 2–only modules (`SimpleHTTPServer`, `SocketServer`, `cStringIO`), therefore `make check` breaks unless a Python 2.7 interpreter is made available.

Keep this playbook under version control. Update it whenever the build moves to a different Qt or Python stack so agents do not have to rediscover the process.
