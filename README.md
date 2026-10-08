# acme-tools

One repo, several packages. Each package installs on its own.

## Layout

```
acme-tools/
├── pyproject.toml                  # workspace root (not installable)
└── packages/
    ├── acme-db/
    │   ├── pyproject.toml
    │   └── src/acme/db/__init__.py
    └── acme-linkage/               # depends on acme-db
        ├── pyproject.toml
        └── src/acme/linkage/__init__.py
```

There is no `src/acme/__init__.py`, so `acme` is a shared namespace:
`from acme.db import upload`, `from acme.linkage import link_and_upload`.

## pyproject.toml

Root: lists the workspace members.

```toml
[tool.uv]
package = false

[tool.uv.workspace]
members = ["packages/*"]
```

Each package: a name, a build backend, and its import path.

```toml
[project]
name = "acme-db"
version = "0.1.0"
dependencies = []

[build-system]
requires = ["uv_build>=0.11.2,<0.12.0"]
build-backend = "uv_build"

[tool.uv.build-backend]
module-name = "acme.db"
```

A package that uses another one adds it as a dependency and points it at the workspace:

```toml
[project]
dependencies = ["acme-db"]

[tool.uv.sources]
acme-db = { workspace = true }
```

## Adding a package

Example: `acme-viz`, imported as `acme.viz`.

```
packages/acme-viz/
├── pyproject.toml
└── src/acme/viz/__init__.py      # no src/acme/__init__.py
```

```toml
[project]
name = "acme-viz"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = ["acme-db"]        # optional: use a sibling package

[build-system]
requires = ["uv_build>=0.11.2,<0.12.0"]
build-backend = "uv_build"

[tool.uv.build-backend]
module-name = "acme.viz"

[tool.uv.sources]
acme-db = { workspace = true }    # only if depending on a sibling
```

To use it from the root environment, also add `"acme-viz"` to the root
`dependencies` and `acme-viz = { workspace = true }` to the root
`[tool.uv.sources]`. Then run `uv sync`.

## Develop

```bash
uv sync     # installs every package, editable
```

## Build

```bash
uv build --package acme-db    # writes dist/
uv build --all-packages
```

## Publish

Push to GitLab and tag a release for each package:

```bash
git tag acme-db/v0.1.0
git push origin acme-db/v0.1.0
```

## Install

```bash
uv add "acme-db @ git+ssh://git@gitlab.yourco.com/group/acme-tools.git@acme-db/v0.1.0#subdirectory=packages/acme-db"
```

Installing `acme-linkage` pulls in `acme-db` automatically (uv only).
