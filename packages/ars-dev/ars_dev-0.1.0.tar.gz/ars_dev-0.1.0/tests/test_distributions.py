import pytest
import jax.numpy as jnp
from ars import ARS, ars
import numpy as np
from scipy import stats
from scipy.stats import kstest, kstat, kstatvar


def test_sampling_from_distributions():
    n_samples = 50000
    dist_domain = [
        (stats.norm, (-np.inf, np.inf)),
        (stats.expon(scale=2), (0, np.inf)),
        (stats.beta(a=2, b=5), (0, 1)),
        (stats.uniform, (0, 1)),
        (stats.truncnorm(a=-1, b=3), (-1, 3)),
        (stats.truncexpon(b=4, scale=0.5), (0, 2)),
    ]

    rng = np.random.default_rng(243)
    for dist, domain in dist_domain:
        # Testing against the good distribution
        unnorm_constant = np.random.randn()
        logpdf = lambda x: dist.logpdf(x) + unnorm_constant
        samples = ars(
            logpdf,
            domain=domain,
            n_samples=n_samples,
            verbose=False,
            random_seed=243,
            is_logpdf=True,
        )
        ks_good = kstest(samples, dist.cdf)
        assert (
            ks_good.pvalue > 0.05
        ), f"KS test failed for {dist} with p-value {ks_good.pvalue}"

        other_dist = rng.choice([d for d, _ in dist_domain if d != dist])
        # Testing against the bad distribution
        ks_bad = kstest(samples, other_dist.cdf)
        assert (
            ks_bad.pvalue < 0.05
        ), f"KS test failed for {dist} with p-value {ks_bad.pvalue}"
