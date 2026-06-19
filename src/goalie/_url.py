"""URL check functions.

Converted from R check-vector functions:
- check-vector-isUrl.R
- check-vector-isExistingUrl.R
- check-vector-isAwsS3Uri.R
"""

import functools
import re
import subprocess
import urllib.error
import urllib.request
from collections.abc import Sequence

from goalie._check import _TRUE, GoalieCheckResult, _false, _to_name
from goalie._vectorize import _check_all


def is_url(x: str) -> GoalieCheckResult:
    """Check that the input contains a URL.

    Simple check based on pattern matching; does not verify
    that the URL exists.

    Parameters
    ----------
    x: Input string.

    Examples
    --------
    >>> is_url("https://www.r-project.org/")
    GoalieCheckResult(ok=True)
    >>> is_url("xxx")
    GoalieCheckResult(ok=False, cause=...)
    """
    if not isinstance(x, str):
        return _false("'%s' is not a string.", _to_name(x))
    if re.match(r"^[^:/]+://.+$", x):
        return _TRUE
    return _false("'%s' is not a URL.", x)


def is_existing_url(
    x: str,
    timeout: float = 5.0,
) -> GoalieCheckResult:
    """Check whether the URL exists (is accessible).

    Supports HTTPS, HTTP, and FTP protocols.

    Args:
        x: URL string.
        timeout: Timeout in seconds.

    Examples
    --------
        >>> is_existing_url("https://www.google.com/")
        GoalieCheckResult(ok=True)
    """
    result = is_url(x)
    if not result:
        return result
    protocol = x.split("://", maxsplit=1)[0].lower()
    if protocol not in ("http", "https", "ftp"):
        return _false(
            "'%s' has unsupported protocol '%s'.",
            x,
            protocol,
        )
    try:
        req = urllib.request.Request(x, method="HEAD")
        with urllib.request.urlopen(
            req,
            timeout=timeout,
        ) as resp:
            if resp.status < 400:
                return _TRUE
    except Exception:
        pass
    # Fallback to GET for servers that don't support HEAD.
    try:
        req = urllib.request.Request(x, method="GET")
        with urllib.request.urlopen(
            req,
            timeout=timeout,
        ) as resp:
            if resp.status < 400:
                return _TRUE
    except Exception:
        pass
    return _false("URL '%s' doesn't exist or is not accessible.", x)


def is_aws_s3_uri(x: str) -> GoalieCheckResult:
    """Check whether the input contains an AWS S3 URI.

    Simple check based on ``s3://`` prefix pattern matching.
    Does not verify that the URI exists.

    Args:
        x: Input string.

    Examples
    --------
        >>> is_aws_s3_uri("s3://my-bucket/key")
        GoalieCheckResult(ok=True)
        >>> is_aws_s3_uri("https://example.com/")
        GoalieCheckResult(ok=False, cause=...)
    """
    if not isinstance(x, str):
        return _false("'%s' is not a string.", _to_name(x))
    if re.match(r"^s3://.+$", x):
        return _TRUE
    return _false("'%s' is not an AWS S3 URI.", x)


def all_are_urls(x: Sequence[str]) -> GoalieCheckResult:
    """Check whether all inputs are URLs.

    Examples
    --------
        >>> all_are_urls([])
        GoalieCheckResult(ok=False, cause="Input has no elements.")
    """
    return _check_all(x, is_url)


def all_are_existing_urls(x: Sequence[str], timeout: float = 5.0) -> GoalieCheckResult:
    """Check whether all inputs are accessible URLs.

    Examples
    --------
        >>> all_are_existing_urls([])
        GoalieCheckResult(ok=False, cause="Input has no elements.")
    """
    return _check_all(x, functools.partial(is_existing_url, timeout=timeout))


def all_are_aws_s3_uris(x: Sequence[str]) -> GoalieCheckResult:
    """Check whether all inputs are AWS S3 URIs.

    Examples
    --------
        >>> all_are_aws_s3_uris([])
        GoalieCheckResult(ok=False, cause="Input has no elements.")
    """
    return _check_all(x, is_aws_s3_uri)


def is_existing_aws_s3_uri(x: str) -> GoalieCheckResult:
    """Check whether an AWS S3 URI exists (object is accessible).

    Requires ``boto3`` (optional) or falls back to the AWS CLI
    (``aws s3api head-object``).  Returns a failure result if neither
    is available or if the object does not exist.

    Parameters
    ----------
    x : str
        S3 URI (e.g. ``s3://bucket/key``).

    Examples
    --------
        >>> result = is_existing_aws_s3_uri("s3://nonexistent-bucket-xyz/key")
        >>> isinstance(result, GoalieCheckResult)
        True
    """
    result = is_aws_s3_uri(x)
    if not result:
        return result
    # Parse bucket and key from s3://bucket/key
    path = x[len("s3://") :]
    parts = path.split("/", 1)
    bucket = parts[0]
    key = parts[1] if len(parts) > 1 else ""
    # Try boto3 first (optional dependency).
    try:
        import boto3  # noqa: PLC0415  # type: ignore[import-not-found]  # ty: ignore[unresolved-import]

        s3 = boto3.client("s3")
        s3.head_object(Bucket=bucket, Key=key)
        return _TRUE
    except ImportError:
        pass
    except Exception:
        return _false("S3 URI '%s' does not exist or is not accessible.", x)
    # Fallback: AWS CLI.
    try:
        cmd = ["aws", "s3api", "head-object", "--bucket", bucket, "--key", key]
        result_proc = subprocess.run(cmd, capture_output=True, check=False)
        if result_proc.returncode == 0:
            return _TRUE
    except FileNotFoundError:
        return _false("Cannot check S3 URI '%s': neither boto3 nor aws CLI available.", x)
    return _false("S3 URI '%s' does not exist or is not accessible.", x)


def all_are_existing_aws_s3_uris(x: Sequence[str]) -> GoalieCheckResult:
    """Check whether all inputs are accessible AWS S3 URIs.

    Examples
    --------
        >>> all_are_existing_aws_s3_uris([])
        GoalieCheckResult(ok=False, cause="Input has no elements.")
    """
    return _check_all(x, is_existing_aws_s3_uri)
