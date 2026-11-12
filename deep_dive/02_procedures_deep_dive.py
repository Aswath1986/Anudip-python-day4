"""
DEEP DIVE 2: PROCEDURES — side effects, done deliberately
=========================================================

FIRST PRINCIPLES
----------------
1. A program is only useful if it CHANGES SOMETHING in the world:
   shows text, saves a file, sends an email, updates a balance.
   These changes are called SIDE EFFECTS.

2. A FUNCTION (query) answers a question and returns a value.
   A PROCEDURE (command) performs a side effect and returns nothing (None).

   Command-Query Separation (CQS, Bertrand Meyer):
       "Asking a question should not change the answer."
   => a routine should EITHER return data OR change state, not both.

3. Kinds of side effects a procedure can have:
     - Output     : print, logging, sending messages
     - Mutation   : changing a list/dict/object passed to it
     - I/O        : files, databases, network
     - Global     : changing module-level state

4. Python passes OBJECT REFERENCES. A procedure can MUTATE a mutable
   object (list, dict, object) the caller gave it, but REBINDING the
   parameter name never affects the caller.

5. Good design: "Functional core, imperative shell" — keep calculations in
   pure functions, and let a thin layer of procedures do the side effects.
   Pure code is easy to test; side effects are kept in one visible place.

Run:  python deep_dive/02_procedures_deep_dive.py
"""
import logging
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Callable

logging.basicConfig(level=logging.INFO, format="  [%(levelname)s] %(message)s")
log = logging.getLogger("procedures")


def section(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# ======================================================================
# PART A — CAPABILITIES
# ======================================================================

# ----------------------------------------------------------------------
section("A1. A procedure always returns None")
# ----------------------------------------------------------------------
def say_hello(name):
    print(f"  Hello, {name}")


returned = say_hello("Ravi")
print("  returned value  ->", returned)
print("  list.sort() is a procedure ->", [3, 1, 2].sort())
print("  sorted() is a function     ->", sorted([3, 1, 2]))


# ----------------------------------------------------------------------
section("A2. Mutation vs rebinding (the #1 source of confusion)")
# ----------------------------------------------------------------------
def mutate(items):
    items.append(99)          # changes the SAME object the caller has


def rebind(items):
    items = [0, 0, 0]         # makes the local name point elsewhere; caller unaffected


def rebind_number(n):
    n += 1                    # ints are immutable: this creates a new int locally


data, num = [1, 2, 3], 10
mutate(data)
print("  after mutate     ->", data)
rebind(data)
print("  after rebind     ->", data, "(unchanged)")
rebind_number(num)
print("  after rebind_num ->", num, "(immutable objects can't be changed in place)")
print("  id check: same object inside & outside?")


def show_id(obj):
    print(f"    inside  id={id(obj)}")


print(f"    outside id={id(data)}")
show_id(data)


# ----------------------------------------------------------------------
section("A3. Guard clauses — validate first, exit early")
# ----------------------------------------------------------------------
def send_sms(phone: str, text: str) -> None:
    if not phone.isdigit() or len(phone) != 10:
        log.warning("invalid phone %r — SMS not sent", phone)
        return
    if not text.strip():
        log.warning("empty message — SMS not sent")
        return
    print(f"  📱 SMS to {phone}: {text}")


send_sms("9876543210", "Your class starts at 10 AM")
send_sms("12ab", "Hi")
send_sms("9876543210", "   ")


# ----------------------------------------------------------------------
section("A4. print vs logging — professional output")
# ----------------------------------------------------------------------
# logging gives levels, timestamps, files, and can be switched off
# without deleting lines of code.
log.debug("hidden: level is INFO")
log.info("normal information")
log.warning("something looks odd")
log.error("something failed")


# ----------------------------------------------------------------------
section("A5. Command-Query Separation in practice")
# ----------------------------------------------------------------------
stock = {"pen": 10, "notebook": 4}


def available(item: str) -> int:                 # QUERY: no side effects
    return stock.get(item, 0)


def remove_stock(item: str, qty: int) -> None:   # COMMAND: changes state
    if qty > available(item):
        raise ValueError(f"only {available(item)} {item}(s) left")
    stock[item] -= qty


remove_stock("pen", 3)
print("  pens available  ->", available("pen"))
print("  calling the query twice gives the same answer:",
      available("pen") == available("pen"))


# ----------------------------------------------------------------------
section("A6. Procedures that accept callbacks (pluggable actions)")
# ----------------------------------------------------------------------
def for_each(items, action: Callable[[object], None]) -> None:
    for item in items:
        action(item)


for_each(["Ravi", "Priya"], lambda n: print(f"  certificate printed for {n}"))


# ----------------------------------------------------------------------
section("A7. Idempotent procedures — safe to run twice")
# ----------------------------------------------------------------------
# Real systems retry. An idempotent command has the same effect whether
# it runs once or many times (e.g. "set status = PAID" vs "add ₹500").
enrolled: set[str] = set()


def enroll(student: str) -> None:
    if student in enrolled:
        log.info("%s already enrolled — nothing to do", student)
        return
    enrolled.add(student)
    log.info("%s enrolled", student)


enroll("Amit")
enroll("Amit")       # second call is harmless


# ----------------------------------------------------------------------
section("A8. Methods are procedures attached to an object")
# ----------------------------------------------------------------------
@dataclass
class Counter:
    value: int = 0

    def increment(self, by: int = 1) -> None:    # command
        self.value += by

    def reset(self) -> None:                     # command
        self.value = 0


c = Counter()
c.increment()
c.increment(5)
print("  counter value   ->", c.value)


# ----------------------------------------------------------------------
section("A9. The main() procedure & `if __name__ == '__main__'`")
# ----------------------------------------------------------------------
print("  __name__ here is:", repr(__name__))
print("  When this file is IMPORTED, __name__ is the module name instead,")
print("  so code under `if __name__ == '__main__':` does not run on import.")
print("  (See the bottom of this file — the use cases run from main().)")


# ======================================================================
# PART B — FOUR REAL-WORLD USE CASES
# ======================================================================

# ----------------------------------------------------------------------
# USE CASE 1: Bank account — state changes with validation & audit trail
# ----------------------------------------------------------------------
class InsufficientFunds(Exception):
    pass


@dataclass
class BankAccount:
    owner: str
    balance: float = 0.0
    history: list = field(default_factory=list)

    def _record(self, kind: str, amount: float) -> None:
        self.history.append((kind, amount, self.balance))

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self.balance += amount
        self._record("DEPOSIT", amount)

    def withdraw(self, amount: float) -> None:
        if amount > self.balance:
            raise InsufficientFunds(f"balance {self.balance}, asked {amount}")
        self.balance -= amount
        self._record("WITHDRAW", amount)

    def print_statement(self) -> None:
        print(f"  Statement for {self.owner}")
        print(f"  {'TYPE':<10}{'AMOUNT':>10}{'BALANCE':>12}")
        for kind, amt, bal in self.history:
            print(f"  {kind:<10}{amt:>10.2f}{bal:>12.2f}")


def transfer(src: BankAccount, dst: BankAccount, amount: float) -> None:
    """A procedure coordinating two others. Withdraw first: if it fails,
    nothing has changed yet, so money is never created or lost."""
    src.withdraw(amount)
    dst.deposit(amount)
    log.info("transferred %.2f from %s to %s", amount, src.owner, dst.owner)


def use_case_bank() -> None:
    section("USE CASE 1: Bank account — commands that change state safely")
    ravi, priya = BankAccount("Ravi"), BankAccount("Priya")
    ravi.deposit(5000)
    ravi.withdraw(1200)
    transfer(ravi, priya, 1500)
    try:
        transfer(ravi, priya, 10_000)
    except InsufficientFunds as e:
        log.error("transfer refused: %s", e)
    ravi.print_statement()
    priya.print_statement()


# ----------------------------------------------------------------------
# USE CASE 2: Inventory with low-stock alerts — observer pattern
# ----------------------------------------------------------------------
# The inventory doesn't know HOW people are alerted. It just calls every
# registered procedure. Add WhatsApp alerts later without touching it.
class Inventory:
    def __init__(self, reorder_level: int = 5):
        self.items: dict[str, int] = {}
        self.reorder_level = reorder_level
        self._listeners: list[Callable[[str, int], None]] = []

    def subscribe(self, listener: Callable[[str, int], None]) -> None:
        self._listeners.append(listener)

    def add(self, item: str, qty: int) -> None:
        self.items[item] = self.items.get(item, 0) + qty

    def sell(self, item: str, qty: int) -> None:
        if self.items.get(item, 0) < qty:
            log.warning("cannot sell %d %s, only %d", qty, item, self.items.get(item, 0))
            return
        self.items[item] -= qty
        if self.items[item] <= self.reorder_level:
            for notify in self._listeners:
                notify(item, self.items[item])


def email_manager(item: str, left: int) -> None:
    print(f"  📧 EMAIL to manager: '{item}' low ({left} left)")


def create_purchase_order(item: str, left: int) -> None:
    print(f"  🧾 PO created: order {20 - left} x '{item}'")


def use_case_inventory() -> None:
    section("USE CASE 2: Shop inventory — procedures as event listeners")
    shop = Inventory(reorder_level=5)
    shop.subscribe(email_manager)
    shop.subscribe(create_purchase_order)
    shop.add("rice_bag", 12)
    shop.add("oil_tin", 30)
    shop.sell("oil_tin", 10)       # no alert
    shop.sell("rice_bag", 8)       # triggers both listeners
    shop.sell("rice_bag", 10)      # refused
    print("  stock now:", shop.items)


# ----------------------------------------------------------------------
# USE CASE 3: Monthly payroll batch — functional core, imperative shell
# ----------------------------------------------------------------------
EMPLOYEES = [
    {"id": "E01", "name": "Anita", "basic": 60000, "days_absent": 0},
    {"id": "E02", "name": "Vikram", "basic": 45000, "days_absent": 2},
    {"id": "E03", "name": "Meera", "basic": 38000, "days_absent": 5},
]


# --- pure functions (the core): easy to unit-test, no side effects ---
def compute_payslip(emp: dict, working_days: int = 26) -> dict:
    per_day = emp["basic"] / working_days
    hra = emp["basic"] * 0.40
    pf = emp["basic"] * 0.12
    absence_cut = per_day * emp["days_absent"]
    gross = emp["basic"] + hra - absence_cut
    tax = max(0.0, (gross - 40000) * 0.10)
    net = gross - pf - tax
    return {**emp, "hra": hra, "pf": pf, "absence_cut": absence_cut,
            "gross": gross, "tax": tax, "net": round(net, 2)}


# --- procedures (the shell): do the side effects ---
def print_payslip(slip: dict) -> None:
    print(f"  {slip['id']} {slip['name']:<7} gross ₹{slip['gross']:>9,.2f}"
          f"  pf ₹{slip['pf']:>7,.2f}  tax ₹{slip['tax']:>7,.2f}"
          f"  NET ₹{slip['net']:>9,.2f}")


def credit_salary(slip: dict, bank_ledger: list) -> None:
    bank_ledger.append((slip["id"], slip["net"]))


def run_payroll(employees: list[dict]) -> None:
    ledger: list = []
    slips = [compute_payslip(e) for e in employees]   # pure
    for slip in slips:                                # effects
        print_payslip(slip)
        credit_salary(slip, ledger)
    log.info("payroll done: %d employees, total ₹%s paid",
             len(ledger), f"{sum(n for _, n in ledger):,.2f}")


def use_case_payroll() -> None:
    section("USE CASE 3: Payroll batch job — pure calculations, thin procedures")
    run_payroll(EMPLOYEES)


# ----------------------------------------------------------------------
# USE CASE 4: Library — issue/return books, fines, idempotent return
# ----------------------------------------------------------------------
class Library:
    LOAN_DAYS, FINE_PER_DAY = 14, 5

    def __init__(self):
        self.catalog: dict[str, int] = {}               # title -> copies available
        self.loans: dict[tuple, date] = {}              # (member, title) -> due date
        self.fines: dict[str, int] = {}

    def add_book(self, title: str, copies: int = 1) -> None:
        self.catalog[title] = self.catalog.get(title, 0) + copies

    def issue(self, member: str, title: str, today: date) -> None:
        if self.fines.get(member, 0) > 0:
            log.warning("%s has unpaid fine ₹%d — cannot issue", member, self.fines[member])
            return
        if self.catalog.get(title, 0) == 0:
            log.warning("'%s' not available", title)
            return
        self.catalog[title] -= 1
        self.loans[(member, title)] = today + timedelta(days=self.LOAN_DAYS)
        log.info("issued '%s' to %s, due %s", title, member,
                 self.loans[(member, title)])

    def return_book(self, member: str, title: str, today: date) -> None:
        due = self.loans.pop((member, title), None)
        if due is None:                                 # idempotent
            log.info("'%s' already returned by %s", title, member)
            return
        self.catalog[title] += 1
        late = (today - due).days
        if late > 0:
            self.fines[member] = self.fines.get(member, 0) + late * self.FINE_PER_DAY
            log.warning("%s returned '%s' %d days late — fine ₹%d",
                        member, title, late, late * self.FINE_PER_DAY)
        else:
            log.info("%s returned '%s' on time", member, title)

    def pay_fine(self, member: str) -> None:
        paid = self.fines.pop(member, 0)
        log.info("%s paid fine ₹%d", member, paid)


def use_case_library() -> None:
    section("USE CASE 4: Library system — issue, return, fines")
    lib = Library()
    lib.add_book("Clean Code", 1)
    d0 = date(2026, 1, 1)
    lib.issue("Neha", "Clean Code", d0)
    lib.issue("Amit", "Clean Code", d0)                     # no copies left
    lib.return_book("Neha", "Clean Code", d0 + timedelta(days=20))
    lib.return_book("Neha", "Clean Code", d0 + timedelta(days=21))   # safe repeat
    lib.issue("Neha", "Clean Code", d0 + timedelta(days=21))         # blocked by fine
    lib.pay_fine("Neha")
    lib.issue("Neha", "Clean Code", d0 + timedelta(days=21))


# ======================================================================
# Entry point — the top-level procedure that orchestrates everything
# ======================================================================
def main() -> None:
    use_case_bank()
    use_case_inventory()
    use_case_payroll()
    use_case_library()


if __name__ == "__main__":
    main()

# KEY TAKEAWAYS
#  * Procedures exist for their SIDE EFFECTS; they return None.
#  * Mutating an argument is visible to the caller; rebinding is not.
#  * Separate commands from queries; keep calculations pure.
#  * Guard clauses, logging and idempotence make procedures production-safe.
#
# CHALLENGES
#  1. Add a `statement_to_file(path)` procedure to BankAccount.
#  2. Add an SMS listener to the Inventory without changing the class.
#  3. Write a unit test (plain assert) for compute_payslip().
#  4. Add a reserve(member, title) command to the Library.
