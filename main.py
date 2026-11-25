#!/usr/bin/env python3
"""Merge two JSON config files, with the second overriding the first.

Nested objects are merged key by key (deep merge); other values are
replaced outright by the second file's value.
"""
import argparse
import json
import sys
from pathlib import Path


def deep_merge(base, override):
    """Return a new dict merging override into base recursively."""
    merged = dict(base)
    for key, value in override.items():
        if (key in merged and isinstance(merged[key], dict)
                and isinstance(value, dict)):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"Error: {path} is not valid JSON: {exc}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(data, dict):
        print(f"Error: {path} must contain a JSON object.", file=sys.stderr)
        sys.exit(1)
    return data


def main():
    parser = argparse.ArgumentParser(
        description="Merge two JSON config files; the second overrides the first.")
    parser.add_argument("base", help="Base JSON config file")
    parser.add_argument("override", help="Overriding JSON config file")
    parser.add_argument("-o", "--output", default=None,
                        help="Write merged JSON here (default: print to stdout)")
    parser.add_argument("--indent", type=int, default=2,
                        help="Indent for output JSON (default: 2)")
    parser.add_argument("--shallow", action="store_true",
                        help="Merge only top-level keys, no deep merge")
    args = parser.parse_args()

    base = load_json(args.base)
    override = load_json(args.override)
    if args.shallow:
        merged = {**base, **override}
    else:
        merged = deep_merge(base, override)

    text = json.dumps(merged, indent=args.indent, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        print(f"Merged config written to {args.output}")
        print(f"Keys: {len(merged)} "
              f"({len(base)} base + {len(override)} override)")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
