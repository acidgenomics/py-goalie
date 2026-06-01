"""URL check functions.

Converted from R check-vector functions:
- check-vector-isUrl.R
- check-vector-isExistingUrl.R
- check-vector-isAwsS3Uri.R
"""

import functools
import re
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
