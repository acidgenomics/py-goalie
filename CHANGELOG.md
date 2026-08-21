# Changelog

## 0.2.0 (2026-08-21)

### Changes

- **Breaking:** Every check function now returns a plain `bool` instead of a
  `GoalieCheckResult`.
- **Breaking:** Removed `GoalieCheckResult`, `assert_`, `validate`, and
  `GoalieAssertionError`. Raise `CheckError`, `CheckTypeError`, or
  `CheckValueError` (new) at the call site instead.
- **Breaking:** Removed 125 functions that duplicated a builtin operator, an
  `isinstance` check, a `pathlib.Path` method, an R-only convention
  (`has_rownames`, `valid_names`, `formal_compress`, ...), or an
  `all_are_*`/`all_have_*` vectorized mirror of a scalar check.
- **Breaking:** Removed the `bio` optional dependency group (`anndata`,
  `scanpy`) and the AnnData-specific checks (`has_clusters`, `has_metrics`,
  `has_multiple_samples`).
- 30 functions and classes remain, across `_collection.py`, `_errors.py`,
  `_filesystem.py`, `_string.py`, `_system.py`, and `_url.py`.

## 0.1.0 (2026-06-19)

### Changes

- Switch license to Apache-2.0.
- Publish to `python.acidgenomics.com` (private PEP 503 index).
- Update installation instructions in README.

---

## 0.0.1 (initial)

Initial release.
