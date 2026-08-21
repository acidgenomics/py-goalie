"""URL check functions."""

import re
import subprocess
import urllib.error
import urllib.request

_URL_PATTERN = re.compile(r"^[^:/]+://.+$")
_S3_URI_PATTERN = re.compile(r"^s3://.+$")


def is_url(x: object) -> bool:
    """Check whether the input contains a URL.

    Simple pattern match; does not verify that the URL exists.

    Parameters
    ----------
    x : object
        Value to check.

    Returns
    -------
    bool
        ``True`` if ``x`` looks like a URL.

    Examples
    --------
    >>> is_url("https://www.python.org/")
    True
    >>> is_url("xxx")
    False
    """
    return isinstance(x, str) and _URL_PATTERN.match(x) is not None


def is_existing_url(x: object, timeout: float = 5.0) -> bool:
    """Check whether the URL exists (is accessible).

    Supports HTTPS, HTTP, and FTP protocols.

    Parameters
    ----------
    x : object
        URL to check.
    timeout : float
        Timeout in seconds.

    Returns
    -------
    bool
        ``True`` if a HEAD or GET request against ``x`` succeeds.

    Examples
    --------
    >>> is_existing_url("not-a-url")
    False
    """
    if not isinstance(x, str) or not is_url(x):
        return False
    protocol = x.split("://", maxsplit=1)[0].lower()
    if protocol not in ("http", "https", "ftp"):
        return False
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(x, method=method)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if resp.status < 400:
                    return True
        except Exception:
            continue
    return False


def is_aws_s3_uri(x: object) -> bool:
    """Check whether the input contains an AWS S3 URI.

    Simple pattern match on the ``s3://`` prefix; does not verify that the
    URI exists.

    Parameters
    ----------
    x : object
        Value to check.

    Returns
    -------
    bool
        ``True`` if ``x`` looks like an S3 URI.

    Examples
    --------
    >>> is_aws_s3_uri("s3://my-bucket/key")
    True
    >>> is_aws_s3_uri("https://example.com/")
    False
    """
    return isinstance(x, str) and _S3_URI_PATTERN.match(x) is not None


def is_existing_aws_s3_uri(x: object) -> bool:
    """Check whether an AWS S3 URI exists (object is accessible).

    Requires ``boto3`` (optional) or falls back to the AWS CLI
    (``aws s3api head-object``).

    Parameters
    ----------
    x : object
        S3 URI to check (e.g. ``s3://bucket/key``).

    Returns
    -------
    bool
        ``True`` if the object exists and is accessible.

    Raises
    ------
    RuntimeError
        If neither ``boto3`` nor the ``aws`` CLI is available, so the
        existence of the object cannot be determined.

    Examples
    --------
    >>> is_existing_aws_s3_uri("not-an-s3-uri")
    False
    """
    if not isinstance(x, str) or not is_aws_s3_uri(x):
        return False
    path = x[len("s3://") :]
    parts = path.split("/", 1)
    bucket = parts[0]
    key = parts[1] if len(parts) > 1 else ""
    try:
        import boto3  # noqa: PLC0415  # type: ignore[import-not-found]  # ty: ignore[unresolved-import]
    except ImportError:
        pass
    else:
        try:
            boto3.client("s3").head_object(Bucket=bucket, Key=key)
        except Exception:
            return False
        return True
    try:
        cmd = ["aws", "s3api", "head-object", "--bucket", bucket, "--key", key]
        result = subprocess.run(cmd, capture_output=True, check=False)
    except FileNotFoundError:
        msg = f"Cannot check S3 URI {x!r}: neither boto3 nor the aws CLI is available."
        raise RuntimeError(msg) from None
    return result.returncode == 0
