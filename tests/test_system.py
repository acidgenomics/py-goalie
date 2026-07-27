"""Tests for goalie._system."""

import platform

from goalie._check import GoalieCheckResult
from goalie._system import (
    all_are_installed,
    all_are_system_commands,
    has_cpu,
    has_internet,
    has_ram,
    is_conda_enabled,
    is_docker,
    is_installed,
    is_linux,
    is_macos,
    is_system_command,
    is_unix,
    is_windows,
)


class TestOsChecks:
    def test_is_linux_returns_result(self):
        result = is_linux()
        assert isinstance(result, GoalieCheckResult)

    def test_is_macos_returns_result(self):
        result = is_macos()
        assert isinstance(result, GoalieCheckResult)

    def test_is_windows_returns_result(self):
        result = is_windows()
        assert isinstance(result, GoalieCheckResult)

    def test_is_unix_returns_result(self):
        result = is_unix()
        assert isinstance(result, GoalieCheckResult)

    def test_exactly_one_os_true(self):
        results = [is_linux(), is_macos(), is_windows()]
        true_count = sum(bool(r) for r in results)
        assert true_count == 1

    def test_unix_on_posix(self):
        import os

        if os.name == "posix":
            assert bool(is_unix())
        else:
            assert not bool(is_unix())

    def test_macos_matches_platform(self):
        if platform.system() == "Darwin":
            assert bool(is_macos())
        else:
            assert not bool(is_macos())


class TestDockerConda:
    def test_is_docker_returns_result(self):
        assert isinstance(is_docker(), GoalieCheckResult)

    def test_is_conda_enabled_returns_result(self):
        assert isinstance(is_conda_enabled(), GoalieCheckResult)


class TestHardware:
    def test_has_cpu_one(self):
        assert bool(has_cpu(1))

    def test_has_cpu_too_many(self):
        assert not bool(has_cpu(99999))

    def test_has_cpu_returns_result(self):
        assert isinstance(has_cpu(1), GoalieCheckResult)

    def test_has_ram_one_gb(self):
        assert bool(has_ram(1))

    def test_has_ram_too_much(self):
        assert not bool(has_ram(99999))


class TestInternet:
    def test_returns_result(self):
        assert isinstance(has_internet(), GoalieCheckResult)


class TestInstalled:
    def test_stdlib_installed(self):
        assert bool(is_installed("os"))
        assert bool(is_installed("sys"))
        assert bool(is_installed("math"))

    def test_not_installed(self):
        assert not bool(is_installed("nonexistent_pkg_xyz_abc"))

    def test_not_a_string(self):
        assert not bool(is_installed(123))

    def test_all_are_installed_pass(self):
        assert bool(all_are_installed(["os", "sys"]))

    def test_all_are_installed_fail(self):
        assert not bool(all_are_installed(["os", "nonexistent_pkg_xyz"]))

    def test_all_are_installed_empty(self):
        assert not bool(all_are_installed([]))


class TestSystemCommand:
    def test_python_available(self):
        assert bool(is_system_command("python")) or bool(is_system_command("python3"))

    def test_missing_command(self):
        assert not bool(is_system_command("nonexistent_cmd_xyz_abc_123"))

    def test_not_a_string(self):
        assert not bool(is_system_command(123))

    def test_all_are_system_commands_empty(self):
        assert not bool(all_are_system_commands([]))
