# Version history

We follow Semantic Versions since the `0.1.0` release.


## WIP

### Misc

- Improves `README`


## 0.8.0

### Features

- Reintroduces the `Maybe` monad, typed!
- Introduces converters from one type to another
- Adds `mypy` plugin to type decorators
- Complete rewrite of `Result` types
- Partial API change, now `Success` and `Failure` are not types, but functions
- New internal types introduced: `FixableContainer` and `ValueUnwrapContainer`

### Bugfixes

- Fixes issue when you could return `IO` container from `Result.bind`
- Fixes `@pipeline` return type

### Misc

- Reapplied all types to `.py` files
- Improved docs about `IO` and `Container` concept
- Adds docs about container composition
- Moves from `Alpha` to `Beta`


## 0.7.0

### Features

- Adds `IO` marker
- Adds `unsafe` module with unsafe functions
- Changes how functions are located inside the project

### Bugfixes

- Fixes container type in `@pipeline`
- Now `is_successful` is public
- Now `raise_exception` is public

### Misc

- Changes how `str()` function works for container types
- Total rename to "container" in the source code


## Version 0.6.0

### Features

- `safe` and `pipeline` now supports `asyncio`
- `is_successful` now returns `Literal` types if possible


## Version 0.5.0

### Features

- Adds `compose` helper function
- Adds public API to `import returns`
- Adds `raise_exception` helper function
- Adds full traceback to `.unwrap()`


### Misc

- Updates multiple dev-dependencies, including `mypy`
- Now search in the docs is working again
- Relicenses this project to `BSD`
- Fixes copyright notice in the docs


## Version 0.4.0 aka Goodbye, Monads!

### Features

- Moves all types to `.pyi` files
- Renames all classes according to new naming pattern
- **HUGE** improvement of types
- Renames `fmap` to `map`
- Renames `do_notation` to `pipeline`, moves it to `functions.py`
- Renames `ebind` to `rescue`
- Renames `efmap` to `fix`
- Renames `Monad` to `Container`
- Removes `Maybe` monad, since typing does not have `NonNullable` type


## Version 0.3.1

### Bugfixes

- Adds `py.typed` file to be `PEP561` compatible


## Version 0.3.0, Renamed to `returns`

The project is renamed to `returns` and moved to `dry-python` org.

### Features

- Adds `.pyi` files for all modules,
  to enable `mypy` support for 3rd party users


## Version 0.2.0

### Features

- Adds `Maybe` monad
- Adds immutability and `__slots__` to all monads
- Adds methods to work with failures
- Adds `safe` decorator to convert exceptions to `Result` monad
- Adds `is_successful()` function to detect if your result is a success
- Adds `failure()` method to unwrap values from failed monads

### Bugfixes

- Changes the type of `.bind` method for `Success` monad
- Changes how equality works, so now `Failure(1) != Success(1)`
- Changes how new instances created on unused methods

### Misc

- Improves docs


## Version 0.1.1

### Bugfixes

- Changes how `PyPI` renders package's page

### Misc

- Improves `README` with new badges and installation steps


## Version 0.1.0

Initial release. Featuring only `Result` and `do_notation`.
