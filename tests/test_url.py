"""Tests for goalie._url module."""

import goalie


class TestIsUrl:
    """Tests for `is_url`."""

    def test_https(self) -> None:
        """True for HTTPS URL."""
        assert goalie.is_url("https://example.com")

    def test_http(self) -> None:
        """True for HTTP URL."""
        assert goalie.is_url("http://example.com")

    def test_ftp(self) -> None:
        """True for FTP URL."""
        assert goalie.is_url("ftp://example.com")

    def test_not_url(self) -> None:
        """False for a plain string."""
        assert not goalie.is_url("just a string")

    def test_non_string(self) -> None:
        """False for non-string input."""
        assert not goalie.is_url(42)


class TestIsExistingUrl:
    """Tests for `is_existing_url`."""

    def test_non_url(self) -> None:
        """False for a non-URL string."""
        assert not goalie.is_existing_url("not-a-url")

    def test_non_string(self) -> None:
        """False for non-string input."""
        assert not goalie.is_existing_url(42)


class TestIsAwsS3Uri:
    """Tests for `is_aws_s3_uri`."""

    def test_valid(self) -> None:
        """True for valid S3 URI."""
        assert goalie.is_aws_s3_uri("s3://my-bucket/path")

    def test_invalid(self) -> None:
        """False for a non-S3 URL."""
        assert not goalie.is_aws_s3_uri("https://example.com")

    def test_non_string(self) -> None:
        """False for non-string input."""
        assert not goalie.is_aws_s3_uri(42)

    def test_empty_s3(self) -> None:
        """False for bare S3 scheme without bucket."""
        assert not goalie.is_aws_s3_uri("s3://")
