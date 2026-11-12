"""
DEEP DIVE 4: FILE OPERATIONS — from bytes on disk to real tools
===============================================================

FIRST PRINCIPLES
----------------
1. RAM is fast but forgets everything when the program ends. A FILE is a
   named sequence of BYTES stored by the operating system so data survives.

2. Every file is just bytes (numbers 0–255). "Text" is an INTERPRETATION:
   bytes are DECODED into characters using an ENCODING (UTF-8, ASCII...).
       text  --encode-->  bytes  --write-->  disk
       disk  --read-->    bytes  --decode--> text
   Wrong encoding = garbled text (mojibake). Always say encoding="utf-8".

3. open() asks the OS for a HANDLE (file descriptor). A file object keeps a
   CURSOR (position). read/write move the cursor; seek() jumps it.

4. Writes are BUFFERED in memory and flushed to disk later. If you don't
   close() (or flush()), data may never reach the disk. `with` guarantees
   closing — even when an exception happens.

5. A FORMAT is an agreement about how bytes are arranged:
   plain text, CSV (rows), JSON (nested data), binary (images, zip).
   Python's standard library has a module for each common format.

6. The OS can fail you at any moment: missing files, no permission, full
   disk. File code must be paired with exception handling.

All examples run inside a temporary folder that is deleted at the end.

Run:  python deep_dive/04_file_operations_deep_dive.py
"""
import csv
import gzip
import hashlib
import json
import os
import shutil
import tempfile
import zipfile
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path


def section(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


WORKDIR = Path(tempfile.mkdtemp(prefix="file_deep_dive_"))
print(f"Working inside temporary folder: {WORKDIR}")


# ======================================================================
# PART A — CAPABILITIES
# ======================================================================

# ----------------------------------------------------------------------
section("A1. Text vs bytes and encodings")
# ----------------------------------------------------------------------
text = "Namaste नमस्ते ₹500"
data = text.encode("utf-8")
print("  characters     :", len(text))
print("  utf-8 bytes    :", len(data), "->", data[:20], "...")
print("  decode back    :", data.decode("utf-8"))
print("  wrong decoding :", data.decode("latin-1")[:25], "...  (mojibake!)")

p = WORKDIR / "hello.txt"
p.write_text(text, encoding="utf-8")
print("  raw bytes on disk:", p.read_bytes()[:12], "...")


# ----------------------------------------------------------------------
section("A2. All open() modes")
# ----------------------------------------------------------------------
#  r  read | w  write (truncate) | a  append | x  exclusive create
#  +  read AND write            | b  binary  | t  text (default)
f = WORKDIR / "modes.txt"
with open(f, "w", encoding="utf-8") as fh:
    fh.write("line 1\n")
with open(f, "a", encoding="utf-8") as fh:
    fh.write("line 2\n")
with open(f, "r+", encoding="utf-8") as fh:      # read + write, no truncate
    first = fh.readline()
    fh.seek(0, os.SEEK_END)
    fh.write("line 3 (added with r+)\n")
print("  content:", f.read_text(encoding="utf-8").splitlines())
try:
    open(f, "x")
except FileExistsError as e:
    print("  'x' mode refuses to overwrite ->", type(e).__name__)


# ----------------------------------------------------------------------
section("A3. The cursor: tell() and seek()")
# ----------------------------------------------------------------------
with open(f, "rb") as fh:                        # binary mode: seek anywhere
    print("  start position  :", fh.tell())
    print("  read 6 bytes    :", fh.read(6))
    print("  position now    :", fh.tell())
    fh.seek(-9, os.SEEK_END)                      # 9 bytes before the end
    print("  last 9 bytes    :", fh.read())


# ----------------------------------------------------------------------
section("A4. Buffering & flush")
# ----------------------------------------------------------------------
buf = WORKDIR / "buffer.txt"
fh = open(buf, "w", encoding="utf-8")
fh.write("not yet on disk?")
print("  size before flush:", buf.stat().st_size, "bytes")
fh.flush()
print("  size after flush :", buf.stat().st_size, "bytes")
fh.close()
print("  closed?          :", fh.closed)


# ----------------------------------------------------------------------
section("A5. Reading strategies for small and HUGE files")
# ----------------------------------------------------------------------
big = WORKDIR / "big.txt"
with open(big, "w", encoding="utf-8") as fh:
    for i in range(100_000):
        fh.write(f"record {i}\n")
print("  file size        :", f"{big.stat().st_size:,} bytes")

# 1) line by line — constant memory
with open(big, encoding="utf-8") as fh:
    count = sum(1 for _ in fh)
print("  lines (streamed) :", count)

# 2) fixed-size chunks — for binary data / hashing
sha = hashlib.sha256()
with open(big, "rb") as fh:
    while chunk := fh.read(64 * 1024):
        sha.update(chunk)
print("  sha256 (chunked) :", sha.hexdigest()[:32], "...")


# ----------------------------------------------------------------------
section("A6. pathlib — modern, object-oriented paths")
# ----------------------------------------------------------------------
report = WORKDIR / "reports" / "2026" / "sales_q1.csv"
report.parent.mkdir(parents=True, exist_ok=True)
report.write_text("region,amount\n", encoding="utf-8")
print("  name   :", report.name)
print("  stem   :", report.stem)
print("  suffix :", report.suffix)
print("  parent :", report.parent.relative_to(WORKDIR))
print("  exists :", report.exists(), "| is_file:", report.is_file())
print("  all .txt files:", sorted(x.name for x in WORKDIR.glob("*.txt")))
print("  recursive .csv:", [str(x.relative_to(WORKDIR)) for x in WORKDIR.rglob("*.csv")])


# ----------------------------------------------------------------------
section("A7. Structured formats: CSV and JSON")
# ----------------------------------------------------------------------
rows = [{"name": "Ravi", "city": "Kolkata", "marks": 85},
        {"name": "Priya, K", "city": "Pune", "marks": 92}]   # comma inside a value!
csv_path = WORKDIR / "students.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as fh:
    writer = csv.DictWriter(fh, fieldnames=["name", "city", "marks"])
    writer.writeheader()
    writer.writerows(rows)
print("  CSV on disk:\n   ", csv_path.read_text().replace("\n", "\n    ").rstrip())
with open(csv_path, newline="", encoding="utf-8") as fh:
    print("  read back  :", [r["name"] for r in csv.DictReader(fh)],
          "(csv module handled the quotes)")

json_path = WORKDIR / "students.json"
json_path.write_text(json.dumps({"batch": "Day4", "students": rows}, indent=2),
                     encoding="utf-8")
loaded = json.loads(json_path.read_text(encoding="utf-8"))
print("  JSON round-trip equal?", loaded["students"] == rows)


# ----------------------------------------------------------------------
section("A8. Binary files, compression and archives")
# ----------------------------------------------------------------------
# A tiny valid 1x1 PNG image, written byte by byte
png = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
    "0000000d49444154789c6360f8cfc0000003010100c9fe92ef0000000049454e44ae426082")
(WORKDIR / "dot.png").write_bytes(png)
print("  PNG signature:", (WORKDIR / "dot.png").read_bytes()[:8])

gz = WORKDIR / "big.txt.gz"
with open(big, "rb") as src, gzip.open(gz, "wb") as dst:
    shutil.copyfileobj(src, dst)
print(f"  gzip: {big.stat().st_size:,} -> {gz.stat().st_size:,} bytes")

zp = WORKDIR / "bundle.zip"
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(csv_path, arcname="students.csv")
    z.write(json_path, arcname="students.json")
with zipfile.ZipFile(zp) as z:
    print("  zip contents:", z.namelist())


# ----------------------------------------------------------------------
section("A9. Copy, move, rename, delete, metadata")
# ----------------------------------------------------------------------
backup = WORKDIR / "backup"
backup.mkdir(exist_ok=True)
shutil.copy2(csv_path, backup / "students_copy.csv")         # copy + metadata
(backup / "students_copy.csv").rename(backup / "students_old.csv")
shutil.move(str(WORKDIR / "dot.png"), backup / "dot.png")
st = csv_path.stat()
print("  backup folder :", sorted(x.name for x in backup.iterdir()))
print("  size          :", st.st_size, "bytes")
print("  modified      :", datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M"))
(backup / "dot.png").unlink()                                 # delete a file
print("  after unlink  :", sorted(x.name for x in backup.iterdir()))


# ----------------------------------------------------------------------
section("A10. Errors you WILL meet, and how to handle them")
# ----------------------------------------------------------------------
attempts = [
    ("missing file", lambda: open(WORKDIR / "nope.txt")),
    ("folder as file", lambda: open(WORKDIR)),
    ("bad encoding", lambda: (WORKDIR / "bad.bin").read_text(encoding="utf-8")),
]
(WORKDIR / "bad.bin").write_bytes(b"\xff\xfe\xfa")      # bytes that are not valid UTF-8
for label, action in attempts:
    try:
        action()
    except FileNotFoundError:
        print(f"  {label:<15}-> FileNotFoundError")
    except (IsADirectoryError, PermissionError) as e:
        print(f"  {label:<15}-> {type(e).__name__}")
    except UnicodeDecodeError as e:
        print(f"  {label:<15}-> UnicodeDecodeError at byte {e.start}")
print("  (all are subclasses of OSError except UnicodeDecodeError)")


# ----------------------------------------------------------------------
section("A11. Atomic writes — never leave a half-written file")
# ----------------------------------------------------------------------
# If the program crashes mid-write, the file is corrupted. Solution:
# write to a temp file in the same folder, then os.replace() — which is
# atomic: readers see either the old file or the new one, never half.
def atomic_write_text(path: Path, content: str) -> None:
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".tmp_")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(content)
            fh.flush()
            os.fsync(fh.fileno())           # force the OS to write to disk
        os.replace(tmp, path)
    except BaseException:
        os.unlink(tmp)
        raise


atomic_write_text(WORKDIR / "important.txt", "safe content\n")
print("  important.txt ->", (WORKDIR / "important.txt").read_text().strip())


# ======================================================================
# PART B — FOUR REAL-WORLD USE CASES
# ======================================================================

# ----------------------------------------------------------------------
section("USE CASE 1: Sales CSV -> region summary CSV + JSON dashboard feed")
# ----------------------------------------------------------------------
sales_csv = WORKDIR / "sales_raw.csv"
with open(sales_csv, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["date", "region", "product", "units", "unit_price"])
    regions = ["East", "West", "North", "South"]
    products = [("Laptop", 52000), ("Mouse", 600), ("Monitor", 11000)]
    for i in range(40):
        name, price = products[i % 3]
        w.writerow([f"2026-03-{i % 28 + 1:02d}", regions[i % 4], name, i % 5 + 1, price])
    w.writerow(["2026-03-30", "East", "Laptop", "two", 52000])   # a bad row


def summarise_sales(src: Path, out_csv: Path, out_json: Path) -> None:
    totals: dict[str, float] = {}
    best: dict[str, Counter] = {}
    skipped = 0
    with open(src, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            try:
                revenue = int(row["units"]) * float(row["unit_price"])
            except ValueError:
                skipped += 1
                continue
            totals[row["region"]] = totals.get(row["region"], 0) + revenue
            best.setdefault(row["region"], Counter())[row["product"]] += int(row["units"])

    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["region", "revenue", "top_product"])
        for region, rev in sorted(totals.items(), key=lambda kv: -kv[1]):
            w.writerow([region, f"{rev:.2f}", best[region].most_common(1)[0][0]])

    out_json.write_text(json.dumps({
        "generated_at": datetime(2026, 4, 1).isoformat(),
        "grand_total": sum(totals.values()),
        "by_region": totals,
        "rows_skipped": skipped,
    }, indent=2), encoding="utf-8")


summarise_sales(sales_csv, WORKDIR / "sales_summary.csv", WORKDIR / "dashboard.json")
print("  sales_summary.csv:")
for line in (WORKDIR / "sales_summary.csv").read_text().splitlines():
    print("   ", line)
dash = json.loads((WORKDIR / "dashboard.json").read_text())
print(f"  dashboard.json: grand_total=₹{dash['grand_total']:,.0f}, "
      f"rows_skipped={dash['rows_skipped']}")


# ----------------------------------------------------------------------
section("USE CASE 2: Application logger with size-based log rotation")
# ----------------------------------------------------------------------
# Servers write logs forever. Rotation keeps app.log small by renaming
# full logs to app.log.1, app.log.2 ... and deleting the oldest.
class RotatingLog:
    def __init__(self, path: Path, max_bytes: int = 300, backups: int = 3):
        self.path, self.max_bytes, self.backups = path, max_bytes, backups

    def _rotate(self) -> None:
        oldest = self.path.with_name(f"{self.path.name}.{self.backups}")
        oldest.unlink(missing_ok=True)
        for i in range(self.backups - 1, 0, -1):
            src = self.path.with_name(f"{self.path.name}.{i}")
            if src.exists():
                src.rename(self.path.with_name(f"{self.path.name}.{i + 1}"))
        self.path.rename(self.path.with_name(f"{self.path.name}.1"))

    def write(self, level: str, message: str, when: datetime) -> None:
        if self.path.exists() and self.path.stat().st_size >= self.max_bytes:
            self._rotate()
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write(f"{when:%Y-%m-%d %H:%M:%S} {level:<5} {message}\n")


logdir = WORKDIR / "logs"
logdir.mkdir()
logger = RotatingLog(logdir / "app.log")
t0 = datetime(2026, 4, 1, 9, 0)
events = ["user login", "order placed", "payment ok", "payment FAILED", "user logout"]
for i in range(30):
    level = "ERROR" if "FAILED" in events[i % 5] else "INFO"
    logger.write(level, f"{events[i % 5]} id={i}", t0 + timedelta(minutes=i))

print("  log files:", {p.name: p.stat().st_size for p in sorted(logdir.iterdir())})
errors = [line for p in logdir.iterdir()
          for line in p.read_text(encoding="utf-8").splitlines() if "ERROR" in line]
print(f"  ERROR lines across kept files: {len(errors)}; latest: {errors and max(errors)}")


# ----------------------------------------------------------------------
section("USE CASE 3: User settings — JSON with defaults, migration, atomic save")
# ----------------------------------------------------------------------
class Settings:
    DEFAULTS = {"version": 2, "theme": "light", "font_size": 14,
                "notifications": {"email": True, "sms": False}}

    def __init__(self, path: Path):
        self.path = path
        self.data = self._load()

    def _load(self) -> dict:
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            print("  no settings file — using defaults")
            return json.loads(json.dumps(self.DEFAULTS))      # deep copy
        except json.JSONDecodeError:
            corrupt = self.path.with_suffix(".corrupt")
            self.path.rename(corrupt)
            print(f"  corrupt settings moved to {corrupt.name} — using defaults")
            return json.loads(json.dumps(self.DEFAULTS))
        if raw.get("version", 1) == 1:                         # migrate old format
            raw = {"version": 2, "theme": "dark" if raw.pop("dark_mode", False) else "light",
                   **{k: v for k, v in raw.items() if k != "version"}}
            print("  migrated settings v1 -> v2")
        return {**self.DEFAULTS, **raw}

    def set(self, key: str, value) -> None:
        self.data[key] = value
        atomic_write_text(self.path, json.dumps(self.data, indent=2))   # from A11


cfg_path = WORKDIR / "settings.json"
s = Settings(cfg_path)                     # first run: defaults
s.set("font_size", 16)
print("  saved:", json.loads(cfg_path.read_text())["font_size"])

cfg_path.write_text('{"dark_mode": true, "font_size": 18}')    # old v1 file
migrated = Settings(cfg_path).data
print("  loaded:", {k: migrated[k] for k in ("version", "theme", "font_size")})

cfg_path.write_text('{"theme": "dark", ')                      # corrupted
print("  loaded:", Settings(cfg_path).data["theme"])


# ----------------------------------------------------------------------
section("USE CASE 4: Downloads folder organiser + duplicate finder + zip backup")
# ----------------------------------------------------------------------
downloads = WORKDIR / "Downloads"
downloads.mkdir()
samples = {
    "resume.pdf": b"%PDF resume", "resume (1).pdf": b"%PDF resume",   # duplicate
    "holiday.jpg": b"\xff\xd8 photo", "screenshot.PNG": b"\x89PNG shot",
    "budget.xlsx": b"PK sheet", "notes.txt": b"todo list",
    "song.mp3": b"ID3 music", "setup.exe": b"MZ program", "README": b"no ext",
}
for name, content in samples.items():
    (downloads / name).write_bytes(content)

CATEGORIES = {
    "Documents": {".pdf", ".docx", ".txt", ".xlsx"},
    "Images": {".jpg", ".jpeg", ".png", ".gif"},
    "Music": {".mp3", ".wav"},
    "Programs": {".exe", ".msi"},
}


def file_hash(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as fh:
        while chunk := fh.read(8192):
            h.update(chunk)
    return h.hexdigest()


def organise(folder: Path, dry_run: bool = False) -> dict:
    seen: dict[str, Path] = {}
    moved = Counter()
    # shortest name first, so "resume.pdf" is kept and "resume (1).pdf" is the duplicate
    for item in sorted(folder.iterdir(), key=lambda p: (len(p.name), p.name)):
        if not item.is_file():
            continue
        digest = file_hash(item)
        if digest in seen:                                   # duplicate content
            target = folder / "Duplicates" / item.name
        else:
            seen[digest] = item
            category = next((c for c, exts in CATEGORIES.items()
                             if item.suffix.lower() in exts), "Others")
            target = folder / category / item.name
        moved[target.parent.name] += 1
        if not dry_run:
            target.parent.mkdir(exist_ok=True)
            shutil.move(str(item), target)
    return dict(moved)


print("  dry run plan:", organise(downloads, dry_run=True))
print("  organised   :", organise(downloads))
for sub in sorted(downloads.iterdir()):
    print(f"    {sub.name + '/':<12}", sorted(x.name for x in sub.iterdir()))

archive = shutil.make_archive(str(WORKDIR / "downloads_backup"), "zip", downloads)
with zipfile.ZipFile(archive) as z:
    files_in_zip = [n for n in z.namelist() if not n.endswith("/")]
    print(f"  backup zip  : {Path(archive).name} with {len(files_in_zip)} files")


# ----------------------------------------------------------------------
section("Clean-up")
# ----------------------------------------------------------------------
shutil.rmtree(WORKDIR)
print("  temporary folder removed:", not WORKDIR.exists())

# KEY TAKEAWAYS
#  * Files are bytes; text needs an encoding — always pass encoding="utf-8".
#  * Use `with` so files are always closed (and buffers flushed).
#  * Stream big files line-by-line or in chunks; never read() a 10 GB file.
#  * Use csv/json/gzip/zipfile modules instead of hand-parsing.
#  * pathlib for paths, shutil for copying/moving, os.replace for atomic saves.
#  * Every file operation can fail: handle OSError subclasses explicitly.
#
# CHALLENGES
#  1. Add a "Videos" category and an --undo option to the organiser.
#  2. Make RotatingLog compress rotated files with gzip.
#  3. Write the rejected rows from summarise_sales() to errors.csv.
#  4. Build a word-frequency counter for any .txt file using Counter.
