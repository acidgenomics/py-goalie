"""Tests for goalie._require."""

import pytest

from goalie._require import require_namespaces


class TestRequireNamespaces:
    def test_installed_stdlib(self):
        require_namespaces(["os", "sys", "math"])

    def test_installed_pytest(self):
        require_namespaces(["pytest"])

    def test_missing_raises(self):
        with pytest.raises(ImportError, match="not installed"):
            require_namespaces(["nonexistent_pkg_xyz_abc_123"])

    def test_missing_lists_name(self):
        with pytest.raises(ImportError, match="nonexistent_pkg_xyz_abc_123"):
            require_namespaces(["nonexistent_pkg_xyz_abc_123"])

    def test_missing_plural(self):
        with pytest.raises(ImportError, match="Packages"):
            require_namespaces(["nonexistent_a", "nonexistent_b"])

    def test_missing_singular(self):
        with pytest.raises(ImportError, match="Package not installed"):
            require_namespaces(["nonexistent_a"])

    def test_empty_passes(self):
        require_namespaces([])
