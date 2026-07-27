"""Tests for goalie._bio."""

from goalie._bio import has_clusters, has_metrics, has_multiple_samples
from goalie._check import GoalieCheckResult


class TestHasClusters:
    def test_not_anndata(self):
        result = has_clusters("not_anndata")
        assert isinstance(result, GoalieCheckResult)
        assert not bool(result)

    def test_not_anndata_dict(self):
        assert not bool(has_clusters({"obs": None, "var": None}))

    def test_pass_with_leiden(self):
        class FakeAnnData:
            class obs:
                columns = ["leiden", "n_counts"]

            var = None
            X = None

        assert bool(has_clusters(FakeAnnData()))

    def test_pass_with_louvain(self):
        class FakeAnnData:
            class obs:
                columns = ["louvain", "n_counts"]

            var = None
            X = None

        assert bool(has_clusters(FakeAnnData()))

    def test_fail_no_clusters(self):
        class FakeAnnData:
            class obs:
                columns = ["n_counts", "total_counts"]

            var = None
            X = None

        assert not bool(has_clusters(FakeAnnData()))


class TestHasMetrics:
    def test_not_anndata(self):
        assert not bool(has_metrics("not_anndata"))

    def test_pass_default_keys(self):
        class FakeObs:
            columns = ["n_genes_by_counts", "total_counts", "other"]

        class FakeAnnData:
            obs = FakeObs()
            var = None
            X = None

        assert bool(has_metrics(FakeAnnData()))

    def test_fail_missing_key(self):
        class FakeObs:
            columns = ["n_genes_by_counts"]

        class FakeAnnData:
            obs = FakeObs()
            var = None
            X = None

        result = has_metrics(FakeAnnData())
        assert not bool(result)
        assert "total_counts" in result.cause

    def test_custom_keys(self):
        class FakeObs:
            columns = ["my_metric"]

        class FakeAnnData:
            obs = FakeObs()
            var = None
            X = None

        assert bool(has_metrics(FakeAnnData(), obs_keys=["my_metric"]))


class TestHasMultipleSamples:
    def test_not_anndata(self):
        assert not bool(has_multiple_samples("not_anndata"))

    def test_missing_sample_key(self):
        class FakeObs:
            columns = ["n_counts"]

            def __contains__(self, item):
                return item in self.columns

        class FakeAnnData:
            obs = FakeObs()
            var = None
            X = None

        assert not bool(has_multiple_samples(FakeAnnData()))

    def test_pass_multiple_samples(self):
        class FakeSeries:
            def nunique(self):
                return 3

        class FakeObs:
            columns = ["sample", "n_counts"]

            def __contains__(self, item):
                return item in self.columns

            def __getitem__(self, key):
                if key == "sample":
                    return FakeSeries()
                raise KeyError(key)

        class FakeAnnData:
            obs = FakeObs()
            var = None
            X = None

        assert bool(has_multiple_samples(FakeAnnData()))

    def test_fail_single_sample(self):
        class FakeSeries:
            def nunique(self):
                return 1

        class FakeObs:
            columns = ["sample"]

            def __contains__(self, item):
                return item in self.columns

            def __getitem__(self, key):
                if key == "sample":
                    return FakeSeries()
                raise KeyError(key)

        class FakeAnnData:
            obs = FakeObs()
            var = None
            X = None

        assert not bool(has_multiple_samples(FakeAnnData()))
