"""
DEEP DIVE 3: EXCEPTIONS — try / except / else / finally and beyond
==================================================================

FIRST PRINCIPLES
----------------
1. Every operation can either SUCCEED or FAIL. A program needs a way to say
   "I could not do what you asked" without returning a misleading value.

2. In Python, a failure is an OBJECT (an instance of an Exception class).
   `raise` throws that object. Python then UNWINDS THE CALL STACK — leaving
   each function, frame by frame — until it finds a matching `except`.
   If nobody catches it, the program stops and prints a TRACEBACK.

3. Exceptions are classes arranged in a HIERARCHY. `except X` also catches
   every SUBCLASS of X. That is why ordering of except blocks matters.

4. Two styles of defensive code:
     LBYL  "Look Before You Leap"   : if key in d: d[key]
     EAFP  "Easier to Ask Forgiveness than Permission": try: d[key] except KeyError
   Python favours EAFP: it avoids race conditions and double work.

5. Resources (files, connections, locks) must be released whether or not an
   error happened. `finally` and context managers (`with`) guarantee that.

Run:  python deep_dive/03_exceptions_deep_dive.py
"""
import contextlib
import csv
import io
import json
import logging
import random
import sys
import time
import traceback
import warnings

logging.basicConfig(level=logging.INFO, format="  [%(levelname)s] %(message)s")
log = logging.getLogger("exceptions")


def section(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# ======================================================================
# PART A — CAPABILITIES
# ======================================================================

# ----------------------------------------------------------------------
section("A1. Exceptions are objects in a class hierarchy")
# ----------------------------------------------------------------------
def show_tree(cls, depth=0, max_depth=2):
    if depth > max_depth:
        return
    print("  " + "   " * depth + cls.__name__)
    for sub in cls.__subclasses__():
        if sub.__module__ == "builtins":
            show_tree(sub, depth + 1, max_depth)


show_tree(BaseException, max_depth=1)
print("  ...")
print("  ZeroDivisionError MRO:",
      " -> ".join(c.__name__ for c in ZeroDivisionError.__mro__))

err = ValueError("bad value", 42)
print("  err.args        ->", err.args)
print("  isinstance(err, Exception) ->", isinstance(err, Exception))


# ----------------------------------------------------------------------
section("A2. Exact execution order of try / except / else / finally")
# ----------------------------------------------------------------------
def flow(should_fail: bool) -> str:
    steps = []
    try:
        steps.append("try")
        if should_fail:
            raise RuntimeError("boom")
    except RuntimeError:
        steps.append("except")
    else:
        steps.append("else")
    finally:
        steps.append("finally")
    return " -> ".join(steps)


print("  success path:", flow(False))
print("  failure path:", flow(True))


# ----------------------------------------------------------------------
section("A3. Order of except blocks matters (specific first)")
# ----------------------------------------------------------------------
def classify(value):
    try:
        return 100 / int(value)
    except ZeroDivisionError:         # subclass of ArithmeticError
        return "division by zero"
    except ArithmeticError:           # catches the rest of the family
        return "other maths error"
    except (ValueError, TypeError) as e:   # catch several types at once
        return f"bad input: {type(e).__name__}"


for v in ("4", "0", "x", None):
    print(f"  classify({v!r:<5}) -> {classify(v)}")


# ----------------------------------------------------------------------
section("A4. finally ALWAYS runs — even after return / break")
# ----------------------------------------------------------------------
def early_return():
    try:
        return "value from try"
    finally:
        print("  finally ran before the function actually returned")


print("  got:", early_return())

for i in range(3):
    try:
        if i == 1:
            break
    finally:
        print(f"  loop {i}: finally runs even on break")

# PITFALL: a `return` inside finally SWALLOWS the exception. Never do this.
def swallow():
    try:
        1 / 0
    finally:
        return "error silently lost!"     # noqa (demonstration only)


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    print("  pitfall:", swallow())


# ----------------------------------------------------------------------
section("A5. raise, re-raise and exception chaining (raise ... from ...)")
# ----------------------------------------------------------------------
def read_port(cfg: dict) -> int:
    try:
        return int(cfg["port"])
    except KeyError as e:
        # translate a low-level error into a meaningful one, keep the cause
        raise LookupError("config is missing 'port'") from e
    except ValueError:
        log.error("port is not a number — re-raising unchanged")
        raise                          # bare raise = re-throw the same exception


try:
    read_port({})
except LookupError as e:
    print("  caught :", e)
    print("  cause  :", repr(e.__cause__))

try:
    read_port({"port": "eighty"})
except ValueError as e:
    print("  caught re-raised:", e)


# ----------------------------------------------------------------------
section("A6. Custom exception hierarchy for your own domain")
# ----------------------------------------------------------------------
class AppError(Exception):
    """Base for every error our app raises — callers can catch just this."""


class ValidationError(AppError):
    def __init__(self, field: str, message: str):
        super().__init__(f"{field}: {message}")
        self.field = field


class NotFoundError(AppError):
    pass


def get_student(roll: int) -> dict:
    db = {1: {"name": "Ravi", "age": 20}}
    if roll <= 0:
        raise ValidationError("roll", "must be positive")
    if roll not in db:
        raise NotFoundError(f"student {roll} not found")
    return db[roll]


for roll in (1, -5, 7):
    try:
        print("  found:", get_student(roll))
    except ValidationError as e:
        print(f"  invalid field '{e.field}' ->", e)
    except AppError as e:
        print(f"  {type(e).__name__} ->", e)


# ----------------------------------------------------------------------
section("A7. Inspecting tracebacks without crashing")
# ----------------------------------------------------------------------
def level3(): return {}["missing"]
def level2(): return level3()
def level1(): return level2()


try:
    level1()
except KeyError:
    tb = traceback.format_exc().strip().splitlines()
    print("  last 4 traceback lines:")
    for line in tb[-4:]:
        print("   |", line)
    # In real apps: log.exception("message") logs the full traceback.


# ----------------------------------------------------------------------
section("A8. Context managers: `with` = try/finally packaged for reuse")
# ----------------------------------------------------------------------
class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        ms = (time.perf_counter() - self.start) * 1000
        status = "FAILED" if exc_type else "OK"
        print(f"  block {status} in {ms:.3f} ms")
        return False              # False = don't suppress the exception


with Timer():
    sum(range(100_000))

try:
    with Timer():
        int("oops")
except ValueError:
    print("  ...and the exception still reached us")


@contextlib.contextmanager
def temporary_setting(settings: dict, key, value):
    old = settings.get(key)
    settings[key] = value
    try:
        yield settings
    finally:
        settings[key] = old       # always restored


cfg = {"debug": False}
with temporary_setting(cfg, "debug", True):
    print("  inside with  ->", cfg)
print("  after with   ->", cfg)

# contextlib.suppress: deliberately ignore a specific, expected error
with contextlib.suppress(FileNotFoundError):
    open("no_such_file.txt")
print("  suppress() ignored FileNotFoundError cleanly")


# ----------------------------------------------------------------------
section("A9. LBYL vs EAFP")
# ----------------------------------------------------------------------
prices = {"tea": 10, "coffee": 25}

# LBYL
item = "juice"
print("  LBYL:", prices[item] if item in prices else "not on menu")

# EAFP
try:
    print("  EAFP:", prices[item])
except KeyError:
    print("  EAFP: not on menu")


# ----------------------------------------------------------------------
section("A10. assert & warnings")
# ----------------------------------------------------------------------
def average(xs):
    assert len(xs) > 0, "average() needs at least one number"   # developer check
    return sum(xs) / len(xs)


try:
    average([])
except AssertionError as e:
    print("  AssertionError:", e)
print("  NOTE: asserts are removed with `python -O`; never use them for user input.")

with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    warnings.warn("old_api() is deprecated, use new_api()", DeprecationWarning)
    print("  warning raised :", caught[0].message)


# ----------------------------------------------------------------------
section("A11. ExceptionGroup & except* (Python 3.11+)")
# ----------------------------------------------------------------------
# When many independent tasks fail at once, report ALL failures together.
if sys.version_info >= (3, 11):
    exec('''
def validate_form(form):
    errors = []
    if "@" not in form["email"]:
        errors.append(ValueError("invalid email"))
    if not form["phone"].isdigit():
        errors.append(ValueError("invalid phone"))
    if form["age"] < 18:
        errors.append(PermissionError("must be 18+"))
    if errors:
        raise ExceptionGroup("form has errors", errors)

try:
    validate_form({"email": "ravi.com", "phone": "98x", "age": 16})
except* ValueError as group:
    for e in group.exceptions:
        print("  ValueError      ->", e)
except* PermissionError as group:
    for e in group.exceptions:
        print("  PermissionError ->", e)
''')
else:
    print("  (requires Python 3.11 or newer)")


# ======================================================================
# PART B — FOUR REAL-WORLD USE CASES
# ======================================================================

# ----------------------------------------------------------------------
section("USE CASE 1: Payment gateway — retries, custom errors, finally")
# ----------------------------------------------------------------------
class PaymentError(Exception): ...
class CardDeclined(PaymentError): ...
class GatewayTimeout(PaymentError): ...      # temporary — worth retrying


random.seed(7)


def call_gateway(card: str, amount: float) -> str:
    if card.endswith("0000"):
        raise CardDeclined("card blocked by bank")
    if random.random() < 0.5:
        raise GatewayTimeout("no response in 3s")
    return f"TXN{random.randint(10000, 99999)}"


def pay(order_id: str, card: str, amount: float, max_tries: int = 4) -> str | None:
    print(f"  Order {order_id}: paying ₹{amount}")
    try:
        for attempt in range(1, max_tries + 1):
            try:
                txn = call_gateway(card, amount)
            except GatewayTimeout as e:
                log.warning("attempt %d: %s — retrying", attempt, e)
                time.sleep(0.01 * attempt)
            else:
                log.info("success, transaction id %s", txn)
                return txn
        raise GatewayTimeout(f"gave up after {max_tries} attempts")
    except CardDeclined as e:
        log.error("declined: %s — ask customer for another card", e)
    except GatewayTimeout as e:
        log.error("%s — mark order as PAYMENT_PENDING", e)
    finally:
        print(f"  Order {order_id}: payment session closed")
    return None


pay("A101", "4111222233334444", 1499)
pay("A102", "4111222233330000", 899)


# ----------------------------------------------------------------------
section("USE CASE 2: Bulk CSV import — keep going, report every bad row")
# ----------------------------------------------------------------------
# Real uploads contain bad rows. Crashing on row 3 of 10,000 is useless;
# instead, collect errors per row and import the good ones.
RAW_CSV = """name,email,age,fee
Ravi,ravi@mail.com,21,15000
Priya,priya-at-mail,22,15000
Amit,amit@mail.com,abc,12000
Neha,neha@mail.com,19,
Karan,karan@mail.com,-3,9000
Sneha,sneha@mail.com,24,18000
"""


class RowError(Exception):
    pass


def parse_row(row: dict) -> dict:
    if "@" not in row["email"]:
        raise RowError(f"invalid email '{row['email']}'")
    try:
        age = int(row["age"])
    except ValueError:
        raise RowError(f"age '{row['age']}' is not a number") from None
    if not 15 <= age <= 60:
        raise RowError(f"age {age} out of range")
    if not row["fee"]:
        raise RowError("fee is missing")
    return {"name": row["name"], "email": row["email"], "age": age, "fee": float(row["fee"])}


def import_students(text: str):
    good, bad = [], []
    for line_no, row in enumerate(csv.DictReader(io.StringIO(text)), start=2):
        try:
            good.append(parse_row(row))
        except RowError as e:
            bad.append((line_no, row["name"], str(e)))
    return good, bad


ok, errors = import_students(RAW_CSV)
print(f"  imported {len(ok)} rows:", [s["name"] for s in ok])
print(f"  rejected {len(errors)} rows:")
for line_no, name, reason in errors:
    print(f"    line {line_no} ({name}): {reason}")


# ----------------------------------------------------------------------
section("USE CASE 3: Database transaction — all-or-nothing with rollback")
# ----------------------------------------------------------------------
# A transfer touches two records. If the second step fails, the first must
# be undone. A context manager makes this impossible to forget.
class TinyDB:
    def __init__(self):
        self.data = {"ravi": 5000, "priya": 1000}

    @contextlib.contextmanager
    def transaction(self):
        snapshot = dict(self.data)            # BEGIN
        try:
            yield self.data
            log.info("COMMIT  -> %s", self.data)
        except Exception as e:
            self.data.clear()
            self.data.update(snapshot)        # ROLLBACK
            log.error("ROLLBACK (%s) -> %s", e, self.data)
            raise


db = TinyDB()


def transfer(frm: str, to: str, amt: int) -> None:
    with db.transaction() as t:
        t[frm] -= amt
        if t[frm] < 0:
            raise ValueError(f"{frm} would go negative")
        if to not in t:
            raise KeyError(f"no account '{to}'")
        t[to] += amt


for args in (("ravi", "priya", 2000), ("ravi", "ghost", 500), ("priya", "ravi", 9999)):
    try:
        transfer(*args)
    except (ValueError, KeyError) as e:
        print(f"  transfer{args} failed: {e}")
print("  final balances:", db.data)


# ----------------------------------------------------------------------
section("USE CASE 4: Config loader — layered fallbacks & clear error chains")
# ----------------------------------------------------------------------
DEFAULTS = {"host": "localhost", "port": 8000, "debug": False}


class ConfigError(Exception):
    pass


def load_config(sources: list) -> dict:
    """Try each source in order; fall back to defaults; validate the result."""
    config = dict(DEFAULTS)
    for name, text in sources:
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            log.warning("skipping %s: invalid JSON (%s)", name, e.msg)
            continue
        except TypeError:
            log.warning("skipping %s: source not available", name)
            continue
        config.update(data)
        log.info("loaded %s", name)
    try:
        config["port"] = int(config["port"])
        if not 1 <= config["port"] <= 65535:
            raise ValueError("port out of range")
    except (TypeError, ValueError) as e:
        raise ConfigError(f"invalid port {config['port']!r}") from e
    return config


sources = [
    ("/etc/app.json", None),                       # file missing
    ("~/.app.json", '{"debug": true, port: 9000}'),  # broken JSON
    ("ENV", '{"port": "9090", "host": "0.0.0.0"}'),
]
print("  final config:", load_config(sources))

try:
    load_config([("ENV", '{"port": "99999"}')])
except ConfigError as e:
    print("  ConfigError:", e, "| caused by:", repr(e.__cause__))


# KEY TAKEAWAYS
#  * An exception is an object that unwinds the stack until caught.
#  * Catch SPECIFIC exceptions; order from specific to general.
#  * else = success-only code; finally = clean-up that always runs.
#  * Use `raise ... from e` to translate errors without losing the cause.
#  * Context managers turn try/finally into reusable, unforgettable blocks.
#  * In batch jobs, catch per item and report, don't crash on the first error.
#
# CHALLENGES
#  1. Make pay() distinguish "InsufficientBalance" as a new PaymentError.
#  2. Write the rejected CSV rows to an errors.csv file (see deep dive 4).
#  3. Turn Timer into a decorator AND a context manager.
#  4. Add a "max_connections" key to the config loader with validation.
