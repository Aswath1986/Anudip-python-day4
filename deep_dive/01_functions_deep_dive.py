"""
DEEP DIVE 1: FUNCTIONS — from first principles to real-world use
=================================================================

FIRST PRINCIPLES
----------------
1. A function is a MAPPING: inputs -> outputs.   f(x) = x * x
   In maths it is "pure": same input always gives the same output.

2. In Python, `def` does two things:
     a) builds a FUNCTION OBJECT (code + defaults + name + docstring)
     b) binds a NAME to that object, just like `x = 5` binds a name.
   => Functions are VALUES. You can store them in variables, lists and
      dicts, pass them into other functions, and return them from functions.

3. Calling a function creates a new FRAME on the CALL STACK. The frame holds
   the local variables. When the function returns, the frame is thrown away.
   That is why local variables "disappear" after the call.

4. Names are looked up with the LEGB rule:
     Local -> Enclosing function -> Global (module) -> Built-in

5. Arguments are passed by OBJECT REFERENCE ("call by sharing"): the
   parameter becomes a new name for the SAME object the caller passed.

Everything below follows from these five ideas.

Run:  python deep_dive/01_functions_deep_dive.py
"""
import functools
import time
from typing import Callable, Iterable, Iterator


def section(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# ======================================================================
# PART A — CAPABILITIES
# ======================================================================

# ----------------------------------------------------------------------
section("A1. Functions are objects (first-class)")
# ----------------------------------------------------------------------
def shout(text):
    """Return text in upper case with an exclamation mark."""
    return text.upper() + "!"


yell = shout                          # another name for the same object
print("yell('hi')        ->", yell("hi"))
print("type(shout)       ->", type(shout))
print("shout.__name__    ->", shout.__name__)
print("shout.__doc__     ->", shout.__doc__)
print("same object?      ->", yell is shout)

operations = {"upper": str.upper, "lower": str.lower, "title": str.title}
for name, op in operations.items():                 # functions inside a dict
    print(f"  {name:<6} -> {op('hello world')}")


# ----------------------------------------------------------------------
section("A2. Every way to pass arguments")
# ----------------------------------------------------------------------
#   def f(pos_only, /, normal, *, kw_only)
#   - parameters before  /  must be passed by position
#   - parameters after   *  must be passed by keyword
def make_user(user_id, /, name, *, active=True, role="student"):
    return {"id": user_id, "name": name, "active": active, "role": role}


print(make_user(1, "Ravi"))
print(make_user(2, name="Priya", role="mentor"))
try:
    make_user(3, "Amit", False)        # active is keyword-only
except TypeError as e:
    print("TypeError:", e)


# *args collects extra POSITIONAL arguments into a tuple
# **kwargs collects extra KEYWORD arguments into a dict
def describe(*args, **kwargs):
    return f"args={args} kwargs={kwargs}"


print(describe(1, 2, 3, city="Kolkata", batch=4))

# Unpacking works the other way round at the call site
nums = [3, 7, 1]
opts = {"sep": " | ", "end": "\n"}
print(*nums, **opts)


# ----------------------------------------------------------------------
section("A3. Type hints & docstrings (documentation the tools understand)")
# ----------------------------------------------------------------------
def bmi(weight_kg: float, height_m: float) -> float:
    """
    Calculate Body Mass Index.

    Args:
        weight_kg: weight in kilograms
        height_m:  height in metres
    Returns:
        BMI rounded to 1 decimal place
    """
    return round(weight_kg / height_m ** 2, 1)


print("bmi(70, 1.75)     ->", bmi(70, 1.75))
print("annotations       ->", bmi.__annotations__)
# Hints are NOT enforced at runtime — they help editors and tools like mypy.


# ----------------------------------------------------------------------
section("A4. The mutable-default trap (why it happens)")
# ----------------------------------------------------------------------
# Defaults are evaluated ONCE, when `def` runs — not on every call.
def add_item_buggy(item, basket=[]):
    basket.append(item)
    return basket


print("buggy:", add_item_buggy("pen"))
print("buggy:", add_item_buggy("book"), "<- the same list was reused!")


def add_item_fixed(item, basket=None):
    if basket is None:
        basket = []                     # a fresh list on every call
    basket.append(item)
    return basket


print("fixed:", add_item_fixed("pen"))
print("fixed:", add_item_fixed("book"))


# ----------------------------------------------------------------------
section("A5. Scope: LEGB, global and nonlocal")
# ----------------------------------------------------------------------
counter = 0                             # Global


def increment_global():
    global counter                      # rebind the module-level name
    counter += 1


increment_global()
increment_global()
print("global counter    ->", counter)


def outer():
    message = "enclosing"               # Enclosing scope

    def inner():
        return f"inner sees '{message}' and built-in len={len(message)}"
    return inner()


print(outer())


# ----------------------------------------------------------------------
section("A6. Closures — functions that remember")
# ----------------------------------------------------------------------
# A closure is an inner function that keeps the variables of its
# enclosing scope alive even after the outer function has returned.
def make_multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply


double, triple = make_multiplier(2), make_multiplier(3)
print("double(10), triple(10) ->", double(10), triple(10))


def make_counter():
    count = 0

    def tick():
        nonlocal count                  # modify the enclosing variable
        count += 1
        return count
    return tick


ticket = make_counter()
print("ticket numbers    ->", ticket(), ticket(), ticket())


# ----------------------------------------------------------------------
section("A7. lambda & higher-order functions (map, filter, sorted, reduce)")
# ----------------------------------------------------------------------
students = [("Ravi", 85), ("Priya", 92), ("Amit", 78), ("Neha", 95)]

print("sorted by marks   ->", sorted(students, key=lambda s: s[1], reverse=True))
print("names (map)       ->", list(map(lambda s: s[0], students)))
print("toppers (filter)  ->", list(filter(lambda s: s[1] >= 90, students)))
print("total (reduce)    ->", functools.reduce(lambda acc, s: acc + s[1], students, 0))
print("comprehension way ->", [name for name, m in students if m >= 90])


# ----------------------------------------------------------------------
section("A8. Recursion — a function calling itself")
# ----------------------------------------------------------------------
# Every recursive function needs: a BASE CASE and a step towards it.
def factorial(n: int) -> int:
    return 1 if n <= 1 else n * factorial(n - 1)


print("factorial(6)      ->", factorial(6))


@functools.lru_cache(maxsize=None)       # memoisation: cache past answers
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)


print("fib(80)           ->", fib(80), "(instant thanks to caching)")
print("cache info        ->", fib.cache_info())


# ----------------------------------------------------------------------
section("A9. Generators — functions that produce values lazily")
# ----------------------------------------------------------------------
# `yield` pauses the function and hands back one value at a time.
# Memory use stays tiny, even for millions of items.
def countdown(n):
    while n > 0:
        yield n
        n -= 1


print("countdown(5)      ->", list(countdown(5)))
squares = (x * x for x in range(1_000_000))        # generator expression
print("first 5 squares   ->", [next(squares) for _ in range(5)])


# ----------------------------------------------------------------------
section("A10. Decorators — wrapping functions to add behaviour")
# ----------------------------------------------------------------------
# A decorator is just a function that takes a function and returns a new one.
#   @timer
#   def f(): ...          is the same as      f = timer(f)
def timer(func):
    @functools.wraps(func)                 # keep the original name/docstring
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        ms = (time.perf_counter() - start) * 1000
        print(f"  [timer] {func.__name__} took {ms:.3f} ms")
        return result
    return wrapper


@timer
def slow_sum(n):
    return sum(range(n))


print("slow_sum(10**6)   ->", slow_sum(10 ** 6))


# functools.partial: pre-fill some arguments to make a new function
power = lambda base, exp: base ** exp
square = functools.partial(power, exp=2)
cube = functools.partial(power, exp=3)
print("square(9), cube(3) ->", square(9), cube(3))


# ======================================================================
# PART B — FOUR REAL-WORLD USE CASES
# ======================================================================

# ----------------------------------------------------------------------
section("USE CASE 1: E-commerce checkout — pluggable discount rules")
# ----------------------------------------------------------------------
# Business keeps changing discount rules. Instead of a giant if/else,
# each rule is a small function. New rule = new function. (Strategy pattern)
Cart = list[dict]
Rule = Callable[[Cart, float], float]


def subtotal(cart: Cart) -> float:
    return sum(item["price"] * item["qty"] for item in cart)


def festive_10_percent(cart: Cart, amount: float) -> float:
    return amount * 0.10


def flat_200_above_2000(cart: Cart, amount: float) -> float:
    return 200 if amount >= 2000 else 0


def buy3_books_get_cheapest_free(cart: Cart, amount: float) -> float:
    books = sorted(i["price"] for i in cart if i["category"] == "book"
                   for _ in range(i["qty"]))
    return books[0] if len(books) >= 3 else 0


def checkout(cart: Cart, rules: Iterable[Rule], gst_rate: float = 0.18) -> dict:
    amount = subtotal(cart)
    applied = {rule.__name__: rule(cart, amount) for rule in rules}
    best_name, best_discount = max(applied.items(), key=lambda kv: kv[1])
    taxable = amount - best_discount
    return {
        "subtotal": amount,
        "all_offers": applied,
        "best_offer": best_name,
        "discount": best_discount,
        "gst": round(taxable * gst_rate, 2),
        "payable": round(taxable * (1 + gst_rate), 2),
    }


cart = [
    {"name": "Python Book", "price": 650, "qty": 1, "category": "book"},
    {"name": "Data Book", "price": 480, "qty": 2, "category": "book"},
    {"name": "Headphones", "price": 1200, "qty": 1, "category": "electronics"},
]
bill = checkout(cart, [festive_10_percent, flat_200_above_2000,
                       buy3_books_get_cheapest_free])
for k, v in bill.items():
    print(f"  {k:<11}: {v}")


# ----------------------------------------------------------------------
section("USE CASE 2: Calling an unreliable API — a reusable retry decorator")
# ----------------------------------------------------------------------
# Networks fail. Rather than copy-pasting retry loops everywhere, write
# the policy ONCE as a decorator factory (a function returning a decorator).
def retry(times: int = 3, delay: float = 0.05, exceptions=(ConnectionError,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"  attempt {attempt}/{times} failed: {e}")
                    if attempt == times:
                        raise
                    time.sleep(delay * 2 ** (attempt - 1))   # exponential backoff
        return wrapper
    return decorator


_calls = make_counter()                 # re-using our closure from A6


@retry(times=4)
def fetch_exchange_rate(currency: str) -> float:
    """Pretend API: fails the first two calls, then succeeds."""
    if _calls() < 3:
        raise ConnectionError("server timeout")
    return {"USD": 83.2, "EUR": 90.1}[currency]


print("  USD rate =", fetch_exchange_rate("USD"))


# ----------------------------------------------------------------------
section("USE CASE 3: Company org chart — recursion over a tree")
# ----------------------------------------------------------------------
# Trees (org charts, folders, menus, comments with replies) are naturally
# recursive: a node's total = its own value + totals of its children.
org = {
    "name": "CEO Anita", "salary": 300_000, "reports": [
        {"name": "CTO Vikram", "salary": 220_000, "reports": [
            {"name": "Dev Ravi", "salary": 90_000, "reports": []},
            {"name": "Dev Priya", "salary": 95_000, "reports": [
                {"name": "Intern Amit", "salary": 25_000, "reports": []},
            ]},
        ]},
        {"name": "CFO Meera", "salary": 210_000, "reports": [
            {"name": "Accountant Neha", "salary": 70_000, "reports": []},
        ]},
    ],
}


def print_tree(node: dict, depth: int = 0) -> None:
    print("  " + "    " * depth + f"└─ {node['name']} (₹{node['salary']:,})")
    for child in node["reports"]:
        print_tree(child, depth + 1)


def team_cost(node: dict) -> int:
    return node["salary"] + sum(team_cost(c) for c in node["reports"])


def find_chain(node: dict, target: str, path=()) -> tuple | None:
    path = path + (node["name"],)
    if target in node["name"]:
        return path
    for child in node["reports"]:
        found = find_chain(child, target, path)
        if found:
            return found
    return None


print_tree(org)
print("  Total payroll          :", f"₹{team_cost(org):,}")
print("  CTO's team cost        :", f"₹{team_cost(org['reports'][0]):,}")
print("  Reporting chain of Amit:", " -> ".join(find_chain(org, "Amit")))


# ----------------------------------------------------------------------
section("USE CASE 4: Analysing a huge server log — generator pipeline")
# ----------------------------------------------------------------------
# Real log files can be many GB. Generators process ONE line at a time,
# chained like a factory assembly line, so memory stays constant.
def fake_log_lines(n: int) -> Iterator[str]:
    """Stands in for `open('access.log')` — yields one line at a time."""
    paths = ["/home", "/login", "/api/orders", "/api/pay", "/about"]
    codes = [200, 200, 200, 404, 500, 200, 302]
    for i in range(n):
        yield f"10.0.0.{i % 50} GET {paths[i % 5]} {codes[i % 7]} {(i * 37) % 900}ms"


def parse(lines: Iterable[str]) -> Iterator[dict]:
    for line in lines:
        ip, method, path, status, ms = line.split()
        yield {"ip": ip, "path": path, "status": int(status), "ms": int(ms[:-2])}


def only_errors(records: Iterable[dict]) -> Iterator[dict]:
    return (r for r in records if r["status"] >= 500)


def summarise(records: Iterable[dict]) -> dict:
    by_path: dict[str, int] = {}
    slowest = None
    for r in records:
        by_path[r["path"]] = by_path.get(r["path"], 0) + 1
        if slowest is None or r["ms"] > slowest["ms"]:
            slowest = r
    return {"errors_by_path": by_path, "slowest_error": slowest}


report = summarise(only_errors(parse(fake_log_lines(1_000_000))))
print("  Processed 1,000,000 lines lazily")
print("  5xx errors by path:", report["errors_by_path"])
print("  Slowest failing request:", report["slowest_error"])


# ======================================================================
# KEY TAKEAWAYS
# ======================================================================
#  * A function is an object; `def` creates it and names it.
#  * Parameters are new names for the caller's objects (call by sharing).
#  * Scope follows LEGB; closures capture enclosing variables.
#  * Higher-order functions & decorators let you plug behaviour in.
#  * Recursion fits tree-shaped data; generators fit stream-shaped data.
#
# CHALLENGES
#  1. Add a "first_order_15_percent" rule to Use Case 1 without touching checkout().
#  2. Extend @retry to log the total time taken using the @timer idea.
#  3. Write count_people(node) recursively for the org chart.
#  4. Add a generator stage `slower_than(records, ms)` to the log pipeline.
