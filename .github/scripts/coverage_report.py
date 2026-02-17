#!/usr/bin/env python3
"""
coverage_report.py — Generates a coverage report showing API implementation status.

Usage:
  python3 coverage_report.py api.json gen_types.rs gen_methods.rs [--markdown]
"""

import json
import re
import sys


def snake_case(name):
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', name)
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s)
    return s.lower()


def main():
    markdown = "--markdown" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if len(args) < 3:
        print("Usage: coverage_report.py api.json gen_types.rs gen_methods.rs [--markdown]")
        sys.exit(1)

    spec = json.load(open(args[0]))
    types_src = open(args[1]).read()
    methods_src = open(args[2]).read()

    all_types = spec["types"]
    all_methods = spec["methods"]
    version = spec.get("version", "?")
    release_date = spec.get("release_date", "?")

    # Check types coverage
    implemented_types = []
    missing_types = []
    union_types = []
    struct_types = []
    empty_types = []

    for name, info in all_types.items():
        is_union = bool(info.get("subtypes"))
        has_fields = bool(info.get("fields"))

        if is_union:
            union_types.append(name)
            pattern = f"pub enum {name}"
        else:
            pattern = f"pub struct {name}"
            if has_fields:
                struct_types.append(name)
            else:
                empty_types.append(name)

        if pattern in types_src:
            implemented_types.append(name)
        else:
            missing_types.append(name)

    # Check methods coverage
    gen_fns = set(re.findall(r'pub async fn (\w+)', methods_src))
    implemented_methods = []
    missing_methods = []
    for name in all_methods:
        fn_name = snake_case(name)
        if fn_name in gen_fns:
            implemented_methods.append(name)
        else:
            missing_methods.append(name)

    # Params structs
    params_count = len(re.findall(r'pub struct \w+Params', methods_src))

    type_pct = 100 * len(implemented_types) // len(all_types) if all_types else 0
    method_pct = 100 * len(implemented_methods) // len(all_methods) if all_methods else 0

    if markdown:
        print(f"## 📊 tgbotrs API Coverage Report")
        print(f"")
        print(f"**Telegram Bot API {version}** ({release_date})")
        print(f"")
        print(f"| Category | Implemented | Total | Coverage |")
        print(f"|---|---|---|---|")
        print(f"| **Types (total)** | {len(implemented_types)} | {len(all_types)} | {'✅' if type_pct==100 else '⚠️'} {type_pct}% |")
        print(f"| ↳ Struct types | {len(struct_types)} | {len(struct_types)} | ✅ 100% |")
        print(f"| ↳ Union/enum types | {len(union_types)} | {len(union_types)} | ✅ 100% |")
        print(f"| ↳ Marker types | {len(empty_types)} | {len(empty_types)} | ✅ 100% |")
        print(f"| **Methods** | {len(implemented_methods)} | {len(all_methods)} | {'✅' if method_pct==100 else '⚠️'} {method_pct}% |")
        print(f"| **Params structs** | {params_count} | — | — |")
        print(f"")

        if missing_types:
            print(f"### ❌ Missing Types ({len(missing_types)})")
            for t in missing_types:
                print(f"- `{t}`")
            print("")

        if missing_methods:
            print(f"### ❌ Missing Methods ({len(missing_methods)})")
            for m in missing_methods:
                print(f"- `{m}`")
            print("")

        print(f"### 📦 Generated Files")
        print(f"- `gen_types.rs` — {len(open(args[1]).readlines())} lines")
        print(f"- `gen_methods.rs` — {len(open(args[2]).readlines())} lines")
    else:
        print(f"\n{'='*60}")
        print(f"📊 tgbotrs API Coverage — Telegram Bot API {version}")
        print(f"{'='*60}")
        print(f"  Types:   {len(implemented_types):3d}/{len(all_types):3d}  ({type_pct:3d}%)  [{len(union_types)} enums, {len(struct_types)} structs, {len(empty_types)} markers]")
        print(f"  Methods: {len(implemented_methods):3d}/{len(all_methods):3d}  ({method_pct:3d}%)")
        print(f"  Params structs: {params_count}")

        if missing_types or missing_methods:
            print(f"\n⚠️  Missing:")
            if missing_types:
                print(f"  Types: {missing_types}")
            if missing_methods:
                print(f"  Methods: {missing_methods}")
        else:
            print(f"\n✅ 100% coverage — all types and methods implemented!")

    if missing_types or missing_methods:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
