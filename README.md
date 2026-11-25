# config-merger

Merge two JSON config files, with the second overriding the first.

Nested objects are merged key by key (deep merge); other values are
replaced outright. Use `--shallow` for a top-level-only merge.

## Requirements

- Python 3
- No third-party packages

## How to run

```bash
python3 main.py base.json override.json [-o merged.json] [--shallow]
```

Without `-o`, the merged JSON is printed to stdout.

## Example

```bash
python3 main.py base.json override.json -o merged.json
```

With `base.json` = `{"port": 8000, "db": {"host": "localhost", "port": 5432}}`
and `override.json` = `{"db": {"port": 5433}, "debug": true}`, the output is:

```json
{
  "db": {
    "host": "localhost",
    "port": 5433
  },
  "debug": true,
  "port": 8000
}
```

```
Merged config written to merged.json
Keys: 3 (2 base + 2 override)
```

## License

MIT — see `LICENSE`.
