import pytest
import numpy as np
from scipy import stats
import jax.scipy.stats as jstats
from ars import ARS
import re


@pytest.fixture
def gaussian_pdf():
    """Provide a simple Gaussian PDF for testing."""
    from scipy.stats import norm

    return norm.pdf


@pytest.fixture
def ars_instance(gaussian_pdf):
    """Instantiate the ARS class with a Gaussian PDF."""
    return ARS(
        pdf=gaussian_pdf, domain=(-np.inf, np.inf), random_seed=42, verbose=False
    )


def test_domain_validation():
    """Test domain validity checks in the ARS initializer."""
    from scipy.stats import norm

    with pytest.raises(AssertionError, match="Domain should be a tuple of length 2"):
        ARS(pdf=norm.pdf, domain=(-np.inf,))  # Invalid domain tuple
    with pytest.raises(AssertionError, match="domain should be in the form"):
        ARS(pdf=norm.pdf, domain=(5, 3))  # Invalid order
    ARS(pdf=norm.pdf, domain=(-np.inf, np.inf))  # Valid domain, should pass


def test_initial_points_validation(gaussian_pdf):
    """Test the initial points validation."""
    domain = (-np.inf, np.inf)

    with pytest.raises(
        AssertionError, match="Initial points should have at least 2 points"
    ):
        ARS(pdf=gaussian_pdf, domain=domain, initial_points=[0])  # Not enough points

    with pytest.raises(
        AssertionError,
        match="Initial points should be less than the right boundary of the domain",
    ):
        beta_pdf = stats.beta(a=2, b=5).pdf
        ARS(
            pdf=beta_pdf, domain=(0, 1), initial_points=[0.1, 1.2]
        )  # initial points not in domain

    with pytest.raises(
        AssertionError,
        match="Initial points should be greater than the left boundary of the domain",
    ):
        beta_pdf = stats.beta(a=2, b=5).pdf
        ARS(
            pdf=beta_pdf, domain=(0, 1), initial_points=[-0.1, 0.8]
        )  # initial points not in domain

    with pytest.raises(
        AssertionError,
        match=re.escape(
            "h' of the smallest initial point should be positive when domain[0] = -inf"
        ),
    ):
        ARS(
            pdf=gaussian_pdf, domain=domain, initial_points=[1, 4]
        )  # If left side infinite, h'(x_0) should be positive

    with pytest.raises(
        AssertionError,
        match=re.escape(
            "h' of the largest initial point should be negative when domain[1] = inf"
        ),
    ):
        ARS(
            pdf=gaussian_pdf, domain=domain, initial_points=[-4, -1]
        )  # If right side infinite, h'(x_1) should be negative

    obj = ARS(pdf=gaussian_pdf, domain=domain, initial_points=[-1.0, 0.0, 1.0])
    assert len(obj.x_values) == len(obj.h_values) == len(obj.hp_values) == 3


def test_search_initial_points(gaussian_pdf):
    """Test the initial points search."""
    # domain = (-np.inf, np.inf)
    with pytest.raises(
        AssertionError, match="Number of initial points should be at least 2"
    ):
        ARS(
            pdf=gaussian_pdf, domain=(-np.inf, np.inf), n_initial_points=1
        )  # Not enough points

    # Valid number of initial points are found
    n_initial_points = 10
    obj = ARS(
        pdf=gaussian_pdf, domain=(-np.inf, np.inf), n_initial_points=n_initial_points
    )
    assert (
        len(obj.x_values) == len(obj.h_values) == len(obj.hp_values) == n_initial_points
    )

    # Closed domain but not defined at bounds
    n_initial_points = 3
    pdf = stats.beta(a=2, b=5).pdf
    obj = ARS(pdf=pdf, domain=(0, 1), n_initial_points=n_initial_points)
    assert (
        len(obj.x_values) == len(obj.h_values) == len(obj.hp_values) == n_initial_points
    )
    assert obj.x_values[0] > 0 and obj.x_values[-1] < 1


def test_log_concavity_validation():
    """Ensure log-concavity is enforced."""
    non_log_concave_pdf = stats.beta(a=1, b=0.5).pdf
    with pytest.raises(ValueError, match="Function is not log-concave"):
        ARS(pdf=non_log_concave_pdf, domain=(0, 1))


def test_update_arrays(ars_instance):
    """Test the update of internal arrays when a new point is added."""
    x, h, hp = 0.0, -1.0, -0.5
    initial_len = len(ars_instance.x_values)
    ars_instance.update_arrays(x, h, hp)
    assert len(ars_instance.x_values) == initial_len + 1
    assert x in ars_instance.x_values


def test_compute_util_arrays(ars_instance):
    """Verify utility arrays computation."""
    ars_instance.compute_util_arrays()
    assert len(ars_instance.z_values) == len(ars_instance.x_values) + 1
    assert np.all(np.diff(ars_instance.z_values) > 0)  # Ensure z_values are sorted


def test_sample_candidate(ars_instance):
    """Test candidate sampling."""
    sample = ars_instance.sample_candidate()
    assert ars_instance.domain[0] <= sample <= ars_instance.domain[1]
    assert not np.isnan(sample)


def test_check_sample(ars_instance):
    """Test the acceptance-rejection of a candidate sample."""
    x_star = 0.0
    accept, h, hp = ars_instance.check_sample(x_star)
    assert isinstance(accept, bool)
    if not accept:
        assert h is not None and hp is not None


def test_sampling_process(ars_instance):
    """Test the overall sampling process."""
    n_samples = 100
    samples = ars_instance(n_samples=n_samples, max_iter=1000)
    assert len(samples) == n_samples
    assert np.all(
        (samples >= ars_instance.domain[0]) & (samples <= ars_instance.domain[1])
    )


def test_large_sampling(gaussian_pdf):
    """Test sampling with a large number of samples."""
    ars = ARS(pdf=gaussian_pdf, domain=(-np.inf, np.inf), random_seed=243)
    n_samples = 8000
    samples = ars(n_samples=n_samples)
    assert len(samples) == n_samples
    assert not np.any(np.isnan(samples))


def test_jax_match_non_jax():
    """Test that JAX and non-JAX implementations match."""
    n_samples = 10000
    jax_pdf = jstats.norm.pdf
    np_pdf = stats.norm.pdf

    jax_ars = ARS(pdf=jax_pdf, domain=(-np.inf, np.inf), random_seed=243)
    np_ars = ARS(pdf=np_pdf, domain=(-np.inf, np.inf), random_seed=243)

    jax_samples = jax_ars(n_samples=n_samples)
    np_samples = np_ars(n_samples=n_samples)
    assert np.allclose(jax_samples, np_samples)
    assert jax_ars.use_jax
    assert not np_ars.use_jax


def test_pdf_match_logpdf():
    """Test that PDF and log PDF implementations match."""
    dist_domain = [
        (stats.norm, (-np.inf, np.inf)),
        (stats.beta(a=2, b=5), (0, 1)),
        (stats.truncnorm(a=-1, b=3), (-1, 3)),
        (stats.expon(scale=2), (0, np.inf)),
    ]
    n_samples = 10000
    for dist, domain in dist_domain:
        pdf = dist.pdf
        logpdf = dist.logpdf
        ars_pdf = ARS(pdf=pdf, domain=domain, random_seed=243)
        ars_logpdf = ARS(pdf=logpdf, domain=domain, random_seed=243, is_logpdf=True)
        pdf_samples = ars_pdf(n_samples=n_samples)
        logpdf_samples = ars_logpdf(n_samples=n_samples)
        assert np.allclose(pdf_samples, logpdf_samples)
