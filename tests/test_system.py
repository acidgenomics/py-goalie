"""Tests for goalie._system module."""

import os
import platform

import pytest

import goalie


class TestOsChecks:
    """Tests for the OS family predicates."""

    def test_exactly_one_os_true(self) -> None:
        """Exactly one of the OS predicates is True."""
        results = [goalie.is_linux(), goalie.is_macos(), goalie.is_windows()]
        assert sum(results) == 1

    def test_unix_on_posix(self) -> None:
        """`is_unix` agrees with `os.name`."""
        assert goalie.is_unix() == (os.name == "posix")

    def test_macos_matches_platform(self) -> None:
        """`is_macos` agrees with `platform.system`."""
        assert goalie.is_macos() == (platform.system() == "Darwin")


class TestDockerConda:
    """Tests that only assert a bool is returned; the answer is machine-specific."""

    def test_is_docker_returns_bool(self) -> None:
        """`is_docker` returns a bool."""
        assert isinstance(goalie.is_docker(), bool)

    def test_is_conda_enabled_returns_bool(self) -> None:
        """`is_conda_enabled` returns a bool."""
        assert isinstance(goalie.is_conda_enabled(), bool)


class TestHardware:
    """Tests for `has_cpu` and `has_ram`."""

    def test_has_cpu_one(self) -> None:
        """Every machine has at least 1 CPU core."""
        assert goalie.has_cpu(1)

    def test_has_cpu_too_many(self) -> None:
        """No machine has 99999 CPU cores."""
        assert not goalie.has_cpu(99999)

    def test_has_ram_one_gb(self) -> None:
        """Every machine has at least 1 GB of RAM."""
        assert goalie.has_ram(1)

    def test_has_ram_too_much(self) -> None:
        """No machine has 99999 GB of RAM."""
        assert not goalie.has_ram(99999)


class TestInternet:
    """Tests that only assert a bool is returned."""

    def test_returns_bool(self) -> None:
        """`has_internet` returns a bool."""
        assert isinstance(goalie.has_internet(), bool)


class TestInstalled:
    """Tests for `is_installed`."""

    def test_stdlib_installed(self) -> None:
        """Standard library modules are importable."""
        assert goalie.is_installed("os")
        assert goalie.is_installed("sys")
        assert goalie.is_installed("math")

    def test_not_installed(self) -> None:
        """A nonexistent package is not installed."""
        assert not goalie.is_installed("nonexistent_pkg_xyz_abc")

    def test_not_a_string(self) -> None:
        """Non-string input returns False."""
        assert not goalie.is_installed(123)


class TestSystemCommand:
    """Tests for `is_system_command`."""

    def test_python_available(self) -> None:
        """Either `python` or `python3` is on PATH."""
        assert goalie.is_system_command("python") or goalie.is_system_command("python3")

    def test_missing_command(self) -> None:
        """A nonexistent command is not on PATH."""
        assert not goalie.is_system_command("nonexistent_cmd_xyz_abc_123")

    def test_not_a_string(self) -> None:
        """Non-string input returns False."""
        assert not goalie.is_system_command(123)


class TestVscode:
    """Tests that only assert a bool is returned."""

    def test_returns_bool(self) -> None:
        """`is_vscode` returns a bool."""
        assert isinstance(goalie.is_vscode(), bool)


class TestGithubPat:
    """Tests that only assert a bool is returned."""

    def test_returns_bool(self) -> None:
        """`has_github_pat` returns a bool."""
        assert isinstance(goalie.has_github_pat(), bool)


class TestPackageVersion:
    """Tests for `is_package_version`."""

    def test_not_installed(self) -> None:
        """A nonexistent package fails the constraint."""
        assert not goalie.is_package_version("nonexistent_pkg_xyz_abc", "1.0.0")

    def test_unsupported_operator(self) -> None:
        """An unsupported operator raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported operator"):
            goalie.is_package_version("goalie", "0.0.1", op="~=")
