"""Tests for goalie._filesystem module."""

import os
import tempfile

import goalie


class TestHasAccess:
    """Tests for `has_access`."""

    def test_home(self) -> None:
        """Home directory is accessible."""
        assert goalie.has_access(os.path.expanduser("~"))

    def test_cwd(self) -> None:
        """Current directory is accessible."""
        assert goalie.has_access(".")

    def test_nonexistent(self) -> None:
        """Nonexistent path returns False."""
        assert not goalie.has_access("nonexistent_xyz_abc")

    def test_write(self) -> None:
        """Home directory has write access."""
        assert goalie.has_access(os.path.expanduser("~"), "w")

    def test_rwx(self) -> None:
        """Home directory has read, write, and execute access."""
        assert goalie.has_access(os.path.expanduser("~"), "rwx")


class TestIsCompressedFile:
    """Tests for `is_compressed_file`."""

    def test_gz(self) -> None:
        """Gzip file is detected as compressed."""
        path = os.path.join(tempfile.gettempdir(), "test.gz")
        with open(path, "w") as f:
            f.write("")
        try:
            assert goalie.is_compressed_file(path)
        finally:
            os.unlink(path)

    def test_bz2(self) -> None:
        """Bz2 file is detected as compressed."""
        path = os.path.join(tempfile.gettempdir(), "test.bz2")
        with open(path, "w") as f:
            f.write("")
        try:
            assert goalie.is_compressed_file(path)
        finally:
            os.unlink(path)

    def test_not_compressed(self) -> None:
        """Non-compressed file returns False."""
        with tempfile.NamedTemporaryFile(suffix=".txt") as f:
            assert not goalie.is_compressed_file(f.name)

    def test_nonexistent(self) -> None:
        """Nonexistent file returns False."""
        assert not goalie.is_compressed_file("missing.gz")


class TestIsTempFile:
    """Tests for `is_temp_file`."""

    def test_temp(self) -> None:
        """Temporary file returns True."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            path = f.name
        try:
            assert goalie.is_temp_file(path)
        finally:
            os.unlink(path)

    def test_not_temp(self) -> None:
        """Non-temporary file returns False."""
        path = os.path.expanduser("~/.bashrc")
        if os.path.isfile(path):
            assert not goalie.is_temp_file(path)

    def test_nonexistent(self) -> None:
        """Nonexistent path returns False."""
        assert not goalie.is_temp_file("nonexistent_file_xyz.txt")


class TestIsGitRepo:
    """Tests for `is_git_repo`."""

    def test_this_repo(self) -> None:
        """Current directory is a git repo."""
        assert goalie.is_git_repo(".")

    def test_tmp(self) -> None:
        """Temp directory is not a git repo."""
        assert not goalie.is_git_repo(tempfile.gettempdir())

    def test_nonexistent(self) -> None:
        """Nonexistent directory returns False."""
        assert not goalie.is_git_repo("nonexistent_dir_xyz")
