#!/usr/bin/env python3

import json
import sys
from pathlib import Path

# -------------------------------------------------
# Telegram abstract / conceptual types
# -------------------------------------------------
IGNORED_TYPES = {
    "InputFile",
    "InputMedia",
}

# -------------------------------------------------
# Helpers
# -------------------------------------------------
def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


# -------------------------------------------------
# Args
# -------------------------------------------------
if len(sys.argv) != 4:
    print("Usage: coverage_report.py api.json gen_types.rs gen_methods.rs")
    sys.exit(2)

api_path, types_path, methods_path = sys.argv[1:]

api = json.loads(read(api_path))
types_src = read(types_path)
methods_src = read(methods_path)

all_types = api.get("types", {})
all_methods = api.get("methods", {})

implemented_types = []
missing_types = []

implemented_methods = []
missing_methods = []

# -------------------------------------------------
# Type coverage
# -------------------------------------------------
for name, info in all_types.items():
    # Skip abstract Telegram types
    if name in IGNORED_TYPES:
        implemented_types.append(name)
        continue

    is_union = bool(info.get("subtypes"))

    if is_union:
        pattern = f"pub enum {name}"
    else:
        pattern = f"pub struct {name}"

    if pattern in types_src:
        implemented_types.append(name)
    else:
        missing_types.append(name)

# -------------------------------------------------
# Method coverage
# Telegram methods are implemented as REQUEST STRUCTS
# e.g. sendMessage -> pub struct SendMessage
# -------------------------------------------------
for name in all_methods:
    struct_name = name[0].upper() + name[1:]
    pattern = f"pub struct {struct_name}"

    if pattern in methods_src:
        implemented_methods.append(name)
    else:
        missing_methods.append(name)

# -------------------------------------------------
# Report
# -------------------------------------------------
total_types = len(all_types)
total_methods = len(all_methods)

types_covered = len(implemented_types)
methods_covered = len(implemented_methods)

types_pct = int((types_covered / total_types) * 100) if total_types else 100
methods_pct = int((methods_covered / total_methods) * 100) if total_methods else 100

print("=" * 60)
print("📊 tgbotrs API Coverage — Telegram Bot API")
print("=" * 60)
print(f"  Types:   {types_covered}/{total_types}  ({types_pct}%)")
print(f"  Methods: {methods_covered}/{total_methods}  ({methods_pct}%)")

if missing_types:
    print("\n⚠️  Missing Types:")
    print(" ", missing_types)

if missing_methods:
    print("\n⚠️  Missing Methods:")
    print(" ", missing_methods)

# -------------------------------------------------
# Strict CI enforcement
# -------------------------------------------------
if missing_types or missing_methods:
    sys.exit(1)
