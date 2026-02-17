#!/usr/bin/env python3
"""
validate_generated.py — Validates that all types and methods from api.json
are present in the generated Rust source files.

Usage: python3 validate_generated.py api.json gen_types.rs gen_methods.rs
"""

import json
import re
import sys


def snake_case(name):
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', name)
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s)
    return s.lower()


def main():
    if len(sys.argv) < 4:
        print("Usage: validate_generated.py <api.json> <gen_types.rs> <gen_methods.rs>")
        sys.exit(1)

    spec = json.load(open(sys.argv[1]))
    types_src = open(sys.argv[2]).read()
    methods_src = open(sys.argv[3]).read()

    errors = []
    warnings = []

    # ──────────────────────────────────────────────
    # Validate Types
    # ──────────────────────────────────────────────
    all_types = spec["types"]
    print(f"\n=== Validating {len(all_types)} types ===")
    
    missing_types = []
    for type_name, type_info in all_types.items():
        is_union = bool(type_info.get("subtypes"))
        
        if is_union:
            pattern = f"pub enum {type_name}"
        else:
            pattern = f"pub struct {type_name}"
        
        if pattern not in types_src:
            missing_types.append(type_name)
            errors.append(f"❌ Missing type: {type_name} (expected '{pattern}')")
        else:
            # Validate fields are present for struct types
            if not is_union and type_info.get("fields"):
                for field in type_info["fields"]:
                    fname = field["name"]
                    # We use the field name directly (serde rename handles mapping)
                    if fname not in types_src:
                        warnings.append(f"⚠️  Field '{fname}' may be missing from {type_name}")

    if missing_types:
        print(f"❌ Missing types ({len(missing_types)}): {missing_types}")
    else:
        print(f"✅ All {len(all_types)} types are present")

    # ──────────────────────────────────────────────
    # Validate Methods
    # ──────────────────────────────────────────────
    all_methods = spec["methods"]
    print(f"\n=== Validating {len(all_methods)} methods ===")

    # Extract all generated function names
    gen_fns = set(re.findall(r'pub async fn (\w+)', methods_src))

    missing_methods = []
    for method_name in all_methods:
        fn_name = snake_case(method_name)
        if fn_name not in gen_fns:
            missing_methods.append((method_name, fn_name))
            errors.append(f"❌ Missing method: {method_name} (expected fn '{fn_name}')")

    if missing_methods:
        print(f"❌ Missing methods ({len(missing_methods)}): {[m[0] for m in missing_methods]}")
    else:
        print(f"✅ All {len(all_methods)} methods are present")

    # ──────────────────────────────────────────────
    # Validate Union Type Variants
    # ──────────────────────────────────────────────
    print(f"\n=== Validating union type variants ===")
    union_errors = 0
    for type_name, type_info in all_types.items():
        subtypes = type_info.get("subtypes", [])
        if not subtypes:
            continue
        for variant in subtypes:
            pattern = f"{variant}({variant})"
            if pattern not in types_src:
                errors.append(f"❌ Missing union variant: {type_name}::{variant}")
                union_errors += 1

    if union_errors == 0:
        print(f"✅ All union type variants are present")
    else:
        print(f"❌ {union_errors} union variants missing")

    # ──────────────────────────────────────────────
    # Report
    # ──────────────────────────────────────────────
    print(f"\n{'='*50}")
    print(f"📊 Validation Summary")
    print(f"  Types:   {len(all_types) - len(missing_types)}/{len(all_types)} ✅")
    print(f"  Methods: {len(all_methods) - len(missing_methods)}/{len(all_methods)} ✅")

    if warnings:
        print(f"\n⚠️  Warnings ({len(warnings)}):")
        for w in warnings[:10]:
            print(f"  {w}")

    if errors:
        print(f"\n❌ Errors ({len(errors)}):")
        for e in errors[:20]:
            print(f"  {e}")
        print(f"\nValidation FAILED with {len(errors)} error(s)")
        sys.exit(1)
    else:
        print(f"\n✅ Validation passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
