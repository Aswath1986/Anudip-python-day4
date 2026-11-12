# Deep Dive (optional, self-paced)

For students who want to go beyond the 15-minute class files in the repository root.
Each file starts from **first principles** (*why* the feature exists and how Python really
works underneath), shows **as many capabilities as possible** (Part A), then applies them to
**4 real-world use cases** (Part B). Every file ends with key takeaways and challenges.

Run any file from the repository root, e.g. `python deep_dive/01_functions_deep_dive.py`.
Requires Python 3.10+ (section A11 of file 03 needs 3.11+ and is skipped otherwise).

| File | First principles | Capabilities covered | Real-world use cases |
|------|------------------|----------------------|----------------------|
| `01_functions_deep_dive.py` | Functions are objects, call stack & frames, LEGB scope, call-by-sharing | First-class functions, positional-only / keyword-only params, `*args`/`**kwargs`, type hints, mutable-default trap, `global`/`nonlocal`, closures, lambda/map/filter/reduce, recursion + `lru_cache`, generators, decorators, `partial` | 1. E-commerce checkout with pluggable discount rules · 2. Retry decorator for an unreliable API · 3. Org-chart recursion (payroll, reporting chain) · 4. Generator pipeline over a 1M-line server log |
| `02_procedures_deep_dive.py` | Side effects, command-query separation, mutation vs rebinding, "functional core, imperative shell" | `None` return, mutation vs rebinding, guard clauses, `logging`, CQS, callbacks, idempotence, methods, `main()` & `__name__` | 1. Bank account with audit trail & safe transfer · 2. Inventory low-stock alerts (observer pattern) · 3. Monthly payroll batch job · 4. Library issue/return with fines |
| `03_exceptions_deep_dive.py` | Exceptions as objects, stack unwinding, class hierarchy, LBYL vs EAFP | Exception hierarchy & MRO, exact try/except/else/finally order, except ordering, `finally` with return/break (and its pitfall), `raise from`, bare re-raise, custom exceptions, `traceback`, context managers (`__enter__/__exit__`, `@contextmanager`, `suppress`), `assert`, `warnings`, `ExceptionGroup`/`except*` | 1. Payment gateway with retries & custom errors · 2. Bulk CSV import reporting every bad row · 3. Database transaction with rollback · 4. Layered config loader with error chaining |
| `04_file_operations_deep_dive.py` | Files are bytes, encodings, file handles & cursor, buffering, formats, OS failures | Encodings & mojibake, all `open()` modes, `seek`/`tell`, `flush`, streaming & chunked reads, hashing, `pathlib`, `csv`, `json`, binary files, `gzip`, `zipfile`, `shutil`, metadata, file errors, atomic writes | 1. Sales CSV → summary CSV + JSON dashboard · 2. Logger with size-based rotation · 3. Settings file with defaults, migration & corruption recovery · 4. Downloads organiser + duplicate finder + zip backup |

File 04 works entirely inside a temporary folder and deletes it at the end, so nothing is left behind.
